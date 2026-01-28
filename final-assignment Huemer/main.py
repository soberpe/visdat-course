import sys
import os
import shutil
import numpy as np
import imageio.v3 as iio
import pyvista as pv
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QSlider, QLabel, QFrame, QLineEdit,
                             QMessageBox, QComboBox, QRadioButton, QButtonGroup,
                             QSplitter, QPushButton, QFileDialog, QCheckBox)
from PyQt6.QtCore import Qt
from pyvistaqt import BackgroundPlotter
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# --- MODERN SCIENTIFIC GUI THEME ---
# hier hab ich das design definiert, sieht ähnlich aus wie css
STYLESHEET = """
QMainWindow {
    background-color: #f0f0f0;
}
/* Linkes Panel (Dunkelgrau für Profi-Look) */
QFrame#ControlsPanel {
    background-color: #2b2b2b;
    border-right: 1px solid #444;
}
QLabel {
    color: #e0e0e0;
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
}
QLabel#Header {
    color: #ffffff;
    font-size: 18px;
    font-weight: bold;
    border-bottom: 2px solid #007acc;
    padding-bottom: 5px;
    margin-bottom: 10px;
}
QLabel#SubHeader {
    color: #007acc; /* Akzentfarbe Blau */
    font-weight: bold;
    margin-top: 10px;
}
/* Slider Styling */
QSlider::groove:horizontal {
    border: 1px solid #555;
    background: #444;
    height: 10px;
    border-radius: 5px;
}
QSlider::sub-page:horizontal {
    background: #007acc;
    border-radius: 5px;
}
QSlider::handle:horizontal {
    background: #ffffff;
    border: 1px solid #555;
    width: 22px;
    height: 22px;
    margin: -6px 0;
    border-radius: 11px;
}
/* Buttons */
QPushButton {
    background-color: #444;
    color: white;
    border: 1px solid #555;
    border-radius: 5px;
    padding: 8px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #555;
    border-color: #007acc;
}
QPushButton:pressed {
    background-color: #007acc;
}
/* Eingabefelder & Combobox */
QLineEdit, QComboBox {
    background-color: #333;
    color: white;
    border: 1px solid #555;
    border-radius: 4px;
    padding: 5px;
}
/* Radio Buttons & Checkbox */
QRadioButton, QCheckBox {
    color: #e0e0e0;
    spacing: 8px;
}
QRadioButton::indicator, QCheckBox::indicator {
    width: 16px;
    height: 16px;
}
QRadioButton::indicator:checked, QCheckBox::indicator:checked {
    background-color: #007acc;
    border: 2px solid white;
    border-radius: 8px; /* Rund für Radio */
}
QCheckBox::indicator:checked {
    border-radius: 3px; /* Eckig für Checkbox */
}
"""

class TerrainFloodApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # fenster einstellungen
        self.setWindowTitle("VisDat Final Project: Advanced Terrain Analysis")
        self.resize(1500, 950)
        self.setStyleSheet(STYLESHEET)

        # --- SPECIAL COLORMAP ---
        # eigene farbpalette definieren damit es realistisch aussieht
        # 0 ist wasser (blau), dann grün, dann braun für berge, oben weiss
        colors = [
            (0.0,  "#33CCFF"), # 0% = Hellblau
            (0.02, "#228B22"), # 2% = Grün
            (0.30, "#DAA520"), # 30% = Ocker
            (0.60, "#8B4513"), # 60% = Braun
            (0.90, "#A9A9A9"), # 90% = Grau
            (1.0,  "#FFFFFF")  # 100% = Weiß
        ]
        self.land_cmap = LinearSegmentedColormap.from_list("custom_land", colors)

        # Haupt-Widget erstellen
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QHBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)

        # ==================== LINKE SEITE: CONTROLS (DARK PANEL) ====================
        # hier kommen alle buttons und slider rein
        self.controls_panel = QFrame()
        self.controls_panel.setObjectName("ControlsPanel")
        self.controls_layout = QVBoxLayout(self.controls_panel)
        self.controls_panel.setFixedWidth(380)

        # Header
        lbl_title = QLabel("Analysis Controls")
        lbl_title.setObjectName("Header")
        self.controls_layout.addWidget(lbl_title)

        # --- 1. Modus ---
        lbl_mode = QLabel("Operation Mode:")
        lbl_mode.setObjectName("SubHeader")
        self.controls_layout.addWidget(lbl_mode)

        # umschalten zwischen nur gelände und flut simulation
        self.mode_group = QButtonGroup(self)
        self.radio_terrain = QRadioButton("Terrain Analysis (Topology)")
        self.radio_terrain.setChecked(True)
        self.radio_terrain.toggled.connect(self.change_mode)
        self.controls_layout.addWidget(self.radio_terrain)
        self.mode_group.addButton(self.radio_terrain)

        self.radio_flood = QRadioButton("Flood Simulation (Hydrology)")
        self.radio_flood.toggled.connect(self.change_mode)
        self.controls_layout.addWidget(self.radio_flood)
        self.mode_group.addButton(self.radio_flood)

        self.controls_layout.addSpacing(15)

        # --- 2. Datei & Import ---
        lbl_data = QLabel("Data Source:")
        lbl_data.setObjectName("SubHeader")
        self.controls_layout.addWidget(lbl_data)

        # Import Button um bilder zu laden
        self.import_btn = QPushButton("📂 Import Image...")
        self.import_btn.clicked.connect(self.import_image)
        self.controls_layout.addWidget(self.import_btn)

        self.file_selector = QComboBox()
        self.file_selector.currentIndexChanged.connect(self.change_map)
        self.controls_layout.addWidget(self.file_selector)
        
        # --- NEU: Checkbox für Downsampling ---
        # checkbox für performance, damit man umschalten kann ob man alle pixel will oder weniger
        self.chk_downsampling = QCheckBox("High Performance (Downsample)")
        self.chk_downsampling.setChecked(True) # Standart ist an weils sonst ruckelt
        # Wenn man umschaltet, Map neu laden
        self.chk_downsampling.toggled.connect(self.change_map) 
        self.controls_layout.addWidget(self.chk_downsampling)

        self.reset_view_btn = QPushButton("↺ Reset Camera (Top-Down)")
        self.reset_view_btn.clicked.connect(self.reset_camera_view)
        self.controls_layout.addWidget(self.reset_view_btn)

        self.controls_layout.addSpacing(15)

        # Calibration
        # eingabe für die maximale höhe in metern
        lbl_calib = QLabel("Calibration (Max Elevation):")
        lbl_calib.setObjectName("SubHeader")
        self.controls_layout.addWidget(lbl_calib)
        self.max_height_input = QLineEdit("3000")
        self.max_height_input.setPlaceholderText("Meters (e.g. 4810)")
        self.max_height_input.editingFinished.connect(self.update_terrain)
        self.controls_layout.addWidget(self.max_height_input)

        self.controls_layout.addSpacing(15)

        # --- Slider 1: Exaggeration ---
        # slider um das terrain übertrieben darzustellen
        lbl_exag = QLabel("Visual Exaggeration:")
        lbl_exag.setObjectName("SubHeader")
        self.controls_layout.addWidget(lbl_exag)
        self.z_slider = QSlider(Qt.Orientation.Horizontal)
        self.z_slider.setMinimum(1)
        self.z_slider.setMaximum(250)
        self.z_slider.setValue(self.z_slider.minimum())
        self.z_slider.valueChanged.connect(self.update_terrain)
        self.controls_layout.addWidget(self.z_slider)

        self.controls_layout.addSpacing(15)

        # --- Slider 2: Slice Direction & Slider ---
        lbl_slice = QLabel("Profile Slice Control:")
        lbl_slice.setObjectName("SubHeader")
        self.controls_layout.addWidget(lbl_slice)

        # Achsen-Auswahl (X oder Y schneiden)
        self.slice_axis_layout = QHBoxLayout()
        self.slice_axis_group = QButtonGroup(self)
        
        self.radio_slice_x = QRadioButton("Slice X-Axis")
        self.radio_slice_x.setChecked(True)
        self.radio_slice_x.toggled.connect(self.update_profile_plot)
        self.slice_axis_group.addButton(self.radio_slice_x)
        self.slice_axis_layout.addWidget(self.radio_slice_x)
        
        self.radio_slice_y = QRadioButton("Slice Y-Axis")
        self.radio_slice_y.toggled.connect(self.update_profile_plot)
        self.slice_axis_group.addButton(self.radio_slice_y)
        self.slice_axis_layout.addWidget(self.radio_slice_y)
        
        self.controls_layout.addLayout(self.slice_axis_layout)

        # Checkbox Slice Plane
        self.chk_show_slice = QCheckBox("Show 3D Slice Plane")
        self.chk_show_slice.setChecked(True)
        self.chk_show_slice.toggled.connect(self.update_profile_plot)
        self.controls_layout.addWidget(self.chk_show_slice)

        # Slider für Position des schnitts
        self.slice_slider = QSlider(Qt.Orientation.Horizontal)
        self.slice_slider.setMinimum(0)
        self.slice_slider.setMaximum(100)
        self.slice_slider.setValue(50)
        self.slice_slider.valueChanged.connect(self.update_profile_plot)
        self.controls_layout.addWidget(self.slice_slider)

        # --- 3. Wasser Controls ---
        # das menü ist versteckt solange man nicht auf flood simulation klickt
        self.water_controls_widget = QWidget()
        self.water_layout = QVBoxLayout(self.water_controls_widget)
        self.water_layout.setContentsMargins(0, 0, 0, 0)

        lbl_water = QLabel("Water Level (Meters):")
        lbl_water.setObjectName("SubHeader")
        self.water_layout.addWidget(lbl_water)
        self.water_input = QLineEdit("0")
        self.water_input.returnPressed.connect(self.water_input_changed)
        self.water_layout.addWidget(self.water_input)

        self.water_slider = QSlider(Qt.Orientation.Horizontal)
        self.water_slider.setMinimum(0)
        self.water_slider.setMaximum(10000)
        self.water_slider.setValue(0)
        self.water_slider.valueChanged.connect(self.water_slider_changed)
        self.water_layout.addWidget(self.water_slider)

        self.controls_layout.addWidget(self.water_controls_widget)
        self.water_controls_widget.setVisible(False)

        self.controls_layout.addStretch()

        # Footer Info text
        self.info_label = QLabel("Ready.")
        self.info_label.setStyleSheet("color: #888; font-size: 11px; border: none;")
        self.controls_layout.addWidget(self.info_label)

        self.main_layout.addWidget(self.controls_panel)

        # ==================== RECHTE SEITE ====================
        # hier teilen wir den bildschirm, oben 2d profil, unten 3d ansicht
        self.right_splitter = QSplitter(Qt.Orientation.Vertical)
        self.main_layout.addWidget(self.right_splitter, stretch=1)

        # Oben: 2D Profil (mit mathplotlib)
        self.profile_frame = QFrame()
        self.profile_layout = QVBoxLayout(self.profile_frame)
        self.profile_layout.setContentsMargins(0, 0, 0, 0)

        self.profile_figure = Figure(figsize=(5, 2), dpi=100, facecolor='#f0f0f0')
        self.profile_canvas = FigureCanvas(self.profile_figure)
        self.profile_ax = self.profile_figure.add_subplot(111)
        self.profile_ax.set_facecolor('#ffffff')
        self.profile_layout.addWidget(self.profile_canvas)

        self.right_splitter.addWidget(self.profile_frame)

        # Unten: 3D Plotter (pyvista)
        self.plotter_frame = QFrame()
        self.plotter_layout = QVBoxLayout(self.plotter_frame)
        self.plotter_layout.setContentsMargins(0, 0, 0, 0)

        self.plotter = BackgroundPlotter(show=False)
        self.plotter_layout.addWidget(self.plotter)

        self.right_splitter.addWidget(self.plotter_frame)
        self.right_splitter.setSizes([250, 750])

        # am anfang einmal ordner scannen ob bilder da sind
        self.scan_data_folder()

    def change_mode(self):
        # funktion um zwischen den ansichten zu wechseln
        is_flood_mode = self.radio_flood.isChecked()
        self.water_controls_widget.setVisible(is_flood_mode)

        if hasattr(self, 'water_plane'):
            if is_flood_mode:
                self.plotter.add_mesh(self.water_plane, color="blue", opacity=0.5, name="water")
            else:
                self.plotter.remove_actor("water")
        self.update_profile_plot()

    def reset_camera_view(self):
        # kamera zurücksetzen auf draufsicht
        self.plotter.view_xy()
        self.plotter.reset_camera()

    def import_image(self):
        # datei dialog öffnen und bild in den data ordner kopieren
        file_name, _ = QFileDialog.getOpenFileName(self, "Import Heightmap", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            try:
                current_dir = os.path.dirname(os.path.abspath(__file__))
                data_dir = os.path.join(current_dir, "data")
                if not os.path.exists(data_dir):
                    os.makedirs(data_dir)

                base_name = os.path.basename(file_name)
                dest_path = os.path.join(data_dir, base_name)
                shutil.copy2(file_name, dest_path)

                self.scan_data_folder()
                index = self.file_selector.findText(base_name)
                if index >= 0:
                    self.file_selector.setCurrentIndex(index)

                QMessageBox.information(self, "Success", f"Imported {base_name} successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not import image: {e}")

    def scan_data_folder(self):
        # schaut im data ordner nach bildern und füllt die combobox
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(current_dir, "data")

        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        files = [f for f in os.listdir(data_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        self.file_selector.blockSignals(True)
        self.file_selector.clear()
        if not files:
            self.file_selector.addItem("No images found")
            self.file_selector.setEnabled(False)
        else:
            self.file_selector.addItems(files)
            self.file_selector.setEnabled(True)
        self.file_selector.blockSignals(False)

        if self.file_selector.count() > 0 and self.file_selector.itemText(0) != "No images found":
             if not hasattr(self, 'image_data'):
                 self.load_data(self.file_selector.itemText(0))

    def change_map(self):
        filename = self.file_selector.currentText()
        if filename and filename != "No images found":
            self.load_data(filename)

    def load_data(self, filename):
        # wichtigste funktion: hier werden die daten geladen und das gitter erstellt
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, "data", filename)

            raw_image = iio.imread(image_path)
            # wir brauchen nur einen kanal, also graustufen
            if len(raw_image.shape) > 2:
                self.image_data = raw_image[:, :, 0]
            else:
                self.image_data = raw_image

            # 90° Drehung im Uhrzeigersinn, sonst passt die orientierung nicht
            self.image_data = np.rot90(self.image_data, k=-1)

            # --- DOWNSAMPLING LOGIK ---
            # wenn checkbox an ist, nehmen wir nur jeden 2. punkt (performance hack)
            if self.chk_downsampling.isChecked():
                step = 2 # Schnell (25% Daten)
            else:
                step = 1 # Detail (100% Daten)

            self.grid_data = self.image_data[::step, ::step]

            dims = self.grid_data.shape
            self.x_size, self.y_size = dims[0], dims[1]

            self.slice_slider.setMaximum(self.x_size - 1)
            self.slice_slider.setValue(self.x_size // 2)

            # hier bauen wir das 3d gitter
            self.grid = pv.StructuredGrid()
            xx, yy = np.meshgrid(np.arange(self.x_size), np.arange(self.y_size), indexing='ij')

            # hier musste ich order='F' benutzen sonst gabs komische zacken im terrain
            self.grid.points = np.c_[
                xx.flatten(order='F'),
                yy.flatten(order='F'),
                np.zeros_like(xx).flatten(order='F')
            ]
            self.grid.dimensions = [self.x_size, self.y_size, 1]

            self.grid["Elevation"] = self.grid_data.flatten(order='F')

            self.current_water_height_m = 0.0
            self.water_plane = pv.Plane(center=(self.x_size/2, self.y_size/2, 0), i_size=self.x_size, j_size=self.y_size)

            self.update_terrain()
            self.reset_camera_view()
            self.plotter.remove_bounds_axes()

            self.info_label.setText(f"Loaded: {filename}\nSize: {self.x_size}x{self.y_size}")

        except Exception as e:
            self.info_label.setText(f"Error: {e}")
            print(e)

    def get_real_max_height(self):
        try:
            return float(self.max_height_input.text())
        except ValueError:
            return 3000.0

    def update_terrain(self):
        # funktion die das gitter "verbiegt" (warping) basierend auf höhenwerten
        if not hasattr(self, 'grid'): return

        z_factor = self.z_slider.value() / 50.0
        real_max = self.get_real_max_height()

        elevation_values = self.grid["Elevation"]
        real_elevation = (elevation_values / 255.0) * real_max
        self.grid["Real Elevation (m)"] = real_elevation

        # hier passiert die magie: 2d gitter wird zu 3d berg
        self.warped_mesh = self.grid.warp_by_scalar("Elevation", factor=z_factor)

        self.plotter.clear()

        self.plotter.add_mesh(
            self.warped_mesh,
            scalars="Real Elevation (m)",
            cmap=self.land_cmap,
            name="terrain",
            show_scalar_bar=True,
            scalar_bar_args={
                'title': "Height (m)",
                'color': 'black',
                'vertical': True,
                'fmt': '%.0f'
            }
        )

        self.change_mode()
        self.update_profile_plot()

    def update_profile_plot(self):
        # kümmert sich um den querschnitt (oben rechts) und die rote linie im 3d bild
        if not hasattr(self, 'grid_data'): return

        slice_axis = 'X' if self.radio_slice_x.isChecked() else 'Y'

        if slice_axis == 'X':
            max_limit = self.x_size - 1
        else:
            max_limit = self.y_size - 1
        
        self.slice_slider.setMaximum(max_limit)
        
        slice_idx = self.slice_slider.value()
        slice_idx = max(0, min(slice_idx, max_limit))

        real_max = self.get_real_max_height()
        
        # daten für das diagramm holen je nach achse
        if slice_axis == 'X':
            profile_data_pixel = self.grid_data[slice_idx, :]
        else:
            profile_data_pixel = self.grid_data[:, slice_idx]

        profile_data_m = (profile_data_pixel / 255.0) * real_max

        # diagramm zeichnen
        self.profile_ax.clear()
        self.profile_ax.set_title(f"Cross-Section Profile ({slice_axis}-Axis Slice)")
        self.profile_ax.set_ylabel("Height (m)")
        self.profile_ax.get_xaxis().set_visible(False)

        x_axis = np.arange(len(profile_data_m))
        self.profile_ax.fill_between(x_axis, profile_data_m, color='green', alpha=0.3, label="Terrain")
        self.profile_ax.plot(x_axis, profile_data_m, color='darkgreen', linewidth=1)

        # wenn flut modus an ist, blaue linie einzeichnen
        if self.radio_flood.isChecked():
            water_h = self.current_water_height_m
            self.profile_ax.axhline(y=water_h, color='blue', linestyle='--', linewidth=2, label="Water Level")
            self.profile_ax.fill_between(x_axis, 0, water_h, color='blue', alpha=0.1)

        self.profile_ax.grid(True, linestyle=':', alpha=0.6)
        self.profile_canvas.draw()

        self.plotter.remove_actor("slice_mesh")
        self.plotter.remove_actor("slice_border")

        # rote schnittebene im 3d raum anzeigen
        if self.chk_show_slice.isChecked():
            z_factor = self.z_slider.value() / 50.0
            current_max_pixel = self.grid_data.max()
            visual_max_z = current_max_pixel * z_factor * 1.1

            # koordinaten für die ebene berechnen
            if slice_axis == 'X':
                p1 = [slice_idx, 0, 0]
                p2 = [slice_idx, self.y_size, 0]
                p3 = [slice_idx, self.y_size, visual_max_z]
                p4 = [slice_idx, 0, visual_max_z]
            else:
                p1 = [0, slice_idx, 0]
                p2 = [self.x_size, slice_idx, 0]
                p3 = [self.x_size, slice_idx, visual_max_z]
                p4 = [0, slice_idx, visual_max_z]

            lines = pv.MultipleLines(points=[p1, p2, p3, p4, p1])
            self.plotter.add_mesh(lines, color="red", line_width=4, name="slice_border")

            face_points = np.array([p1, p2, p3, p4])
            face = np.array([4, 0, 1, 2, 3])
            plane_mesh = pv.PolyData(face_points, face)

            self.plotter.add_mesh(plane_mesh, color="red", opacity=0.1, name="slice_mesh", show_edges=False)

    def water_slider_changed(self):
        # update wenn man am wasser slider zieht
        val = self.water_slider.value()
        percent = val / 10000.0
        real_height = percent * self.get_real_max_height()
        self.current_water_height_m = real_height

        self.water_input.blockSignals(True)
        self.water_input.setText(f"{real_height:.2f}")
        self.water_input.blockSignals(False)

        self.update_water_visuals()

    def water_input_changed(self):
        # update wenn man den wert manuell eingibt
        try:
            val_text = float(self.water_input.text())
            self.current_water_height_m = val_text
            real_max = self.get_real_max_height()

            if real_max > 0:
                percent = val_text / real_max
            else:
                percent = 0

            percent = max(0.0, min(1.0, percent))
            slider_val = int(percent * 10000)

            self.water_slider.blockSignals(True)
            self.water_slider.setValue(slider_val)
            self.water_slider.blockSignals(False)

            self.update_water_visuals()

        except ValueError:
            pass

    def update_water_visuals(self):
        self.update_profile_plot()

        if not hasattr(self, 'water_plane'): return

        real_max = self.get_real_max_height()
        if real_max == 0: return

        percent = self.current_water_height_m / real_max
        pixel_height = percent * 255.0
        z_factor = self.z_slider.value() / 50.0
        visual_height = pixel_height * z_factor

        # wasser plane neu berechnen und setzen
        self.water_plane = pv.Plane(center=(self.x_size/2, self.y_size/2, visual_height),
                                    i_size=self.x_size, j_size=self.y_size)

        if self.radio_flood.isChecked():
            self.plotter.add_mesh(self.water_plane, color="blue", opacity=0.5, name="water")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = TerrainFloodApp()
    window.show()
    sys.exit(app.exec())