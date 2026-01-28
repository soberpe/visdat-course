#Input Widgets

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




#Display Widgets
from PyQt6.QtWidgets import (
    QLabel,         # Text or image display
    QProgressBar,   # Progress indication
    QLCDNumber,     # Digital LCD display
)

# Example: Progress bar
progress = QProgressBar()
progress.setRange(0, 100)
progress.setValue(50)



#Container Widgets
from PyQt6.QtWidgets import (
    QGroupBox,      # Labeled box grouping widgets
    QTabWidget,     # Tabbed interface
    QScrollArea,    # Scrollable content area
)

# Example: Tabs
tabs = QTabWidget()
tabs.addTab(QWidget(), "Tab 1")
tabs.addTab(QWidget(), "Tab 2")