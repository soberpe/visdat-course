from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QFileDialog,
    QGroupBox, QComboBox, QCheckBox,
    QPushButton, QSlider, QMessageBox, QInputDialog
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from matplotlib import scale
from pyvistaqt import QtInteractor
import pyvista as pv
import sys

class FEMViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        # definieren der Attribute
        self.colormaps = [
            "viridis",
            "plasma",
            "inferno",
            "magma",
            "cividis",
            "jet",
            "coolwarm"
        ]

        self.mesh = None
        self.original_mesh = None
        self.deformed_mesh = None
        self.current_field = None
        self.last_camera_position = None
        self.camera_history = []
        self.undeformed_actor = None
        self.deformed_actor = None
        self.show_undeformed = True
        self.is_dirty = False

        # definieren des GUI
        self.setWindowTitle("FEM Viewer")
        self.resize(1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # definieren der Steuerungselemente
        controls = self.create_controls()
        main_layout.addWidget(controls)

        self.field_combo.currentTextChanged.connect(self.update_field_display)
        self.edges_checkbox.stateChanged.connect(self.update_display_options)
        self.scalar_bar_checkbox.stateChanged.connect(self.update_display_options)


        self.plotter = QtInteractor(self)

        main_layout.addWidget(self.plotter.interactor, stretch=3)

        self.create_menus()
        self.statusBar().showMessage("Ready")

    def create_menus(self):
        menubar = self.menuBar()
        # File Menü 
        file_menu = menubar.addMenu("&File")
        
        open_action = QAction("&Open Mesh...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.setShortcutContext(Qt.ShortcutContext.ApplicationShortcut)
        open_action.triggered.connect(self.open_mesh)
        file_menu.addAction(open_action)
        
        export_action = QAction("&Export Screenshot...", self)
        export_action.setShortcut("Ctrl+S")
        export_action.setShortcutContext(Qt.ShortcutContext.ApplicationShortcut)
        export_action.triggered.connect(self.export_screenshot)
        file_menu.addAction(export_action)

        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setShortcutContext(Qt.ShortcutContext.ApplicationShortcut)
        exit_action.triggered.connect(self.close) # nutzen der Standard-Close-Funktion
        file_menu.addAction(exit_action)

        # Camera Menü
        camera_menu = menubar.addMenu("&Camera")

        undo_cam_action = QAction("&Undo Camera (Ctrl+Z)", self)
        undo_cam_action.setShortcut("Ctrl+Z")
        undo_cam_action.setShortcutContext(Qt.ShortcutContext.ApplicationShortcut)
        undo_cam_action.triggered.connect(self.undo_camera)
        camera_menu.addAction(undo_cam_action)


        save_cam_action = QAction("&Save Camera", self)
        save_cam_action.setShortcut("C")
        save_cam_action.setShortcutContext(Qt.ShortcutContext.ApplicationShortcut)
        save_cam_action.triggered.connect(self.save_camera_state)
        camera_menu.addAction(save_cam_action)

        restore_cam_action = QAction("&Restore Camera", self)
        restore_cam_action.setShortcut("Shift+C")
        restore_cam_action.setShortcutContext(Qt.ShortcutContext.ApplicationShortcut)
        restore_cam_action.triggered.connect(self.restore_camera)
        camera_menu.addAction(restore_cam_action)

        reset_action = QAction("&Reset Camera", self)
        reset_action.setShortcut("R")
        reset_action.setShortcutContext(Qt.ShortcutContext.ApplicationShortcut)
        reset_action.triggered.connect(self.reset_camera)
        camera_menu.addAction(reset_action)

        # View Menü
        view_menu = menubar.addMenu("&View")

        top_action = QAction("Top", self)
        top_action.setShortcut("1")
        top_action.setShortcutContext(Qt.ShortcutContext.ApplicationShortcut)
        top_action.triggered.connect(self.view_top)
        view_menu.addAction(top_action)

        front_action = QAction("Front", self)
        front_action.setShortcut("2")
        front_action.setShortcutContext(Qt.ShortcutContext.ApplicationShortcut)
        front_action.triggered.connect(self.view_front)
        view_menu.addAction(front_action)

        iso_action = QAction("Isometric", self)
        iso_action.setShortcut("3")
        iso_action.setShortcutContext(Qt.ShortcutContext.ApplicationShortcut)
        iso_action.triggered.connect(self.view_iso)
        view_menu.addAction(iso_action)

        

    def open_mesh(self): 
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Mesh File",
            "c:/visdat-course/data",
            "VTK Files (*.vtu *.vtk *.vti);;All Files (*.*)"
        )
        if not filename:
            return

        try:
            # Mesh laden
            self.mesh = pv.read(filename)

            # Original- und Deformationszustand setzen
            self.original_mesh = self.mesh.copy(deep=True)
            self.deformed_mesh = None

            # Kamera automatisch an Bauteil anpassen
            self.align_camera_to_mesh_bounds()

            print(self.mesh)
            print(self.mesh.point_data.keys())

            # GUI-Zustände zurücksetzen
            self.deform_checkbox.setChecked(False)

            # GUI & Plot aktualisieren
            self.populate_field_selector()
            self.display_mesh()
            self.update_mesh_info()

            self.statusBar().showMessage(f"Loaded: {filename}", 3000)

            import os
            self.setWindowTitle(f"FEM Viewer - {os.path.basename(filename)}")

        except Exception as e:
            self.statusBar().showMessage(f"Error loading file: {str(e)}", 5000)

    def align_camera_to_mesh_bounds(self):
        if self.mesh is None or not hasattr(self, "plotter"):
            return

        xmin, xmax, ymin, ymax, zmin, zmax = self.mesh.bounds

        cx = 0.5 * (xmin + xmax)
        cy = 0.5 * (ymin + ymax)
        cz = 0.5 * (zmin + zmax)

        dx = xmax - xmin
        dy = ymax - ymin
        dz = zmax - zmin

        d = max(dx, dy, dz) * 2.0  # Abstand der Kamera

        cam = self.plotter.camera
        cam.position = (cx + d, cy + d, cz + d)   # ISO-Ansicht
        cam.focal_point = (cx, cy, cz)
        cam.up = (0, 0, 1)

        self.plotter.reset_camera_clipping_range()
        self.plotter.render()
                

    def populate_field_selector(self):
        self.field_combo.blockSignals(True)
        self.field_combo.clear()

        if self.mesh is None:
            self.field_combo.blockSignals(False)
            return

        # Geometry only
        self.field_combo.addItem("(No Field)")

        # Point data fields
        for field_name in self.mesh.point_data.keys():
            self.field_combo.addItem(field_name)

        self.field_combo.blockSignals(False)

        if self.field_combo.count() > 1:
            self.field_combo.setCurrentIndex(1)

    def update_mesh_info(self):
        """Update mesh information display"""
        if self.mesh is None:
            self.info_label.setText("No mesh loaded")
            return
    
        n_points = self.mesh.n_points
        n_cells = self.mesh.n_cells
        n_fields = len(self.mesh.point_data.keys())
    
        info_text = (
                f"Points: {n_points:,}\n"
                f"Cells: {n_cells:,}\n"
                f"Point Fields: {n_fields}\n"
                        )
        self.info_label.setText(info_text)

    # Zoomen, Drehen, Feldwechsel, Verformungsänderung merken
    def display_mesh(self):

        if self.mesh is None:
            return

        self.plotter.clear()


        # Skalarfeld bestimmen
        field_name = self.field_combo.currentText()
        scalars = None if field_name == "(No Field)" else field_name

        # Threshold
        threshold_percent = self.threshold_slider.value()
        self.threshold_label.setText(f"{threshold_percent} %")
        mesh = self.deformed_mesh if self.deformed_mesh is not None else self.mesh
        mesh_to_plot = mesh

        if scalars and threshold_percent > 0:
            data = mesh.point_data[scalars]
            vmin, vmax = data.min(), data.max()
            thresh_value = vmin + (threshold_percent / 100.0) * (vmax - vmin)
            mesh_to_plot = mesh.threshold(value=thresh_value, scalars=scalars)
            # falls kein Mesh mehr übrig ist
            if mesh_to_plot.n_cells == 0:
                self.statusBar().showMessage(
                        "Threshold removed all cells – reset threshold",
                        3000
                    )
                return
        # undeformiertes Mesh 
        if self.undeformed_checkbox.isChecked():
            self.plotter.add_mesh(
                self.original_mesh,
                color="lightgray",
                style="wireframe",
                opacity=0.4,
                name="undeformed"
            )

        # Colormap
        cmap = self.colormaps[self.cmap_slider.value()]
        self.cmap_label.setText(cmap)

        # deformiertes / gefiltertes Mesh
        self.plotter.add_mesh(
            mesh_to_plot,
            scalars=scalars,
            cmap=cmap,
            show_edges=self.edges_checkbox.isChecked(),
            name="deformed"
        )

        if self.scalar_bar_checkbox.isChecked() and scalars:
            self.plotter.add_scalar_bar(title=scalars)

        self.plotter.reset_camera_clipping_range()
        self.plotter.render()

    
    # letzte Kameraposition speichern
    def reset_camera(self):
        if self.plotter:
            self.plotter.reset_camera()
            self.plotter.render()
            self.statusBar().showMessage("Camera reset", 2000)

    def view_iso(self):
        if self.plotter:
            self.plotter.view_isometric()
            self.plotter.render()

    def view_top(self):
        if self.plotter:
            self.plotter.view_xy()
            self.plotter.render()

    def view_front(self):
        if self.plotter:
            self.plotter.view_xz()
            self.plotter.render()

    # Rückgängig-Funktion für die Kamera
    def undo_camera(self):
        
        if not self.camera_history:
            self.statusBar().showMessage("No previous camera state", 2000)
            return

        pos, focal, up = self.camera_history.pop()
        cam = self.plotter.camera
        cam.position = pos
        cam.focal_point = focal
        cam.up = up

        self.plotter.reset_camera_clipping_range()
        self.plotter.render()

        self.statusBar().showMessage("Camera undo", 1500)


    # speichern der letzten Kameraposition
    def save_camera_state(self):
        cam = self.plotter.camera
        state = (cam.position, cam.focal_point, cam.up)

        # 1. Für die Restore-Funktion speichern
        self.last_camera_position = state 

        # 2. Für die Undo-Historie speichern
        if not self.camera_history or self.camera_history[-1] != state:
            self.camera_history.append(state)
            if len(self.camera_history) > 20:
                self.camera_history.pop(0)
                
        self.statusBar().showMessage("Camera position saved", 2000)

    # wiederherstellen der letzten Kameraposition
    def restore_camera(self):
        if self.plotter and self.last_camera_position is not None:
            self.plotter.camera_position = self.last_camera_position
            self.plotter.render()
            self.statusBar().showMessage("Camera restored", 2000)
        else:
            self.statusBar().showMessage("No camera position saved", 2000)

    def save_mesh(self):
        if self.mesh is None:
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Mesh speichern", "", "VTK Unstructured Grid (*.vtu)"
        )
        if filename:
            self.mesh.save(filename)
            self.is_dirty = False
            self.statusBar().showMessage(f"Gespeichert: {filename}")

    def closeEvent(self, event):
        if self.is_dirty:
            reply = QMessageBox.question(
                self, 'Beenden',
                "Ungespeicherte Änderungen vorhanden. Wirklich schließen?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.No:
                event.ignore()
                return

        if self.plotter:
            self.plotter.close()
        event.accept()


    def create_controls(self):
        """Create control panel with field selection and display options"""
        controls = QGroupBox("Visualization Controls") # Erstellen eines Gruppenfeldes für die Steuerungselemente
        layout = QVBoxLayout() # alle Elemente werden vertikal angeordnet
        controls.setLayout(layout) 
        
        # Field selection
        layout.addWidget(QLabel("Display Field:")) # Menü nutzen, um zwischen Datensätzen, z.B. Spannungen, Verschiebungen umzuschalten
        self.field_combo = QComboBox() # Dropdown-Menü zur Auswahl des darzustellenden Feldes
        layout.addWidget(self.field_combo) # Hinzufügen des Dropdown-Menüs zum Layout

        layout.addWidget(QLabel("Colormap:"))

        self.cmap_slider = QSlider(Qt.Orientation.Horizontal)
        self.cmap_slider.setRange(0, len(self.colormaps) - 1)
        self.cmap_slider.setValue(0)
        self.cmap_slider.valueChanged.connect(self.display_mesh)
        layout.addWidget(self.cmap_slider)

        self.cmap_label = QLabel(self.colormaps[0])
        layout.addWidget(self.cmap_label)

        layout.addWidget(QLabel("Threshold (%):"))

        self.threshold_slider = QSlider(Qt.Orientation.Horizontal)
        self.threshold_slider.setRange(0, 100)
        self.threshold_slider.setValue(0)
        self.threshold_slider.valueChanged.connect(self.display_mesh)
        layout.addWidget(self.threshold_slider)

        self.threshold_label = QLabel("0 %")
        layout.addWidget(self.threshold_label)
    
        # Display options
        self.edges_checkbox = QCheckBox("Show Edges") # Kontrollkästchen zum Ein- und Ausschalten der Kantendarstellung
        self.edges_checkbox.setChecked(True) # standardmäßig sind Kanten sichtbar
        layout.addWidget(self.edges_checkbox) # Hinzufügen des Kontrollkästchens zum Layout
        
        self.scalar_bar_checkbox = QCheckBox("Show Scalar Bar") # Kontrollkästchen zum Ein- und Ausschalten der Skalenleiste
        self.scalar_bar_checkbox.setChecked(True) # standardmäßig ist die Skalenleiste sichtbar
        layout.addWidget(self.scalar_bar_checkbox) # Hinzufügen des Kontrollkästchens zum Layout
        
        layout.addWidget(QLabel("\nDeformation:"))

        self.deform_checkbox = QCheckBox("Show Deformed")
        self.deform_checkbox.setChecked(False)
        self.deform_checkbox.stateChanged.connect(self.update_deformation)
        layout.addWidget(self.deform_checkbox)

        self.undeformed_checkbox = QCheckBox("Show Undeformed")
        self.undeformed_checkbox.setChecked(True)
        self.undeformed_checkbox.stateChanged.connect(self.display_mesh)
        layout.addWidget(self.undeformed_checkbox)


        layout.addWidget(QLabel("Scale Factor:"))
        self.deform_slider = QSlider(Qt.Orientation.Horizontal)
        self.deform_slider.setRange(1, 10000)  # 0.1x to 1000x
        self.deform_slider.setValue(10)  # 1.0x
        self.deform_slider.valueChanged.connect(self.update_deformation)
        layout.addWidget(self.deform_slider)

        self.deform_label = QLabel("1.0x")
        layout.addWidget(self.deform_label)

        # Mesh info
        layout.addWidget(QLabel("\nMesh Information:")) # Anzeige von Informationen über das geladene Mesh
        self.info_label = QLabel("No mesh loaded") # Standardtext, wenn kein Mesh geladen ist
        self.info_label.setWordWrap(True) # Zeilenumbruch für lange Texte aktivieren
        layout.addWidget(self.info_label) # Hinzufügen des Informationslabels zum Layout
        
        # Reset button
        reset_button = QPushButton("Reset View") # Button zum Zurücksetzen der Kameraposition
        reset_button.clicked.connect(self.reset_camera) # Verlinken des Buttons mit der reset_camera - Funktion
        layout.addWidget(reset_button) # Hinzufügen des Buttons zum Layout
        
        # Push controls to top
        layout.addStretch() # sorgt dafür, dass die Steuerelemente oben im Panel bleiben
        
        # Fixed width for control panel
        controls.setFixedWidth(280) # feste Breite für das Steuerungsfeld
        
        return controls
    
    def update_field_display(self, field_name):
        """Update display when field selection changes"""
        self.display_mesh()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Z and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.undo_camera()
            event.accept()
            return
        super().keyPressEvent(event)

    def update_display_options(self):
        """Update display when checkboxes change"""
        self.display_mesh()
    
    def update_deformation(self):
        # Kein Mesh geladen
        if self.original_mesh is None:
            return

        # Checkbox AUS → nur Original anzeigen
        if not self.deform_checkbox.isChecked():
            self.deformed_mesh = None
            self.display_mesh()
            return

        self.is_dirty = True # Änderungen vorgenommen?

        # Verschiebungsfeld suchen
        disp_name = None
        for name in ["displacement", "U", "Displacement", "DISPL"]:
            if name in self.original_mesh.point_data:
                disp_name = name
                break

        if disp_name is None:
            self.statusBar().showMessage("No displacement field found", 3000)
            self.deform_checkbox.setChecked(False)
            return

        # Skalierungsfaktor aus Slider
        scale = self.deform_slider.value() / 10.0
        self.deform_label.setText(f"{scale:.1f}x")

        disp = self.original_mesh.point_data[disp_name]

        # 2D → 3D absichern
        import numpy as np
        if disp.shape[1] == 2:
            disp = np.c_[disp, np.zeros(disp.shape[0])]

        # Verformtes Mesh erzeugen
        self.deformed_mesh = self.original_mesh.copy(deep=True)
        self.deformed_mesh.points = (
            self.original_mesh.points + scale * disp
        )

        self.display_mesh()


    def export_screenshot(self):
        """Save current view as image"""
        if self.mesh is None:
            self.statusBar().showMessage("No mesh to export", 2000)
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Screenshot",
            "screenshot.png",
            "PNG Images (*.png);;JPEG Images (*.jpg);;All Files (*.*)"
        )
        
        if filename:
            try:
                self.plotter.screenshot(filename, transparent_background=True)
                self.statusBar().showMessage(f"Saved: {filename}", 3000)
            except Exception as e:
                self.statusBar().showMessage(f"Error saving: {str(e)}", 5000)

def main():
    app = QApplication(sys.argv)
    window = FEMViewer()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()