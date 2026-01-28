from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QLabel, QFileDialog, QLineEdit,
    QDialog, QMessageBox
)

from final_assignment.gersdorfer.code.source.data_loader import load_measurement_csv
from signal_processing import compute_fft
from plotter import create_transfer_function_plot, update_limits


class PlotControlDialog(QDialog):
    def __init__(self, fig, ax, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Plot-Bereich einstellen")

        self.fig = fig
        self.ax = ax

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Frequenzbereich [Hz]"))
        self.fmin_input = QLineEdit("0")
        self.fmax_input = QLineEdit("40")
        layout.addWidget(self.fmin_input)
        layout.addWidget(self.fmax_input)

        layout.addWidget(QLabel("Amplitudenbereich"))
        self.amin_input = QLineEdit("0")
        self.amax_input = QLineEdit("10")
        layout.addWidget(self.amin_input)
        layout.addWidget(self.amax_input)

        self.update_button = QPushButton("Plot aktualisieren")
        self.update_button.clicked.connect(self.update_plot)
        layout.addWidget(self.update_button)

    def update_plot(self):
        try:
            fmin = float(self.fmin_input.text())
            fmax = float(self.fmax_input.text())
            amin = float(self.amin_input.text())
            amax = float(self.amax_input.text())
        except ValueError:
            QMessageBox.warning(self, "Eingabefehler", "Bitte nur Zahlen eingeben.")
            return

        if fmin >= fmax or amin >= amax:
            QMessageBox.warning(self, "Bereichsfehler", "Min-Wert muss kleiner als Max-Wert sein.")
            return

        update_limits(self.ax, self.fig, fmin, fmax, amin, amax)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FFT Analyse – stabile Version")
        self.resize(500, 420)

        self.file_path = None

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

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

        btn_analyze = QPushButton("Übertragungsfunktion anzeigen")
        btn_analyze.clicked.connect(self.run_analysis)
        layout.addWidget(btn_analyze)

    def open_file(self):
        self.file_path, _ = QFileDialog.getOpenFileName(
            self,
            "CSV auswählen",
            "",
            "CSV Files (*.csv)"
        )
        if self.file_path:
            self.label.setText(self.file_path)

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

        fig, ax = create_transfer_function_plot(freq, H)

        self.hide()
        dialog = PlotControlDialog(fig, ax, self)
        dialog.exec()
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
