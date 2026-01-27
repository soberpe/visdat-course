
from fileinput import filename
import os
import pyvista as pv
import numpy as np
from PyQt6.QtCore import Qt, QTimer


from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
import sys

from pyvistaqt import QtInteractor
import pyvista as pv

from PyQt6.QtWidgets import QFileDialog

from PyQt6.QtWidgets import (
    QGroupBox, QComboBox, QCheckBox,
    QPushButton
)

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QFileDialog,
    QGroupBox, QComboBox, QCheckBox,
    QPushButton, QSlider  # Add QSlider
)

from PyQt6.QtWidgets import QMessageBox

#----------------------------------------------------------------------------------------


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

        # Update field selector
        self.populate_field_selector()

        # Display mesh (will be refined in next step)
        self.display_mesh()

        # Update info
        self.update_mesh_info()

        # Update status and title
        self.statusBar().showMessage(f"Loaded: {filename}", 3000)
        self.setWindowTitle(f"FEM Viewer - {os.path.basename(filename)}")

    except Exception as e:
        self.statusBar().showMessage(f"Error loading file: {str(e)}", 5000)



def reset_camera(self):
    """Reset the camera view for all plotters"""
    if not self.plotters:
        return

    for plotter in self.plotters:
        plotter.reset_camera()  # Jeder Plotter bekommt ein Reset

    self.statusBar().showMessage("Camera reset", 2000)


def closeEvent(self, event):
    """Clean up VTK resources before closing"""
    if self.plotters:
        for plotter in self.plotters:
            if plotter is not None:
                try:
                    plotter.close()   # PyVista QtInteractor Cleanup
                except Exception:
                    pass
    event.accept()

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
    """Display mesh with current settings for all plotters (Multiple Views)"""
    if self.mesh is None:
        return

    # Alte Actors-Liste leeren
    self.deformed_actors = []

    # Prüfen, ob Wireframe angezeigt werden soll
    show_undeformed = self.show_undeformed_checkbox.isChecked() and self.original_mesh is not None

    # Aktuell ausgewähltes Feld
    field_name = self.field_combo.currentText()

    if field_name == "(No Field)" or not field_name:
        # Nur Geometrie
        display_field = None
        title = ""
        color = 'lightgray'           # Mesh-Farbe für „rohes“ Mesh
        show_scalar_bar = False        # keine Scalar Bar
    else:
        # Felddaten abrufen
        field_data = self.mesh.point_data[field_name]

        # Prüfen, ob Vektorfeld
        if field_data.ndim > 1 and field_data.shape[1] > 1:
            magnitude = np.linalg.norm(field_data, axis=1)
            mag_field_name = f"{field_name}_magnitude"
            self.mesh[mag_field_name] = magnitude
            display_field = mag_field_name
            title = f"{field_name} (Magnitude)"
        else:
            display_field = field_name
            title = field_name

        color = None
        show_scalar_bar = self.scalar_bar_checkbox.isChecked()

    # Über alle Plotter iterieren
    for plotter in self.plotters:
        plotter.clear()

        # Undeformed Mesh als Wireframe anzeigen
        if show_undeformed:
            plotter.add_mesh(
                self.original_mesh,
                color='black',
                style='wireframe',
                line_width=1,
                name='undeformed'
            )

        # Mesh anzeigen (mit Feld oder nur Geometrie)
        deformed_actor = plotter.add_mesh(
            self.mesh,
            scalars=display_field,
            color=color,
            cmap='coolwarm' if display_field else None,
            show_edges=self.edges_checkbox.isChecked(),
            show_scalar_bar=show_scalar_bar,
            scalar_bar_args={'title': title} if display_field else None
        )

        # Actor speichern für spätere Updates (z.B. Deformation)
        self.deformed_actors.append(deformed_actor)

        # Kamera für jede View zurücksetzen
        plotter.reset_camera()