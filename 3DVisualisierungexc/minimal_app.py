import matplotlib
matplotlib.use("QtAgg")

# from PyQt6.QtWidgets import QApplication, QWidget

# # 1. Create the application object
# app = QApplication([])

# # 2. Create the main window
# window = QWidget()
# window.setWindowTitle("My First Qt App")
# window.resize(400, 300)

# # 3. Show the window
# window.show()

# # 4. Start the event loop
# app.exec()



# from PyQt6.QtWidgets import QApplication, QWidget, QPushButton

# app = QApplication([])
# window = QWidget()
# window.setWindowTitle("Button Example")
# window.resize(400, 300)

# # Create button with text and parent
# button = QPushButton("Click Me", parent=window)
# button.move(150, 120)  # Position manually (not recommended, but works for one widget)

# # Connect signal to slot
# button.clicked.connect(lambda: print("Button clicked!"))

# window.show()
# app.exec()











# from PyQt6.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout,
#     QPushButton, QLabel, QLineEdit
# )

# app = QApplication([])
# window = QWidget()
# window.setWindowTitle("Layout Example")

# # Create layout
# layout = QVBoxLayout()

# # Create widgets
# label = QLabel("Enter your name:")
# text_input = QLineEdit()
# button = QPushButton("Greet")
# result_label = QLabel("")

# # Add widgets to layout
# layout.addWidget(label)
# layout.addWidget(text_input)
# layout.addWidget(button)
# layout.addWidget(result_label)

# # Connect button to action
# def on_button_clicked():
#     name = text_input.text()
#     result_label.setText(f"Hello, {name}!")

# button.clicked.connect(on_button_clicked)

# # Apply layout to window
# window.setLayout(layout)

# window.show()
# app.exec() #blocking




# from PyQt6.QtWidgets import (
#     QApplication, QMainWindow, QWidget,
#     QVBoxLayout, QPushButton, QLabel
# )
# from PyQt6.QtGui import QAction

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()  # Initialize the QMainWindow base class
#         self.setWindowTitle("QMainWindow Example")
#         self.resize(600, 400)
        
#         # QMainWindow uses a central widget for its main content area
#         central_widget = QWidget()
#         self.setCentralWidget(central_widget)
        
#         # Create layout for central widget
#         layout = QVBoxLayout()
#         central_widget.setLayout(layout)
        
#         # Add content
#         self.label = QLabel("Status: Ready")
#         layout.addWidget(self.label)
        
#         button = QPushButton("Do Something")
#         button.clicked.connect(self.on_button_clicked)
#         layout.addWidget(button)
        
#         # Create menu bar
#         menu = self.menuBar()
#         file_menu = menu.addMenu("&File")
        
#         # Add menu actions
#         open_action = QAction("&Open", self)
#         open_action.triggered.connect(self.open_file)
#         file_menu.addAction(open_action)
        
#         exit_action = QAction("E&xit", self)
#         exit_action.triggered.connect(self.close)
#         file_menu.addAction(exit_action)
        
#         # Create status bar
#         self.statusBar().showMessage("Application started")
    
#     def on_button_clicked(self):
#         self.label.setText("Status: Button clicked")
#         self.statusBar().showMessage("Action performed", 3000)  # 3 second timeout
    
#     def open_file(self):
#         self.label.setText("Status: Open file dialog (not implemented)")

# app = QApplication([])
# window = MainWindow()
# window.show()
# app.exec()







# from PyQt6.QtWidgets import (
#     QApplication, QMainWindow, QWidget,
#     QVBoxLayout, QPushButton, QLabel, QFileDialog
# )

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("File Dialog Example")
#         self.resize(500, 300)
        
#         central_widget = QWidget()
#         self.setCentralWidget(central_widget)
#         layout = QVBoxLayout()
#         central_widget.setLayout(layout)
        
#         self.label = QLabel("No file selected")
#         layout.addWidget(self.label)
        
#         open_button = QPushButton("Open File")
#         open_button.clicked.connect(self.open_file)
#         layout.addWidget(open_button)
        
#         save_button = QPushButton("Save File")
#         save_button.clicked.connect(self.save_file)
#         layout.addWidget(save_button)
    
#     def open_file(self):
#         filename, _ = QFileDialog.getOpenFileName(
#             self,
#             "Select File",
#             "",  # Starting directory (empty = last used)
#             "Data Files (*.csv *.h5);;All Files (*.*)"
#         )
        
#         if filename:  # User might cancel
#             self.label.setText(f"Selected: {filename}")
#             # Here you would load the file
    
#     def save_file(self):
#         filename, _ = QFileDialog.getSaveFileName(
#             self,
#             "Save File",
#             "output.csv",
#             "CSV Files (*.csv);;All Files (*.*)"
#         )
        
#         if filename:
#             self.label.setText(f"Would save to: {filename}")
#             # Here you would save data

# app = QApplication([])
# window = MainWindow()
# window.show()
# app.exec()








# import sys
# from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
# from pyvistaqt import QtInteractor
# import pyvista as pv

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("PyVista in Qt")
#         self.resize(800, 600)
        
#         # Create central widget and layout
#         central_widget = QWidget()
#         self.setCentralWidget(central_widget)
#         layout = QVBoxLayout()
#         central_widget.setLayout(layout)
        
#         # Create PyVista Qt widget
#         self.plotter = QtInteractor(central_widget)
#         layout.addWidget(self.plotter.interactor)
        
#         # Add some geometry
#         mesh = pv.Sphere()
#         self.plotter.add_mesh(mesh, color='lightblue', show_edges=True)
        
#         # Reset camera to show the entire scene
#         self.plotter.reset_camera()
    
#     def closeEvent(self, event):
#         # Clean up plotter before closing to prevent VTK errors
#         self.plotter.close()
#         self.plotter = None
#         event.accept()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())










# import sys
# from PyQt6.QtWidgets import (
#     QApplication, QMainWindow, QWidget,
#     QVBoxLayout, QHBoxLayout, QSlider,
#     QLabel, QPushButton, QGroupBox
# )
# from PyQt6.QtCore import Qt
# from pyvistaqt import QtInteractor
# import pyvista as pv
# import numpy as np

# class MeshViewer(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Interactive Mesh Viewer")
#         self.resize(1000, 600)
        
#         # Create central widget
#         central_widget = QWidget()
#         self.setCentralWidget(central_widget)
        
#         # Main layout: horizontal split
#         main_layout = QHBoxLayout()
#         central_widget.setLayout(main_layout)
        
#         # Left side: Controls
#         controls_widget = self.create_controls()
#         main_layout.addWidget(controls_widget)
        
#         # Right side: 3D view
#         self.plotter = QtInteractor(central_widget)
#         main_layout.addWidget(self.plotter.interactor, stretch=3)
        
#         # Create initial mesh
#         self.create_mesh()
    
#     def create_controls(self):
#         """Create control panel with sliders and buttons"""
#         controls = QGroupBox("Controls")
#         layout = QVBoxLayout()
#         controls.setLayout(layout)
        
#         # Resolution slider
#         layout.addWidget(QLabel("Sphere Resolution:"))
#         self.resolution_slider = QSlider(Qt.Orientation.Horizontal)
#         self.resolution_slider.setRange(5, 100)
#         self.resolution_slider.setValue(30)
#         self.resolution_slider.valueChanged.connect(self.update_mesh)
#         layout.addWidget(self.resolution_slider)
        
#         self.resolution_label = QLabel("30")
#         layout.addWidget(self.resolution_label)
        
#         # Deformation slider
#         layout.addWidget(QLabel("Deformation:"))
#         self.deform_slider = QSlider(Qt.Orientation.Horizontal)
#         self.deform_slider.setRange(0, 100)
#         self.deform_slider.setValue(0)
#         self.deform_slider.valueChanged.connect(self.update_deformation)
#         layout.addWidget(self.deform_slider)
        
#         self.deform_label = QLabel("0.00")
#         layout.addWidget(self.deform_label)
        
#         # Reset button
#         reset_button = QPushButton("Reset View")
#         reset_button.clicked.connect(lambda: self.plotter.reset_camera())
#         layout.addWidget(reset_button)
        
#         # Add stretch to push controls to top
#         layout.addStretch()
        
#         controls.setFixedWidth(250)
#         return controls
    
#     def create_mesh(self):
#         """Create sphere mesh with scalar field"""
#         resolution = self.resolution_slider.value()
#         self.mesh = pv.Sphere(radius=1.0, theta_resolution=resolution, 
#                              phi_resolution=resolution)
        
#         # Add scalar field based on z-height (creates colorful bands)
#         points = self.mesh.points
#         self.mesh['height'] = points[:, 2]  # Z-coordinate
        
#         # Store original points for deformation
#         self.original_points = points.copy()
        
#         # Plot mesh and store actor reference for dynamic updates
#         self.plotter.clear()
#         self.actor = self.plotter.add_mesh(
#             self.mesh,
#             scalars='height',
#             cmap='coolwarm',
#             show_edges=False,
#             show_scalar_bar=True
#         )
#         self.plotter.reset_camera()
    
#     def update_mesh(self, value):
#         """Update mesh resolution"""
#         self.resolution_label.setText(str(value))
#         self.create_mesh()
        
#         # Reapply current deformation
#         deform = self.deform_slider.value() / 100.0
#         if deform > 0:
#             self.apply_deformation(deform)
    
#     def update_deformation(self, value):
#         """Update mesh deformation"""
#         deform = value / 100.0
#         self.deform_label.setText(f"{deform:.2f}")
#         self.apply_deformation(deform)
    
#     def apply_deformation(self, factor):
#         """Apply vertical stretching to mesh"""
#         points = self.original_points.copy()
        
#         # Scale in z-direction only (stretch vertically)
#         deformed = points.copy()
#         deformed[:, 2] = points[:, 2] * (1.0 + factor)
        
#         self.mesh.points = deformed
        
#         # Update scalars based on new z-height
#         self.mesh['height'] = deformed[:, 2]
        
#         # Dynamically update color range based on current min/max
#         scalar_range = [self.mesh['height'].min(), self.mesh['height'].max()]
#         self.actor.mapper.scalar_range = scalar_range
        
#         # Force update
#         self.plotter.update()
    
#     def closeEvent(self, event):
#         # Clean up plotter before closing
#         self.plotter.close()
#         self.plotter = None
#         event.accept()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MeshViewer()
#     window.show()
#     sys.exit(app.exec())













# import sys
# from PyQt6.QtWidgets import (
#     QApplication, QMainWindow, QWidget,
#     QVBoxLayout, QHBoxLayout, QPushButton,
#     QComboBox, QLabel, QFileDialog, QGroupBox
# )
# from pyvistaqt import QtInteractor
# import pyvista as pv
# import numpy as np

# import matplotlib
# matplotlib.use("QtAgg")



# class FEMViewer(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("FEM Results Viewer")
#         self.resize(1200, 700)
        
#         central_widget = QWidget()
#         self.setCentralWidget(central_widget)
#         main_layout = QHBoxLayout()
#         central_widget.setLayout(main_layout)
        
#         # Controls
#         controls = self.create_controls()
#         main_layout.addWidget(controls)
        
#         # 3D view
#         self.plotter = QtInteractor(central_widget)
#         main_layout.addWidget(self.plotter.interactor, stretch=3)
        
#         # State
#         self.mesh = None
#         self.actor = None  # Store mesh actor for updates
    
#     def create_controls(self):
#         """Create control panel"""
#         controls = QGroupBox("Analysis Controls")
#         layout = QVBoxLayout()
#         controls.setLayout(layout)
        
#         # Load button
#         load_button = QPushButton("Load Mesh (VTU)")
#         load_button.clicked.connect(self.load_mesh)
#         layout.addWidget(load_button)
        
#         # Field selection
#         layout.addWidget(QLabel("Display Field:"))
#         self.field_combo = QComboBox()
#         self.field_combo.currentTextChanged.connect(self.update_display)
#         layout.addWidget(self.field_combo)
        
#         # Info label
#         self.info_label = QLabel("No mesh loaded")
#         self.info_label.setWordWrap(True)
#         layout.addWidget(self.info_label)
        
#         # Reset view
#         reset_button = QPushButton("Reset Camera")
#         reset_button.clicked.connect(lambda: self.plotter.reset_camera())
#         layout.addWidget(reset_button)
        
#         layout.addStretch()
#         controls.setFixedWidth(250)
#         return controls
    
#     def load_mesh(self):
#         """Load mesh file using file dialog"""
#         filename, _ = QFileDialog.getOpenFileName(
#             self,
#             "Select Mesh File",
#             "",
#             "VTK Files (*.vtu *.vtk);;All Files (*.*)"
#         )
        
#         if not filename:
#             return
        
#         try:
#             self.mesh = pv.read(filename)
            
#             # Update field combo
#             self.field_combo.clear()
#             point_arrays = list(self.mesh.point_data.keys())
#             cell_arrays = list(self.mesh.cell_data.keys())
            
#             if point_arrays:
#                 self.field_combo.addItems(point_arrays)
            
#             # Update info
#             n_points = self.mesh.n_points
#             n_cells = self.mesh.n_cells
#             self.info_label.setText(
#                 f"Loaded: {filename.split('/')[-1]}\n"
#                 f"Points: {n_points}\n"
#                 f"Cells: {n_cells}\n"
#                 f"Fields: {len(point_arrays)}"
#             )
            
#             # Display first field
#             if point_arrays:
#                 self.update_display(point_arrays[0])
#             else:
#                 self.plotter.clear()
#                 self.plotter.add_mesh(self.mesh, color='lightgray')
#                 self.plotter.reset_camera()
            
#         except Exception as e:
#             self.info_label.setText(f"Error loading file:\n{str(e)}")
    
#     def update_display(self, field_name):
#         """Update displayed field"""
#         if self.mesh is None or not field_name:
#             return
        
#         self.plotter.clear()
        
#         # Check if field exists
#         if field_name not in self.mesh.point_data:
#             return
        
#         # Get field data
#         field_data = self.mesh.point_data[field_name]
        
#         # Handle vector fields (show magnitude)
#         if field_data.ndim > 1:
#             scalars = np.linalg.norm(field_data, axis=1)
#             scalar_name = f"{field_name} (magnitude)"
#             self.mesh[scalar_name] = scalars
#             display_field = scalar_name
#         else:
#             display_field = field_name
        
#         # Plot with scalar bar
#         self.actor = self.plotter.add_mesh(
#             self.mesh,
#             scalars=display_field,
#             cmap='coolwarm',
#             show_edges=False,
#             show_scalar_bar=True,
#             scalar_bar_args={'title': display_field}
#         )
        
#         self.plotter.reset_camera()
    
#     def closeEvent(self, event):
#         # Clean up plotter before closing
#         self.plotter.close()
#         self.plotter = None
#         event.accept()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = FEMViewer()
#     window.show()
#     sys.exit(app.exec())
















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