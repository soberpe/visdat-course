"""
LVM Plotter (PyQt6) – Plot im GUI + Peak-Erkennung

Was ich mit diesem Programm mache:
1) Ich lade Messdaten im .lvm-Format (X- und/oder Y-Richtung).
2) Ich wähle einen Frequenzbereich (f_min bis f_max).
3) Ich definiere ein Peak-Level für den Imaginärteil.
4) Ich finde alle lokalen Peaks (positive UND negative), die dieses Level überschreiten.
5) Ich stelle den Plot direkt im GUI dar.
6) Ich markiere die Peaks als Punkte und beschrifte sie mit der Frequenz.
7) Ich zeige die Peak-Werte zusätzlich in einem Textfeld an.
"""

# -------------------------------------------------
# Imports
# -------------------------------------------------
import sys
import pandas as pd

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog,
    QDoubleSpinBox, QMessageBox, QPlainTextEdit
)

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar


# -------------------------------------------------
# Funktion: LVM-Datei einlesen
# -------------------------------------------------
def load_lvm_as_df(path: str, freq_scale: float = 1.0) -> pd.DataFrame:
    """
    Lese .lvm-Datei ein
    freq_scale skaliert die Frequenzspalte direkt beim Einlesen
    """
    df = pd.read_csv(
        path,
        sep="\t",
        skiprows=1,
        header=None,
        decimal=",",
        engine="python"
    )
    df.columns = ["freq", "imag"]

    # -------- Frequenz direkt skalieren --------
    freq_scale=0.1
    df["freq"] = df["freq"] * freq_scale #da Messdaten in 10*Hz ausgegeben wurden

    return df


# -------------------------------------------------
# Funktion: positive Peaks finden
# -------------------------------------------------
def find_positive_peaks(df: pd.DataFrame, level: float):
    """
    Positiver Peak:
    y[i-1] < y[i] > y[i+1]  UND  y[i] >= level
    """
    if df is None or df.empty or len(df) < 3:
        return []

    df = df.sort_values("freq").reset_index(drop=True)
    x = df["freq"].to_numpy()
    y = df["imag"].to_numpy()

    peaks = []
    for i in range(1, len(df) - 1):
        if y[i-1] < y[i] and y[i] > y[i+1] and y[i] >= level:
            peaks.append((float(x[i]), float(y[i])))

    return peaks


# -------------------------------------------------
# Funktion: negative Peaks finden
# -------------------------------------------------
def find_negative_peaks(df: pd.DataFrame, level: float):
    """
    Negativer Peak (Minimum):
    y[i-1] > y[i] < y[i+1]  UND  y[i] <= -level
    """
    if df is None or df.empty or len(df) < 3:
        return []

    df = df.sort_values("freq").reset_index(drop=True)
    x = df["freq"].to_numpy()
    y = df["imag"].to_numpy()

    peaks = []
    for i in range(1, len(df) - 1):
        if y[i-1] > y[i] and y[i] < y[i+1] and y[i] <= -level:
            peaks.append((float(x[i]), float(y[i])))

    return peaks


# -------------------------------------------------
# GUI Klasse
# -------------------------------------------------
class LvmPlotGui(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LVM Plotter – Peaks im GUI")

        # gespeicherte Dateipfade
        self.file_x = ""
        self.file_y = ""

        # -------------------------
        # Layout
        # -------------------------
        main_layout = QVBoxLayout()

        # -------- Datei X --------
        row_x = QHBoxLayout()
        row_x.addWidget(QLabel("Datei X (optional):"))

        self.path_x = QLineEdit()
        self.path_x.setReadOnly(True)
        row_x.addWidget(self.path_x, 1)

        btn_x = QPushButton("Auswählen")
        btn_x.clicked.connect(self.select_file_x)
        row_x.addWidget(btn_x)
        btn_x_clear = QPushButton("X löschen")
        btn_x_clear.clicked.connect(self.clear_file_x)
        row_x.addWidget(btn_x_clear)


        main_layout.addLayout(row_x)

        # -------- Datei Y --------
        row_y = QHBoxLayout()
        row_y.addWidget(QLabel("Datei Y (optional):"))

        self.path_y = QLineEdit()
        self.path_y.setReadOnly(True)
        row_y.addWidget(self.path_y, 1)

        btn_y = QPushButton("Auswählen")
        btn_y.clicked.connect(self.select_file_y)
        row_y.addWidget(btn_y)

        btn_y_clear = QPushButton("Y löschen")
        btn_y_clear.clicked.connect(self.clear_file_y)
        row_y.addWidget(btn_y_clear)


        main_layout.addLayout(row_y)

        # -------- Parameter --------
        params = QHBoxLayout()

        params.addWidget(QLabel("f_min [Hz]:"))
        self.spin_fmin = QDoubleSpinBox()
        self.spin_fmin.setDecimals(2)
        self.spin_fmin.setRange(0, 1e9)
        self.spin_fmin.setValue(0.0)
        params.addWidget(self.spin_fmin)

        params.addWidget(QLabel("f_max [Hz]:"))
        self.spin_fmax = QDoubleSpinBox()
        self.spin_fmax.setDecimals(2)
        self.spin_fmax.setRange(0, 1e9)
        self.spin_fmax.setValue(40.0)
        params.addWidget(self.spin_fmax)

        params.addWidget(QLabel("Peak-Level |imag| ≥"))
        self.spin_level = QDoubleSpinBox()
        self.spin_level.setDecimals(3)
        self.spin_level.setSingleStep(0.001)
        self.spin_level.setRange(0.0, 1e9)
        self.spin_level.setValue(0.01)
        params.addWidget(self.spin_level)

        main_layout.addLayout(params)

        # -------- Start Button --------
        btn_plot = QPushButton("Plot + Peaks berechnen")
        btn_plot.clicked.connect(self.update_plot)
        main_layout.addWidget(btn_plot)

        # -------- Plot --------
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.ax = self.figure.add_subplot(111)

        main_layout.addWidget(self.toolbar)
        main_layout.addWidget(self.canvas, 1)

        # -------- Ergebnisbox --------
        self.results_box = QPlainTextEdit()
        self.results_box.setReadOnly(True)
        self.results_box.setMaximumHeight(220)
        main_layout.addWidget(self.results_box)

        self.setLayout(main_layout)

    # -------------------------------------------------
    # Datei-Auswahl
    # -------------------------------------------------
    def select_file_x(self):
        f, _ = QFileDialog.getOpenFileName(self, "X-Datei", "", "*.lvm")
        if f:
            self.file_x = f
            self.path_x.setText(f)

    def clear_file_x(self):       #"""Diese Funktion löscht die aktuell ausgewählte Y-Datei.Dadurch arbeitet das Programm danach nur noch mit der X-Richtung.
        self.file_x = ""          # internen Dateipfad zurücksetzen
        self.path_x.setText("")   # Textfeld im GUI leeren


    def select_file_y(self):
        f, _ = QFileDialog.getOpenFileName(self, "Y-Datei", "", "*.lvm")
        if f:
            self.file_y = f
            self.path_y.setText(f)

    def clear_file_y(self):       #"""Diese Funktion löscht die aktuell ausgewählte Y-Datei.Dadurch arbeitet das Programm danach nur noch mit der X-Richtung.
        self.file_y = ""          # internen Dateipfad zurücksetzen
        self.path_y.setText("")   # Textfeld im GUI leeren

    # -------------------------------------------------
    # Plot + Peak-Erkennung
    # -------------------------------------------------
    def update_plot(self):

        if not self.file_x and not self.file_y:
            QMessageBox.warning(self, "Fehler", "Bitte mindestens eine Datei auswählen.")
            return

        f_min = self.spin_fmin.value()
        f_max = self.spin_fmax.value()
        level = self.spin_level.value()

        self.ax.clear()

        text = f"Peak-Level |imag| ≥ {level}\n\n"
        # -------------------------------------------------
        # Offsets für Peak-Beschriftungen (dynamisch)
        # -------------------------------------------------
        ymin, ymax = self.ax.get_ylim()
        y_offset = 0.03 * (ymax - ymin)   # 3 % der y-Achse
        x_offset = 0.0                   # kein horizontaler Versatz


        # -------- X-Richtung --------
        if self.file_x: 
            df_x = load_lvm_as_df(self.file_x) 
            df_x = df_x[(df_x["freq"] >= f_min) & (df_x["freq"] <= f_max)]


            peaks_x = find_positive_peaks(df_x, level) + find_negative_peaks(df_x, level)
            peaks_x = sorted(peaks_x, key=lambda t: t[0])

            self.ax.plot(df_x["freq"], df_x["imag"], label="Z-Richtung")

            for k, (f, im) in enumerate(peaks_x):
                self.ax.plot(f, im, marker="o", linestyle="None", color="green")

                dy = y_offset * (1 + 0.6 * (k % 3))  # Staffelung

                # self.ax.text(
                #     f + x_offset,
                #     im + dy,
                #     f"{f:.1f} Hz",
                #     fontsize=8,
                #     ha="center",
                #     va="bottom"
                # )


            self.ax.plot([], [], marker="o", linestyle="None",
                         color="green", label="Z Peaks")

            text += f"Z-Peaks ({len(peaks_x)}):\n"
            for f, im in peaks_x:
                text += f"  f = {f:.2f} Hz, imag = {im:.4g}\n"
            text += "\n"

        # -------- Y-Richtung --------
        if self.file_y: 
            df_y = load_lvm_as_df(self.file_y) 
            df_y = df_y[(df_y["freq"] >= f_min) & (df_y["freq"] <= f_max)]

            peaks_y = find_positive_peaks(df_y, level) + find_negative_peaks(df_y, level)
            peaks_y = sorted(peaks_y, key=lambda t: t[0])

            self.ax.plot(df_y["freq"], df_y["imag"], label="Y-Richtung")

            for k, (f, im) in enumerate(peaks_y):
                self.ax.plot(f, im, marker="o", linestyle="None", color="red")

                dy = y_offset * (1 + 0.6 * (k % 3))

                # self.ax.text(
                #     f + x_offset,
                #     im - dy,
                #     f"{f:.1f} Hz",
                #     fontsize=8,
                #     ha="center",
                #     va="top"
                # )


            self.ax.plot([], [], marker="o", linestyle="None",
                         color="red", label="Y Peaks")

            text += f"Y-Peaks ({len(peaks_y)}):\n"
            for f, im in peaks_y:
                text += f"  f = {f:.2f} Hz, imag = {im:.4g}\n"

        # -------- Plot Format --------
        self.ax.set_xlabel("Frequenz [Hz]")
        self.ax.set_ylabel("Imaginärteil")
        self.ax.set_title("Imaginärteil über Frequenz")
        self.ax.set_xlim(left=0)
        self.ax.grid(True)
        self.ax.legend()

        self.results_box.setPlainText(text)
        self.canvas.draw()


# -------------------------------------------------
# Programmstart
# -------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = LvmPlotGui()
    w.resize(1100, 750)
    w.show()
    sys.exit(app.exec())
