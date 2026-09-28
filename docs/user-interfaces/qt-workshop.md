---
title: Qt Workshop - Build an FEM Viewer
sidebar_position: 4
---

# Qt Workshop: Build an FEM Visualization Application

This optional workshop provides hands-on practice building a complete FEM (Finite Element Method) results viewer that combines PyQt6 and PyVista. Work through the exercises at your own pace to reinforce the concepts covered in class.

**Suggested approach**: Complete the three blocks progressively, taking breaks between sections. Each block builds on the previous one, creating increasingly sophisticated functionality.

:::tip Homework Exercise
This workshop is designed as additional practice to deepen your understanding of Qt and PyVista integration. You can complete it after class to solidify the concepts, or use it as a reference for your own projects.
:::

## Prerequisites

Ensure your environment is configured:

```bash
# Activate virtual environment
.venv\Scripts\activate

# Verify installations
python -c "import PyQt6; print('PyQt6:', PyQt6.QtCore.PYQT_VERSION_STR)"
python -c "import pyvista; print('PyVista:', pyvista.__version__)"
python -c "import pyvistaqt; print('PyVistaQt: OK')"
```

All packages should import without errors.

## Workshop Data

We'll use the sample FEM beam data from the course repository: `data/beam_stress.vtu`. This file contains a finite element mesh with complete FEM results including displacement (U), stress (S), von Mises stress (S_MISES), strain (E), and reaction forces (RF).

You can verify the available fields:

```python
import pyvista as pv

# Load the beam mesh with results (adjust path to your repository location)
mesh = pv.read('data/beam_stress.vtu')

# Check available fields
print("Available fields:", list(mesh.point_data.keys()))
# Output: ['U', 'S', 'S_MISES', 'E', 'RF', ...]
```

## Block 1: Application Structure and File Loading (45 min)

### Exercise 1.1: Create Main Window (10 min)

Create the basic application structure with menu bar and central widget.

**File**: `fem_viewer.py`

```python
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
```

**Test**: Run the application. You should see a window with File and View menus. Clicking menu items shows status messages.

**Checkpoint questions:**
1. What happens when you press Ctrl+O?
2. Why do we use `sys.exit(app.exec())`?
3. What's the purpose of the status bar?

### Exercise 1.2: Add PyVista Plotter (15 min)

Replace the placeholder label with a PyVista rendering widget.

**Add these imports:**
```python
from pyvistaqt import QtInteractor
import pyvista as pv
```

**Modify `__init__` method:**

```python
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
```

**Update `reset_camera` method:**
```python
def reset_camera(self):
    """Reset camera view"""
    if self.plotter:
        self.plotter.reset_camera()
        self.statusBar().showMessage("Camera reset", 2000)
```

**Add cleanup method to prevent VTK errors:**
```python
def closeEvent(self, event):
    """Clean up VTK resources before closing"""
    if self.plotter:
        self.plotter.close()
        self.plotter = None
    event.accept()
```

:::note Preventing VTK Errors
The `closeEvent` method ensures proper cleanup of VTK rendering resources before the window closes. Setting `plotter = None` helps the garbage collector release OpenGL contexts properly, preventing `wglMakeCurrent` errors on Windows.
:::

**Test**: You should see a blue sphere with edges. Try rotating it (left mouse drag) and zooming (scroll wheel). Press 'R' to reset the camera. Close the window to verify no errors appear.

**Checkpoint questions:**
1. What does `QtInteractor` provide?
2. Why do we use `self.plotter.interactor` instead of `self.plotter`?
3. What's the difference between `show_edges=True` and `show_edges=False`?

### Exercise 1.3: Implement File Loading (20 min)

Add functionality to load mesh files using a file dialog.

**Add import:**
```python
from PyQt6.QtWidgets import QFileDialog
```

**Implement `open_mesh` method:**

```python
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
```

**Remove the test sphere from `__init__`:**

Now that you have file loading, remove these lines from the `__init__` method:

```python
# Remove these lines:
sphere = pv.Sphere()
self.plotter.add_mesh(sphere, color='lightblue', show_edges=True)
self.plotter.reset_camera()
```

The plotter will start empty, and you'll load meshes using the file dialog.

**Test**: 
1. Run the application - the 3D view should be empty
2. Press Ctrl+O or use File → Open Mesh
3. Select `beam_stress.vtu` from the data folder (or any VTU file)
4. The mesh should display
5. Window title should show the filename

**Challenge**: What happens if you try to load a non-existent file? How could you improve error handling?

**Checkpoint questions:**
1. Why do we check `if not filename`?
2. What does `plotter.clear()` do?
3. Why is the try-except block important?

## Block 2: Interactive Controls (45 min)

### Exercise 2.1: Create Control Panel (15 min)

Add a control panel on the left side with field selection and display options.

**Add imports:**
```python
from PyQt6.QtWidgets import (
    QGroupBox, QComboBox, QCheckBox,
    QPushButton
)
```

**Modify `__init__` to add control panel:**

Replace the section after creating `main_layout` with:

```python
# Create control panel
controls = self.create_controls()
main_layout.addWidget(controls)

# PyVista plotter (move existing plotter code here)
self.plotter = QtInteractor(central_widget)
main_layout.addWidget(self.plotter.interactor, stretch=3)  # Give more space to 3D view

# Create menus and status bar
self.create_menus()
self.statusBar().showMessage("Ready")
```

**Implement `create_controls` method:**

```python
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
```

**Test**: You should see a control panel on the left with dropdown and checkboxes. They won't do anything yet until we implement the handler methods.

### Exercise 2.2: Populate Field Selector (15 min)

Update the `open_mesh` method to detect available fields and populate the combo box.

**Replace the `open_mesh` method's mesh display section:**

```python
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
```

**Implement helper methods:**

```python
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
```

**Test**: Load a mesh file. The field combo box should populate with available fields, and the first field will be automatically selected and displayed. 

:::note Controls Not Yet Interactive
At this stage, manually selecting different fields or toggling checkboxes won't update the display because the signal connections haven't been added yet. That comes in Exercise 2.3!
:::

### Exercise 2.3: Connect Display Options (15 min)

Implement handlers for the checkboxes to update display options interactively.

**Implement the handler methods:**

```python
def update_field_display(self, field_name):
    """Update display when field selection changes"""
    self.display_mesh()

def update_display_options(self):
    """Update display when checkboxes change"""
    self.display_mesh()
```

**Connect all the signals:**

```python
# Add these lines in create_controls method after creating the widgets:
self.field_combo.currentTextChanged.connect(self.update_field_display)
self.edges_checkbox.stateChanged.connect(self.update_display_options)
self.scalar_bar_checkbox.stateChanged.connect(self.update_display_options)
```

**Test**: 
1. Load a mesh
2. Toggle "Show Edges" - edges should appear/disappear
3. Toggle "Show Scalar Bar" - color bar should show/hide
4. Switch between fields - display should update

**Challenge**: The current implementation redraws the entire mesh for every change. Can you optimize it to only update what changed?

**Checkpoint questions:**
1. Why do we use `blockSignals(True)` when populating the combo box?
2. What's the purpose of `scalar_bar_args={'title': field_name}`?
3. How would you handle vector fields (e.g., displacement with 3 components)?

## Block 3: Advanced Features (45 min)

### Exercise 3.1: Handle Vector Fields (15 min)

Modify the display logic to handle vector fields by showing their magnitude.

**Update `display_mesh` method:**

```python
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
```

**Test**: If your mesh has vector fields (like displacement), selecting them should display their magnitude automatically.

### Exercise 3.2: Add Deformation Visualization (20 min)

Add ability to visualize deformed shapes with a scale factor.

**Add import for QSlider:**

```python
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QFileDialog,
    QGroupBox, QComboBox, QCheckBox,
    QPushButton, QSlider  # Add QSlider
)
```

**Add to control panel (in `create_controls`):**

```python
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
```

**Add instance variable to store original mesh:**

```python
def __init__(self):
    # ... existing code ...
    self.mesh = None
    self.original_mesh = None  # Store undeformed mesh
```

**Implement deformation logic:**

```python
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
```

**Update `open_mesh` to reset deformation state:**

```python
# In open_mesh, after self.mesh = pv.read(filename):
self.original_mesh = None  # Reset deformation state
self.deform_checkbox.setChecked(False)
```

**Test**:
1. Load a mesh with displacement field
2. Check "Show Deformed"
3. Move the scale slider - mesh should deform
4. Uncheck "Show Deformed" - should return to original
5. Change fields - deformation should persist

**Challenge**: Add ability to show both undeformed (wireframe) and deformed (solid) meshes simultaneously.

### Exercise 3.3: Add Screenshot Export (10 min)

Implement screenshot functionality.

**Add to File menu:**

```python
# In create_menus, before file_menu.addSeparator():
export_action = QAction("&Export Screenshot...", self)
export_action.setShortcut("Ctrl+S")
export_action.triggered.connect(self.export_screenshot)
file_menu.addAction(export_action)
```

**Implement export method:**

```python
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
```

**Test**: Load a mesh, press Ctrl+S, choose location, verify image is saved.

## Final Complete Application

You now have a functional FEM viewer with:
- File loading with dialog
- Automatic field detection
- Interactive field selection
- Display option controls
- Vector field handling (magnitude)
- Deformation visualization with scaling
- Screenshot export
- Keyboard shortcuts
- Status messages

## Extension Challenges

If you finish early or want to continue developing:

**Challenge 1: Color Map Selection**
Add a combo box to choose different color maps (viridis, plasma, jet, coolwarm).

**Challenge 2: Clipping Plane**
Add controls to clip the mesh with a plane (see PyVista `clip()` method).

**Challenge 3: Multiple Views**
Split the display into two plotters showing different fields side-by-side.

**Challenge 4: Data Export**
Add functionality to export processed data (e.g., max stress, displacement statistics) to CSV.

**Challenge 5: Animation**
Add a "Play" button next to the deformation slider that animates the mesh with harmonic oscillation. Keep the slider as the maximum scale, but multiply it by `sin(time * frequency)` during animation to create vibration. Use `QTimer` to update at regular intervals (e.g., 30 FPS) and update the deformation accordingly. The animation should oscillate between undeformed and the maximum slider value.

**Challenge 6: Measurement Tool**
Add ability to pick points on the mesh and display their coordinates and field values.

## Debugging Tips

**Nothing displays after loading:**
- Check if `plotter.reset_camera()` is called
- Verify mesh isn't empty: `print(mesh.n_points)`
- Try adding a simple sphere to verify plotter works

**Slow performance:**
- Disable edges for large meshes
- Check mesh size: `print(f"Points: {mesh.n_points}, Cells: {mesh.n_cells}")`
- Consider downsampling very large meshes

**Deformation doesn't work:**
- Print available fields: `print(mesh.point_data.keys())`
- Check displacement field shape: `print(mesh['U'].shape)`
- Verify scale factor: `print(scale)`

**UI doesn't update:**
- Ensure signals are connected: `slider.valueChanged.connect(...)`
- Check if `blockSignals` is preventing updates
- Call `plotter.update()` if mesh properties changed

## Summary

You've built a professional-quality FEM visualization application combining:
- **PyQt6** for application structure, menus, and controls
- **PyVista** for 3D rendering and mesh handling
- **Signal-slot mechanism** for interactive updates
- **File dialogs** for user-friendly file operations
- **Layout management** for responsive UI

This pattern extends to any engineering visualization application: load data, provide controls, visualize interactively, export results.

**Key takeaways:**
1. Separate data management from visualization
2. Use layouts, not manual positioning
3. Provide immediate feedback through status bar
4. Handle errors gracefully with try-except
5. Store state in instance variables
6. Use `plotter.update()` for small changes, `display_mesh()` for complete refresh

## Next Steps

- Explore [PyVista documentation](https://docs.pyvista.org/) for advanced visualization techniques
- Study [Qt documentation](https://doc.qt.io/) for more UI components
- Build specialized tools for your specific engineering domain
- Share your applications with colleagues to improve their workflows!
