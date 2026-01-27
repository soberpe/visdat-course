import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton,
    QComboBox, QLabel, QFileDialog, QGroupBox
)
from pyvistaqt import QtInteractor
import pyvista as pv
import numpy as np

class FEMViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FEM Results Viewer")
        self.resize(1200, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Controls
        controls = self.create_controls()
        main_layout.addWidget(controls)
        
        # 3D view
        self.plotter = QtInteractor(central_widget)
        main_layout.addWidget(self.plotter.interactor, stretch=3)
        
        # State
        self.mesh = None
        self.actor = None  # Store mesh actor for updates
    
    def create_controls(self):
        """Create control panel"""
        controls = QGroupBox("Analysis Controls")
        layout = QVBoxLayout()
        controls.setLayout(layout)
        
        # Load button
        load_button = QPushButton("Load Mesh (VTU)")
        load_button.clicked.connect(self.load_mesh)
        layout.addWidget(load_button)
        
        # Field selection
        layout.addWidget(QLabel("Display Field:"))
        self.field_combo = QComboBox()
        self.field_combo.currentTextChanged.connect(self.update_display)
        layout.addWidget(self.field_combo)
        
        # Info label
        self.info_label = QLabel("No mesh loaded")
        self.info_label.setWordWrap(True)
        layout.addWidget(self.info_label)
        
        # Reset view
        reset_button = QPushButton("Reset Camera")
        reset_button.clicked.connect(lambda: self.plotter.reset_camera())
        layout.addWidget(reset_button)
        
        layout.addStretch()
        controls.setFixedWidth(250)
        return controls
    
    def load_mesh(self):
        """Load mesh file using file dialog"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Mesh File",
            "",
            "VTK Files (*.vtu *.vtk);;All Files (*.*)"
        )
        
        if not filename:
            return
        
        try:
            self.mesh = pv.read(filename)
            
            # Update field combo
            self.field_combo.clear()
            point_arrays = list(self.mesh.point_data.keys())
            cell_arrays = list(self.mesh.cell_data.keys())
            
            if point_arrays:
                self.field_combo.addItems(point_arrays)
            
            # Update info
            n_points = self.mesh.n_points
            n_cells = self.mesh.n_cells
            self.info_label.setText(
                f"Loaded: {filename.split('/')[-1]}\n"
                f"Points: {n_points}\n"
                f"Cells: {n_cells}\n"
                f"Fields: {len(point_arrays)}"
            )
            
            # Display first field
            if point_arrays:
                self.update_display(point_arrays[0])
            else:
                self.plotter.clear()
                self.plotter.add_mesh(self.mesh, color='lightgray')
                self.plotter.reset_camera()
            
        except Exception as e:
            self.info_label.setText(f"Error loading file:\n{str(e)}")
    
    def update_display(self, field_name):
        """Update displayed field"""
        if self.mesh is None or not field_name:
            return
        
        self.plotter.clear()
        
        # Check if field exists
        if field_name not in self.mesh.point_data:
            return
        
        # Get field data
        field_data = self.mesh.point_data[field_name]
        
        # Handle vector fields (show magnitude)
        if field_data.ndim > 1:
            scalars = np.linalg.norm(field_data, axis=1)
            scalar_name = f"{field_name} (magnitude)"
            self.mesh[scalar_name] = scalars
            display_field = scalar_name
        else:
            display_field = field_name
        
        # Plot with scalar bar
        self.actor = self.plotter.add_mesh(
            self.mesh,
            scalars=display_field,
            cmap='coolwarm',
            show_edges=False,
            show_scalar_bar=True,
            scalar_bar_args={'title': display_field}
        )
        
        self.plotter.reset_camera()
    
    def closeEvent(self, event):
        # Clean up plotter before closing
        self.plotter.close()
        self.plotter = None
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FEMViewer()
    window.show()
    sys.exit(app.exec())