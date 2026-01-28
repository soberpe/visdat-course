---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  section {
    font-size: 26px;
    padding: 40px 50px;
  }
  h1 {
    font-size: 46px;
    color: #2c3e50;
    margin-bottom: 20px;
  }
  h2 {
    font-size: 36px;
    color: #34495e;
    margin-bottom: 15px;
  }
  code {
    font-size: 20px;
  }
  pre {
    margin: 10px 0;
  }
---

# User Interface Development
## For Engineering Applications

**Visualization and Data Analysis Course**
Building Professional Tools with Qt and Python

---

## Today's Agenda

**Block 1 (45 min)**: UI Overview
- Why user interfaces matter in engineering
- Historical evolution and modern landscape
- Desktop vs Web: choosing the right approach
- Why Qt dominates engineering software

**Block 2 (45 min)**: PyQt6 Basics
- Installation and minimal application
- Layouts, widgets, and signals/slots
- QMainWindow structure and event loop

**Block 3 (45 min)**: PyVista Integration
- Embedding 3D visualization in Qt
- Workshop reference for hands-on practice

---

# Block 1: UI Fundamentals

---

## Why User Interfaces Matter

User interfaces bridge computational power and human understanding.

**Impact on engineering:**
- **Accessibility**: Domain experts can use tools without programming
- **Productivity**: Fast path from data to insights
- **Error Prevention**: Immediate feedback prevents mistakes
- **Collaboration**: Teams share and discuss visualizations
- **Decision Making**: Complex data becomes understandable

> A well-designed interface transforms specialized software into team tools.

---

## The Evolution of User Interfaces

**1960s-1970s: Command Line Era**
- Batch processing on mainframes
- Printed output only
- Engineers submit jobs and wait

**1980s: Desktop Revolution**
- Xerox Alto, Macintosh, Windows
- First CAD systems (AutoCAD, CATIA)
- Direct interaction with visual data

**1990s-2000s: Native Applications**
- MFC, Win32, .NET Windows Forms
- MATLAB, ParaView
- Platform-specific, maximum performance

---

## The Evolution (continued)

**2010s: The Web Era**
- WebGL, Three.js for browser-based 3D
- Cloud computing + web interfaces
- Universal access, no installation
- Jupyter notebooks: code + visualization

**Today: Hybrid Approaches**
- Desktop for performance (millions of elements)
- Web for collaboration and review
- Python frameworks bridge both worlds
- Many products use both!

---

## Desktop vs Web: Architecture

**Desktop Applications:**
- Native code with direct hardware access
- Maximum 3D rendering performance
- OpenGL/Vulkan integration
- Works offline
- Platform-specific compilation

**Web Applications:**
- **Frontend**: HTML/CSS/JavaScript (browser)
- **Backend**: Python/Node.js/Go (server)
- **API**: HTTP/WebSocket connection
- Universal access, automatic updates
- Browser sandbox limits performance

---

## When to Choose Desktop

**Choose Desktop (Qt/Native) when:**
- Working with very large datasets (millions of cells)
- Requiring maximum 3D rendering performance
- Needing offline capability
- Integrating with system resources (CAD formats, GPU)
- Building tools for daily use by individual engineers

**Examples:**
- ParaView (FEM postprocessing)
- Autodesk Maya (3D modeling)
- MATLAB (numerical computing)
- All major CAD software

---

## When to Choose Web

**Choose Web when:**
- Enabling team collaboration and sharing
- Supporting occasional use by many users
- Simplifying deployment across organizations
- Integrating with cloud computing
- Building dashboards and monitoring

**Examples:**
- Plotly Dash (data science dashboards)
- Streamlit (ML model interfaces)
- Jupyter notebooks (collaborative analysis)
- Web-based viewers for results review

**Hybrid**: Desktop for intensive work, web for collaboration!

---

# Block 2: PyQt6 Basics

---

## Why Qt for Engineering?

Qt is the de facto standard for professional desktop applications.

**Powers:**
- **Scientific**: ParaView, Mathematica, LabPlot, QtiPlot
- **Engineering**: Autodesk Maya, Dassault Systèmes tools
- **Media**: VLC, Audacity, OBS Studio

**Why Qt dominates:**
1. Native performance with direct hardware access
2. Over 25 years of production use
3. Comprehensive (UI, networking, files, SQL, XML...)
4. True cross-platform (Windows, macOS, Linux)
5. Professional support and licensing available
6. Seamless OpenGL/Vulkan for 3D graphics

---

## Brief Qt History

**Origins**: Created 1991 by Norwegian programmers Haavard Nord and Eirik Chambe-Eng for ultrasound imaging project.

**Key Milestones:**
- 1995: First public release (Qt 0.90)
- 2000: Released under GPL → open-source adoption
- 2008: Acquired by Nokia (Qt in mobile phones)
- 2011: Sold to Digia (later Qt Company)
- 2020: Qt 6 with modern C++ and better Python support

**Philosophy**: "Write once, compile anywhere" with native look and feel on each platform.

---

## Python + Qt = Productivity

**PyQt6** and **PySide6**: Python bindings for Qt
- PyQt6: GPL/Commercial licensing
- PySide6: Qt's official bindings, LGPL
- Nearly identical APIs, interchangeable

**Why perfect for engineering:**
- Python ecosystem: NumPy, Pandas, Matplotlib, **PyVista**
- Rapid development: hours instead of weeks
- Scientific computing focus
- Industry relevance: internal tools at engineering companies
- Learning path: concepts transfer to C++ Qt if needed

**PyVista Connection:**
PyVista uses Qt for interactive windows - you're already using it!

---

## Installation

Install PyQt6 in your virtual environment:

```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/macOS

# Install PyQt6
pip install PyQt6

# For 3D visualization integration
pip install pyvista pyvistaqt
```

**Best practice**: Always use virtual environments to isolate dependencies and prevent version conflicts.

---

## Minimal Application

Every PyQt6 application follows this pattern:

```python
from PyQt6.QtWidgets import QApplication, QWidget

# 1. Create application object
app = QApplication([])

# 2. Create main window
window = QWidget()
window.setWindowTitle("My First Qt App")
window.resize(400, 300)

# 3. Show window
window.show()

# 4. Start event loop
app.exec()
```

Run it: `python minimal_app.py`

---

## Layouts: Responsive Design

Qt uses layouts instead of manual positioning:

```python
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QLabel, QLineEdit
)

app = QApplication([])
window = QWidget()

# Create vertical layout
layout = QVBoxLayout()
layout.addWidget(QLabel("Enter name:"))
layout.addWidget(QLineEdit())
layout.addWidget(QPushButton("Submit"))

window.setLayout(layout)
window.show()
app.exec()
```

**Layout types**: VBox (vertical), HBox (horizontal), Grid, Form

Automatically handles resizing, fonts, platform differences!

---

## Signals and Slots

Qt's distinctive feature: loose coupling between components.

**Concept:**
- **Signal**: Event notification (click, value changed)
- **Slot**: Function that responds to signal
- **Connection**: Link them at runtime

```python
# Connect button click to function
button = QPushButton("Click Me")
button.clicked.connect(lambda: print("Clicked!"))

# Can connect multiple slots
button.clicked.connect(update_display)
button.clicked.connect(save_state)

# Can disconnect later
button.clicked.disconnect(save_state)
```

**Benefits**: Decoupled, flexible, thread-safe

---

## QMainWindow Structure

`QMainWindow` provides structure for complex applications:

```python
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtGui import QAction

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Application")
        
        # Central widget (required)
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        central.setLayout(layout)
        
        # Menu bar
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        exit_action = QAction("E&xit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
```

---

## Parent-Child Hierarchy

Qt uses parent-child trees for automatic memory management:

```python
window = QMainWindow()  # No parent

# Button's parent is window
button = QPushButton("Click", parent=window)

# When window is deleted, button is automatically deleted
```

**Key principle**: Parent deletion → all children deleted
- Prevents memory leaks
- Simplifies resource management
- Mirrors visual hierarchy

---

## The Event Loop

Qt applications are **event-driven**, not procedural:

```python
app = QApplication([])
window = QMainWindow()
window.show()

# Event loop starts here - program waits
app.exec()

# Only executes after window closes
print("Application closed")
```

**The loop:**
1. Wait for events (clicks, keys, timers, signals)
2. Dispatch to handlers
3. Update UI
4. Repeat until exit

**Implication**: Long computations block UI → use `QThread`!

---

# Block 3: PyVista Integration

---

## Why Embed PyVista in Qt?

Standalone PyVista is great for quick visualization, but production tools need:

- **Custom controls**: Sliders, buttons for parameters
- **Data management**: File dialogs, forms
- **Multiple views**: Split screens, synchronized cameras
- **Integration**: Combine 3D with tables, plots
- **Professional UI**: Menus, toolbars, consistent layout

**Qt provides the framework, PyVista handles 3D.**

---

## Basic Embedding: QtInteractor

```python
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from pyvistaqt import QtInteractor
import pyvista as pv
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyVista in Qt")
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        central.setLayout(layout)
        
        # Create PyVista Qt widget
        self.plotter = QtInteractor(central)
        layout.addWidget(self.plotter.interactor)
        
        # Add geometry
        mesh = pv.Sphere()
        self.plotter.add_mesh(mesh, color='lightblue')
        self.plotter.reset_camera()
```

---

## Cleanup Pattern

Always clean up VTK resources properly:

```python
def closeEvent(self, event):
    """Override to prevent VTK errors on close"""
    if self.plotter:
        self.plotter.close()
        self.plotter = None
    event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
```

**Without this**: Harmless but annoying error messages when closing.
**With this**: Clean shutdown, no errors.

---

## Adding Interactive Controls

Combine PyVista with Qt widgets for complete control:

```python
# Horizontal layout: controls | 3D view
main_layout = QHBoxLayout()

# Control panel
controls = QGroupBox("Controls")
controls_layout = QVBoxLayout()
controls.setLayout(controls_layout)

# Resolution slider
res_slider = QSlider(Qt.Orientation.Horizontal)
res_slider.setRange(5, 100)
res_slider.valueChanged.connect(self.update_mesh)
controls_layout.addWidget(res_slider)

main_layout.addWidget(controls)

# PyVista 3D view
self.plotter = QtInteractor(central)
main_layout.addWidget(self.plotter.interactor, stretch=3)
```

**Pattern**: Controls on left/top, 3D view takes remaining space.

---

## Dynamic Updates

Update mesh when slider changes:

```python
def update_mesh(self, value):
    """Called when slider moves"""
    # Create new mesh with resolution
    self.mesh = pv.Sphere(
        theta_resolution=value,
        phi_resolution=value
    )
    
    # Update display
    self.plotter.clear()
    self.plotter.add_mesh(
        self.mesh,
        color='lightblue',
        show_edges=True
    )
    self.plotter.reset_camera()
```

**Result**: Drag slider → mesh updates immediately!

---

## Efficient Geometry Updates

For animations or frequent updates, modify points in-place:

```python
def animate_deformation(self):
    """Update mesh geometry without full redraw"""
    # Update mesh points directly
    self.mesh.points = new_points
    
    # Efficient render (no clear/add_mesh)
    self.plotter.render()
```

**Use `display_mesh()` for**: Field changes, major updates
**Use `plotter.render()` for**: Geometry-only updates, animations

This prevents scalar bar flickering!

---

## Complete Application Example

**Workshop available online with step-by-step guide:**

Navigate to: **Course Website → User Interfaces → Qt Workshop**

**Build a professional FEM viewer:**
- File loading with QFileDialog
- Field selection from mesh data
- Deformation visualization with sliders
- Animation using QTimer
- Screenshot export

**Three progressive blocks:**
1. Application skeleton and file I/O
2. Interactive controls with signals/slots
3. Advanced features (deformation, animation)

Work through as homework to practice today's concepts.

---

## Resources

**Documentation:**
- [Qt Documentation](https://doc.qt.io/) - C++ reference (concepts transfer)
- [PyQt6 Docs](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [PySide6 Docs](https://doc.qt.io/qtforpython/) - Qt's official Python bindings
- [PyVista](https://docs.pyvista.org/) - 3D visualization

**Course Materials:**
- [User Interface Overview](https://username.github.io/visdat-course/user-interfaces/ui-overview)
- [PyQt6 Basics](https://username.github.io/visdat-course/user-interfaces/pyqt-basics)
- [PyVista-Qt Integration](https://username.github.io/visdat-course/user-interfaces/pyvista-qt-integration)
- [Workshop Guide](https://username.github.io/visdat-course/user-interfaces/qt-workshop)

---

## Summary and Next Steps

**Topics covered today:**
✅ Why user interfaces matter in engineering
✅ Historical evolution and modern landscape  
✅ Desktop vs Web architectures
✅ Qt fundamentals (signals, slots, widgets, layouts)
✅ PyQt6 + PyVista integration

**Workshop materials:**
Access the complete hands-on Qt workshop at:
**Course Website → User Interfaces → Qt Workshop**

**Questions?**
