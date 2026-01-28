#-------------------------------------------------------------------------------------
# FEM Results Viewer with PyVista and PyQt6
#-------------------------------------------------------------------------------------

from fileinput import filename
import os
import pyvista as pv
import numpy as np
from PyQt6.QtCore import Qt, QTimer


# Load the beam mesh with results (adjust path to your repository location)
mesh = pv.read('data/beam_stress.vtu')

# Check available fields
print("Available fields:", list(mesh.point_data.keys()))
# Output: ['U', 'S', 'S_MISES', 'E', 'RF', ...]

#-------------------------------------------------------------------------------------

# hier stehen alle Module und Bibliotheken die gebraucht werden zur Verfügug
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
import sys

from pyvistaqt import QtInteractor
import pyvista as pv

from PyQt6.QtWidgets import QFileDialog

from PyQt6.QtWidgets import (
    QGroupBox, QComboBox, QCheckBox,
    QPushButton
)

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QFileDialog,
    QGroupBox, QComboBox, QCheckBox,
    QPushButton, QSlider  # Add QSlider
)

from PyQt6.QtWidgets import QMessageBox

#-------------------------------------------------------------------------------------

class FEMViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FEM Results Viewer")
        self.resize(1200, 800)
    
        # State variables
        self.mesh = None
    
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
    
        # Create main layout (horizontal split)
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
    
        # Create control panel-----------------
        controls = self.create_controls()
        main_layout.addWidget(controls)

        # Zwei Ansichten nebeneinander-----------------------------------------------------------------------
        # Liste für die Plotter und die Anzahl der Ansichten werden hier erzeugt
        self.plotters = [] # Liste für die Plotter
        for i in range(2):  # Anzahl der Ansichten  
            plot_widget = QtInteractor(central_widget)
            main_layout.addWidget(plot_widget.interactor, stretch=3)
            self.plotters.append(plot_widget)
        #--------------------------------------------------------------------------------------------------

        # Create menus and status bar-----------
        self.create_menus()
        self.statusBar().showMessage("Ready")

        self.mesh = None
        self.original_mesh = None  # Store undeformed mesh

        self.undeformed_actor = None
        self.deformed_actor = None

        # Neue Variablen für zwei Plotter-------------------------------------------------------------------
        # speichert die Actors für deformierte Meshes in beiden Plottern
        # Wichtig für: Deformation, Edge-Updates, Re-Rendering
        self.deformed_actors = []
        #--------------------------------------------------------------------------------------------------


    def create_controls(self):
        """Create control panel with field selection and display options"""
        controls = QGroupBox("Visualization Controls")
        layout = QVBoxLayout()
        controls.setLayout(layout)

        # Slice / Cut Plane Controls
        layout.addWidget(QLabel("\nSlice Plane:"))

        #----------------------------------------------------------------------
        # Diese Code-Passage definiert alle Freiheitsgrade der Slice-Plane 
        # und koppelt sie über Qt-Signals an eine einzige Update-Funktion
        self.slice_checkbox = QCheckBox("Show Slice Plane")
        self.slice_checkbox.setChecked(False)
        self.slice_checkbox.stateChanged.connect(self.update_slice)
        layout.addWidget(self.slice_checkbox)

        layout.addWidget(QLabel("Slice Position (0-100%):"))
        self.slice_slider = QSlider(Qt.Orientation.Horizontal)
        self.slice_slider.setRange(0, 100)
        self.slice_slider.setValue(50)
        self.slice_slider.valueChanged.connect(self.update_slice)
        layout.addWidget(self.slice_slider)

        layout.addWidget(QLabel("Slice Axis:"))
        self.slice_axis_combo = QComboBox()
        self.slice_axis_combo.addItems(["X", "Y", "Z"])
        self.slice_axis_combo.currentTextChanged.connect(self.update_slice)
        layout.addWidget(self.slice_axis_combo)
        #----------------------------------------------------------------------
    
        # Field selection
        layout.addWidget(QLabel("Display Field:"))
        self.field_combo = QComboBox()
        layout.addWidget(self.field_combo)
    
        # Display options
        self.edges_checkbox = QCheckBox("Show Edges")
        self.edges_checkbox.setChecked(True)
        layout.addWidget(self.edges_checkbox)
    
        self.scalar_bar_checkbox = QCheckBox("Show Scalar Bar")
        self.scalar_bar_checkbox.setChecked(True)
        layout.addWidget(self.scalar_bar_checkbox)

        self.scalar_bar_checkbox.stateChanged.connect(self.update_scalar_bar)

        self.show_undeformed_checkbox = QCheckBox("Show Undeformed Mesh (Wireframe)")
        self.show_undeformed_checkbox.setChecked(False)
        self.show_undeformed_checkbox.stateChanged.connect(self.display_mesh)
        layout.addWidget(self.show_undeformed_checkbox)

        # Add after scalar bar checkbox
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

        # Ein Box für Animation---------------------------------------------
        # Die Checkbox steuert ob animiert wird
        self.animation_checkbox = QCheckBox("Animate Deformation")
        self.animation_checkbox.setChecked(False)
        self.animation_checkbox.stateChanged.connect(self.run_animation)
        layout.addWidget(self.animation_checkbox)
        # das Label zeigt wie stark die Verformung aktuell ist
        self.deform_label = QLabel("1.0x")
        layout.addWidget(self.deform_label)
        #--------------------------------------------------------------------
    
        # Mesh info
        layout.addWidget(QLabel("\nMesh Information:"))
        self.info_label = QLabel("No mesh loaded")
        self.info_label.setWordWrap(True)
        layout.addWidget(self.info_label)
    
        # Reset button
        reset_button = QPushButton("Reset View")
        reset_button.clicked.connect(self.reset_camera)
        layout.addWidget(reset_button)

        # Add these lines in create_controls method after creating the widgets:
        self.field_combo.currentTextChanged.connect(self.update_field_display)
        self.edges_checkbox.stateChanged.connect(self.update_display_options)
        self.scalar_bar_checkbox.stateChanged.connect(self.update_display_options)
    
        # Push controls to top
        layout.addStretch()
    
        # Fixed width for control panel
        controls.setFixedWidth(280)
    
        return controls
    
    def create_menus(self): # hier werden die Menüs erstellt File und View
        """Create application menus"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        open_action = QAction("&Open Mesh...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_mesh)
        file_menu.addAction(open_action)

        # In create_menus, before file_menu.addSeparator():
        export_action = QAction("&Export Screenshot...", self)
        export_action.setShortcut("Ctrl+S")
        export_action.triggered.connect(self.export_screenshot)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        reset_action = QAction("&Reset Camera", self)
        reset_action.setShortcut("R")
        reset_action.triggered.connect(self.reset_camera)
        view_menu.addAction(reset_action)
    
    def open_mesh(self): # öffnet eine Mesh-Datei
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
    
            # Update field selector
            self.populate_field_selector()
    
            # Display mesh (will be refined in next step)
            self.display_mesh()
    
            # Update info
            self.update_mesh_info()
    
            # Update status and title
            self.statusBar().showMessage(f"Loaded: {filename}", 3000)
            self.setWindowTitle(f"FEM Viewer - {os.path.basename(filename)}")
    
        except Exception as e:
            self.statusBar().showMessage(f"Error loading file: {str(e)}", 5000)


    
    def reset_camera(self): #kamera resetten für alle Ansichten
        """Reset the camera view for all plotters"""
        if not self.plotters:
            return

        for plotter in self.plotters:
            plotter.reset_camera()  # Jeder Plotter bekommt ein Reset

        self.statusBar().showMessage("Camera reset", 2000)


    def closeEvent(self, event): # beim Schließen der Application wird alles richtig geschlossen ohne Fehlermeldungen
        """Clean up VTK resources before closing"""
        if self.plotters:
            for plotter in self.plotters:
                if plotter is not None:
                    try:
                        plotter.close()   # PyVista QtInteractor Bereinigung
                    except Exception:
                        pass
        event.accept()

    def populate_field_selector(self): # Feld-Auswahl füllen und updaten
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

    def update_mesh_info(self): # Mesh-Informationen updaten
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

    def display_mesh(self): # zeigt das Mesh mit den aktuellen Einstellungen für alle Plotter an (Mehrere Ansichten)
        """Display mesh with current settings for all plotters (Multiple Views)"""
        if self.mesh is None:
            return

        # Alte Actors-Liste leeren
        self.deformed_actors = []

        # Prüfen, ob Wireframe angezeigt werden soll
        show_undeformed = self.show_undeformed_checkbox.isChecked() and self.original_mesh is not None

        # Aktuell ausgewähltes Feld
        field_name = self.field_combo.currentText()

        if field_name == "(No Field)" or not field_name:
            # Nur Geometrie
            display_field = None
            title = ""
            color = 'lightgray'           # Mesh-Farbe für „rohes“ Mesh
            show_scalar_bar = False        # keine Scalar Bar
        else:
            # Felddaten abrufen
            field_data = self.mesh.point_data[field_name]

            # Prüfen, ob Vektorfeld
            if field_data.ndim > 1 and field_data.shape[1] > 1:
                magnitude = np.linalg.norm(field_data, axis=1)
                mag_field_name = f"{field_name}_magnitude"
                self.mesh[mag_field_name] = magnitude
                display_field = mag_field_name
                title = f"{field_name} (Magnitude)"
            else:
                display_field = field_name
                title = field_name

            color = None
            show_scalar_bar = self.scalar_bar_checkbox.isChecked()

        # Über alle Plotter iterieren
        # zeigt das Mesh mit den aktuellen Einstellungen für alle Plotter an (Mehrere Ansichten)
        for plotter in self.plotters:
            plotter.clear()

            # Undeformed Mesh als Wireframe anzeigen
            if show_undeformed:
                plotter.add_mesh(
                    self.original_mesh,
                    color='black',
                    style='wireframe',
                    line_width=1,
                    name='undeformed'
                )

            # Mesh anzeigen (mit Feld oder nur Geometrie)
            deformed_actor = plotter.add_mesh(
                self.mesh,
                scalars=display_field,
                color=color,
                cmap='coolwarm' if display_field else None,
                show_edges=self.edges_checkbox.isChecked(),
                show_scalar_bar=show_scalar_bar,
                scalar_bar_args={'title': title} if display_field else None
            )

            # Actor speichern für spätere Updates (z.B. Deformation)
            self.deformed_actors.append(deformed_actor)

            # Kamera für jede View zurücksetzen
            plotter.reset_camera()

    def update_field_display(self, field_name):
            """Update display when field selection changes"""
            self.display_mesh()

    def update_display_options(self):
        if not self.deformed_actors or not self.plotters:
            return

        for actor in self.deformed_actors:
            if actor is None:
                continue
            prop = actor.GetProperty()
            if self.edges_checkbox.isChecked():
                prop.EdgeVisibilityOn()
            else:
                prop.EdgeVisibilityOff()

        # Render für alle Plotter
        for plotter in self.plotters:
            plotter.render()


    def update_deformation(self):
        """Apply deformation to mesh for all plotters"""
        if self.mesh is None or not self.deform_checkbox.isChecked():
            # Restore original if not deforming
            if self.original_mesh is not None:
                self.mesh = self.original_mesh.copy()
            self.display_mesh()
            return

        # Find displacement field (common names)
        displacement_field = None
        for field_name in ['U', 'Displacement', 'displacement', 'DISPL']:
            if field_name in self.mesh.point_data:
                displacement_field = field_name
                break

        if displacement_field is None:
            self.statusBar().showMessage("No displacement field found", 3000)
            self.deform_checkbox.setChecked(False)
            return

        # Scale factor from slider
        scale = self.deform_slider.value() / 10.0
        self.deform_label.setText(f"{scale:.1f}x")

        # Store original if not already stored
        if self.original_mesh is None:
            self.original_mesh = self.mesh.copy()

        # Apply deformation
        displacement = self.mesh.point_data[displacement_field]

        # Ensure 3D displacement
        if displacement.shape[1] == 2:
            displacement = np.hstack([displacement, np.zeros((displacement.shape[0], 1))])

        deformed_points = self.original_mesh.points + scale * displacement
        self.mesh.points = deformed_points

        # Update all plotters
        if self.deformed_actors:
            for deformed_actor, plotter in zip(self.deformed_actors, self.plotters):
                deformed_actor.GetMapper().SetInputData(self.mesh)
                plotter.render()
        else:
            # Fallback beim ersten Mal
            self.display_mesh()



    def get_display_field(self, field_name):
        field_data = self.mesh.point_data[field_name]
        if field_data.ndim > 1 and field_data.shape[1] > 1:
            magnitude = np.linalg.norm(field_data, axis=1)
            mag_field_name = f"{field_name}_magnitude"
            self.mesh[mag_field_name] = magnitude
            return mag_field_name, f"{field_name} (Magnitude)"
        else:
            return field_name, field_name
        
    def update_scalar_bar(self):
        if self.mesh is None:
            return

        # Actor bewusst neu aufbauen
        self.deformed_actor = None
        self.display_mesh()

    def export_screenshot(self):
        """Save current view(s) as image(s)"""
        if not self.plotters or self.mesh is None:
            self.statusBar().showMessage("No mesh to export", 2000)
            return

        # Dialog zum Speichern
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Screenshot",
            "screenshot.png",
            "PNG Images (*.png);;JPEG Images (*.jpg);;All Files (*.*)"
        )

        if not filename:
            return

        # Prüfen, ob Extension angegeben ist
        base, ext = os.path.splitext(filename)
        if not ext:
            ext = ".png"

        try:
            # Alle Plotter speichern
            for i, plotter in enumerate(self.plotters, start=1):
                file_i = f"{base}_{i}{ext}" if len(self.plotters) > 1 else f"{base}{ext}"
                plotter.set_background("white")
                plotter.screenshot(file_i, transparent_background=False)

            self.statusBar().showMessage(f"Saved screenshots: {base}_1...{base}_{len(self.plotters)}", 3000)
        except Exception as e:
            self.statusBar().showMessage(f"Error saving screenshots: {str(e)}", 5000)

    def run_animation(self):
        """Animate deformation by moving the slider automatically"""
        if not self.animation_checkbox.isChecked():
            return  # Animation wurde deaktiviert

        # Maximalwert des Sliders
        max_value = self.deform_slider.maximum()
        min_value = self.deform_slider.minimum()
        
        # Einfacher Slider von min → max → min
        step = 500  # Geschwindigkeit (höher = schneller)
        
        def animate():
            if not self.animation_checkbox.isChecked():
                return  # Stoppt, wenn Checkbox deaktiviert wird

            current = self.deform_slider.value()
            # Richtung umdrehen, wenn wir an den Grenzen sind
            if current >= max_value:
                self._animation_direction = -1
            elif current <= min_value:
                self._animation_direction = 1

            # Sliderwert aktualisieren
            self.deform_slider.setValue(current + self._animation_direction * step)

            # Wiederhole die Funktion nach kurzer Verzögerung
            QTimer.singleShot(5, animate)  

        # Startrichtung initialisieren
        self._animation_direction = 1
        animate()

    def update_slice(self):
        """Display a slice of the mesh along the selected axis"""
        if self.mesh is None or not self.slice_checkbox.isChecked():
            self.display_mesh()
            return

        axis = self.slice_axis_combo.currentText().upper()
        pos_percent = self.slice_slider.value() / 100.0
        bounds = self.mesh.bounds

        if axis == "X":
            pos = bounds[0] + pos_percent * (bounds[1] - bounds[0])
            slice_mesh = self.mesh.slice(normal=[1, 0, 0], origin=[pos, 0, 0])
        elif axis == "Y":
            pos = bounds[2] + pos_percent * (bounds[3] - bounds[2])
            slice_mesh = self.mesh.slice(normal=[0, 1, 0], origin=[0, pos, 0])
        else:  # Z
            pos = bounds[4] + pos_percent * (bounds[5] - bounds[4])
            slice_mesh = self.mesh.slice(normal=[0, 0, 1], origin=[0, 0, pos])

        # **Check for empty mesh**
        if slice_mesh.n_points == 0:
            # Warnung ausgeben und Original-Mesh anzeigen
            self.statusBar().showMessage("Slice erzeugt leeres Mesh – verschiebe den Slider.", 3000)
            self.display_mesh()
            return

        # Plotter aktualisieren
        for plotter in self.plotters:
            plotter.clear()
            plotter.add_mesh(
                slice_mesh,
                scalars=self.field_combo.currentText() if self.field_combo.currentText() != "(No Field)" else None,
                cmap='coolwarm',
                show_edges=self.edges_checkbox.isChecked(),
                show_scalar_bar=self.scalar_bar_checkbox.isChecked()
            )

            if self.show_undeformed_checkbox.isChecked() and self.original_mesh is not None:
                plotter.add_mesh(
                    self.original_mesh,
                    color='black',
                    style='wireframe',
                    line_width=1
                )
            plotter.reset_camera()

# öffnet und schließt die Application richtig
def main():
    app = QApplication(sys.argv)
    window = FEMViewer()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 

