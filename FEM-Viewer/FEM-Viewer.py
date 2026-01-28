from fileinput import filename
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel
)
from PyQt6.QtWidgets import (
    QGroupBox, QComboBox, QCheckBox,
    QPushButton
)
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import Qt
from pyvistaqt import QtInteractor
import pyvista as pv
import sys

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
    
    # Create control panel
        controls = self.create_controls()
        main_layout.addWidget(controls)

    # PyVista plotter (move existing plotter code here)
        self.plotter = QtInteractor(central_widget)
        main_layout.addWidget(self.plotter.interactor, stretch=3)  # Give more space to 3D view

    # Create menus and status bar
        self.create_menus()
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

    def reset_camera(self):
        """Reset camera view"""
        if  self.plotter:
            self.plotter.reset_camera()
            self.statusBar().showMessage("Camera reset", 2000)

    def closeEvent(self, event):
        """Clean up VTK resources before closing"""
        if self.plotter:
            self.plotter.close()
            self.plotter = None
        event.accept()

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

def main():
    app = QApplication(sys.argv)
    window = FEMViewer()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()