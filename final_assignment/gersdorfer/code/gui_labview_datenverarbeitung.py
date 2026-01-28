# Standard-Bibliotheken

import sys
import os

#Third-Party Bibliotheken
import numpy as np

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit, QMessageBox)

from matplotlib.backends.backend_qtagg import (FigureCanvasQTAgg, NavigationToolbar2QT)

from matplotlib.figure import Figure


# ============================================================
# Projektpfade
# ============================================================

#Basisverzeichnis (dient zur Vermeidung von Absolutpfaden)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))      #Bestimmung des Basisverzeichnis

# Python-Module (Datenverarbeitung/PLots etc.)
SOURCE_DIR = os.path.join(BASE_DIR, "source")
sys.path.insert(0, SOURCE_DIR)       #Zugriff auf meine Module/Funktionen in Source


# ============================================================
# Eigene Module importieren
# ============================================================
import data_loader as dl
import signal_processing as sp
from export_dialog import ExportCSVDialog
import plotter as plo



# ============================================================
# GUI-Hauptfenster
# ============================================================

class MainWindow(QMainWindow):

    #Hauptfenster der FFT-Analyse-Anwendung.

    #Aufgaben:
    #- Einlesen von CSV-Messdaten
    #- Konfiguration der Analyseparameter
    #- Berechnung der Übertragungsfunktion (FFT)
    #- Darstellung der Ergebnisse in einem eingebetteten Matplotlib-Plot
    #- Export ausgewählter Signale als CSV
    


    def __init__(self):
        super().__init__()

        # -----------------------------
        # Fenster-Einstellungen
        # -----------------------------
        self.setWindowTitle("FFT Analyse Tool")
        self.resize(1000, 700)

        # Aktuell ausgewählte Datei
        self.file_path = None

        # Speicher für exportierbare Signale
        self.available_signals = None

        # -----------------------------
        # Zentrales Widget & Layout
        # -----------------------------
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # -----------------------------
        # Dateiauswahl
        # -----------------------------
        self.label = QLabel("Keine Datei ausgewählt")
        layout.addWidget(self.label)

        btn_open = QPushButton("CSV-Datei auswählen")
        btn_open.clicked.connect(self.open_file)
        layout.addWidget(btn_open)

        # -----------------------------
        # Analyseparameter
        # -----------------------------
        layout.addWidget(QLabel("Samplingfrequenz [Hz]:"))
        self.fs_input = QLineEdit("12800")
        layout.addWidget(self.fs_input)

        layout.addWidget(QLabel("Header-Zeilen überspringen:"))
        self.header_input = QLineEdit("22")
        layout.addWidget(self.header_input)

        layout.addWidget(QLabel("Spalte Acceleration:"))
        self.acc_input = QLineEdit("Acceleration")
        layout.addWidget(self.acc_input)

        layout.addWidget(QLabel("Spalte Force:"))
        self.force_input = QLineEdit("Force")
        layout.addWidget(self.force_input)

        layout.addWidget(QLabel("Spalte Imaginärteil:"))
        self.imag_input = QLineEdit("Untitled")
        layout.addWidget(self.imag_input)

        # -----------------------------
        # Aktions-Buttons
        # -----------------------------
        btn_plot = QPushButton("Übertragungsfunktion plotten")
        btn_plot.clicked.connect(self.run_analysis)
        layout.addWidget(btn_plot)

        self.btn_export = QPushButton("CSV exportieren")
        self.btn_export.setEnabled(False)
        self.btn_export.clicked.connect(self.export_csv)
        layout.addWidget(self.btn_export)

        # -----------------------------
        # Matplotlib-Plot (eingebettet)
        # -----------------------------
        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvasQTAgg(self.figure)
        layout.addWidget(self.canvas)

        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        layout.addWidget(self.toolbar)

        self.ax = self.figure.add_subplot(111)  # Achse für alle Plots

    # ========================================================
    # Datei-Auswahl
    # ========================================================
    #Öffnet einen Fenster zur Auswahl einer CSV-Messdatei

    def open_file(self):
        self.file_path, _ = QFileDialog.getOpenFileName(
            self,
            "CSV auswählen",
            "",
            "CSV Files (*.csv)"
        )
        if self.file_path:
            self.label.setText(self.file_path)

     # ========================================================
    # Analyse & Plot
    # ========================================================

    #Führt die FFT-Analyse durch und stellt die Übertragungsfunktion dar.
    def run_analysis(self):
        if not self.file_path:
            QMessageBox.warning(self, "Fehler", "Bitte zuerst eine Datei auswählen.")
            return


        # -----------------------------
        # Parameter aus GUI lesen
        # -----------------------------
        try:
            fs = float(self.fs_input.text())
            header_rows = int(self.header_input.text())
        except ValueError:
            QMessageBox.warning(self, "Eingabefehler", "Samplingfrequenz oder Header-Zeilen ungültig.")
            return

        acc_col = self.acc_input.text()
        force_col = self.force_input.text()
        imag_col = self.imag_input.text()

        # -----------------------------
        # Daten einlesen
        # -----------------------------

        try:
            freq_imag, acc, force = dl.load_measurement_csv(
                self.file_path,
                header_rows,
                acc_col,
                force_col,
                imag_col
            )
        except Exception as e:
            QMessageBox.critical(self, "Ladefehler", str(e))
            return


        # -----------------------------
        # Signalverarbeitung
        # -----------------------------
        
        freq, H = sp.compute_fft(acc, force, fs)

        # Zeitachse (für Export)
        time = np.arange(len(acc)) / fs

        # -----------------------------
        # Exportierbare Signale sammeln
        # -----------------------------
        self.available_signals = {
            "time": time,
            "frequency": freq,
            "acceleration": acc,
            "force": force,
            "H_abs": np.abs(H),
            "H_phase": np.angle(H),
            "H_real": np.real(H),
            "H_imag": np.imag(H),
        }

        # -----------------------------
        # Plot aktualisieren
        # -----------------------------
        plo.plot_transfer_function(self.ax, freq, H, f_max=40, title="Übertragungsfunktion |H(f)|")
        self.canvas.draw()
        self.btn_export.setEnabled(True)

    # ========================================================
    # CSV Export
    # ========================================================
    def export_csv(self):
        if not self.available_signals:
            return

        dialog = ExportCSVDialog(self.available_signals, self)
        dialog.exec()


# ============================================================
# Programmstart
# ============================================================

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
