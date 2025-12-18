---
title: Integrating PyVista with Qt
sidebar_position: 3
---

# Integrating PyVista with Qt

This guide shows you how to embed PyVista 3D visualizations into PyQt6 applications, creating complete engineering analysis tools with custom controls and interactive 3D graphics.

## Why Embed PyVista in Qt?

Standalone PyVista windows are excellent for quick visualization, but production tools need:

- **Custom controls**: Sliders, buttons, and input fields to control visualization parameters
- **Data management**: Load, process, and save data through file dialogs and forms
- **Multiple views**: Split screens, synchronized cameras, or different analysis modes
- **Integration**: Combine 3D visualization with tables, plots, and text output
- **Professional appearance**: Menus, toolbars, and consistent layout

Qt provides the application framework, while PyVista handles 3D rendering. Together, they create powerful specialized tools.

## Installation

Ensure you have both frameworks installed:

```bash
pip install PyQt6 pyvista vtk
```

PyVista uses VTK (Visualization Toolkit) for rendering, which includes Qt integration support.

## Basic Embedding: QtInteractor

PyVista provides `QtInteractor`, a Qt widget that embeds a VTK rendering window:

```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from pyvistaqt import QtInteractor
import pyvista as pv

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyVista in Qt")
        self.resize(800, 600)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Create PyVista Qt widget
        self.plotter = QtInteractor(central_widget)
        layout.addWidget(self.plotter.interactor)
        
        # Add some geometry
        mesh = pv.Sphere()
        self.plotter.add_mesh(mesh, color='lightblue', show_edges=True)
        
        # Reset camera to show the entire scene
        self.plotter.reset_camera()
    
    def closeEvent(self, event):
        # Clean up plotter before closing to prevent VTK errors
        self.plotter.close()
        self.plotter = None
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
```

**Key components:**

- `QtInteractor`: PyVista's Qt-compatible plotter
- `plotter.interactor`: The actual Qt widget to add to layouts
- All standard PyVista methods work: `add_mesh()`, `add_points()`, `show_edges`, etc.
- Camera controls work automatically (rotate with left drag, zoom with scroll)
- `closeEvent`: Override to properly clean up VTK resources before closing

:::note Cleanup Pattern
The `closeEvent` override with `plotter.close()` and `plotter = None` is necessary to prevent VTK cleanup errors during application shutdown. Without this, you may see harmless but annoying AttributeError messages in the console when closing the window. This pattern should be used in all PyVista + Qt applications.
:::

:::warning Import Error
If you get `ModuleNotFoundError: No module named 'pyvistaqt'`, install it explicitly:
```bash
pip install pyvistaqt
```
While PyVista includes Qt support, the `pyvistaqt` package must be installed separately.
:::

## Adding Interactive Controls

The power of Qt integration is combining 3D visualization with interactive controls:

```python
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QSlider,
    QLabel, QPushButton, QGroupBox
)
from PyQt6.QtCore import Qt
from pyvistaqt import QtInteractor
import pyvista as pv
import numpy as np

class MeshViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interactive Mesh Viewer")
        self.resize(1000, 600)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout: horizontal split
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Left side: Controls
        controls_widget = self.create_controls()
        main_layout.addWidget(controls_widget)
        
        # Right side: 3D view
        self.plotter = QtInteractor(central_widget)
        main_layout.addWidget(self.plotter.interactor, stretch=3)
        
        # Create initial mesh
        self.create_mesh()
    
    def create_controls(self):
        """Create control panel with sliders and buttons"""
        controls = QGroupBox("Controls")
        layout = QVBoxLayout()
        controls.setLayout(layout)
        
        # Resolution slider
        layout.addWidget(QLabel("Sphere Resolution:"))
        self.resolution_slider = QSlider(Qt.Orientation.Horizontal)
        self.resolution_slider.setRange(5, 100)
        self.resolution_slider.setValue(30)
        self.resolution_slider.valueChanged.connect(self.update_mesh)
        layout.addWidget(self.resolution_slider)
        
        self.resolution_label = QLabel("30")
        layout.addWidget(self.resolution_label)
        
        # Deformation slider
        layout.addWidget(QLabel("Deformation:"))
        self.deform_slider = QSlider(Qt.Orientation.Horizontal)
        self.deform_slider.setRange(0, 100)
        self.deform_slider.setValue(0)
        self.deform_slider.valueChanged.connect(self.update_deformation)
        layout.addWidget(self.deform_slider)
        
        self.deform_label = QLabel("0.00")
        layout.addWidget(self.deform_label)
        
        # Reset button
        reset_button = QPushButton("Reset View")
        reset_button.clicked.connect(lambda: self.plotter.reset_camera())
        layout.addWidget(reset_button)
        
        # Add stretch to push controls to top
        layout.addStretch()
        
        controls.setFixedWidth(250)
        return controls
    
    def create_mesh(self):
        """Create sphere mesh with scalar field"""
        resolution = self.resolution_slider.value()
        self.mesh = pv.Sphere(radius=1.0, theta_resolution=resolution, 
                             phi_resolution=resolution)
        
        # Add scalar field based on z-height (creates colorful bands)
        points = self.mesh.points
        self.mesh['height'] = points[:, 2]  # Z-coordinate
        
        # Store original points for deformation
        self.original_points = points.copy()
        
        # Plot mesh and store actor reference for dynamic updates
        self.plotter.clear()
        self.actor = self.plotter.add_mesh(
            self.mesh,
            scalars='height',
            cmap='coolwarm',
            show_edges=False,
            show_scalar_bar=True
        )
        self.plotter.reset_camera()
    
    def update_mesh(self, value):
        """Update mesh resolution"""
        self.resolution_label.setText(str(value))
        self.create_mesh()
        
        # Reapply current deformation
        deform = self.deform_slider.value() / 100.0
        if deform > 0:
            self.apply_deformation(deform)
    
    def update_deformation(self, value):
        """Update mesh deformation"""
        deform = value / 100.0
        self.deform_label.setText(f"{deform:.2f}")
        self.apply_deformation(deform)
    
    def apply_deformation(self, factor):
        """Apply vertical stretching to mesh"""
        points = self.original_points.copy()
        
        # Scale in z-direction only (stretch vertically)
        deformed = points.copy()
        deformed[:, 2] = points[:, 2] * (1.0 + factor)
        
        self.mesh.points = deformed
        
        # Update scalars based on new z-height
        self.mesh['height'] = deformed[:, 2]
        
        # Dynamically update color range based on current min/max
        scalar_range = [self.mesh['height'].min(), self.mesh['height'].max()]
        self.actor.mapper.scalar_range = scalar_range
        
        # Force update
        self.plotter.update()
    
    def closeEvent(self, event):
        # Clean up plotter before closing
        self.plotter.close()
        self.plotter = None
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MeshViewer()
    window.show()
    sys.exit(app.exec())
```

**Key patterns demonstrated:**

1. **Layout management**: `QHBoxLayout` splits controls and 3D view
2. **Signal-slot connections**: Sliders trigger mesh updates
3. **Dynamic updates**: `plotter.update()` refreshes the display without recreating the window
4. **State management**: Store original mesh data for interactive modifications
5. **Responsive controls**: Immediate feedback as sliders move

## Loading and Displaying FEM Results

Real engineering applications load mesh data and simulation results:

```python
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
```

**Engineering application features:**

- File dialog for mesh loading
- Automatic detection of available fields
- Dropdown to switch between result fields
- Vector field handling (display magnitude)
- Error handling for file loading
- Information display (mesh statistics)

## Multiple Views and Comparison

Compare different fields or configurations side-by-side:

```python
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
```

:::tip The copy_mesh Parameter
When adding the same mesh object to multiple plotters or multiple times with different scalars, always use `copy_mesh=True`. This prevents rendering state conflicts where one view's active scalars affect another view's display. See [Exercise 2 of the Mesh Visualization Workshop](../visualization/mesh-visualization-workshop#exercise-2-comparing-stress-and-displacement-fields) for detailed explanation.
:::

## Exporting and Screenshots

Add export functionality to your application:

```python
def export_screenshot(self):
    """Save current view as image"""
    filename, _ = QFileDialog.getSaveFileName(
        self,
        "Save Screenshot",
        "screenshot.png",
        "PNG Images (*.png);;JPEG Images (*.jpg)"
    )
    
    if filename:
        self.plotter.screenshot(filename, transparent_background=False)
        self.statusBar().showMessage(f"Saved: {filename}", 3000)

def export_mesh(self):
    """Save current mesh with results"""
    if self.mesh is None:
        return
    
    filename, _ = QFileDialog.getSaveFileName(
        self,
        "Save Mesh",
        "output.vtu",
        "VTK XML (*.vtu);;Legacy VTK (*.vtk)"
    )
    
    if filename:
        self.mesh.save(filename)
        self.statusBar().showMessage(f"Saved: {filename}", 3000)
```

Add these methods to your `QMainWindow` class and connect them to menu actions or buttons.

## Best Practices for Qt + PyVista Applications

**Performance:**
- For large meshes (>1M cells), consider using `opacity=0.5` or `show_edges=False` to improve frame rate
- Update display only when necessary (not on every slider movement for very dense meshes)
- Use `plotter.update()` instead of `plotter.clear()` + `plotter.add_mesh()` when only scalar values change

**Memory Management:**
- Clear plotters when loading new data: `plotter.clear()`
- Store only necessary mesh copies in instance variables
- Use `copy_mesh=True` when adding the same mesh multiple times

**User Experience:**
- Always provide "Reset Camera" button
- Show progress indicators for loading large files
- Display mesh statistics (number of points/cells)
- Provide keyboard shortcuts for common actions
- Use status bar for temporary messages

**Code Organization:**
- Separate data loading from display logic
- Create reusable components (e.g., `MeshControlPanel` class)
- Use signals for communication between components
- Keep plotter creation and configuration in `__init__`

## Common Issues and Solutions

**Issue**: Plotter appears black or doesn't render
**Solution**: Ensure you call `plotter.reset_camera()` after adding meshes

**Issue**: Updates don't appear in the view
**Solution**: Call `plotter.update()` after modifying mesh properties

**Issue**: Application crashes when closing window
**Solution**: Properly clear plotters in `closeEvent()`:
```python
def closeEvent(self, event):
    self.plotter.close()
    event.accept()
```

**Issue**: Colors wrong when using same mesh in multiple views
**Solution**: Use `copy_mesh=True` parameter in `add_mesh()`

**Issue**: Slow performance with large meshes
**Solution**: Reduce visual complexity (disable edges, reduce opacity) or implement level-of-detail

## Next Steps

You now can integrate PyVista into professional Qt applications. Continue to:

- **[Qt Workshop](qt-workshop)** - Build a complete FEM visualization tool
- **[Mesh Visualization Workshop](../visualization/mesh-visualization-workshop)** - PyVista techniques applicable to Qt integration


## Practice Challenge

**Build a Deformation Animator:**

Create an application that:
1. Loads an undeformed mesh and displacement field
2. Displays the mesh with a slider controlling deformation scale
3. Has a "Play" button that animates the deformation
4. Uses `QTimer` to update the display periodically
5. Provides controls for animation speed

**Hints:**
- Store original mesh positions
- Deformed position = original + scale × displacement vector
- Use `QTimer.timeout` signal to advance animation frame
- Update mesh points: `mesh.points = deformed_points`
- Call `plotter.update()` to refresh display

This combines Qt timers, PyVista mesh manipulation, and interactive controls in a practical engineering visualization scenario.
