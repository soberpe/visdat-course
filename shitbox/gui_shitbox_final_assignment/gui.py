#import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt


from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit, QDialog, QCheckBox, QDialogButtonBox, QGroupBox)




from final_assignment.gersdorfer.code.source.data_loader import load_measurement_csv
from signal_processing import compute_fft
from plotter import plot_transfer_function, plot_imaginary_comparison



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Dialog Example")
        self.resize(500, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.label = QLabel("No file selected")
        layout.addWidget(self.label)

        open_button = QPushButton("Open File")
        open_button.clicked.connect(self.open_file)
        self.file_path = None
        layout.addWidget(open_button)

        # Samplingfrequenz
        layout.addWidget(QLabel("Samplingfrequenz [Hz]:"))
        self.fs_input = QLineEdit("12800")
        layout.addWidget(self.fs_input)

        # Header-Zeilen
        layout.addWidget(QLabel("Header-Zeilen überspringen:"))
        self.header_input = QLineEdit("22")
        layout.addWidget(self.header_input)

        # Spaltennamen
        layout.addWidget(QLabel("Spaltenname Acceleration:"))
        self.acc_input = QLineEdit("Acceleration")
        layout.addWidget(self.acc_input)

        layout.addWidget(QLabel("Spaltenname Force:"))
        self.force_input = QLineEdit("Force")
        layout.addWidget(self.force_input)

        layout.addWidget(QLabel("Spaltenname Imaginärteil:"))
        self.imag_input = QLineEdit("Untitled")
        layout.addWidget(self.imag_input)


        #save_button = QPushButton("Save File")
        #save_button.clicked.connect(self.save_file)
        #layout.addWidget(save_button)

    def open_file(self):
        
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "CSV Files (*.csv)")
        if not file_path:
            return


        self.file_path = file_path
        self.label.setText(f"Selected: {self.file_path}")
        

        # GUI-Werte lesen
        fs = float(self.fs_input.text())                #Sample Frequenz - Float, da diese eine Kommazahl ist
        header_rows = int(self.header_input.text())     #Anzahl der übersprungenen Header Zeilen - Integer, da dieser Wert ganzzahlig ist

        acc_col = self.acc_input.text()
        force_col = self.force_input.text()
        freq_imag_col = self.imag_input.text()

        f_max = 40

        freq_imag, acc_timedata, force_timedata  = load_measurement_csv(file_path, header_rows, acc_col, force_col, freq_imag_col)

        freq, H = compute_fft(acc_timedata, force_timedata, fs)

        plot_transfer_function(freq, H, f_max, title="Übertragungsfunktion Betrag")

        plot_imaginary_comparison(freq, H, freq_imag, f_max)

    #def save_file(self):
    #pass   # Platzhalter, damit der Button existiert


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()



