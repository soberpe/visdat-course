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

class FEMViewer(QMainWindow):
    
    

# öffnet und schließt die Application richtig
    def main():
        app = QApplication(sys.argv)
        window = FEMViewer()
        window.show()
        sys.exit(app.exec())

    if __name__ == "__main__":
        main() 