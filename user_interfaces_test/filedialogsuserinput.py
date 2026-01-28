from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QPushButton, QLabel, QFileDialog
)


from data_loader import load_measurement_csv
from signal_processing import compute_fft
from plotter import (plot_transfer_function,plot_imaginary_comparison)


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
        layout.addWidget(open_button)
        
        save_button = QPushButton("Save File")
        save_button.clicked.connect(self.save_file)
        layout.addWidget(save_button)
    
    def open_file(self):
    filename, _ = QFileDialog.getOpenFileName(
        self,
        "Select File",
        "",
        "Data Files (*.csv *.h5);;All Files (*.*)"
    )

    if not filename:
        return

    self.label.setText(f"Selected: {filename}")

    fs = 12800
    f_max = 40

    freq_imag, acc, force = load_measurement_csv(filename)
    freq, H = compute_fft(acc, force, fs)

    plot_transfer_function(
        freq, H, f_max,
        title="Übertragungsfunktion Betrag"
    )

    plot_imaginary_comparison(freq, H, freq_imag, f_max)

    #def save_file(self):
        #filename, _ = QFileDialog.getSaveFileName(
            #self,
            #"Save File",
            #"output.csv",
            #"CSV Files (*.csv);;All Files (*.*)"
        #)
        
        #if filename:
        #    self.label.setText(f"Would save to: {filename}")
        #    # Here you would save data

app = QApplication([])
window = MainWindow()
window.show()
app.exec()