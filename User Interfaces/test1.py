import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel
)
from pyvistaqt import QtInteractor
import pyvista as pv
import numpy as np

class ComparisonViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multi-View Comparison")
        self.resize(1400, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Create grid of plotters
        grid = QGridLayout()
        layout.addLayout(grid)
        
        # Left view
        left_label = QLabel("Von Mises Stress")
        grid.addWidget(left_label, 0, 0)
        self.plotter_left = QtInteractor(central_widget)
        grid.addWidget(self.plotter_left.interactor, 1, 0)
        
        # Right view
        right_label = QLabel("Displacement")
        grid.addWidget(right_label, 0, 1)
        self.plotter_right = QtInteractor(central_widget)
        grid.addWidget(self.plotter_right.interactor, 1, 1)
        
        # Control buttons
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        
        sync_button = QPushButton("Sync Cameras")
        sync_button.clicked.connect(self.sync_cameras)
        button_layout.addWidget(sync_button)
        
        reset_button = QPushButton("Reset Both")
        reset_button.clicked.connect(self.reset_both)
        button_layout.addWidget(reset_button)
        
        # Load demo data
        self.load_demo_data()
    
    def load_demo_data(self):
        """Create demo mesh with two scalar fields"""
        mesh = pv.Sphere(radius=1.0, theta_resolution=50, phi_resolution=50)
        
        # Simulate stress field (higher at poles)
        points = mesh.points
        stress = np.abs(points[:, 2]) * 100  # Z-coordinate based
        mesh['S_Mises'] = stress
        
        # Simulate displacement field (higher at equator)
        disp_mag = np.sqrt(points[:, 0]**2 + points[:, 1]**2) * 0.5
        mesh['U_magnitude'] = disp_mag
        
        # Display in both views with copy_mesh=True
        self.plotter_left.clear()
        self.plotter_left.add_mesh(
            mesh,
            scalars='S_Mises',
            cmap='jet',
            show_scalar_bar=True,
            scalar_bar_args={'title': 'Stress [MPa]'},
            copy_mesh=True  # Important when using same mesh multiple times!
        )
        
        self.plotter_right.clear()
        self.plotter_right.add_mesh(
            mesh,
            scalars='U_magnitude',
            cmap='viridis',
            show_scalar_bar=True,
            scalar_bar_args={'title': 'Displacement [mm]'},
            copy_mesh=True  # Important when using same mesh multiple times!
        )
        
        self.plotter_left.reset_camera()
        self.plotter_right.reset_camera()
    
    def sync_cameras(self):
        """Synchronize right camera to left"""
        cam_left = self.plotter_left.camera
        cam_right = self.plotter_right.camera
        
        # Copy camera parameters
        cam_right.position = cam_left.position
        cam_right.focal_point = cam_left.focal_point
        cam_right.up = cam_left.up
        
        self.plotter_right.update()
    
    def reset_both(self):
        """Reset both cameras"""
        self.plotter_left.reset_camera()
        self.plotter_right.reset_camera()
    
    def closeEvent(self, event):
        # Clean up both plotters before closing
        self.plotter_left.close()
        self.plotter_right.close()
        self.plotter_left = None
        self.plotter_right = None
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ComparisonViewer()
    window.show()
    sys.exit(app.exec())