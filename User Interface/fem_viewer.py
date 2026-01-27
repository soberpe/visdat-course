import sys
import os
import pyvista as pv
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QFileDialog,
    QGroupBox, QComboBox, QCheckBox,
    QPushButton, QSlider  # Add QSlider
)
from PyQt6.QtGui import QAction
from pyvistaqt import QtInteractor


class FEMViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FEM Results Viewer")
        self.resize(1200, 800)
        
        # -----------------------------
        # State variables
        # -----------------------------
        self.mesh = None
        
        # -----------------------------
        # Create central widget
        # -----------------------------
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout (horizontal split)
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # -----------------------------
        # Create control panel (left)
        # -----------------------------
        controls = self.create_controls()
        main_layout.addWidget(controls)

        # -----------------------------
        # PyVista plotter (RIGHT SIDE)
        # IMPORTANT: only create ONCE
        # -----------------------------
        self.plotter = QtInteractor(central_widget)
        main_layout.addWidget(self.plotter.interactor, stretch=3)

        # -----------------------------
        # Create menus and status bar
        # -----------------------------
        self.create_menus()
        self.statusBar().showMessage("Ready")

    def create_controls(self):
        """Create control panel with field selection and display options"""
        controls = QGroupBox("Visualization Controls")
        layout = QVBoxLayout()
        controls.setLayout(layout)
        
        # -----------------------------
        # Field selection
        # -----------------------------
        layout.addWidget(QLabel("Display Field:"))
        self.field_combo = QComboBox()
        self.field_combo.currentIndexChanged.connect(self.display_mesh)
        layout.addWidget(self.field_combo)
        
        # -----------------------------
        # Display options
        # -----------------------------
        self.edges_checkbox = QCheckBox("Show Edges")
        self.edges_checkbox.setChecked(True)
        self.edges_checkbox.stateChanged.connect(self.display_mesh)
        layout.addWidget(self.edges_checkbox)
        
        self.scalar_bar_checkbox = QCheckBox("Show Scalar Bar")
        self.scalar_bar_checkbox.setChecked(True)
        self.scalar_bar_checkbox.stateChanged.connect(self.display_mesh)
        layout.addWidget(self.scalar_bar_checkbox)

        # Add these lines in create_controls method after creating the widgets:
        self.field_combo.currentTextChanged.connect(self.update_field_display)
        self.edges_checkbox.stateChanged.connect(self.update_display_options)
        self.scalar_bar_checkbox.stateChanged.connect(self.update_display_options)
        
        # -----------------------------
        # Mesh info
        # -----------------------------
        layout.addWidget(QLabel("\nMesh Information:"))
        self.info_label = QLabel("No mesh loaded")
        self.info_label.setWordWrap(True)
        layout.addWidget(self.info_label)
        
        # -----------------------------
        # Reset button
        # -----------------------------
        reset_button = QPushButton("Reset View")
        reset_button.clicked.connect(self.reset_camera)
        layout.addWidget(reset_button)
        
        # Push controls to top
        layout.addStretch()
        
        # Fixed width for control panel
        controls.setFixedWidth(280)
        
        return controls
    
    def create_menus(self):
        """Create application menus"""
        menubar = self.menuBar()
        
        # -----------------------------
        # File menu
        # -----------------------------
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
        
        # -----------------------------
        # View menu
        # -----------------------------
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
            # -----------------------------
            # Load mesh
            # -----------------------------
            self.mesh = pv.read(filename)
            
            # Update UI elements
            self.populate_field_selector()
            self.display_mesh()
            self.update_mesh_info()
            
            # Update status and title
            self.statusBar().showMessage(f"Loaded: {filename}", 3000)
            self.setWindowTitle(f"FEM Viewer - {os.path.basename(filename)}")
            
        except Exception as e:
            self.statusBar().showMessage(f"Error loading file: {str(e)}", 5000)

    def populate_field_selector(self):
        """Populate field combo box with available scalar fields"""
        self.field_combo.blockSignals(True)
        self.field_combo.clear()
        
        if self.mesh is None:
            self.field_combo.blockSignals(False)
            return
        
        # Geometry-only option
        self.field_combo.addItem("(No Field)")
        
        # Add all point data fields
        for field_name in self.mesh.point_data.keys():
            self.field_combo.addItem(field_name)
        
        self.field_combo.blockSignals(False)
        
        # Select first scalar field if available
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
            f"Point Fields: {n_fields}"
        )
        
        self.info_label.setText(info_text)

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

    def update_field_display(self, field_name):
        """Update display when field selection changes"""
        self.display_mesh()

    def update_display_options(self):
        """Update display when checkboxes change"""
        self.display_mesh()
    
    def reset_camera(self):
        """Reset camera view"""
        if self.plotter:
            self.plotter.reset_camera()
            self.statusBar().showMessage("Camera reset", 2000)


# --------------------------------------------------
# Application entry point
# --------------------------------------------------

def main():
    app = QApplication(sys.argv)
    window = FEMViewer()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()