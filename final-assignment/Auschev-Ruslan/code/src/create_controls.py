
# Controls wurde so verändert, dass ein Slider für die Slice-Position und ein ComboBox für die Slice-Achse hinzugefügt wurden.
# Außerdem wurde ein Slider für den Deformations-Skalierungsfaktor hinzugefügt.
# Zusätzlich wurde eine Checkbox für die Animation der Deformation eingefügt.

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QFileDialog,
    QGroupBox, QComboBox, QCheckBox,
    QPushButton, QSlider  # Add QSlider
)

from PyQt6.QtCore import Qt, QTimer

def create_controls(self):
    """Create control panel with field selection and display options"""
    controls = QGroupBox("Visualization Controls")
    layout = QVBoxLayout()
    controls.setLayout(layout)

    # Slice / Cut Plane Controls
    layout.addWidget(QLabel("\nSlice Plane:"))

    self.slice_checkbox = QCheckBox("Show Slice Plane")
    self.slice_checkbox.setChecked(False)
    self.slice_checkbox.stateChanged.connect(self.update_slice)
    layout.addWidget(self.slice_checkbox)

    layout.addWidget(QLabel("Slice Position (0-100%):"))
    self.slice_slider = QSlider(Qt.Orientation.Horizontal)
    self.slice_slider.setRange(0, 100)
    self.slice_slider.setValue(50)
    self.slice_slider.valueChanged.connect(self.update_slice)
    layout.addWidget(self.slice_slider)

    layout.addWidget(QLabel("Slice Axis:"))
    self.slice_axis_combo = QComboBox()
    self.slice_axis_combo.addItems(["X", "Y", "Z"])
    self.slice_axis_combo.currentTextChanged.connect(self.update_slice)
    layout.addWidget(self.slice_axis_combo)


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

    self.scalar_bar_checkbox.stateChanged.connect(self.update_scalar_bar)

    self.show_undeformed_checkbox = QCheckBox("Show Undeformed Mesh (Wireframe)")
    self.show_undeformed_checkbox.setChecked(False)
    self.show_undeformed_checkbox.stateChanged.connect(self.display_mesh)
    layout.addWidget(self.show_undeformed_checkbox)

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
    # Ein Box für Animation---------------------------------------------
    self.animation_checkbox = QCheckBox("Animate Deformation")
    self.animation_checkbox.setChecked(False)
    self.animation_checkbox.stateChanged.connect(self.run_animation)
    layout.addWidget(self.animation_checkbox)
    # -------------------------------------------------------------------
    self.deform_label = QLabel("1.0x")
    layout.addWidget(self.deform_label)

    # Mesh info
    layout.addWidget(QLabel("\nMesh Information:"))
    self.info_label = QLabel("No mesh loaded")
    self.info_label.setWordWrap(True)
    layout.addWidget(self.info_label)

    # Reset button
    reset_button = QPushButton("Reset View")
    reset_button.clicked.connect(self.reset_camera)
    layout.addWidget(reset_button)

    # Add these lines in create_controls method after creating the widgets:
    self.field_combo.currentTextChanged.connect(self.update_field_display)
    self.edges_checkbox.stateChanged.connect(self.update_display_options)
    self.scalar_bar_checkbox.stateChanged.connect(self.update_display_options)

    # Push controls to top
    layout.addStretch()

    # Fixed width for control panel
    controls.setFixedWidth(280)

    return controls