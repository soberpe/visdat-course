from fileinput import filename
# Importiert alle benötigten Qt-Widgets für das GUI
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QFileDialog,
    QGroupBox, QComboBox, QCheckBox,
    QPushButton, QSlider  # Slider für Skalierung / Clipping
)

# QAction wird für Menüeinträge (Menüleiste) benötigt
from PyQt6.QtGui import QAction

# Qt-Core, z. B. für Ausrichtungen (Qt.Horizontal)
from PyQt6.QtCore import Qt, QTimer

# Systemfunktionen (z. B. Programmstart/-ende)
import sys
import math



# PyVista-Qt-Widget zum Einbetten eines VTK-Renderfensters in Qt
from pyvistaqt import QtInteractor

# Text-Eingabefelder
from PyQt6.QtWidgets import QLineEdit

# PyVista-Bibliothek für 3D-Meshes und Visualisierung
import pyvista as pv

# Hauptfenster-Klasse des FEM-Viewers

class FEMViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        # Fenstertitel und Startgröße
        self.setWindowTitle("FEM Results Viewer")
        self.resize(1200, 800)
        
        # Zustandsvariablen

        # Aktuelles Mesh (kann deformiert sein)
        self.mesh = None

        # Aktive Colormap für Skalardaten
        self.current_cmap = "coolwarm"

        # Optionen für die Skalardarstellung
        self.scalar_auto = True        # automatische Skalierung
        self.scalar_symmetric = False  # symmetrische Skala (±max)
        self.scalar_min = None         # manuelles Minimum
        self.scalar_max = None         # manuelles Maximum

        # Zentrales Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Hauptlayout: horizontal (links Controls, rechts 3D-View)
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Clipping-Zustand
        self.clip_enabled = False
        self.clip_normal = "X"   # Schnittebene normal zur X/Y/Z-Achse
        self.clip_offset = 0.0   # relative Verschiebung der Ebene

        # Animation state
        self.anim_timer = QTimer()
        self.anim_timer.timeout.connect(self.animate_deformation)
        self.anim_direction = 1  # 1 = vorwärts, -1 = rückwärts
        self.anim_speed_ms = 30 # Millisekunden pro Schritt
        self.anim_phase = 0.0


        # Kontrollpanel (linke Seite)
        controls = self.create_controls()
        main_layout.addWidget(controls)

        # PyVista-Plotter (rechte Seite)

        # QtInteractor kapselt ein VTK-Renderfenster
        self.plotter = QtInteractor(central_widget)

        # stretch=3 → mehr Platz für die 3D-Ansicht als für das Panel
        main_layout.addWidget(self.plotter.interactor, stretch=3)

        # Menüleiste und Statusleiste
        self.create_menus()
        self.statusBar().showMessage("Ready")
        
        # Originalmesh (unverformt), wird für Deformation benötigt
        self.mesh = None
        self.original_mesh = None  

   
    def update_deformation(self):
        
        ##Wendet eine geometrische Deformation auf das Mesh an,
        ##basierend auf einem Verschiebungsfeld (Displacement).
        

        # Wenn kein Mesh geladen ist oder Deformation deaktiviert:
        # → Originalzustand anzeigen
        if self.mesh is None or not self.deform_checkbox.isChecked():
            if self.original_mesh is not None:
                self.mesh = self.original_mesh.copy()
            self.display_mesh()
            return
        
        # Suche nach einem geeigneten Verschiebungsfeld
        displacement_field = None
        for field_name in ['U', 'Displacement', 'displacement', 'DISPL']:
            if field_name in self.mesh.point_data:
                displacement_field = field_name
                break
        
        # Kein Verschiebungsfeld gefunden
        if displacement_field is None:
            self.statusBar().showMessage("No displacement field found", 3000)
            self.deform_checkbox.setChecked(False)
            return
        
        # Skalierungsfaktor aus dem Slider (z. B. 1.0x, 5.0x)
        scale = self.deform_slider.value() / 10.0
        self.deform_label.setText(f"{scale:.1f}x")
        
        # Originalmesh speichern (nur einmal)
        if self.original_mesh is None:
            self.original_mesh = self.mesh.copy()
        
        # Verschiebungsdaten aus dem Mesh lesen
        import numpy as np
        displacement = self.mesh.point_data[displacement_field]
        
        # Falls 2D-Verschiebung → Z-Komponente mit 0 ergänzen
        if displacement.shape[1] == 2:
            displacement = np.hstack([
                displacement,
                np.zeros((displacement.shape[0], 1))
            ])
        
        # Neues deformiertes Mesh erzeugen
        self.mesh = self.original_mesh.copy()
        self.mesh.points = self.original_mesh.points + scale * displacement

        # Anzeige aktualisieren
        self.display_mesh()

    def create_menus(self):
        """Erstellt die Menüleiste der Anwendung"""

        menubar = self.menuBar()
        
        # Datei-Menü

        file_menu = menubar.addMenu("&File")
        
        open_action = QAction("&Open Mesh...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_mesh)
        file_menu.addAction(open_action)

        export_action = QAction("&Export Screenshot...", self)
        export_action.setShortcut("Ctrl+S")
        export_action.triggered.connect(self.export_screenshot)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View-Menü (Kamerasteuerung)

        view_menu = menubar.addMenu("&View")
        
        reset_action = QAction("&Reset Camera", self)
        reset_action.setShortcut("R")
        reset_action.triggered.connect(self.reset_camera)
        view_menu.addAction(reset_action)

        front_action = QAction("Front", self)
        front_action.setShortcut("1")
        front_action.triggered.connect(self.view_front)
        view_menu.addAction(front_action)

        left_action = QAction("Left", self)
        left_action.setShortcut("2")
        left_action.triggered.connect(self.view_left)
        view_menu.addAction(left_action)

        right_action = QAction("Right", self)
        right_action.setShortcut("3")
        right_action.triggered.connect(self.view_right)
        view_menu.addAction(right_action)

        top_action = QAction("Top", self)
        top_action.setShortcut("4")
        top_action.triggered.connect(self.view_top)
        view_menu.addAction(top_action)

        view_menu.addSeparator()

        iso_action = QAction("Isometric", self)
        iso_action.setShortcut("5")
        iso_action.triggered.connect(self.view_isometric)
        view_menu.addAction(iso_action)

    def create_controls(self):
        """Create control panel with field selection and display options"""
        controls = QGroupBox("Visualization Controls")
        layout = QVBoxLayout()
        controls.setLayout(layout)
        
        # Field selection
        layout.addWidget(QLabel("Display Field:"))
        self.field_combo = QComboBox()
        layout.addWidget(self.field_combo)

        # Colormap selection
        layout.addWidget(QLabel("Colormap:"))
        self.cmap_combo = QComboBox()
        self.cmap_combo.addItems(["viridis", "plasma", "jet", "coolwarm"])
        self.cmap_combo.setCurrentText(self.current_cmap)
        self.cmap_combo.currentTextChanged.connect(self.change_colormap)
        layout.addWidget(self.cmap_combo)
    
        # Scalar Range
        layout.addWidget(QLabel("\nScalar Range:"))

        self.scalar_auto_checkbox = QCheckBox("Auto Scale")
        self.scalar_auto_checkbox.setChecked(True)
        self.scalar_auto_checkbox.stateChanged.connect(self.update_scalar_range)
        layout.addWidget(self.scalar_auto_checkbox)

        self.scalar_sym_checkbox = QCheckBox("Symmetric (±max)")
        self.scalar_sym_checkbox.stateChanged.connect(self.update_scalar_range)
        layout.addWidget(self.scalar_sym_checkbox)

        range_layout = QHBoxLayout()

        self.scalar_min_edit = QLineEdit()
        self.scalar_min_edit.setPlaceholderText("Min")
        self.scalar_min_edit.editingFinished.connect(self.update_scalar_range)
        range_layout.addWidget(self.scalar_min_edit)

        self.scalar_max_edit = QLineEdit()
        self.scalar_max_edit.setPlaceholderText("Max")
        self.scalar_max_edit.editingFinished.connect(self.update_scalar_range)
        range_layout.addWidget(self.scalar_max_edit)

        layout.addLayout(range_layout)


        
        # Display options
        self.edges_checkbox = QCheckBox("Show Edges")
        self.edges_checkbox.setChecked(True)
        layout.addWidget(self.edges_checkbox)
        
        self.scalar_bar_checkbox = QCheckBox("Show Scalar Bar")
        self.scalar_bar_checkbox.setChecked(True)
        layout.addWidget(self.scalar_bar_checkbox)

        # Connect signals to update display
        self.field_combo.currentTextChanged.connect(self.update_field_display)
        self.edges_checkbox.stateChanged.connect(self.update_display_options)
        self.scalar_bar_checkbox.stateChanged.connect(self.update_display_options)

    
        # Deformation
        layout.addWidget(QLabel("\nDeformation:"))

        self.deform_checkbox = QCheckBox("Show Deformed")
        self.deform_checkbox.setChecked(False)
        self.deform_checkbox.stateChanged.connect(self.update_deformation)
        layout.addWidget(self.deform_checkbox)

        layout.addWidget(QLabel("Scale Factor:"))
        self.deform_slider = QSlider(Qt.Orientation.Horizontal)
        self.deform_slider.setRange(1, 10000)  # 0.1x to 1000x
        self.deform_slider.setValue(10)  # 1.0x
        self.deform_slider.valueChanged.connect(self.update_deformation)
        layout.addWidget(self.deform_slider)

        self.deform_label = QLabel("1.0x")
        layout.addWidget(self.deform_label)

        # Animation controls
        anim_layout = QHBoxLayout()

        self.play_button = QPushButton("▶")
        self.play_button.setCheckable(True)
        self.play_button.clicked.connect(self.toggle_animation)
        anim_layout.addWidget(self.play_button)

        layout.addLayout(anim_layout)

        
        #  Clipping 
        layout.addWidget(QLabel("\nClipping Plane:"))

        self.clip_checkbox = QCheckBox("Enable Clipping")
        self.clip_checkbox.stateChanged.connect(self.update_clipping)
        layout.addWidget(self.clip_checkbox)

        layout.addWidget(QLabel("Plane Normal:"))
        self.clip_normal_combo = QComboBox()
        self.clip_normal_combo.addItems(["X", "Y", "Z"])
        self.clip_normal_combo.currentTextChanged.connect(self.update_clipping)
        layout.addWidget(self.clip_normal_combo)

        layout.addWidget(QLabel("Plane Offset:"))
        self.clip_slider = QSlider(Qt.Orientation.Horizontal)
        self.clip_slider.setRange(-40, 100)
        self.clip_slider.setValue(0)
        self.clip_slider.valueChanged.connect(self.update_clipping)
        layout.addWidget(self.clip_slider)

         # Mesh info
        layout.addWidget(QLabel("\nMesh Information:"))
        self.info_label = QLabel("No mesh loaded")
        self.info_label.setWordWrap(True)
        layout.addWidget(self.info_label)
        
        # Reset button
        reset_button = QPushButton("Reset View")
        reset_button.clicked.connect(self.reset_camera)
        layout.addWidget(reset_button)


        # Push controls to top
        layout.addStretch()
        
        # Fixed width for control panel
        controls.setFixedWidth(280)
        
        return controls
    
    def change_colormap(self, cmap_name):
        """Change active colormap"""
        self.current_cmap = cmap_name
        self.display_mesh()

    def update_scalar_range(self):
        self.scalar_auto = self.scalar_auto_checkbox.isChecked()
        self.scalar_symmetric = self.scalar_sym_checkbox.isChecked()

        try:
            self.scalar_min = float(self.scalar_min_edit.text())
        except ValueError:
            self.scalar_min = None

        try:
            self.scalar_max = float(self.scalar_max_edit.text())
        except ValueError:
            self.scalar_max = None

        enabled = not self.scalar_auto
        self.scalar_min_edit.setEnabled(enabled)
        self.scalar_max_edit.setEnabled(enabled)
        self.display_mesh()


    
    def open_mesh(self):
        """Open mesh file using file dialog"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Mesh File",
            "c:/visdat-course/data",  # Starting directory
            "VTK Files (*.vtu *.vtk *.vti);;All Files (*.*)"
        )
        
        if not filename:
            return  # User canceled
        
        try:
            # Load mesh
            self.mesh = pv.read(filename)

            self.original_mesh = None  # Reset deformation state
            self.deform_checkbox.setChecked(False)
            
            # Update field selector
            self.populate_field_selector()
            
            # Display mesh (will be refined in next step)
            self.display_mesh()
            
            # Update info
            self.update_mesh_info()
            
            # Update status and title
            self.statusBar().showMessage(f"Loaded: {filename}", 3000)
            import os
            self.setWindowTitle(f"FEM Viewer - {os.path.basename(filename)}")
            
        except Exception as e:
            self.statusBar().showMessage(f"Error loading file: {str(e)}", 5000)
    
    def populate_field_selector(self):
        """Populate field combo box with available scalar fields"""
        self.field_combo.blockSignals(True)  # Prevent triggering updates
        self.field_combo.clear()
        
        if self.mesh is None:
            self.field_combo.blockSignals(False)
            return
        
        # Add "Geometry Only" option
        self.field_combo.addItem("(No Field)")
        
        # Add point data fields
        for field_name in self.mesh.point_data.keys():
            self.field_combo.addItem(field_name)
        
        self.field_combo.blockSignals(False)
        
        # Select first field if available
        if self.field_combo.count() > 1:
            self.field_combo.setCurrentIndex(1)  # Skip "(No Field)"

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

    def display_mesh(self):
        """Display mesh with current settings"""
        mesh_to_display = self.mesh
        if self.mesh is None:
            return
        
        self.plotter.clear()

        # Show undeformed mesh in background if deformation is active
        if self.deform_checkbox.isChecked() and self.original_mesh is not None:
            self.plotter.add_mesh(
                self.original_mesh,
                color="lightgray",
                opacity=0.3,
                show_edges=False
            )

        # Show undeformed mesh in background if clipping is active
        if self.clip_enabled and self.mesh is not None:
            background_mesh = (
                self.original_mesh if self.original_mesh is not None else self.mesh)

            self.plotter.add_mesh(
                background_mesh,
                color="lightgray",
                opacity=0.3,
                show_edges=False
            )


        
        # Get current field selection
        field_name = self.field_combo.currentText()

        if self.clip_enabled and mesh_to_display is not None:
            bounds = mesh_to_display.bounds
            center = mesh_to_display.center

            if self.clip_normal == "X":
                normal = (1, 0, 0)
                origin = (center[0] + self.clip_offset * (bounds[1] - bounds[0]), center[1], center[2])
            elif self.clip_normal == "Y":
                normal = (0, 1, 0)
                origin = (center[0], center[1] + self.clip_offset * (bounds[3] - bounds[2]), center[2])
            else:  # Z
                normal = (0, 0, 1)
                origin = (center[0], center[1], center[2] + self.clip_offset * (bounds[5] - bounds[4]))

            mesh_to_display = mesh_to_display.clip(
                normal=normal,
                origin=origin
            )
        
        # Determine what to display
        if field_name == "(No Field)" or not field_name:
            # Display geometry only
            self.plotter.add_mesh(
                mesh_to_display,
                color='lightgray',
                show_edges=self.edges_checkbox.isChecked(),
                show_scalar_bar=False
            )
        else:
            if field_name not in mesh_to_display.point_data:
                # Fallback: Geometry only
                self.plotter.add_mesh(
                    mesh_to_display,
                    color="lightgray",
                    show_edges=self.edges_checkbox.isChecked(),
                    show_scalar_bar=False
                )
                self.plotter.render()
                return

            # Get field data
            field_data = mesh_to_display.point_data[field_name]
            
            # Check if vector field (multi-component)
            if field_data.ndim > 1 and field_data.shape[1] > 1:
                # Compute magnitude
                import numpy as np
                magnitude = np.linalg.norm(field_data, axis=1)
                
                # Add as new field
                mag_field_name = f"{field_name}_magnitude"
                mesh_to_display[mag_field_name] = magnitude
                display_field = mag_field_name
                title = f"{field_name} (Magnitude)"
            else:
                display_field = field_name
                title = field_name
            
            # Display with scalar field
            clim = None

            if not self.scalar_auto:
                if self.scalar_symmetric and field_data is not None:
                    vmax = max(abs(field_data.min()), abs(field_data.max()))
                    clim = (-vmax, vmax)
                elif self.scalar_min is not None and self.scalar_max is not None:
                    clim = (self.scalar_min, self.scalar_max)

            self.plotter.add_mesh(
                mesh_to_display,
                scalars=display_field,
                cmap=self.current_cmap,
                clim=clim,
                show_edges=self.edges_checkbox.isChecked(),
                show_scalar_bar=self.scalar_bar_checkbox.isChecked(),
                scalar_bar_args={'title': title}
            )

        
        self.plotter.reset_camera()
        self.plotter.render()
    
    def animate_deformation(self):
        if not self.deform_checkbox.isChecked():
            self.deform_checkbox.setChecked(True)

        self.anim_phase += 0.1
        mid = (self.deform_slider.maximum() + self.deform_slider.minimum()) / 2
        amp = (self.deform_slider.maximum() - self.deform_slider.minimum()) / 2

        value = int(mid + amp * math.sin(self.anim_phase))
        self.deform_slider.setValue(value)


    def toggle_animation(self):
        if self.play_button.isChecked():
            self.play_button.setText("⏸")
            self.anim_timer.start(self.anim_speed_ms)
        else:
            self.play_button.setText("▶")
            self.anim_timer.stop()


    def update_field_display(self, field_name):
        """Update display when field selection changes"""
        self.display_mesh()

    def update_display_options(self):
        """Update display when checkboxes change"""
        self.display_mesh()

    def update_clipping(self):
        """Update clipping parameters"""
        self.clip_enabled = self.clip_checkbox.isChecked()
        self.clip_normal = self.clip_normal_combo.currentText()
        self.clip_offset = self.clip_slider.value() / 100.0
        self.display_mesh()

    def reset_camera(self):
        """Reset camera view"""
        if self.plotter:
            self.plotter.reset_camera()
            self.statusBar().showMessage("Camera reset", 2000)

    def view_front(self):
        if self.plotter:
            self.plotter.view_xy()
            self.plotter.render()

    def view_left(self):
        if self.plotter:
            self.plotter.view_yz()
            self.plotter.render()

    def view_right(self):
        if self.plotter:
            self.plotter.view_yz()
            self.plotter.camera.azimuth += 180
            self.plotter.render()

    def view_top(self):
        if self.plotter:
            self.plotter.view_xz()
            self.plotter.render()

    def view_isometric(self):
        if self.plotter:
            self.plotter.view_isometric()
            self.plotter.render()


    def closeEvent(self, event):
        """Clean up VTK resources before closing"""
        if self.plotter:
            self.plotter.close()
            self.plotter = None
        event.accept()

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