from __future__ import annotations

"""PyQt6 GUI for the Final Assignment.

What the program does
---------------------
- Load 6 LabVIEW .lvm files (excitation point 1..6; response is always at point 1).
- Compute FRFs (H1 estimator) for each excitation.
- Peak-pick modal frequencies on the mean magnitude |H|.
- For a selected mode, compute a complex participation vector (windowed average
  around the peak) and show it on a simple 3D stick model.
- Export FRF plot PNG, 3D screenshot PNG, and a short 3D animation GIF.

Change requested for the final submission
----------------------------------------
- All functionality related to coherence was removed.
"""

import sys
from pathlib import Path

import numpy as np

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QDoubleSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

import pyvista as pv
from pyvistaqt import QtInteractor

from exporting import save_figure_png, save_gif
from frf_analysis import (
    avg_magnitude,
    compute_frf_h1,
    estimate_fs,
    participation_vector_windowed,
    pick_modes_peak_picking,
)
from geometry import building_points_16, building_edges_16, fixed_ground_indices
from io_lvm import load_lvm_time_force_acc
from ui_canvases import FRFCanvas, Mode2DCanvas
from viewer3d import build_frame, deform, points_poly


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()

        self.base_dir = Path(__file__).resolve().parent
        self.setWindowTitle("Hochhaus – FRF & Mode Visualizer")

        # ----------- data containers -----------
        self.f: np.ndarray | None = None
        self.frfs: list[np.ndarray] = []  # 6 complex FRFs (excitation points 1..6)
        self.mode_indices: np.ndarray = np.array([], dtype=int)
        self.current_mode_row: int = -1  # for peak/prominence highlighting

        # ----------- 3D model (16 nodes) -----------
        self.points0 = building_points_16(width=0.4, depth=None)
        self.edges = building_edges_16()
        self.frame_mesh = build_frame(self.points0, self.edges)

        # Motion direction: we only have a single response direction.
        self.direction = np.array([1.0, 0.0, 0.0])

        self.v_complex = np.zeros(len(self.points0), dtype=complex)
        self.omega = 2.0 * np.pi * 5.0
        self.t = 0.0

        # Export directory (project-root/assets/screenshots)
        self.export_dir = Path(__file__).resolve().parents[1] / "assets" / "screenshots"
        self.export_dir.mkdir(parents=True, exist_ok=True)

        # ----------- build UI -----------
        self._build_ui()

        # ----------- 3D scene -----------
        self._init_3d_scene()

        # Animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self._animate_step)

        # Auto-rescale plots when fmax changes
        self.fmax.valueChanged.connect(self.update_frf_plot)

    # ---------------------------------------------------------------------
    # UI construction
    # ---------------------------------------------------------------------

    def _build_ui(self) -> None:
        """Create all widgets and layouts."""

        # ========================
        # LEFT: files + parameters
        # ========================
        left = QWidget()
        left_layout = QVBoxLayout(left)

        files_box = QGroupBox(
            "Messdateien (.lvm)"
        )
        grid = QGridLayout(files_box)

        self.file_edits: list[QLineEdit] = []
        for i in range(6):
            edit = QLineEdit()

            # Default path: relative to this script
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
        self.n_modes.setValue(4)

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
        self.scale.setValue(0.1)
        self.scale.setSingleStep(0.1)

        pgrid.addWidget(QLabel("Anzahl Moden:"), 0, 0)
        pgrid.addWidget(self.n_modes, 0, 1)
        pgrid.addWidget(QLabel("fmax:"), 1, 0)
        pgrid.addWidget(self.fmax, 1, 1)
        pgrid.addWidget(QLabel("Prominence:"), 2, 0)
        pgrid.addWidget(self.prom, 2, 1)
        pgrid.addWidget(QLabel("Peak-Band (±):"), 3, 0)
        pgrid.addWidget(self.peak_band, 3, 1)
        pgrid.addWidget(QLabel("3D Scale:"), 4, 0)
        pgrid.addWidget(self.scale, 4, 1)

        left_layout.addWidget(params_box)

        self.btn_analyze = QPushButton("Analyze")
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

        # ========================
        # RIGHT: tabs
        # ========================
        self.tabs = QTabWidget()

        # FRF tab
        frf_tab = QWidget()
        frf_layout = QVBoxLayout(frf_tab)
        self.frf_canvas = FRFCanvas()
        frf_layout.addWidget(self.frf_canvas)
        self.tabs.addTab(frf_tab, "FRFs")

        # Mode (2D) tab: static mode shape (mean of left/right per level)
        mode2d_tab = QWidget()
        mode2d_layout = QVBoxLayout(mode2d_tab)

        # --- top bar: mode selector ---
        mode2d_top = QHBoxLayout()
        mode2d_top.addWidget(QLabel("Mode:"))

        self.mode2d_combo = QComboBox()
        self.mode2d_combo.setToolTip("Select a mode/peak to show in the 2D view")
        mode2d_top.addWidget(self.mode2d_combo, stretch=1)

        mode2d_layout.addLayout(mode2d_top)

        # --- canvas ---
        self.mode2d_canvas = Mode2DCanvas()
        mode2d_layout.addWidget(self.mode2d_canvas)

        self.tabs.addTab(mode2d_tab, "Mode 2D")

        # --- connect selection change ---
        self.mode2d_combo.currentIndexChanged.connect(self.on_mode2d_selected)


        # Modes tab
        modes_tab = QWidget()
        modes_layout = QVBoxLayout(modes_tab)
        modes_layout.addWidget(QLabel("Gefundene Moden:"))
        self.mode_list = QListWidget()
        self.mode_list.currentRowChanged.connect(self.on_mode_selected_from_list)
        modes_layout.addWidget(self.mode_list)
        self.tabs.addTab(modes_tab, "Moden")

        # 3D tab
        view_tab = QWidget()
        view_layout = QVBoxLayout(view_tab)

        ctrl_row = QWidget()
        ctrl_layout = QHBoxLayout(ctrl_row)
        ctrl_layout.setContentsMargins(0, 0, 0, 0)
        ctrl_layout.addWidget(QLabel("Mode:"))
        self.mode_combo = QComboBox()
        self.mode_combo.currentIndexChanged.connect(self.on_mode_selected_from_combo)
        ctrl_layout.addWidget(self.mode_combo, 1)
        view_layout.addWidget(ctrl_row)

        self.plotter = QtInteractor(view_tab)
        self.plotter.set_background("white")
        view_layout.addWidget(self.plotter.interactor)

        self.tabs.addTab(view_tab, "3D")

        # ========================
        # Main layout
        # ========================
        main = QWidget()
        main_layout = QHBoxLayout(main)
        main_layout.addWidget(left, 1)
        main_layout.addWidget(self.tabs, 2)
        self.setCentralWidget(main)

    def _init_3d_scene(self) -> None:
        """Create initial 3D actors."""
        self.frame_actor = self.plotter.add_mesh(
            self.frame_mesh,
            color="black",
            line_width=6,
            render_lines_as_tubes=True,
        )

        # -------------------------------------------------
        # Ground grid (static, only at z = 0)
        # -------------------------------------------------
        # Bounding box of building footprint
        xmin, ymin, _ = np.min(self.points0, axis=0)
        xmax, ymax, _ = np.max(self.points0, axis=0)

        # Extend grid beyond the building edges
        side = max(xmax - xmin, ymax - ymin)
        margin = 0.30 * side  # 30% beyond the footprint

        gxmin = xmin - margin
        gxmax = xmax + margin
        gymin = ymin - margin
        gymax = ymax + margin

        n_lines = 11  # grid density (odd number looks nice)

        lines_pts = []
        # Lines parallel to Y (constant X)
        for x in np.linspace(gxmin, gxmax, n_lines):
            lines_pts.append([[x, gymin, 0.0], [x, gymax, 0.0]])
        # Lines parallel to X (constant Y)
        for y in np.linspace(gymin, gymax, n_lines):
            lines_pts.append([[gxmin, y, 0.0], [gxmax, y, 0.0]])

        pts = np.array([p for seg in lines_pts for p in seg], dtype=float)
        cells = []
        for i in range(0, len(pts), 2):
            cells.extend([2, i, i + 1])  # VTK polyline cell: [nPoints, id0, id1]

        grid_poly = pv.PolyData()
        grid_poly.points = pts
        grid_poly.lines = np.array(cells, dtype=np.int64)

        self.ground_grid_actor = self.plotter.add_mesh(
            grid_poly,
            color="lightgray",
            line_width=1,
            opacity=0.6,
        )

        # --- Points: create ONCE and update in-place each frame (prevents scalar bar flicker) ---

        self.points_pd = points_poly(self.points0, scalars=np.zeros(len(self.points0)))


        self.points_actor = self.plotter.add_mesh(

            self.points_pd,

            scalars="amp",

            cmap="viridis",

            point_size=16,

            render_points_as_spheres=True,

            clim=(0.0, 1.0),

            show_scalar_bar=True,

            scalar_bar_args={"title": "amp"},

        )

        self.plotter.show_axes()
        self.plotter.reset_camera()

    # ---------------------------------------------------------------------
    # File browsing / resolving
    # ---------------------------------------------------------------------

    def browse_file(self, idx: int) -> None:
        start_dir = self.base_dir / "data" / "sample"
        p, _ = QFileDialog.getOpenFileName(
            self,
            "Select .lvm file",
            str(start_dir),
            "LabVIEW Measurement (*.lvm);;All Files (*)",
        )
        if p:
            self.file_edits[idx].setText(p)

    def _resolve_paths(self) -> list[str]:
        """Collect file paths from the UI.

        If a field is empty, try to use the bundled sample files under:
        code/data/sample/Time 1-1.lvm ... Time 1-6.lvm
        """
        paths: list[str] = []
        for i, edit in enumerate(self.file_edits):
            p = edit.text().strip()
            if not p:
                sample = self.base_dir / "data" / "sample" / f"Time 1-{i+1}.lvm"
                if sample.exists():
                    p = str(sample)
                    edit.setText(p)
                else:
                    raise ValueError(f"Bitte Datei für Punkt {i+1} auswählen.")
            paths.append(p)
        return paths

    # ---------------------------------------------------------------------
    # Analysis
    # ---------------------------------------------------------------------

    def load_and_analyze(self) -> None:
        """Load all files, compute FRFs, pick modes, update UI."""
        try:
            paths = self._resolve_paths()

            self.frfs.clear()
            self.f = None
            self.mode_indices = np.array([], dtype=int)

            for p in paths:
                df = load_lvm_time_force_acc(p)
                t_s = df["t_s"].to_numpy(dtype=float)
                acc_g = df["acc_g"].to_numpy(dtype=float)
                force_N = df["force_N"].to_numpy(dtype=float)

                fs = estimate_fs(t_s)
                f, H = compute_frf_h1(acc_g, force_N, fs=fs, nperseg=4096)

                if self.f is None:
                    self.f = f
                else:
                    # For simplicity we require identical frequency grids.
                    if len(f) != len(self.f) or np.max(np.abs(f - self.f)) > 1e-6:
                        raise ValueError(
                            "Frequenzraster nicht identisch (Interpolation kann man später ergänzen)."
                        )

                self.frfs.append(H)

            # Peak picking on mean |H|
            M = avg_magnitude(self.frfs)
            self.mode_indices = pick_modes_peak_picking(
                self.f,
                M,
                n_modes=int(self.n_modes.value()),
                fmax=float(self.fmax.value()),
                prominence_rel=float(self.prom.value()),
            )

            # Fill list + combo (synchronised)
            self.mode_list.blockSignals(True)
            self.mode_combo.blockSignals(True)
            self.mode2d_combo.blockSignals(True)

            self.mode_list.clear()
            self.mode_combo.clear()
            self.mode2d_combo.clear()

            for k, idx in enumerate(self.mode_indices, start=1):
                label = f"Mode {k}: f = {self.f[idx]:.3f} Hz"
                self.mode_list.addItem(label)
                self.mode_combo.addItem(label)
                self.mode2d_combo.addItem(label)

            self.mode_list.blockSignals(False)
            self.mode_combo.blockSignals(False)
            self.mode2d_combo.blockSignals(False)

            self.update_frf_plot()

            # Auto-select first mode if available
            if self.mode_indices.size > 0:
                self.mode_list.setCurrentRow(0)
                self.mode_combo.setCurrentIndex(0)
                self.mode2d_combo.setCurrentIndex(0)

            QMessageBox.information(self, "OK", "Analyse fertig: FRFs + Moden.")

        except Exception as e:
            QMessageBox.critical(self, "Fehler", str(e))

    # ---------------------------------------------------------------------
    # Plotting
    # ---------------------------------------------------------------------

    def update_frf_plot(self) -> None:
        """Update FRF magnitude/phase plot."""
        if self.f is None or not self.frfs:
            return

        fmax = float(self.fmax.value())
        mask = self.f <= fmax

        ax_mag = self.frf_canvas.ax_mag
        ax_ph = self.frf_canvas.ax_ph
        ax_mag.clear()
        ax_ph.clear()

        # Plot each FRF (transparent)
        for H in self.frfs:
            ax_mag.plot(self.f[mask], np.abs(H)[mask], alpha=0.30)

        # Mean magnitude (bold)
        M = avg_magnitude(self.frfs)
        ax_mag.plot(self.f[mask], M[mask], linewidth=2)
        ax_mag.set_ylabel("|H(f)| (acc/force)")
        ax_mag.grid(True)
        ax_mag.set_xlim(0, fmax)

        # Phase from first FRF (unwrap)
        ph0 = np.unwrap(np.angle(self.frfs[0]))

        # A) Mark found modes
        if self.mode_indices.size > 0:
            f_modes = self.f[self.mode_indices]
            ax_mag.vlines(
                f_modes,
                ymin=0,
                ymax=M[self.mode_indices],
                linestyles="--",
                alpha=0.7,
            )
            ax_mag.scatter(f_modes, M[self.mode_indices], s=35, zorder=5)

            ax_ph.vlines(
                f_modes,
                ymin=np.min(ph0[mask]),
                ymax=np.max(ph0[mask]),
                linestyles="--",
                alpha=0.25,
            )

        # B) Shade peak-band around all detected modes
        if self.mode_indices.size > 0:
            band = float(self.peak_band.value())
            for idx_center in self.mode_indices:
                f0 = float(self.f[int(idx_center)])
                ax_mag.axvspan(f0 - band, f0 + band, alpha=0.08)
                ax_ph.axvspan(f0 - band, f0 + band, alpha=0.05)

        # C) Visualise the prominence threshold and, if a mode is selected, the
        #    *actual* prominence bracket for the selected peak.
        prom_rel = float(self.prom.value())
        thr = prom_rel * float(np.max(M[mask]))
        ax_mag.axhline(
            thr,
            linestyle=":",
            linewidth=1.5,
            alpha=0.7,
            label=f"Prominence threshold ≈ {thr:.3g}",
        )

        if self.current_mode_row >= 0 and self.mode_indices.size > 0:
            import scipy.signal as sig

            f_sub = self.f[mask]
            M_sub = M[mask]

            # Map peak indices into the masked array
            sub_peaks = np.searchsorted(f_sub, self.f[self.mode_indices])
            sub_peaks = sub_peaks[(sub_peaks >= 0) & (sub_peaks < len(M_sub))]

            if len(sub_peaks) > 0:
                prominences, left_bases, right_bases = sig.peak_prominences(M_sub, sub_peaks)

                k = min(self.current_mode_row, len(sub_peaks) - 1)
                p_idx = int(sub_peaks[k])
                prom = float(prominences[k])
                base_level = float(max(M_sub[left_bases[k]], M_sub[right_bases[k]]))
                peak_level = float(M_sub[p_idx])
                f_peak = float(f_sub[p_idx])

                ax_mag.vlines(f_peak, base_level, peak_level, linewidth=3, alpha=0.9)
                ax_mag.hlines(base_level, f_peak - 0.15, f_peak + 0.15, linewidth=3, alpha=0.9)
                ax_mag.text(f_peak, peak_level, f"  prom={prom:.3g}", va="bottom")

        ax_ph.plot(self.f[mask], ph0[mask])
        ax_ph.set_xlabel("f [Hz]")
        ax_ph.set_ylabel("Phase [rad]")
        ax_ph.grid(True)
        ax_ph.set_xlim(0, fmax)

        self.frf_canvas.draw()

    # ---------------------------------------------------------------------
    # Mode selection
    # ---------------------------------------------------------------------

    def on_mode_selected_from_list(self, row: int) -> None:
        if row < 0:
            return
        if self.mode_combo.currentIndex() != row:
            self.mode_combo.blockSignals(True)
            self.mode_combo.setCurrentIndex(row)
            self.mode_combo.blockSignals(False)
        if self.mode2d_combo.currentIndex() != row:
            self.mode2d_combo.blockSignals(True)
            self.mode2d_combo.setCurrentIndex(row)
            self.mode2d_combo.blockSignals(False)

        self._apply_mode(row)

    
    def on_mode2d_selected(self, row: int) -> None:
    
        if row < 0:
            return

        # keep all selectors in sync
        if self.mode_list.currentRow() != row:
            self.mode_list.blockSignals(True)
            self.mode_list.setCurrentRow(row)
            self.mode_list.blockSignals(False)

        if self.mode_combo.currentIndex() != row:
            self.mode_combo.blockSignals(True)
            self.mode_combo.setCurrentIndex(row)
            self.mode_combo.blockSignals(False)

        # reuse existing logic (computes v6/v16 + updates 2D/3D)
        self._apply_mode(row)

    
    
    
    def on_mode_selected_from_combo(self, row: int) -> None:
        if row < 0:
            return
        if self.mode_list.currentRow() != row:
            self.mode_list.blockSignals(True)
            self.mode_list.setCurrentRow(row)
            self.mode_list.blockSignals(False)
        self._apply_mode(row)

    def _apply_mode(self, row: int) -> None:
        """Compute participation vector for selected mode and update 3D."""
        self.current_mode_row = row

        if self.f is None or not self.frfs or self.mode_indices.size == 0:
            return

        idx_center = int(self.mode_indices[row])
        f_mode = float(self.f[idx_center])

        # Compute complex participation for the 6 excitations.
        band = float(self.peak_band.value())
        v6 = participation_vector_windowed(self.frfs, self.f, idx_center, band_hz=band, ref=0)

        # Map 6 measured participation values to the 16-node visualization model.
        #
        # Measurement/excitation points are 1..6 on the FRONT frame:
        #   1-2 (top), 3-4 (mid), 5-6 (lower), 7-8 (ground / fixed, not excited)
        # BACK frame 9..16 is for 3D appearance only -> we copy the FRONT displacements.
        v16 = np.zeros(16, dtype=complex)
        v16[0:6] = v6            # points 1..6
        # points 7..8 (indices 6,7) stay 0 (fixed ground)
        v16[8:14] = v6           # points 9..14 mirror 1..6
        # points 15..16 (indices 14,15) stay 0 (fixed ground)

        self.v_complex = v16
        #self.omega = 2.0 * np.pi * f_mode
        self.omega = 2.0 * np.pi * 1
        self.t = 0.0

        # ---------------------------
        # Mode 2D (static) view
        # ---------------------------
        # Align global phase such that reference (sensor at point 1) is real-positive.
        phi = np.angle(v6[0]) if np.abs(v6[0]) > 0 else 0.0
        v6_aligned = v6 * np.exp(-1j * phi)

        # Mean of left/right per level on the FRONT frame:
        # levels are ordered TOP -> ... -> GROUND in our node numbering.
        u_top = 0.5 * (v6_aligned[0] + v6_aligned[1])
        u_mid = 0.5 * (v6_aligned[2] + v6_aligned[3])
        u_low = 0.5 * (v6_aligned[4] + v6_aligned[5])
        u_gnd = 0.0  # fixed ground / EG

        # Use the real part for a clear signed shape; normalize by max abs.
        u = np.real(np.array([u_gnd, u_low, u_mid, u_top], dtype=complex))
        umax = float(np.max(np.abs(u))) if np.size(u) else 1.0
        if umax <= 0:
            umax = 1.0
        u_norm = u / umax

        z = np.array([0.0, 1.0/3.0, 2.0/3.0, 1.0], dtype=float)
        self.mode2d_canvas.plot_mode(z=z, u=u_norm, title=f"Mode @ {f_mode:.2f} Hz (2D)")

        self._update_3d_points(self.points0, np.abs(self.v_complex))

        if not self.timer.isActive():
            self.timer.start(16)

        # Re-draw FRF plot to update the prominence bracket for this mode.
        self.update_frf_plot()

    # ---------------------------------------------------------------------
    # 3D animation
    # ---------------------------------------------------------------------

    def _animate_step(self) -> None:
        self.t += 0.016

        pts_def = deform(
            self.points0,
            self.v_complex,
            self.direction,
            t=self.t,
            omega=self.omega,
            scale=float(self.scale.value()),
        )

        self.frame_mesh.points = pts_def
        self._update_3d_points(pts_def, np.abs(self.v_complex))

    def _update_3d_points(self, points: np.ndarray, scalars: np.ndarray) -> None:
        """Update point coordinates + scalars in-place (no actor re-creation)."""
        # Update geometry
        self.points_pd.points = points

        # Update scalar values (normalize to [0, 1] for stable colorbar)
        s = np.asarray(scalars, dtype=float)
        smax = float(np.max(s)) if np.size(s) else 1.0
        if smax <= 0:
            s_norm = s * 0.0
        else:
            s_norm = s / smax
        arr = self.points_pd["amp"]
        if arr.shape != s_norm.shape:
            # first time / unexpected -> replace
            self.points_pd["amp"] = s_norm
        else:
            arr[:] = s_norm
        self.points_pd.Modified()

        # Render once per frame; scalar bar stays stable because actor is stable.
        self.plotter.render()

    def export_frf_png(self) -> None:
        try:
            out = self.export_dir / "frf_plot.png"
            save_figure_png(self.frf_canvas.figure, out, dpi=200)
            QMessageBox.information(self, "Export", f"FRF Plot gespeichert: {out}")
        except Exception as e:
            QMessageBox.critical(self, "Export-Fehler", str(e))

    def export_3d_png(self) -> None:
        try:
            out = self.export_dir / "3d_view.png"
            self.plotter.screenshot(str(out))
            QMessageBox.information(self, "Export", f"3D Screenshot gespeichert: {out}")
        except Exception as e:
            QMessageBox.critical(self, "Export-Fehler", str(e))

    def export_3d_gif(self) -> None:
        try:
            if self.f is None or self.mode_indices.size == 0:
                raise ValueError("Bitte zuerst analysieren und eine Mode auswählen.")

            fps = 30
            seconds = 3.0
            n_frames = int(fps * seconds)
            dt = 1.0 / fps

            frames: list[np.ndarray] = []
            for k in range(n_frames):
                t = k * dt

                pts_def = deform(
                    self.points0,
                    self.v_complex,
                    self.direction,
                    t=t,
                    omega=self.omega,
                    scale=float(self.scale.value()),
                )
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





def run_app() -> None:
    """Entry point used by main.py."""
    app = QApplication(sys.argv)
    w = MainWindow()
    w.resize(1400, 780)
    w.show()
    sys.exit(app.exec())

