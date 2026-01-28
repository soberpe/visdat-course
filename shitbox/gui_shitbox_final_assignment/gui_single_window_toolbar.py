from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QLabel, QFileDialog, QLineEdit, QMessageBox
)

from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT
)
from matplotlib.figure import Figure
import numpy as np

from final_assignment.gersdorfer.code.source.data_loader import load_measurement_csv
from signal_processing import compute_fft


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FFT Analyse – Single Window")
        self.resize(1000, 700)

        self.file_path = None

        # ---------- Zentrales Widget ----------
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # ---------- Datei & Parameter ----------
        self.label = QLabel("Keine Datei ausgewählt")
        layout.addWidget(self.label)

        btn_open = QPushButton("CSV-Datei auswählen")
        btn_open.clicked.connect(self.open_file)
        layout.addWidget(btn_open)

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

        btn_plot = QPushButton("Übertragungsfunktion plotten")
        btn_plot.clicked.connect(self.run_analysis)
        layout.addWidget(btn_plot)

        # ---------- Matplotlib Plot ----------
        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvasQTAgg(self.figure)
        layout.addWidget(self.canvas)

        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        layout.addWidget(self.toolbar)

        self.ax = self.figure.add_subplot(111)

    # ---------- Datei auswählen ----------
    def open_file(self):
        self.file_path, _ = QFileDialog.getOpenFileName(
            self,
            "CSV auswählen",
            "",
            "CSV Files (*.csv)"
        )
        if self.file_path:
            self.label.setText(self.file_path)

    # ---------- Analyse & Plot ----------
    def run_analysis(self):
        if not self.file_path:
            QMessageBox.warning(self, "Fehler", "Bitte zuerst eine Datei auswählen.")
            return

        try:
            fs = float(self.fs_input.text())
            header_rows = int(self.header_input.text())
        except ValueError:
            QMessageBox.warning(self, "Eingabefehler", "Samplingfrequenz oder Header-Zeilen ungültig.")
            return

        acc_col = self.acc_input.text()
        force_col = self.force_input.text()
        imag_col = self.imag_input.text()

        try:
            _, acc, force = load_measurement_csv(
                self.file_path,
                header_rows,
                acc_col,
                force_col,
                imag_col
            )
        except Exception as e:
            QMessageBox.critical(self, "Ladefehler", str(e))
            return

        freq, H = compute_fft(acc, force, fs)

        # Plot aktualisieren
        self.ax.clear()
        self.ax.plot(freq, np.abs(H))
        self.ax.set_xlim(0, 40)
        self.ax.set_xlabel("Frequenz [Hz]")
        self.ax.set_ylabel("Amplitude")
        self.ax.set_title("Übertragungsfunktion |H(f)|")
        self.ax.grid(True)

        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
