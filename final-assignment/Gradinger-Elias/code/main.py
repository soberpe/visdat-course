import sys
import numpy as np
import pyvista as pv
from pyvistaqt import QtInteractor

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel,
    QFileDialog, QGroupBox, QComboBox,
    QCheckBox, QPushButton, QSlider
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt


class FEMViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FEM Results Viewer")
        self.resize(1200, 800)

        # State variables
        self.mesh = None
        self.original_mesh = None
        self.current_cmap = "coolwarm"

        # Clipping state
        self.clip_enabled = False
        self.clip_axis = "X"
        self.clip_value = 0.0

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Controls
        controls = self.create_controls()
        main_layout.addWidget(controls)

        # PyVista plotter
        self.plotter = QtInteractor(central_widget)
        main_layout.addWidget(self.plotter.interactor, stretch=3)

        # Menus
        self.create_menus()
        self.statusBar().showMessage("Ready")

    def create_menus(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("&File")

        open_action = QAction("&Open Mesh...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_mesh)
        file_menu.addAction(open_action)

        export_action = QAction("&Export Screenshot...", self)
        export_action.setShortcut("Ctrl+S")
        export_action.triggered.connect(self.export_screenshot)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        view_menu = menubar.addMenu("&View")

        reset_action = QAction("&Reset Camera", self)
        reset_action.setShortcut("R")
        reset_action.triggered.connect(self.reset_camera)
        view_menu.addAction(reset_action)

    def create_controls(self):
        controls = QGroupBox("Visualization Controls")
        layout = QVBoxLayout()
        controls.setLayout(layout)

        # Field selection
        layout.addWidget(QLabel("Display Field:"))
        self.field_combo = QComboBox()
        layout.addWidget(self.field_combo)

        # Color map selection
        layout.addWidget(QLabel("Color Map:"))
        self.cmap_combo = QComboBox()
        self.cmap_combo.addItems(["viridis", "plasma", "jet", "coolwarm"])
        self.cmap_combo.setCurrentText(self.current_cmap)
        layout.addWidget(self.cmap_combo)

        # Display options
        self.edges_checkbox = QCheckBox("Show Edges")
        self.edges_checkbox.setChecked(True)
        layout.addWidget(self.edges_checkbox)

        self.scalar_bar_checkbox = QCheckBox("Show Scalar Bar")
        self.scalar_bar_checkbox.setChecked(True)
        layout.addWidget(self.scalar_bar_checkbox)

        # Deformation
        layout.addWidget(QLabel("\nDeformation:"))
        self.deform_checkbox = QCheckBox("Show Deformed")
        self.deform_checkbox.setChecked(False)
        layout.addWidget(self.deform_checkbox)

        layout.addWidget(QLabel("Scale Factor:"))
        self.deform_slider = QSlider(Qt.Orientation.Horizontal)
        self.deform_slider.setRange(1, 10000)
        self.deform_slider.setValue(10)
        layout.addWidget(self.deform_slider)

        self.deform_label = QLabel("1.0x")
        layout.addWidget(self.deform_label)

        # Clipping Plane
        layout.addWidget(QLabel("\nClipping Plane:"))
        self.clip_checkbox = QCheckBox("Enable Clipping")
        layout.addWidget(self.clip_checkbox)

        layout.addWidget(QLabel("Axis:"))
        self.clip_axis_combo = QComboBox()
        self.clip_axis_combo.addItems(["X", "Y", "Z"])
        layout.addWidget(self.clip_axis_combo)

        layout.addWidget(QLabel("Position:"))
        self.clip_slider = QSlider(Qt.Orientation.Horizontal)
        self.clip_slider.setRange(0, 100)
        layout.addWidget(self.clip_slider)

        # Mesh info
        layout.addWidget(QLabel("\nMesh Information:"))
        self.info_label = QLabel("No mesh loaded")
        self.info_label.setWordWrap(True)
        layout.addWidget(self.info_label)

        # Reset button
        reset_button = QPushButton("Reset View")
        reset_button.clicked.connect(self.reset_camera)
        layout.addWidget(reset_button)

        # Signals
        self.field_combo.currentTextChanged.connect(self.update_field_display)
        self.cmap_combo.currentTextChanged.connect(self.update_colormap)
        self.edges_checkbox.stateChanged.connect(self.update_display_options)
        self.scalar_bar_checkbox.stateChanged.connect(self.update_display_options)
        self.deform_checkbox.stateChanged.connect(self.update_deformation)
        self.deform_slider.valueChanged.connect(self.update_deformation)

        self.clip_checkbox.stateChanged.connect(self.update_clipping)
        self.clip_axis_combo.currentTextChanged.connect(self.update_clipping)
        self.clip_slider.valueChanged.connect(self.update_clipping)

        layout.addStretch()
        controls.setFixedWidth(280)

        return controls

    def open_mesh(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Mesh File",
            "c:/visdat-course/data",
            "VTK Files (*.vtu *.vtk *.vti);;All Files (*.*)"
        )

        if not filename:
            return

        self.mesh = pv.read(filename)
        self.original_mesh = None
        self.deform_checkbox.setChecked(False)

        bounds = self.mesh.bounds
        self.clip_slider.setValue(50)

        self.populate_field_selector()
        self.display_mesh()
        self.update_mesh_info()

        self.statusBar().showMessage(f"Loaded: {filename}", 3000)

    def populate_field_selector(self):
        self.field_combo.blockSignals(True)
        self.field_combo.clear()

        self.field_combo.addItem("(No Field)")
        for name in self.mesh.point_data.keys():
            self.field_combo.addItem(name)

        self.field_combo.blockSignals(False)
        if self.field_combo.count() > 1:
            self.field_combo.setCurrentIndex(1)

    def update_mesh_info(self):
        self.info_label.setText(
            f"Points: {self.mesh.n_points:,}\n"
            f"Cells: {self.mesh.n_cells:,}\n"
            f"Point Fields: {len(self.mesh.point_data)}"
        )

    def apply_clipping(self, mesh):
        if not self.clip_checkbox.isChecked():
            return mesh

        axis = self.clip_axis_combo.currentText()
        bounds = mesh.bounds

        if axis == "X":
            origin = (bounds[0] + (bounds[1] - bounds[0]) * self.clip_slider.value() / 100, 0, 0)
            normal = (1, 0, 0)
        elif axis == "Y":
            origin = (0, bounds[2] + (bounds[3] - bounds[2]) * self.clip_slider.value() / 100, 0)
            normal = (0, 1, 0)
        else:
            origin = (0, 0, bounds[4] + (bounds[5] - bounds[4]) * self.clip_slider.value() / 100)
            normal = (0, 0, 1)

        return mesh.clip(origin=origin, normal=normal)

    def display_mesh(self):
        if self.mesh is None:
            return

        self.plotter.clear()
        field_name = self.field_combo.currentText()

        mesh = self.apply_clipping(self.mesh)

        # Sicherstellen, dass das Feld existiert
        if field_name not in mesh.point_data:
            field_name = "(No Field)"

        if field_name == "(No Field)":
            self.plotter.add_mesh(
                mesh,
                color="lightgray",
                show_edges=self.edges_checkbox.isChecked(),
                show_scalar_bar=False
            )
        else:
            data = mesh.point_data[field_name]

            if data.ndim > 1:
                scalars = np.linalg.norm(data, axis=1)
                title = f"{field_name} (Magnitude)"
            else:
                scalars = data
                title = field_name

            self.plotter.add_mesh(
                mesh,
                scalars=scalars,
                cmap=self.current_cmap,
                show_edges=self.edges_checkbox.isChecked(),
                show_scalar_bar=self.scalar_bar_checkbox.isChecked(),
                scalar_bar_args={"title": title}
            )

        self.plotter.reset_camera()

    def update_field_display(self, _):
        self.display_mesh()

    def update_display_options(self):
        self.display_mesh()

    def update_colormap(self, cmap):
        self.current_cmap = cmap
        self.display_mesh()

    def update_clipping(self):
        self.display_mesh()

    def update_deformation(self):
        if self.mesh is None or not self.deform_checkbox.isChecked():
            if self.original_mesh is not None:
                self.mesh = self.original_mesh.copy()
            self.display_mesh()
            return

        for name in ["U", "Displacement", "displacement"]:
            if name in self.mesh.point_data:
                disp_name = name
                break
        else:
            self.deform_checkbox.setChecked(False)
            return

        scale = self.deform_slider.value() / 10.0
        self.deform_label.setText(f"{scale:.1f}x")

        if self.original_mesh is None:
            self.original_mesh = self.mesh.copy()

        disp = self.original_mesh.point_data[disp_name]
        if disp.shape[1] == 2:
            disp = np.hstack([disp, np.zeros((disp.shape[0], 1))])

        self.mesh.points = self.original_mesh.points + scale * disp
        self.display_mesh()

    def reset_camera(self):
        self.plotter.reset_camera()

    def export_screenshot(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Screenshot",
            "screenshot.png",
            "PNG Images (*.png);;JPEG Images (*.jpg)"
        )
        if filename:
            self.plotter.screenshot(filename)


def main():
    app = QApplication(sys.argv)
    window = FEMViewer()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
