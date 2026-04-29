from fileinput import filename
# Importiert alle benötigten Qt-Widgets für das GUI
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QFileDialog,
    QGroupBox, QComboBox, QCheckBox,
    QPushButton, QSlider  # Slider für Skalierung / Clipping
)

# QAction wird für Menüeinträge (Menüleiste) benötigt
from PyQt6.QtGui import QAction

# Qt-Core, z. B. für Ausrichtungen (Qt.Horizontal)
from PyQt6.QtCore import Qt, QTimer

# Systemfunktionen (z. B. Programmstart/-ende)
import sys
import math



# PyVista-Qt-Widget zum Einbetten eines VTK-Renderfensters in Qt
from pyvistaqt import QtInteractor

# Text-Eingabefelder
from PyQt6.QtWidgets import QLineEdit

# PyVista-Bibliothek für 3D-Meshes und Visualisierung
import pyvista as pv
from fem_viewer_haumer import FEMViewer

def main():
    app = QApplication(sys.argv)
    window = FEMViewer()
    window.show()
    sys.exit(app.exec())
    
if __name__ == "__main__":
    main()