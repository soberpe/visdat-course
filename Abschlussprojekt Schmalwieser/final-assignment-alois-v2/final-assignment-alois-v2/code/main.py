from __future__ import annotations

import sys
from pathlib import Path
import numpy as np

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QLineEdit, QFileDialog, QSpinBox, QDoubleSpinBox,
    QTabWidget, QListWidget, QMessageBox, QGroupBox, QCheckBox, QComboBox
)

import matplotlib
matplotlib.use("QtAgg")
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import scipy.signal as sig

import pyvista as pv
from pyvistaqt import QtInteractor

# =========================================================
# IO: LabVIEW .lvm Loader
# =========================================================

def load_lvm_time_force_acc(path: str):
    """
    Load LabVIEW .lvm time-domain data.
    Header length can vary; we search the table header line that starts with 'X_Value'
    and contains 'Acceleration' and 'Force'.

    Returns arrays: t_s, acc_g, force_N
    """
    with open(path, "r", errors="ignore") as f:
        lines = f.readlines()

    start = None
    for i, l in enumerate(lines):
        s = l.strip()
        if s.startswith("X_Value") and ("Acceleration" in s) and ("Force" in s):
            start = i
            break
    if start is None:
        raise ValueError(
            "Konnte Datenheader nicht finden. Erwartet: Zeile mit 'X_Value', 'Acceleration', 'Force'."
        )

    import pandas as pd
    df = pd.read_csv(path, sep="\t", decimal=",", skiprows=start, engine="python")

    cols = df.columns.tolist()
    t_col = cols[0]
    acc_col = next((c for c in cols if "Acceleration" in c), None)
    force_col = next((c for c in cols if "Force" in c), None)
    if acc_col is None or force_col is None:
        raise ValueError(f"Spalten fehlen. Gefunden: {cols}")

    df = df[[t_col, acc_col, force_col]].dropna()
    t_s = df[t_col].to_numpy(dtype=float)
    acc_g = df[acc_col].to_numpy(dtype=float)
    force_N = df[force_col].to_numpy(dtype=float)
    return t_s, acc_g, force_N


# =========================================================
# FRF / Coherence / Peak Picking
# =========================================================

def estimate_fs(t_s: np.ndarray) -> float:
    dt = float(np.mean(np.diff(t_s)))
    if not np.isfinite(dt) or dt <= 0:
        raise ValueError("Ungültiger Zeitvektor; fs kann nicht bestimmt werden.")
    return 1.0 / dt


def compute_frf_h1_and_coherence(acc: np.ndarray, force: np.ndarray, fs: float, nperseg: int = 4096):
    """
    H1 FRF:
      H = S_af / S_ff

    Coherence:
      gamma^2 = |S_af|^2 / (S_aa * S_ff)

    Returns: f [Hz], H complex, coh [0..1]
    """
    acc = sig.detrend(acc)
    force = sig.detrend(force)

    f, S_ff = sig.welch(force, fs=fs, nperseg=nperseg)
    _, S_af = sig.csd(acc, force, fs=fs, nperseg=nperseg)
    H = S_af / (S_ff + np.finfo(float).eps)

    f_coh, coh = sig.coherence(acc, force, fs=fs, nperseg=nperseg)
    if len(f_coh) != len(f) or np.max(np.abs(f_coh - f)) > 1e-9:
        coh = np.interp(f, f_coh, coh)

    return f, H, coh


def avg_magnitude(frfs: list[np.ndarray]) -> np.ndarray:
    mags = np.vstack([np.abs(H) for H in frfs])
    return mags.mean(axis=0)


def pick_modes_peak_picking(f: np.ndarray, M: np.ndarray, n_modes: int, fmax: float, prominence_rel: float):
    """
    Simple peak picking on M(f) in range [0, fmax].
    Returns indices into f/M.
    """
    mask = f <= fmax
    if not np.any(mask):
        return np.array([], dtype=int)

    prom = prominence_rel * float(np.max(M[mask]))
    peaks, _ = sig.find_peaks(M[mask], prominence=prom)
    if peaks.size == 0:
        return np.array([], dtype=int)

    full_idx = np.flatnonzero(mask)[peaks]
    top = full_idx[np.argsort(M[full_idx])[::-1]][:n_modes]  # strongest peaks
    return np.sort(top)  # sorted by freq


def participation_vector_windowed(frfs: list[np.ndarray], f: np.ndarray, idx_center: int, band_hz: float, ref: int = 0):
    """
    Robust complex participation by averaging complex FRF values in a frequency window ±band_hz.
    This avoids the "single FFT bin" jitter.

    Returns v (len(frfs),) complex, normalized max(|v|)=1, phase referenced to ref index.
    """
    f0 = float(f[idx_center])
    idx_window = np.where((f >= f0 - band_hz) & (f <= f0 + band_hz))[0]
    if idx_window.size == 0:
        idx_window = np.array([idx_center], dtype=int)

    v = np.array([np.mean(H[idx_window]) for H in frfs], dtype=complex)

    if np.abs(v[ref]) > 0:
        v = v * np.exp(-1j * np.angle(v[ref]))

    m = np.max(np.abs(v))
    if m > 0:
        v = v / m
    return v


# =========================================================
# 3D Geometry: 16 nodes (square base) + fixed bottom storey
# =========================================================

def building_points_16(size: float = 1.0, height_levels: tuple[float, float, float, float] = (0.0, 0.4, 0.8, 1.2)) -> np.ndarray:
    """
    16 nodes = 4 corners per level * 4 levels.

    We model a square footprint with corners:
      (-s/2, -s/2), (s/2, -s/2), (s/2, s/2), (-s/2, s/2)

    Levels (z): e.g. [0.0, 0.4, 0.8, 1.2]
      Level 0 = fixed "foundation storey"  (indices 0..3)  -> should not move
      Level 1 = bottom (indices 4..7)
      Level 2 = middle (indices 8..11)
      Level 3 = top    (indices 12..15)
    """
    s = float(size)
    half = 0.5 * s
    corners_xy = np.array([
        [-half, -half],  # corner 0
        [ half, -half],  # corner 1
        [ half,  half],  # corner 2
        [-half,  half],  # corner 3
    ], dtype=float)

    pts = []
    for z in height_levels:
        for (x, y) in corners_xy:
            pts.append([x, y, float(z)])
    return np.array(pts, dtype=float)


def building_edges_16() -> list[tuple[int, int]]:
    """
    Frame edges:
    - Per level: square perimeter (4 edges)
    - Columns: connect corresponding corners between adjacent levels
    """
    edges: list[tuple[int, int]] = []

    # square perimeter edges for a level starting index o (4 nodes)
    def level_edges(o: int):
        return [(o+0, o+1), (o+1, o+2), (o+2, o+3), (o+3, o+0)]

    # 4 levels -> offsets: 0,4,8,12
    for o in (0, 4, 8, 12):
        edges += level_edges(o)

    # vertical columns between levels
    for level in range(3):  # connect 0-1, 1-2, 2-3
        oA = level * 4
        oB = (level + 1) * 4
        for c in range(4):
            edges.append((oA + c, oB + c))

    return edges

def build_ground_grid(z: float, size: float = 1.2, n: int = 8) -> pv.PolyData:
    """
    Erzeugt ein fixes Grid in der Ebene z.
    size: Kantenlänge (etwas größer als Gebäude)
    n: Anzahl Unterteilungen pro Seite
    """
    half = size / 2
    xs = np.linspace(-half, half, n + 1)
    ys = np.linspace(-half, half, n + 1)

    points = []
    lines = []

    def add_line(p0, p1):
        i0 = len(points); points.append(p0)
        i1 = len(points); points.append(p1)
        lines.extend([2, i0, i1])

    # horizontale Linien (y konstant)
    for y in ys:
        add_line([-half, y, z], [half, y, z])

    # vertikale Linien (x konstant)
    for x in xs:
        add_line([x, -half, z], [x, half, z])

    poly = pv.PolyData(np.array(points))
    poly.lines = np.array(lines, dtype=np.int64)
    return poly






def build_frame(points_xyz: np.ndarray, edges: list[tuple[int, int]]) -> pv.PolyData:
    poly = pv.PolyData(points_xyz)
    lines = []
    for a, b in edges:
        lines += [2, a, b]
    poly.lines = np.array(lines, dtype=np.int64)
    return poly


def points_poly(points_xyz: np.ndarray, scalars: np.ndarray | None = None) -> pv.PolyData:
    poly = pv.PolyData(points_xyz)
    if scalars is not None:
        poly["amp"] = scalars
    return poly


def deform(points_xyz: np.ndarray, v_complex: np.ndarray, direction: np.ndarray, t: float, omega: float, scale: float) -> np.ndarray:
    direction = direction / (np.linalg.norm(direction) + 1e-12)
    disp = scale * np.real(v_complex * np.exp(1j * omega * t))  # (N,)
    return points_xyz + disp[:, None] * direction[None, :]


# =========================================================
# Export helpers
# =========================================================

def save_figure_png(fig, path: Path, dpi: int = 200):
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=dpi, bbox_inches="tight")


def save_gif(frames_rgb: list[np.ndarray], path: Path, fps: int = 30):
    path.parent.mkdir(parents=True, exist_ok=True)
    import imageio.v2 as imageio
    imageio.mimsave(path, frames_rgb, fps=fps)


# =========================================================
# Matplotlib canvases
# =========================================================

class FRFCanvas(FigureCanvas):
    """Magnitude + phase canvas."""
    def __init__(self):
        fig = Figure(figsize=(6, 4))
        self.ax_mag = fig.add_subplot(211)
        self.ax_ph = fig.add_subplot(212, sharex=self.ax_mag)
        super().__init__(fig)


class CoherenceCanvas(FigureCanvas):
    """Coherence canvas."""
    def __init__(self):
        fig = Figure(figsize=(6, 3))
        self.ax = fig.add_subplot(111)
        super().__init__(fig)


# =========================================================
# Main GUI
# =========================================================

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.base_dir = Path(__file__).resolve().parent
        self.setWindowTitle("Hochhaus – Mode Visualizer")
        # Merkt sich, welche Mode aktuell ausgewählt ist (für Peak-Band shading im Plot)
        # -1 bedeutet: keine Mode ausgewählt
        self.current_mode_row = -1
        # -----------------------
        # Data containers
        # -----------------------
        self.frfs: list[np.ndarray] = []        # 6 complex FRFs (excitation point 1..6)
        self.coherences: list[np.ndarray] = []
        self.f: np.ndarray | None = None
        self.mode_indices: np.ndarray = np.array([], dtype=int)
        

        # -----------------------
        # 3D Model (16 nodes)
        # -----------------------
        self.points0 = building_points_16(size=1.0, height_levels=(0.0, 0.4, 0.8, 1.2))
        self.edges = building_edges_16()
        self.frame_mesh = build_frame(self.points0, self.edges)

        # Level 0 (indices 0..3) = fixed foundation storey
        self.fixed_indices = np.array([0, 1, 2, 3], dtype=int)

        # Motion direction (because you measured only ONE direction)
        self.direction = np.array([1.0, 0.0, 0.0])

        self.v_complex = np.zeros(16, dtype=complex)  # will be set when mode selected
        self.omega = 2*np.pi*5.0
        self.t = 0.0

        # Export folder (relative to project)
        self.export_dir = Path(__file__).resolve().parents[1] / "assets" / "screenshots"
        self.export_dir.mkdir(parents=True, exist_ok=True)

        # =====================================================
        # LEFT: files + params + export
        # =====================================================
        left = QWidget()
        left_layout = QVBoxLayout(left)

        files_box = QGroupBox("Messdateien (.lvm) – Anregung Punkt 1..6 (Response immer Punkt 1)")
        grid = QGridLayout(files_box)
        
        
        self.file_edits: list[QLineEdit] = []

        for i in range(6):
            edit = QLineEdit()

            # --------------------------------------------------
            # Default-Pfad: relativ zu main.py
            # code/data/sample/Time 1-X.lvm
            # --------------------------------------------------
            default_file = self.base_dir / "data" / "sample" / f"Time 1-{i+1}.lvm"
            if default_file.exists():
                edit.setText(str(default_file))
            else:
                edit.setPlaceholderText("Datei wählen …")

            btn = QPushButton("Browse")
            btn.clicked.connect(lambda _, k=i: self.browse_file(k))

            self.file_edits.append(edit)
            grid.addWidget(QLabel(f"Punkt {i+1}"), i, 0)
            grid.addWidget(edit, i, 1)
            grid.addWidget(btn, i, 2)







        left_layout.addWidget(files_box)

        params_box = QGroupBox("Analyse-Parameter")
        pgrid = QGridLayout(params_box)

        self.n_modes = QSpinBox()
        self.n_modes.setRange(1, 10)
        self.n_modes.setValue(5)

        self.fmax = QDoubleSpinBox()
        self.fmax.setRange(1.0, 2000.0)
        self.fmax.setValue(60.0)
        self.fmax.setSuffix(" Hz")

        self.prom = QDoubleSpinBox()
        self.prom.setRange(0.001, 1.0)
        self.prom.setDecimals(3)
        self.prom.setSingleStep(0.01)
        self.prom.setValue(0.05)

        # Peak window half-band (±) in Hz for robust complex averaging
        self.peak_band = QDoubleSpinBox()
        self.peak_band.setRange(0.0, 50.0)
        self.peak_band.setDecimals(2)
        self.peak_band.setSingleStep(0.1)
        self.peak_band.setValue(0.3)
        self.peak_band.setSuffix(" Hz")

        self.scale = QDoubleSpinBox()
        self.scale.setRange(0.01, 20.0)
        self.scale.setValue(1.0)
        self.scale.setSingleStep(0.1)

        self.show_all_coh = QCheckBox("Alle Kohärenzen plotten (sonst nur Mittelwert)")
        self.show_all_coh.setChecked(False)
        self.show_all_coh.stateChanged.connect(self.update_coherence_plot)

        pgrid.addWidget(QLabel("Anzahl Moden:"), 0, 0)
        pgrid.addWidget(self.n_modes, 0, 1)
        pgrid.addWidget(QLabel("fmax Peak-Picking:"), 1, 0)
        pgrid.addWidget(self.fmax, 1, 1)
        pgrid.addWidget(QLabel("Prominence (rel.):"), 2, 0)
        pgrid.addWidget(self.prom, 2, 1)
        pgrid.addWidget(QLabel("Peak-Band (±):"), 3, 0)
        pgrid.addWidget(self.peak_band, 3, 1)
        pgrid.addWidget(QLabel("3D Scale:"), 4, 0)
        pgrid.addWidget(self.scale, 4, 1)
        pgrid.addWidget(self.show_all_coh, 5, 0, 1, 2)

        left_layout.addWidget(params_box)

        self.btn_analyze = QPushButton("Load & Analyze")
        self.btn_analyze.clicked.connect(self.load_and_analyze)
        left_layout.addWidget(self.btn_analyze)

        export_box = QGroupBox("Export")
        ex = QGridLayout(export_box)

        self.btn_export_frf = QPushButton("Export FRF Plot (PNG)")
        self.btn_export_frf.clicked.connect(self.export_frf_png)
        self.btn_export_3d = QPushButton("Export 3D Screenshot (PNG)")
        self.btn_export_3d.clicked.connect(self.export_3d_png)
        self.btn_export_gif = QPushButton("Export 3D Animation (GIF)")
        self.btn_export_gif.clicked.connect(self.export_3d_gif)

        ex.addWidget(self.btn_export_frf, 0, 0, 1, 2)
        ex.addWidget(self.btn_export_3d, 1, 0, 1, 2)
        ex.addWidget(self.btn_export_gif, 2, 0, 1, 2)

        left_layout.addWidget(export_box)
        left_layout.addStretch(1)

        # =====================================================
        # RIGHT: tabs
        # =====================================================
        self.tabs = QTabWidget()

        # FRF tab
        frf_tab = QWidget()
        frf_layout = QVBoxLayout(frf_tab)
        self.frf_canvas = FRFCanvas()
        frf_layout.addWidget(self.frf_canvas)
        self.tabs.addTab(frf_tab, "FRFs")

        # Coherence tab
        coh_tab = QWidget()
        coh_layout = QVBoxLayout(coh_tab)
        self.coh_canvas = CoherenceCanvas()
        coh_layout.addWidget(self.coh_canvas)
        self.tabs.addTab(coh_tab, "Kohärenz")

        # Modes tab (list)
        modes_tab = QWidget()
        modes_layout = QVBoxLayout(modes_tab)
        modes_layout.addWidget(QLabel("Gefundene Moden:"))
        self.mode_list = QListWidget()
        self.mode_list.currentRowChanged.connect(self.on_mode_selected_from_list)
        modes_layout.addWidget(self.mode_list)
        self.tabs.addTab(modes_tab, "Moden")

        # 3D tab with dropdown selector
        view_tab = QWidget()
        view_layout = QVBoxLayout(view_tab)

        ctrl_row = QWidget()
        ctrl_layout = QHBoxLayout(ctrl_row)
        ctrl_layout.setContentsMargins(0, 0, 0, 0)
        ctrl_layout.addWidget(QLabel("Mode auswählen:"))
        self.mode_combo = QComboBox()
        self.mode_combo.currentIndexChanged.connect(self.on_mode_selected_from_combo)
        ctrl_layout.addWidget(self.mode_combo, 1)
        view_layout.addWidget(ctrl_row)

        self.plotter = QtInteractor(view_tab)
        # ===== Fixed ground grid (never deformed)
        ground = build_ground_grid(z=float(self.points0[self.fixed_indices[0], 2]), size=1.6, n=10)
        self.ground_actor = self.plotter.add_mesh(
            ground,
            color="gray",
            line_width=3,
            render_lines_as_tubes=True
)

        self.plotter.set_background("white")
        view_layout.addWidget(self.plotter.interactor)

        self.tabs.addTab(view_tab, "3D")

        # =====================================================
        # Main layout
        # =====================================================
        main = QWidget()
        main_layout = QHBoxLayout(main)
        main_layout.addWidget(left, 1)
        main_layout.addWidget(self.tabs, 2)
        self.setCentralWidget(main)

        # =====================================================
        # 3D Scene: black tubes on white background
        # =====================================================
        # Render lines as tubes -> always clearly visible
        self.frame_actor = self.plotter.add_mesh(
            self.frame_mesh,
            color="black",
            line_width=8,
            render_lines_as_tubes=True
        )

        # Points actor (colored by amplitude)
        self.points_actor = self.plotter.add_mesh(
            points_poly(self.points0, scalars=np.zeros(16)),
            scalars="amp",
            cmap="viridis",
            point_size=18,
            render_points_as_spheres=True
        )

        self.plotter.show_axes()
        self.plotter.reset_camera()

        # Animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_step)

        # Auto-rescale plots when fmax changes
        self.fmax.valueChanged.connect(self.update_frf_plot)
        self.fmax.valueChanged.connect(self.update_coherence_plot)

    # =====================================================
    # File browsing / loading
    # =====================================================

    def browse_file(self, idx: int):
        start_dir = self.base_dir / "data" / "sample"
        p, _ = QFileDialog.getOpenFileName(
            self,
            "Select .lvm file",
            str(start_dir),
            "LabVIEW Measurement (*.lvm);;All Files (*)"
        )


        if p:
            self.file_edits[idx].setText(p)

    def _resolve_paths(self) -> list[str]:
        """
        If user didn't select files, try local sample folder:
          code/data/sample/Time 1-1.lvm ... Time 1-6.lvm
        """
        paths = []
        for i in range(6):
            p = self.file_edits[i].text().strip()
            if not p:
                sample = Path(__file__).parent / "data" / "sample" / f"Time 1-{i+1}.lvm"
                if sample.exists():
                    p = str(sample)
                    self.file_edits[i].setText(p)
                else:
                    raise ValueError(f"Bitte Datei für Punkt {i+1} auswählen.")
            paths.append(p)
        return paths

    # =====================================================
    # Analysis
    # =====================================================

    def load_and_analyze(self):
        try:
            paths = self._resolve_paths()

            self.frfs.clear()
            self.coherences.clear()
            self.f = None

            for p in paths:
                t_s, acc_g, force_N = load_lvm_time_force_acc(p)
                fs = estimate_fs(t_s)
                f, H, coh = compute_frf_h1_and_coherence(acc_g, force_N, fs=fs, nperseg=4096)

                if self.f is None:
                    self.f = f
                else:
                    if len(f) != len(self.f) or np.max(np.abs(f - self.f)) > 1e-6:
                        raise ValueError("Frequenzraster nicht identisch (Interpolation kann man später ergänzen).")

                self.frfs.append(H)
                self.coherences.append(coh)

            # Peak picking on mean |H|
            M = avg_magnitude(self.frfs)
            self.mode_indices = pick_modes_peak_picking(
                self.f, M,
                n_modes=int(self.n_modes.value()),
                fmax=float(self.fmax.value()),
                prominence_rel=float(self.prom.value())
            )

            # Fill list + combo (synchronized)
            self.mode_list.blockSignals(True)
            self.mode_combo.blockSignals(True)

            self.mode_list.clear()
            self.mode_combo.clear()

            for k, idx in enumerate(self.mode_indices, start=1):
                label = f"Mode {k}: f = {self.f[idx]:.3f} Hz"
                self.mode_list.addItem(label)
                self.mode_combo.addItem(label)

            self.mode_list.blockSignals(False)
            self.mode_combo.blockSignals(False)

            self.update_frf_plot()
            self.update_coherence_plot()

            # Auto-select first mode if available
            if self.mode_indices.size > 0:
                self.mode_list.setCurrentRow(0)
                self.mode_combo.setCurrentIndex(0)

            QMessageBox.information(self, "OK", "Analyse fertig: FRFs + Kohärenz + Moden.")
        except Exception as e:
            QMessageBox.critical(self, "Fehler", str(e))

    # =====================================================
    # Plotting
    # =====================================================

    def update_frf_plot(self):
        if self.f is None or not self.frfs:
            return

        fmax = float(self.fmax.value())
        mask = self.f <= fmax

        ax_mag = self.frf_canvas.ax_mag
        ax_ph = self.frf_canvas.ax_ph
        ax_mag.clear()
        ax_ph.clear()

        for H in self.frfs:
            ax_mag.plot(self.f[mask], np.abs(H)[mask], alpha=0.30)

        M = avg_magnitude(self.frfs)
        ax_mag.plot(self.f[mask], M[mask], linewidth=2)
        ax_mag.set_ylabel("|H(f)| (acc/force)")
        ax_mag.grid(True)
        ax_mag.set_xlim(0, fmax)
        ph0 = np.unwrap(np.angle(self.frfs[0]))
        # ======================================================
# A) Moden als vertikale Linien + Marker
# ======================================================
# self.mode_indices enthält die Indizes der gefundenen Peaks in f/M.
# Wir zeichnen:
#   - gestrichelte vertikale Linie bei jeder Eigenfrequenz
#   - Punkt/Marker am Peakwert
        if self.mode_indices.size > 0:
            f_modes = self.f[self.mode_indices]
            ax_mag.vlines(
                f_modes,
                ymin=0,
                ymax=M[self.mode_indices],
                linestyles="--",
                alpha=0.7
            )
            ax_mag.scatter(f_modes, M[self.mode_indices], s=35, zorder=5)

            # Optional auch im Phasenplot Linien (hilft beim Erkennen des Phasensprungs)
            ax_ph.vlines(
                f_modes,
                ymin=np.min(ph0[mask]),
                ymax=np.max(ph0[mask]),
                linestyles="--",
                alpha=0.25
            )

        # ======================================================
        # B) Peak-Band (± Peak-Band) für ALLE Moden schattieren
        # ======================================================
        if self.mode_indices.size > 0:
            band = float(self.peak_band.value())
            for idx_center in self.mode_indices:
                f0 = float(self.f[int(idx_center)])
                ax_mag.axvspan(f0 - band, f0 + band, alpha=0.08)
                ax_ph.axvspan(f0 - band, f0 + band, alpha=0.05)


        # ======================================================
        # C) Prominence visuell darstellen
        # ======================================================
        # Prominence (Peak-Prominenz) bedeutet: "Wie stark ragt der Peak über seine Umgebung?"
        # In deinem Peak-Picking nutzt du prominence_rel * max(M) als Mindestkriterium.
        prom_rel = float(self.prom.value())
        thr = prom_rel * float(np.max(M[mask]))

        # 1) Globale Schwelle als horizontale Linie:
        ax_mag.axhline(
            thr,
            linestyle=":",
            linewidth=1.5,
            alpha=0.7,
            label=f"Prominence threshold ≈ {thr:.3g}"
        )

        # 2) Zusätzlich: echte lokale Prominence (SciPy) als "Klammer" am gewählten Peak
        #    Damit sieht man: Peak-Höhe minus "Base level" (Sattelpunkt).
        if self.current_mode_row >= 0 and self.mode_indices.size > 0:
            import scipy.signal as sig

            f_sub = self.f[mask]
            M_sub = M[mask]

            # Peak-Indizes auf sub-array mappen:
            sub_peaks = np.searchsorted(f_sub, self.f[self.mode_indices])
            sub_peaks = sub_peaks[(sub_peaks >= 0) & (sub_peaks < len(M_sub))]

            if len(sub_peaks) > 0:
                prominences, left_bases, right_bases = sig.peak_prominences(M_sub, sub_peaks)

                k = min(self.current_mode_row, len(sub_peaks) - 1)
                p_idx = sub_peaks[k]              # Index des Peak in M_sub
                prom = prominences[k]             # echte Prominence
                base_level = max(M_sub[left_bases[k]], M_sub[right_bases[k]])
                peak_level = M_sub[p_idx]
                f_peak = f_sub[p_idx]

                # Vertikale Klammer von base -> peak
                ax_mag.vlines(f_peak, base_level, peak_level, linewidth=3, alpha=0.9)

                # kleiner Querstrich am base-level
                ax_mag.hlines(base_level, f_peak - 0.15, f_peak + 0.15, linewidth=3, alpha=0.9)

                ax_mag.text(f_peak, peak_level, f"  prom={prom:.3g}", va="bottom")













        ax_ph.plot(self.f[mask], ph0[mask])
        ax_ph.set_xlabel("f [Hz]")
        ax_ph.set_ylabel("Phase [rad]")
        ax_ph.grid(True)
        ax_ph.set_xlim(0, fmax)

        self.frf_canvas.draw()

    def update_coherence_plot(self):
        if self.f is None or not self.coherences:
            return

        fmax = float(self.fmax.value())
        mask = self.f <= fmax

        ax = self.coh_canvas.ax
        ax.clear()

        if self.show_all_coh.isChecked():
            for coh in self.coherences:
                ax.plot(self.f[mask], coh[mask], alpha=0.30)

        coh_mean = np.mean(np.vstack(self.coherences), axis=0)
        ax.plot(self.f[mask], coh_mean[mask], linewidth=2)
        ax.set_xlabel("f [Hz]")
        ax.set_ylabel("Kohärenz γ²")
        ax.set_ylim(0.0, 1.05)
        ax.grid(True)
        ax.set_xlim(0, fmax)

        self.coh_canvas.draw()

    # =====================================================
    # Mode selection (list + combo) -> shared handler
    # =====================================================

    def on_mode_selected_from_list(self, row: int):
        if row < 0:
            return
        # keep combo synced
        if self.mode_combo.currentIndex() != row:
            self.mode_combo.blockSignals(True)
            self.mode_combo.setCurrentIndex(row)
            self.mode_combo.blockSignals(False)
        self._apply_mode(row)

    def on_mode_selected_from_combo(self, row: int):
        if row < 0:
            return
        # keep list synced
        if self.mode_list.currentRow() != row:
            self.mode_list.blockSignals(True)
            self.mode_list.setCurrentRow(row)
            self.mode_list.blockSignals(False)
        self._apply_mode(row)

    def _apply_mode(self, row: int):
        # Speichern, welche Mode gerade aktiv ist (für Visualisierung im FRF-Plot)
        self.current_mode_row = row

        if self.f is None or not self.frfs or self.mode_indices.size == 0:
            return

        idx_center = int(self.mode_indices[row])
        f_mode = float(self.f[idx_center])

        # IMPORTANT INTERPRETATION:
        # With your measurement setup (only response at point 1),
        # we can not reconstruct a spatial mode shape.
        # We can only compute a per-excitation "participation" at the mode frequency.
        band = float(self.peak_band.value())
        v6 = participation_vector_windowed(self.frfs, self.f, idx_center, band_hz=band, ref=0)

        # -----------------------------
        # Mapping 6 participation values -> 16-node building
        #
        # Your excitation points are (as you described) on ONE facade:
        #   top-left(1), top-right(2), mid-left(3), mid-right(4), bot-left(5), bot-right(6)
        #
        # Our 16-node square building has 4 corners per level.
        # We'll map:
        #   Level 3 (top)    : front-left, front-right  <- v6[0], v6[1]
        #   Level 2 (middle) : front-left, front-right  <- v6[2], v6[3]
        #   Level 1 (bottom) : front-left, front-right  <- v6[4], v6[5]
        #
        # And for a symmetric look we mirror to the back-left/back-right corners
        # with the same amplitudes. All other corners (side corners) get the same
        # as their nearest front/back counterpart.
        #
        # Level 0 (foundation) is FIXED: amplitude forced to 0.
        # -----------------------------

        # Node indices per level (4 nodes each):
        # level0: 0..3 (fixed)
        # level1: 4..7
        # level2: 8..11
        # level3: 12..15
        #
        # Corner order in each level:
        # 0: (-x,-y)  front-left-ish
        # 1: (+x,-y)  front-right-ish
        # 2: (+x,+y)  back-right-ish
        # 3: (-x,+y)  back-left-ish

        v16 = np.zeros(16, dtype=complex)

        # Level 3 (top): use v6[0], v6[1]
        v16[12 + 0] = v6[0]
        v16[12 + 1] = v6[1]
        v16[12 + 2] = v6[1]  # mirror
        v16[12 + 3] = v6[0]  # mirror

        # Level 2 (middle): v6[2], v6[3]
        v16[8 + 0] = v6[2]
        v16[8 + 1] = v6[3]
        v16[8 + 2] = v6[3]
        v16[8 + 3] = v6[2]

        # Level 1 (bottom): v6[4], v6[5]
        v16[4 + 0] = v6[4]
        v16[4 + 1] = v6[5]
        v16[4 + 2] = v6[5]
        v16[4 + 3] = v6[4]

        # Level 0 fixed:
        v16[self.fixed_indices] = 0.0 + 0.0j

        self.v_complex = v16
        self.omega = 2*np.pi*f_mode
        self.t = 0.0

        # Color nodes by amplitude (foundation stays at 0 -> visible but darkest)
        self._update_3d_points(self.points0, np.abs(self.v_complex))

        if not self.timer.isActive():
            self.timer.start(16)
        # FRF neu zeichnen -> zeigt Peak-Band + Prominence-Klammer für aktuelle Mode
        self.update_frf_plot()

    # =====================================================
    # Animation
    # =====================================================

    def animate_step(self):
        self.t += 0.016

        pts_def = deform(
            self.points0, self.v_complex, self.direction,
            t=self.t, omega=self.omega, scale=float(self.scale.value())
        )

        # Hard clamp the fixed foundation storey (just to be 100% safe)
        pts_def[self.fixed_indices, :] = self.points0[self.fixed_indices, :]

        # Update frame geometry + points
        self.frame_mesh.points = pts_def
        self._update_3d_points(pts_def, np.abs(self.v_complex))

    def _update_3d_points(self, points: np.ndarray, scalars: np.ndarray):
        try:
            self.plotter.remove_actor(self.points_actor)
        except Exception:
            pass

        self.points_actor = self.plotter.add_mesh(
            points_poly(points, scalars=scalars),
            scalars="amp",
            cmap="viridis",
            point_size=18,
            render_points_as_spheres=True
        )
        self.plotter.render()

    # =====================================================
    # Export
    # =====================================================

    def export_frf_png(self):
        try:
            out = self.export_dir / "frf_plot.png"
            save_figure_png(self.frf_canvas.figure, out)
            QMessageBox.information(self, "Export", f"FRF Plot gespeichert: {out}")
        except Exception as e:
            QMessageBox.critical(self, "Export-Fehler", str(e))

    def export_3d_png(self):
        try:
            out = self.export_dir / "3d_view.png"
            self.plotter.screenshot(str(out))
            QMessageBox.information(self, "Export", f"3D Screenshot gespeichert: {out}")
        except Exception as e:
            QMessageBox.critical(self, "Export-Fehler", str(e))

    def export_3d_gif(self):
        try:
            if self.f is None or self.mode_indices.size == 0:
                raise ValueError("Bitte zuerst analysieren und eine Mode auswählen.")

            fps = 30
            seconds = 3.0
            n_frames = int(fps * seconds)
            dt = 1.0 / fps

            frames = []
            for k in range(n_frames):
                t = k * dt

                pts_def = deform(
                    self.points0, self.v_complex, self.direction,
                    t=t, omega=self.omega, scale=float(self.scale.value())
                )
                pts_def[self.fixed_indices, :] = self.points0[self.fixed_indices, :]

                self.frame_mesh.points = pts_def
                self._update_3d_points(pts_def, np.abs(self.v_complex))

                img = self.plotter.screenshot(return_img=True)
                if img is None:
                    raise RuntimeError("Screenshot returned None.")
                if img.shape[-1] == 4:
                    img = img[..., :3]
                frames.append(img.astype(np.uint8))

            out = self.export_dir / "3d_animation.gif"
            save_gif(frames, out, fps=fps)
            QMessageBox.information(self, "Export", f"GIF gespeichert: {out}")
        except Exception as e:
            QMessageBox.critical(self, "Export-Fehler", str(e))


def main():
    # Absoluter Pfad zum Ordner, in dem main.py liegt
    

    app = QApplication(sys.argv)
    w = MainWindow()
    w.resize(1400, 780)
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
