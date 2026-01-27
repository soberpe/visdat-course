from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import pandas as pd

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QLineEdit, QFileDialog, QSpinBox, QDoubleSpinBox,
    QTabWidget, QListWidget, QMessageBox, QGroupBox
)

import matplotlib
matplotlib.use("QtAgg")
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from pyvistaqt import QtInteractor

from src.io_lvm import load_lvm_time_force_acc
from src.frf import estimate_fs, compute_frf_h1, avg_magnitude
from src.modal import pick_modes, participation_vector_at
from src.plotting import mag_phase
from src.geometry import default_points_xyz, stick_lines
from src.viewer3d import build_frame, deform

class MplCanvas(FigureCanvas):
    def __init__(self):
        fig = Figure(figsize=(6,4))
        self.ax1 = fig.add_subplot(211)
        self.ax2 = fig.add_subplot(212, sharex=self.ax1)
        super().__init__(fig)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hochhaus Modal Viewer (FRF → Moden → 3D)")

        self.paths = ["" for _ in range(6)]
        self.frfs: list[np.ndarray] = []
        self.f: np.ndarray | None = None
        self.mode_indices: np.ndarray = np.array([], dtype=int)

        # --- Left controls
        left = QWidget()
        left_layout = QVBoxLayout(left)

        files_box = QGroupBox("Messdateien (.lvm) – Anregung Punkt j")
        grid = QGridLayout(files_box)
        self.file_edits = []
        for i in range(6):
            lbl = QLabel(f"Punkt {i+1}:")
            edit = QLineEdit()
            edit.setPlaceholderText("Datei wählen …")
            btn = QPushButton("Browse")
            btn.clicked.connect(lambda _, k=i: self.browse_file(k))
            self.file_edits.append(edit)
            grid.addWidget(lbl, i, 0)
            grid.addWidget(edit, i, 1)
            grid.addWidget(btn, i, 2)
        left_layout.addWidget(files_box)

        params_box = QGroupBox("Analyse-Parameter")
        pgrid = QGridLayout(params_box)

        self.n_modes = QSpinBox()
        self.n_modes.setRange(1, 10)
        self.n_modes.setValue(5)

        self.fmax = QDoubleSpinBox()
        self.fmax.setRange(1.0, 1000.0)
        self.fmax.setValue(60.0)
        self.fmax.setSuffix(" Hz")

        self.prom = QDoubleSpinBox()
        self.prom.setRange(0.001, 1.0)
        self.prom.setDecimals(3)
        self.prom.setSingleStep(0.01)
        self.prom.setValue(0.05)

        self.scale = QDoubleSpinBox()
        self.scale.setRange(0.01, 10.0)
        self.scale.setValue(1.0)
        self.scale.setSingleStep(0.1)

        pgrid.addWidget(QLabel("Anzahl Moden:"), 0, 0)
        pgrid.addWidget(self.n_modes, 0, 1)
        pgrid.addWidget(QLabel("fmax für Peak-Picking:"), 1, 0)
        pgrid.addWidget(self.fmax, 1, 1)
        pgrid.addWidget(QLabel("Prominence (rel.):"), 2, 0)
        pgrid.addWidget(self.prom, 2, 1)
        pgrid.addWidget(QLabel("3D Scale:"), 3, 0)
        pgrid.addWidget(self.scale, 3, 1)

        left_layout.addWidget(params_box)

        self.btn_analyze = QPushButton("Load & Analyze")
        self.btn_analyze.clicked.connect(self.load_and_analyze)
        left_layout.addWidget(self.btn_analyze)

        left_layout.addStretch(1)

        # --- Right tabs
        self.tabs = QTabWidget()

        # FRF tab
        frf_tab = QWidget()
        frf_layout = QVBoxLayout(frf_tab)
        self.canvas = MplCanvas()
        frf_layout.addWidget(self.canvas)
        self.tabs.addTab(frf_tab, "FRFs")
        self.fmax.valueChanged.connect(self.update_frf_plot)

        # Modes tab
        modes_tab = QWidget()
        modes_layout = QVBoxLayout(modes_tab)
        modes_layout.addWidget(QLabel("Gefundene Moden (Peak-Picking auf Mittelwert |H|):"))
        self.mode_list = QListWidget()
        self.mode_list.currentRowChanged.connect(self.on_mode_selected)
        modes_layout.addWidget(self.mode_list)
        self.tabs.addTab(modes_tab, "Modes")

        # 3D tab
        view_tab = QWidget()
        view_layout = QVBoxLayout(view_tab)
        self.plotter = QtInteractor(view_tab)
        view_layout.addWidget(self.plotter.interactor)
        self.tabs.addTab(view_tab, "3D")

        # --- Main layout
        main = QWidget()
        main_layout = QHBoxLayout(main)
        main_layout.addWidget(left, 1)
        main_layout.addWidget(self.tabs, 2)
        self.setCentralWidget(main)

        # --- 3D scene setup
        self.points0 = default_points_xyz()
        self.edges = stick_lines()
        self.direction = np.array([1.0, 0.0, 0.0])  # measured DOF direction (x)
        self.frame_mesh = build_frame(self.points0, self.edges)
        self.spheres = None
        self.plotter.add_mesh(self.frame_mesh, color="white", line_width=4)
        self.points_actor = self.plotter.add_mesh(pv_points(self.points0), scalars=None, color="orange", point_size=12, render_points_as_spheres=True)
        self.plotter.show_axes()
        self.plotter.reset_camera()

        # animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_step)
        self.t = 0.0
        self.omega = 2*np.pi*5.0
        self.v_complex = np.ones(6, dtype=complex)

    def browse_file(self, idx: int):
        p, _ = QFileDialog.getOpenFileName(self, "Select .lvm file", str(Path.cwd()), "LabVIEW Measurement (*.lvm);;All Files (*)")
        if p:
            self.paths[idx] = p
            self.file_edits[idx].setText(p)

    def load_and_analyze(self):
        try:
            # gather paths (allow empty -> fallback to sample)
            paths = []
            for i in range(6):
                p = self.file_edits[i].text().strip()
                if not p:
                    # fallback to bundled sample filenames if present
                    sample = Path(__file__).parent / "data" / "sample" / f"Time 1-{i+1}.lvm"
                    if sample.exists():
                        p = str(sample)
                    else:
                        raise ValueError(f"Bitte Datei für Punkt {i+1} auswählen.")
                paths.append(p)

            # load + FRF per file
            frfs = []
            f_ref = None
            fs_ref = None
            for p in paths:
                df = load_lvm_time_force_acc(p)
                fs = estimate_fs(df["t_s"].to_numpy())
                if fs_ref is None:
                    fs_ref = fs
                # compute FRF
                f, H = compute_frf_h1(df["acc_g"].to_numpy(), df["force_N"].to_numpy(), fs=fs, nperseg=4096)
                if f_ref is None:
                    f_ref = f
                else:
                    if len(f) != len(f_ref) or np.max(np.abs(f - f_ref)) > 1e-6:
                        # for simplicity require identical grid; can add interpolation later
                        raise ValueError("Frequenzraster der FRFs ist nicht identisch. (Kann man später mit Interpolation lösen.)")
                frfs.append(H)

            self.frfs = frfs
            self.f = f_ref

            # plot FRFs
            self.update_frf_plot()

            # peak picking on average magnitude
            M = avg_magnitude(self.frfs)
            idxs = pick_modes(self.f, M, n_modes=self.n_modes.value(), fmax=self.fmax.value(), prominence_rel=self.prom.value())
            self.mode_indices = idxs

            self.mode_list.clear()
            for k, idx in enumerate(idxs, start=1):
                self.mode_list.addItem(f"Mode {k}: f = {self.f[idx]:.3f} Hz")

            if len(idxs) > 0:
                self.mode_list.setCurrentRow(0)

            QMessageBox.information(self, "OK", "FRFs berechnet und Moden gefunden.")
        except Exception as e:
            QMessageBox.critical(self, "Fehler", str(e))

    def update_frf_plot(self):
        if self.f is None or not self.frfs:
            return
        ax1, ax2 = self.canvas.ax1, self.canvas.ax2
        ax1.clear(); ax2.clear()

        # show all magnitudes lightly + average
        for H in self.frfs:
            mag, ph = mag_phase(H)
            ax1.plot(self.f, mag, alpha=0.35)
        M = avg_magnitude(self.frfs)
        ax1.plot(self.f, M, linewidth=2)
        ax1.set_xlim(0,self.fmax.value())
        ax1.set_xlabel("f [Hz]")
        ax1.set_ylabel("|H(f)| (acc/force)")
        ax1.grid(True)
        

        # phase of first FRF
        mag0, ph0 = mag_phase(self.frfs[0])
        ax2.plot(self.f, ph0)
        ax2.set_xlim(0,self.fmax.value())
        ax2.set_xlabel("f [Hz]")
        ax2.set_ylabel("Phase [rad]")
        ax2.grid(True)

        self.canvas.draw()

    def on_mode_selected(self, row: int):
        if row < 0 or self.f is None or not self.frfs or self.mode_indices.size == 0:
            return
        idx = int(self.mode_indices[row])
        f_mode = float(self.f[idx])

        # participation across excitation points at this frequency
        v = participation_vector_at(self.frfs, idx, ref=0)
        self.v_complex = v
        self.omega = 2*np.pi*f_mode

        # update 3D scalar display (abs)
        self.update_3d_scalars(np.abs(v))

        # start animation
        self.t = 0.0
        if not self.timer.isActive():
            self.timer.start(16)  # ~60 fps

    def update_3d_scalars(self, scalars: np.ndarray):
        # rebuild point cloud with scalars
        pts = pv_points(self.points0, scalars=scalars)
        self.plotter.remove_actor(self.points_actor)
        self.points_actor = self.plotter.add_mesh(
            pts, scalars="amp", cmap="viridis",
            point_size=18, render_points_as_spheres=True
        )
        self.plotter.render()

    def animate_step(self):
        # animate all 6 nodes by v_complex (this visualizes "excitation participation", not response mode shape)
        self.t += 0.016
        pts_def = deform(self.points0, self.v_complex, self.direction, self.t, self.omega, self.scale.value())

        # update frame and points
        self.frame_mesh.points = pts_def
        pts = pv_points(pts_def, scalars=np.abs(self.v_complex))
        self.plotter.remove_actor(self.points_actor)
        self.points_actor = self.plotter.add_mesh(
            pts, scalars="amp", cmap="viridis",
            point_size=18, render_points_as_spheres=True
        )
        self.plotter.render()

def pv_points(points_xyz: np.ndarray, scalars: np.ndarray | None = None):
    import pyvista as pv
    poly = pv.PolyData(points_xyz)
    if scalars is not None:
        poly["amp"] = scalars
    return poly

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.resize(1200, 700)
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
