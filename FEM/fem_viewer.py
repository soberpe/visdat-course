#Prerequisites
# Activate virtual environment
#.venv\Scripts\activate

# Verify installations
#python -c "import PyQt6; print('PyQt6:', PyQt6.QtCore.PYQT_VERSION_STR)"
#python -c "import pyvista; print('PyVista:', pyvista.__version__)"
#python -c "import pyvistaqt; print('PyVistaQt: OK')"
#Workshop Data


import pyvista as pv

# Load the beam mesh with results (adjust path to your repository location)
mesh = pv.read('data/beam_stress.vtu')

# Check available fields
print("Available fields:", list(mesh.point_data.keys()))
# Output: ['U', 'S', 'S_MISES', 'E', 'RF', ...]




#Erster Code von Professor
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
import sys

class FEMViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FEM Results Viewer")
        self.resize(1200, 800)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Placeholder for now
        label = QLabel("FEM Viewer - Coming Soon")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(label)
        
        # Create menu bar
        self.create_menus()
        
        # Create status bar
        self.statusBar().showMessage("Ready")
    
    def create_menus(self):
        """Create application menus"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        open_action = QAction("&Open Mesh...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_mesh)
        file_menu.addAction(open_action)
        
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
    
    def open_mesh(self):
        """Open mesh file (to be implemented)"""
        self.statusBar().showMessage("Open mesh - not implemented yet", 2000)
    
    def reset_camera(self):
        """Reset camera view (to be implemented)"""
        self.statusBar().showMessage("Reset camera - not implemented yet", 2000)

def main():
    app = QApplication(sys.argv)
    window = FEMViewer()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

# Fragestellung nach diesem Code:
#What happens when you press Ctrl+O?
#Beim Drücken von Ctrl+O wird „Open Mesh…“ ausgeführt.

#Why do we use sys.exit(app.exec())?
#Diese Zeile hält die Anwendung am Laufen, bis der Benutzer sie schließt, und beendet sie danach korrekt

#What's the purpose of the status bar?
#Dient dazu, dem Benutzer Rückmeldungen zu geben.





# Zweiter Code von Prpfessor
from pyvistaqt import QtInteractor
import pyvista as pv



#Dritter Code von Professor
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
    
    # Left side will be controls (later)
    # For now, just add plotter
    
    # Right side: PyVista 3D view
    self.plotter = QtInteractor(central_widget)
    main_layout.addWidget(self.plotter.interactor)
    
    # Add a sample sphere for testing
    sphere = pv.Sphere()
    self.plotter.add_mesh(sphere, color='lightblue', show_edges=True)
    self.plotter.reset_camera()
    
    # Create menus and status bar
    self.create_menus()
    self.statusBar().showMessage("Ready")




 #Vierter Code von Professor
    def reset_camera(self): 
        """Reset camera view"""
    if self.plotter:
        self.plotter.reset_camera()
        self.statusBar().showMessage("Camera reset", 2000)




 #Fünfter Code von Professor
    def closeEvent(self, event): """Clean up VTK resources before closing"""
    if self.plotter:
        self.plotter.close()
        self.plotter = None
    event.accept()

#Fragen nach diesem Code:
#What does QtInteractor provide?
#QtInteractor ist die Verbindung zwischen VTK und PyQt-

#Why do we use self.plotter.interactor instead of self.plotter?
#self.plotter ist ein Python-Objekt, das PyVista-Funktionen kapselt
#self.plotter.interactor ist ein Qt-Widget (QWidget)

#What's the difference between show_edges=True and show_edges=False?
#show_edges=True
#Elementkanten werden sichtbar dargestellt
#Ideal für:
#FEM-Netze
#Debugging
#Überprüfung der Elementstruktur

#show_edges=False
#Nur die Oberfläche wird dargestellt
#Glatte Darstellungen
#Ideal für:
#Präsentationen
#Ergebnisplots (z. B. Spannungen)





#Sechster Code von Professor
    from PyQt6.QtWidgets import QFileDialog

    #Siebter Code von Professor
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
        
        # Clear previous display
        self.plotter.clear()
        
        # Display mesh
        self.plotter.add_mesh(
            self.mesh,
            color='lightgray',
            show_edges=True
        )
        self.plotter.reset_camera()
        
        # Update status
        self.statusBar().showMessage(f"Loaded: {filename}", 3000)
        
        # Update window title
        import os
        self.setWindowTitle(f"FEM Viewer - {os.path.basename(filename)}")
        
    except Exception as e:
        self.statusBar().showMessage(f"Error loading file: {str(e)}", 5000)

#Achter Code von Professor
# Remove these lines:
sphere = pv.Sphere()
self.plotter.add_mesh(sphere, color='lightblue', show_edges=True)
self.plotter.reset_camera()

#Why do we check if not filename?
#verhindert unnötige Fehler, bricht die Funktion sauber ab und verbessert die Benutzerfreundlichkeit
#Kurz: Kein Dateiname = nichts laden = Funktion beenden

#What does plotter.clear() do?
#entfernt alle aktuell dargestellten Objekte aus dem 3D-Viewport
#löscht: Meshes, Farben, Skalarfelder, Darstellungsoptionen
#Es wird nicht: das Fenster geschlossen, der Plotter zerstört

#Why is the try-except block important?
#Beim Laden und Anzeigen von FEM-Daten kann vieles schiefgehen:
#Datei existiert nicht, falsches Dateiformat, beschädigte VTU-Datei, fehlende Ergebnisfelder
#Der try-except-Block: fängt solche Fehler ab, verhindert einen Programmabsturz,erlaubt eine kontrollierte Fehlermeldung

# Neunter Code von Proefessor
from PyQt6.QtWidgets import (
    QGroupBox, QComboBox, QCheckBox,
    QPushButton
)

# Zehnter Code von Professor
# Create control panel
controls = self.create_controls()
main_layout.addWidget(controls)

# PyVista plotter (move existing plotter code here)
self.plotter = QtInteractor(central_widget)
main_layout.addWidget(self.plotter.interactor, stretch=3)  # Give more space to 3D view

# Create menus and status bar
self.create_menus()
self.statusBar().showMessage("Ready")

#Elfter Code von Professor
def create_controls(self):
    """Create control panel with field selection and display options"""
    controls = QGroupBox("Visualization Controls")
    layout = QVBoxLayout()
    controls.setLayout(layout)
    
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

# Zwölfter Code von Professor
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
    import os
    self.setWindowTitle(f"FEM Viewer - {os.path.basename(filename)}")
    
except Exception as e:
    self.statusBar().showMessage(f"Error loading file: {str(e)}", 5000)

# Dreizehnter Code von Professor
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
    if self.mesh is None:
        return
    
    self.plotter.clear()
    
    # Get current field selection
    field_name = self.field_combo.currentText()
    
    # Determine what to display
    if field_name == "(No Field)" or not field_name:
        # Display geometry only
        self.plotter.add_mesh(
            self.mesh,
            color='lightgray',
            show_edges=self.edges_checkbox.isChecked(),
            show_scalar_bar=False
        )
    else:
        # Display with scalar field
        self.plotter.add_mesh(
            self.mesh,
            scalars=field_name,
            cmap='coolwarm',
            show_edges=self.edges_checkbox.isChecked(),
            show_scalar_bar=self.scalar_bar_checkbox.isChecked(),
            scalar_bar_args={'title': field_name}
        )
    
    self.plotter.reset_camera()

# Vierzehnter Code von Professor
def update_field_display(self, field_name):
    """Update display when field selection changes"""
    self.display_mesh()

def update_display_options(self):
    """Update display when checkboxes change"""
    self.display_mesh()

# Fünfzehnter Code von Proefessor
# Add these lines in create_controls method after creating the widgets:
self.field_combo.currentTextChanged.connect(self.update_field_display)
self.edges_checkbox.stateChanged.connect(self.update_display_options)
self.scalar_bar_checkbox.stateChanged.connect(self.update_display_options)

#Fragen nach diesem Code:
#Why do we use blockSignals(True) when populating the combo box?
#Beim Hinzufügen von Einträgen zu einer QComboBox wird normalerweise das Signal currentIndexChanged automatisch ausgelöst.

#What's the purpose of scalar_bar_args={'title': field_name}?
#Damit wird die Farblegende (Colorbar) konfiguriert:
# field_name ist der aktuell dargestellte Ergebnisname
#der Titel erscheint direkt an der Colorbar

#How would you handle vector fields (e.g., displacement with 3 components)?
#Standard: Betrag anzeigen (|U|)
#Optional: Komponenten per Auswahl
#Advanced: Pfeile ein/ausblendbar




#Sechzehnter Code von Professor
def display_mesh(self):
    """Display mesh with current settings"""
    if self.mesh is None:
        return
    
    self.plotter.clear()
    
    # Get current field selection
    field_name = self.field_combo.currentText()
    
    if field_name == "(No Field)" or not field_name:
        # Geometry only
        self.plotter.add_mesh(
            self.mesh,
            color='lightgray',
            show_edges=self.edges_checkbox.isChecked(),
            show_scalar_bar=False
        )
    else:
        # Get field data
        field_data = self.mesh.point_data[field_name]
        
        # Check if vector field (multi-component)
        if field_data.ndim > 1 and field_data.shape[1] > 1:
            # Compute magnitude
            import numpy as np
            magnitude = np.linalg.norm(field_data, axis=1)
            
            # Add as new field
            mag_field_name = f"{field_name}_magnitude"
            self.mesh[mag_field_name] = magnitude
            display_field = mag_field_name
            title = f"{field_name} (Magnitude)"
        else:
            display_field = field_name
            title = field_name
        
        # Display with scalar field
        self.plotter.add_mesh(
            self.mesh,
            scalars=display_field,
            cmap='coolwarm',
            show_edges=self.edges_checkbox.isChecked(),
            show_scalar_bar=self.scalar_bar_checkbox.isChecked(),
            scalar_bar_args={'title': title}
        )
    
    self.plotter.reset_camera()

#Siebzehnter Code von Professor
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QFileDialog,
    QGroupBox, QComboBox, QCheckBox,
    QPushButton, QSlider  # Add QSlider
)

#Achtzehnter Code von Proefessor
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

self.deform_label = QLabel("1.0x")
layout.addWidget(self.deform_label)

#Neunzehnter Code von Professor
def __init__(self):
    # ... existing code ...
    self.mesh = None
    self.original_mesh = None  # Store undeformed mesh

#Zwanzigster Code von Professor
def update_deformation(self):
    """Apply deformation to mesh based on displacement field"""
    if self.mesh is None or not self.deform_checkbox.isChecked():
        # Restore original if not deforming
        if self.original_mesh is not None:
            self.mesh = self.original_mesh.copy()
        self.display_mesh()
        return
    
    # Find displacement field (common names: U, Displacement, displacement)
    displacement_field = None
    for field_name in ['U', 'Displacement', 'displacement', 'DISPL']:
        if field_name in self.mesh.point_data:
            displacement_field = field_name
            break
    
    if displacement_field is None:
        self.statusBar().showMessage("No displacement field found", 3000)
        self.deform_checkbox.setChecked(False)
        return
    
    # Get scale factor
    scale = self.deform_slider.value() / 10.0
    self.deform_label.setText(f"{scale:.1f}x")
    
    # Store original if not already stored
    if self.original_mesh is None:
        self.original_mesh = self.mesh.copy()
    
    # Apply deformation
    import numpy as np
    displacement = self.mesh.point_data[displacement_field]
    
    # Ensure displacement is 3D
    if displacement.shape[1] == 2:
        # 2D displacement, add zero Z component
        displacement = np.hstack([displacement, np.zeros((displacement.shape[0], 1))])
    
    # Create deformed mesh
    deformed_points = self.original_mesh.points + scale * displacement
    self.mesh.points = deformed_points
    
    # Update display
    self.display_mesh()

    #Einundzwanzigster Code von Professor
    # In open_mesh, after self.mesh = pv.read(filename):
self.original_mesh = None  # Reset deformation state
self.deform_checkbox.setChecked(False)

#Zweiundzwanzigster Code von Professor
# In create_menus, before file_menu.addSeparator():
export_action = QAction("&Export Screenshot...", self)
export_action.setShortcut("Ctrl+S")
export_action.triggered.connect(self.export_screenshot)
file_menu.addAction(export_action)

#Dreiundzwanzigster Code von Professor
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

#Ende