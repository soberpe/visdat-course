---
title: Getting Started with PyQt6
sidebar_position: 2
---

# Getting Started with PyQt6

This guide walks you through installing PyQt6 and creating your first application, progressing from minimal examples to interactive interfaces.

## Installation

PyQt6 is available through pip and should be added to your project's virtual environment:

```bash
# Activate your virtual environment first
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/macOS

# Install PyQt6
pip install PyQt6
```

For 3D visualization integration, also install:

```bash
pip install pyvista vtk
```

:::tip Virtual Environment Best Practice
Always use a virtual environment for your projects. PyQt6 is a large package with native dependencies, and keeping it isolated prevents version conflicts. See the [Python Overview](../python/python-overview#virtual-environments) for details on creating and managing environments.
:::

## Minimal Application Structure

Every PyQt6 application follows the same basic pattern:

```python
from PyQt6.QtWidgets import QApplication, QWidget

# 1. Create the application object
app = QApplication([])

# 2. Create the main window
window = QWidget()
window.setWindowTitle("My First Qt App")
window.resize(400, 300)

# 3. Show the window
window.show()

# 4. Start the event loop
app.exec()
```

**Understanding each component:**

1. **QApplication**: The application object manages the entire program. There must be exactly one per program, created before any widgets.

2. **QWidget**: The base class for all UI objects. Here we use it as a simple top-level window. For more complex applications, you'll typically use `QMainWindow` (which inherits from `QWidget`) to get built-in support for menus, toolbars, and status bars.

3. **show()**: Windows are hidden by default. Calling `show()` makes them visible.

4. **exec()**: Starts the event loop, which processes user input and updates the UI. The program waits here until the user closes the window.

Save this as `minimal_app.py` and run it:

```bash
python minimal_app.py
```

You should see an empty window. Closing it terminates the application.

## Adding a Single Widget

Let's add a button that does something when clicked:

```python
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton

app = QApplication([])
window = QWidget()
window.setWindowTitle("Button Example")
window.resize(400, 300)

# Create button with text and parent
button = QPushButton("Click Me", parent=window)
button.move(150, 120)  # Position manually (not recommended, but works for one widget)

# Connect signal to slot
button.clicked.connect(lambda: print("Button clicked!"))

window.show()
app.exec()
```

**Key concepts introduced:**

- **Parent-child relationship**: The button's parent is the window, so it's automatically deleted when the window closes
- **Signal-slot connection**: `clicked` is a signal; we connect it to a lambda function that prints
- **Manual positioning**: `move()` places the widget at specific coordinates (we'll replace this with layouts soon)

:::warning Manual Positioning
Using `move()` and `resize()` creates brittle interfaces that don't adapt to different screen sizes or font settings. This is acceptable for single-widget examples, but real applications must use layouts.
:::

## Multiple Widgets with Layouts

Layouts automatically arrange widgets and handle resizing:

```python
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QLabel, QLineEdit
)

app = QApplication([])
window = QWidget()
window.setWindowTitle("Layout Example")

# Create layout
layout = QVBoxLayout()

# Create widgets
label = QLabel("Enter your name:")
text_input = QLineEdit()
button = QPushButton("Greet")
result_label = QLabel("")

# Add widgets to layout
layout.addWidget(label)
layout.addWidget(text_input)
layout.addWidget(button)
layout.addWidget(result_label)

# Connect button to action
def on_button_clicked():
    name = text_input.text()
    result_label.setText(f"Hello, {name}!")

button.clicked.connect(on_button_clicked)

# Apply layout to window
window.setLayout(layout)

window.show()
app.exec()
```

**What's happening:**

1. `QVBoxLayout` stacks widgets vertically
2. `addWidget()` adds each widget in order
3. The button's click signal connects to a function that reads input and updates a label
4. `setLayout()` applies the layout to the window

Try resizing the window - widgets automatically adjust!

## Understanding the Event Loop

The event loop is Qt's heart. When you call `app.exec()`, Qt enters a loop that:

1. Waits for events (mouse clicks, key presses, timer ticks)
2. Routes events to appropriate widgets
3. Updates the display
4. Repeats until the application exits

**Implication**: If you run a long computation in the main thread, the UI freezes:

```python
import time

# ❌ This freezes the UI for 5 seconds
def slow_operation():
    time.sleep(5)  # Simulating computation
    print("Done!")

button.clicked.connect(slow_operation)
```

During those 5 seconds, the window won't respond to any input - it appears frozen. The solution is to run heavy computations in background threads, which we'll cover in the [PyVista integration](pyvista-qt-integration) section where it's practically necessary.

## Using QMainWindow for Complex Applications

`QMainWindow` (which inherits from `QWidget`) provides structure for applications with menus, toolbars, and status bars. We create our own class inheriting from `QMainWindow` to customize its behavior and add our application logic:

```python
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QPushButton, QLabel
)
from PyQt6.QtGui import QAction

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()  # Initialize the QMainWindow base class
        self.setWindowTitle("QMainWindow Example")
        self.resize(600, 400)
        
        # QMainWindow uses a central widget for its main content area
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout for central widget
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Add content
        self.label = QLabel("Status: Ready")
        layout.addWidget(self.label)
        
        button = QPushButton("Do Something")
        button.clicked.connect(self.on_button_clicked)
        layout.addWidget(button)
        
        # Create menu bar
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        
        # Add menu actions
        open_action = QAction("&Open", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        exit_action = QAction("E&xit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Create status bar
        self.statusBar().showMessage("Application started")
    
    def on_button_clicked(self):
        self.label.setText("Status: Button clicked")
        self.statusBar().showMessage("Action performed", 3000)  # 3 second timeout
    
    def open_file(self):
        self.label.setText("Status: Open file dialog (not implemented)")

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
```

**QMainWindow structure:**

- **Central widget**: Main content area (required)
- **Menu bar**: `menuBar()` returns the menu bar; add menus with `addMenu()`
- **Status bar**: `statusBar()` returns the status bar; use `showMessage()` for temporary messages
- **Toolbars**: Can add with `addToolBar()` (not shown here)
- **Dock widgets**: Can add with `addDockWidget()` for side panels

:::note Class-Based vs Functional
For anything beyond trivial examples, use a class inheriting from `QMainWindow` or `QWidget`. This provides:
- Better organization of signals/slots
- State management (instance variables)
- Ability to override Qt methods
- Easier testing and maintenance
:::

## File Dialogs and User Input

Real applications need to interact with the filesystem:

```python
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QPushButton, QLabel, QFileDialog
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Dialog Example")
        self.resize(500, 300)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        self.label = QLabel("No file selected")
        layout.addWidget(self.label)
        
        open_button = QPushButton("Open File")
        open_button.clicked.connect(self.open_file)
        layout.addWidget(open_button)
        
        save_button = QPushButton("Save File")
        save_button.clicked.connect(self.save_file)
        layout.addWidget(save_button)
    
    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            "",  # Starting directory (empty = last used)
            "Data Files (*.csv *.h5);;All Files (*.*)"
        )
        
        if filename:  # User might cancel
            self.label.setText(f"Selected: {filename}")
            # Here you would load the file
    
    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save File",
            "output.csv",
            "CSV Files (*.csv);;All Files (*.*)"
        )
        
        if filename:
            self.label.setText(f"Would save to: {filename}")
            # Here you would save data

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
```

**File dialog patterns:**

- `getOpenFileName()`: Select one existing file
- `getOpenFileNames()`: Select multiple files (note plural)
- `getSaveFileName()`: Choose location to save a file
- `getExistingDirectory()`: Select a folder

All return tuples: `(selected_path, selected_filter)`. Check if path is not empty before using (user might cancel).

## Common Widgets Overview

Here's a quick reference of frequently used widgets:

**Input Widgets:**
```python
from PyQt6.QtWidgets import (
    QLineEdit,      # Single-line text input
    QTextEdit,      # Multi-line text editor
    QSpinBox,       # Integer input with up/down buttons
    QDoubleSpinBox, # Float input with up/down buttons
    QSlider,        # Slider for numeric range
    QComboBox,      # Dropdown selection
    QCheckBox,      # Boolean checkbox
    QRadioButton,   # Mutually exclusive options
)

# Example: SpinBox for numeric input
spinbox = QDoubleSpinBox()
spinbox.setRange(0.0, 100.0)
spinbox.setValue(50.0)
spinbox.setSuffix(" mm")  # Display unit
spinbox.valueChanged.connect(lambda val: print(f"Value: {val}"))
```

**Display Widgets:**
```python
from PyQt6.QtWidgets import (
    QLabel,         # Text or image display
    QProgressBar,   # Progress indication
    QLCDNumber,     # Digital LCD display
)

# Example: Progress bar
progress = QProgressBar()
progress.setRange(0, 100)
progress.setValue(50)
```

**Container Widgets:**
```python
from PyQt6.QtWidgets import (
    QGroupBox,      # Labeled box grouping widgets
    QTabWidget,     # Tabbed interface
    QScrollArea,    # Scrollable content area
)

# Example: Tabs
tabs = QTabWidget()
tabs.addTab(QWidget(), "Tab 1")
tabs.addTab(QWidget(), "Tab 2")
```

## Next Steps

You now have the foundation for building Qt applications. Continue to:

- **[Integrating PyVista with Qt](pyvista-qt-integration)** - Embed 3D visualization in Qt windows
- **[Hands-on Workshop](qt-workshop)** - Build a complete FEM visualization application

## Practice Exercises

**Exercise 1: Temperature Converter**
Create an application with:
- Two `QDoubleSpinBox` widgets (Celsius and Fahrenheit)
- When one changes, automatically update the other
- Add `QLabel` widgets for clarity
- Use `QHBoxLayout` or `QFormLayout`

**Exercise 2: Simple Text Editor**
Create an application with:
- `QTextEdit` for content
- Menu with "File" → "Open", "Save", "Exit"
- Use `QFileDialog` to open/save `.txt` files
- Display filename in window title
- Add status bar showing character count

**Exercise 3: Data Range Explorer**
Create an application with:
- `QSlider` for selecting a value
- `QLabel` showing current value
- `QProgressBar` visualizing value as percentage of range
- `QPushButton` to reset to center
- All widgets update when slider moves

Try implementing these before checking the solutions in the workshop section!
