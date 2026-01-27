import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys
from PyQt6 import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas



# CSV einlesen
df = pd.read_csv('final-assignment/Zierler/Code/data/Schlagdaten.csv', sep=';')

# Dezimalzahlen konvertieren
df["Carry (m)"] = df["Carry (m)"].str.replace(',', '.').astype(float)
df["Side (m)"] = df["Side (m)"].str.replace(',', '.').astype(float)
df["Ball Speed (m/s)"] = df["Ball Speed (m/s)"].str.replace(',', '.').astype(float)
df["start Ang. (Deg)"] = df["start Ang. (Deg)"].str.replace(',', '.').astype(float)
df["max. Hight (m)"] = df["max. Hight (m)"].str.replace(',', '.').astype(float)

#  Fenster erstellen
class ScatterWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Carry-Distanz vs Seitenabweichung")
        self.setGeometry(100, 100, 800, 600)

        # Layout
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        # Dropdown-Box mit allen Clubs
        self.club_selector = QtWidgets.QComboBox()
        self.club_selector.addItems(sorted(df["Club"].unique()))
        layout.addWidget(self.club_selector)

        # Matplotlib Figure
        self.figure, self.ax = plt.subplots(figsize=(8,5))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Event: Wenn Auswahl geändert wird
        self.club_selector.currentTextChanged.connect(self.update_plot)

        # Start-Plot
        self.update_plot(self.club_selector.currentText())

    def update_plot(self, club_name):
        self.ax.clear()  # vorherigen Plot löschen
        df_club = df[df["Club"] == club_name]
        self.ax.scatter(df_club["Carry (m)"], df_club["Side (m)"], color='blue', s=50)
        self.ax.set_xlabel("Carry Länge (m)")
        self.ax.set_ylabel("Side (m)")
        self.ax.set_title(f"Carry-Distanz vs Seitenabweichung {club_name}")
        self.ax.grid(True)
        self.canvas.draw()


app = QtWidgets.QApplication(sys.argv)
window = ScatterWindow()
window.show()
sys.exit(app.exec())

