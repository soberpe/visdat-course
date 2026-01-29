import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton
)

class PlotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Matplotlib + PyQt6 GUI")
        self.setGeometry(100, 100, 1000, 600)

        # ===== MENU BAR =====
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("Datei")
        exit_action = file_menu.addAction("Beenden")
        exit_action.triggered.connect(self.close)

        # ===== STATUS BAR =====
        self.statusBar().showMessage("Bereit")

        # ===== CENTRAL WIDGET =====
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # ===== CONTROL PANEL (LEFT) =====
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)

        control_layout.addWidget(QLabel("Control Panel"))

        btn_update = QPushButton("Plot aktualisieren")
        control_layout.addWidget(btn_update)

        control_layout.addStretch()  # schiebt alles nach oben

        main_layout.addWidget(control_panel, 1)

        # ===== PLOT AREA (RIGHT) =====
        x = np.linspace(0, 10, 100)
        y = np.sin(x)

        self.fig, self.ax = plt.subplots()
        self.ax.plot(x, y, label="sin(x)")
        self.ax.set_title("Sinus Kurve")
        self.ax.grid(True)
        self.ax.legend()

        self.canvas = FigureCanvas(self.fig)
        main_layout.addWidget(self.canvas, 4)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlotWindow()
    window.show()
    sys.exit(app.exec())
