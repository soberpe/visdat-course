
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

#-------------------------------------------------------------------------------------



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

    # Create control panel-----------------
    controls = self.create_controls()
    main_layout.addWidget(controls)

    # Zwei Plotter nebeneinander-----------------------------------------------------------------------
    self.plotters = []
    for i in range(2):  # Anzahl der Ansichten
        plot_widget = QtInteractor(central_widget)
        main_layout.addWidget(plot_widget.interactor, stretch=3)
        self.plotters.append(plot_widget)
    #--------------------------------------------------------------------------------------------------

    # Create menus and status bar-----------
    self.create_menus()
    self.statusBar().showMessage("Ready")

    self.mesh = None
    self.original_mesh = None  # Store undeformed mesh

    self.undeformed_actor = None
    self.deformed_actor = None

    #neue Variablen für zwei Plotter-------------------------------------------------------------------
    self.deformed_actors = []
    #--------------------------------------------------------------------------------------------------