import sys
import numpy as np
import pandas as pd
from scipy.signal import find_peaks

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QDoubleSpinBox,
    QMessageBox, QGroupBox, QFormLayout,
    QTableWidget, QTableWidgetItem, QHeaderView
)

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar


class UebertragungsfunktionGUI(QWidget):
    def __init__(self):
        super().__init__()

        # ============================================================
        # ZIEL DES PROGRAMMS (kurz zusammengefasst)
        # ============================================================
        # Ich möchte zwei Messdateien (X und Y) einlesen, daraus die Moden/Peaks
        # einer Übertragungsfunktion bestimmen und anschließend:
        #  - die Kurven im Plot anzeigen (rechts im Fenster)
        #  - eine Tabelle mit den gefundenen Moden anzeigen (links im Fenster)

        # ============================================================
        # 1) Fenster-Einstellungen
        # ============================================================
        self.setWindowTitle("Übertragungsfunktionen - Modalanalyse")
        self.resize(1250, 720)  # Startgröße des Fensters

        # ============================================================
        # 2) FIXE Mode/Peak-Parameter (nicht im GUI sichtbar)
        # ============================================================
        # min_dist_hz:
        #   Minimaler Abstand zwischen zwei gefundenen Moden in Hz.
        #   Hintergrund: find_peaks nimmt "distance" in Samples/Index-Schritten.
        #   Daher muss ich min_dist_hz später in "Anzahl Samples" umrechnen.
        self.min_dist_hz = 3.0

        # prominence_factor:
        #   Steuert, wie "deutlich" ein Peak sein muss, um als Mode zu zählen.
        #   Ich berechne später die tatsächliche Prominenz so:
        #     prom = prominence_factor * (max(abs(signal)) - min(abs(signal)))
        #   -> das skaliert automatisch mit der Signalhöhe (robust bei unterschiedlichen Messungen)
        self.prominence_factor = 0.09

        # ============================================================
        # 3) Default-Dateien (Startwerte)
        # ============================================================
        # Diese Pfade sind nur ein Startwert. Im GUI kann ich sie über Buttons ersetzen.
        self.file_x = r"final-assignment/hutterer/code/data/Messung_Gestell_Anregung_X1/Imaginaerteil_uber_Frequenz_Uebertragungsfunktion_x.lvm"
        self.file_y = r"final-assignment/hutterer/code/data/Messung_Gestell_Anregung_X1/Imaginaerteil_uber_Frequenz_Uebertragungsfunktion_y.lvm"

        # ============================================================
        # 4) Layout-Aufbau: links Bedienfeld, rechts Plot
        # ============================================================
        # main = horizontales Layout, weil ich links und rechts nebeneinander haben will
        main = QHBoxLayout(self)

        # left = links: Datei-Auswahl, Parameter, Button, Tabelle
        left = QVBoxLayout()
        main.addLayout(left, 0)

        # right = rechts: Matplotlib Plot
        right = QVBoxLayout()
        main.addLayout(right, 1)

        # ============================================================
        # 5) Dateiauswahl (X/Y)
        # ============================================================
        # QGroupBox ist nur eine optische Gruppierung mit Rahmen + Titel
        files_box = QGroupBox("Daten einlesen")
        files_layout = QVBoxLayout(files_box)

        # ---------- X-Datei ----------
        row_x = QHBoxLayout()  # Button + Label nebeneinander
        btn_x = QPushButton("Datei X auswählen…")

        # clicked.connect(...) verbindet Button-Klick mit einer Funktion.
        # Hier: nur Pfad setzen + Label updaten, aber NICHT sofort plotten.
        btn_x.clicked.connect(self.pick_x)

        # Label zeigt den Pfad an (gekürzt, damit er ins Fenster passt)
        self.lbl_x = QLabel(self._short(self.file_x))
        # Damit ich den Pfad markieren und kopieren kann
        self.lbl_x.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        row_x.addWidget(btn_x)
        row_x.addWidget(self.lbl_x, 1)  # "1" = Label darf breit werden
        files_layout.addLayout(row_x)

        # ---------- Y-Datei ----------
        row_y = QHBoxLayout()
        btn_y = QPushButton("Datei Y auswählen…")
        btn_y.clicked.connect(self.pick_y)

        self.lbl_y = QLabel(self._short(self.file_y))
        self.lbl_y.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        row_y.addWidget(btn_y)
        row_y.addWidget(self.lbl_y, 1)
        files_layout.addLayout(row_y)

        left.addWidget(files_box)

        # ============================================================
        # 6) Parameter: im GUI nur f_max einstellbar
        # ============================================================
        # f_max ist die maximale Frequenz, die ich berücksichtige bzw.- darstelle.
        # Praktisch, wenn ich nur 0 bis 100 Hz betrachten will.
        params_box = QGroupBox("Parameter")
        form = QFormLayout(params_box)  # FormLayout = Beschriftung links, Widget rechts

        self.spin_fmax = QDoubleSpinBox()
        self.spin_fmax.setRange(1, 1e6)   # zulässiger Bereich
        self.spin_fmax.setDecimals(1)     # 1 Nachkommastelle
        self.spin_fmax.setValue(100.0)    # Startwert für die maximale Frequenz

        # Wichtig: KEIN valueChanged -> keine automatische Aktualisierung.
        # Update passiert nur durch Button.
        form.addRow("f_max [Hz]", self.spin_fmax)

        left.addWidget(params_box)

        # ============================================================
        # 7) Aktionen: nur Button "Plot aktualisieren"
        # ============================================================
        actions_box = QGroupBox("Aktionen")
        actions_layout = QVBoxLayout(actions_box)

        self.btn_plot = QPushButton("Plot aktualisieren")
        # Beim Klick wird die komplette Pipeline ausgeführt (Einlesen -> Moden -> Plot + Tabelle)
        self.btn_plot.clicked.connect(self.update_plot)
        actions_layout.addWidget(self.btn_plot)

        left.addWidget(actions_box)

        # ============================================================
        # 8) Tabelle: Ausgabe der gefundenen Moden
        # ============================================================
        table_box = QGroupBox("Gefundene Moden")
        table_layout = QVBoxLayout(table_box)

        # QTableWidget: einfache Tabelle.
        # 3 Spalten:
        #  - Richtung: X oder Y
        #  - Frequenz: Frequenz der Mode
        #  - Imaginärteil: Imaginärteil der Übertragungsfunktion an der Mode
        self.table = QTableWidget(0, 3)  # 0 Zeilen initial, 3 Spalten
        self.table.setHorizontalHeaderLabels(["Richtung", "Frequenz [Hz]", "Imaginärteil"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSortingEnabled(True)  # ich kann im GUI sortieren (z.B. nach Frequenz)
        table_layout.addWidget(self.table)

        # "1" sorgt dafür, dass die Tabelle den restlichen Platz im linken Panel bekommt
        left.addWidget(table_box, 1)

        # ============================================================
        # 9) Matplotlib in Qt einbetten (Plot rechts)
        # ============================================================
        # Figure = Matplotlib "Zeichenfläche"
        self.fig = Figure()

        # Canvas = Qt-Widget, das diese Matplotlib-Figure anzeigen kann
        self.canvas = FigureCanvas(self.fig)

        # Toolbar = Zoom/Pan/Reset/Speichern direkt im GUI
        self.toolbar = NavigationToolbar(self.canvas, self)

        right.addWidget(self.toolbar)
        right.addWidget(self.canvas, 1)

        # Hinweis: Ich plotte beim Start nicht automatisch.
        # -> Ich will bewusst, dass erst nach Button-Klick gerechnet wird.

    # ============================================================
    # Helper: lange Pfade kürzen (nur für Darstellung)
    # ============================================================
    def _short(self, path: str) -> str:
        # Wenn keine Datei gewählt ist, zeige ich einen Platzhalter
        if not path:
            return "(keine Datei ausgewählt)"
        # Wenn der Pfad kurz genug ist, gebe ich ihn vollständig aus,
        # sonst schneide ich vorne ab und zeige nur das Ende (meist der wichtige Teil)
        return path if len(path) <= 90 else "…" + path[-87:]

    # ============================================================
    # Dateidialog X: nur Pfad setzen + Label updaten
    # ============================================================
    def pick_x(self):
        # QFileDialog liefert (dateipfad, filterstring)
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Übertragungsfunktion X auswählen",
            "",
            "LVM (*.lvm);;Alle Dateien (*)"
        )
        if path:
            self.file_x = path
            self.lbl_x.setText(self._short(path))

    # ============================================================
    # Dateidialog Y: nur Pfad setzen + Label updaten
    # ============================================================
    def pick_y(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Übertragungsfunktion Y auswählen",
            "",
            "LVM (*.lvm);;Alle Dateien (*)"
        )
        if path:
            self.file_y = path
            self.lbl_y.setText(self._short(path))

    # ============================================================
    # LVM einlesen
    # ============================================================
    def read_lvm(self, file_path: str) -> pd.DataFrame:
        # Ich lese die Datei mit pandas.read_csv ein.
        # sep=r"\s+" bedeutet: Trennzeichen sind Whitespaces (Leerzeichen/Tabs), auch mehrfach.
        # decimal="," ist wichtig, weil in vielen Messfiles Dezimalkomma steht (z.B. 1,23).
        df = pd.read_csv(
            file_path,
            sep=r"\s+",
            engine="python",
            decimal=","
        )
        # Spaltennamen säubern (unsichtbare Leerzeichen entfernen),
        # weil LVM/ASCII-Dateien hier gerne "X_Value " statt "X_Value" haben.
        df.columns = df.columns.str.strip()
        return df

    # ============================================================
    # Tabelle füllen: DataFrame -> QTableWidget
    # ============================================================
    def fill_table(self, modes_df: pd.DataFrame):
        # Sorting kurz deaktivieren, damit die Zeilen sauber eingefügt werden.
        self.table.setSortingEnabled(False)

        # Tabelle leeren
        self.table.setRowCount(0)

        # Zeile für Zeile aus dem DataFrame in die GUI-Tabelle schreiben
        for _, row in modes_df.iterrows():
            r = self.table.rowCount()
            self.table.insertRow(r)

            # Richtung als String (X oder Y)
            self.table.setItem(r, 0, QTableWidgetItem(str(row["Richtung"])))

            # Frequenz mit 3 Nachkommastellen
            self.table.setItem(r, 1, QTableWidgetItem(f"{row['Frequenz_Hz']:.3f}"))

            # Imaginärteil kompakt (6 signifikante Stellen)
            self.table.setItem(r, 2, QTableWidgetItem(f"{row['Imaginärteil']:.6g}"))

        # Sorting wieder aktivieren
        self.table.setSortingEnabled(True)

    # ============================================================
    # Hauptfunktion: komplette Auswertung + Plot + Tabelle
    # Wird nur ausgeführt, wenn ich auf "Plot aktualisieren" klicke.
    # ============================================================
    def update_plot(self):
        try:
            # ------------------------------------------------------------
            # 1) Eingaben prüfen
            # ------------------------------------------------------------
            if not self.file_x or not self.file_y:
                raise ValueError("Bitte sowohl X- als auch Y-Datei auswählen.")

            # f_max aus dem GUI
            f_max = float(self.spin_fmax.value())

            # fixe Parameter aus dem Code
            min_dist_hz = self.min_dist_hz
            prominence_factor = self.prominence_factor

            # ------------------------------------------------------------
            # 2) Daten einlesen
            # ------------------------------------------------------------
            df_x = self.read_lvm(self.file_x)
            df_y = self.read_lvm(self.file_y)

            df_x["X_Value"] = df_x["X_Value"] * 0.1
            df_y["X_Value"] = df_y["X_Value"] * 0.1

            # ------------------------------------------------------------
            # 3) Filter: nur Frequenzen <= f_max behalten
            # ------------------------------------------------------------
            df_x = df_x[df_x["X_Value"] <= f_max]
            df_y = df_y[df_y["X_Value"] <= f_max]

            # ------------------------------------------------------------
            # 4) Umwandlung in NumPy Arrays
            # ------------------------------------------------------------
            # fx/fy: Frequenzwerte (x-Achse)
            # ax/ay: Übertragungsfunktion (y-Achse) (bei dir: Spalte "Comment")
            fx = df_x["X_Value"].to_numpy()
            ax = df_x["Comment"].to_numpy()
            fy = df_y["X_Value"].to_numpy()
            ay = df_y["Comment"].to_numpy()

            # Wenn nach dem Filtern zu wenig Punkte übrig bleiben, macht Peak-Suche keinen Sinn
            if len(fx) < 3 or len(fy) < 3:
                raise ValueError("Zu wenige Datenpunkte (nach Filter). Prüfe f_max oder Dateien.")

            # ------------------------------------------------------------
            # 5) Moden/Peaks finden (find_peaks)
            # ------------------------------------------------------------
            # Ich suche Peaks auf dem Betrag (abs),
            # weil die Übertragungsfunktion auch negative Werte haben kann.
            ax_abs = np.abs(ax)
            ay_abs = np.abs(ay)

            # Frequenzauflösung dfx/dfy:
            # -> median(diff(f)) ist robust gegen kleine Unregelmäßigkeiten
            dfx = float(np.median(np.diff(fx)))
            dfy = float(np.median(np.diff(fy)))

            # Umrechnung min_dist_hz (Hz) -> distance (Samples/Indices):
            # find_peaks distance ist NICHT in Hz, sondern in "wie viele Punkte Abstand".
            dist_x = max(1, int(min_dist_hz / dfx)) if min_dist_hz > 0 else 1
            dist_y = max(1, int(min_dist_hz / dfy)) if min_dist_hz > 0 else 1

            # Prominenz-Threshold:
            # - (max - min) ist die Signalspanne im Betrag
            # - prominence_factor ist ein Anteil davon
            # -> je größer prominence_factor, desto weniger (aber "wichtigere") Moden
            prom_x = prominence_factor * (ax_abs.max() - ax_abs.min())
            prom_y = prominence_factor * (ay_abs.max() - ay_abs.min())

            # find_peaks liefert Indizes der Peaks (modes_x/modes_y)
            modes_x, _ = find_peaks(ax_abs, prominence=prom_x, distance=dist_x)
            modes_y, _ = find_peaks(ay_abs, prominence=prom_y, distance=dist_y)

            # Die Indizes nutze ich, um Frequenzen und Imaginärteile an diesen Stellen zu holen
            mode_freqs_x = fx[modes_x]
            mode_vals_x = ax[modes_x]
            mode_freqs_y = fy[modes_y]
            mode_vals_y = ay[modes_y]

            # ------------------------------------------------------------
            # 6) Tabelle bauen und anzeigen
            # ------------------------------------------------------------
            # Ich kombiniere X und Y in einer Tabelle, damit man alle Moden auf einen Blick sieht.
            # Sortiert wird nach Frequenz.
            modes_df = pd.DataFrame({
                "Richtung": (["X"] * len(mode_freqs_x)) + (["Y"] * len(mode_freqs_y)),
                "Frequenz_Hz": np.concatenate([mode_freqs_x, mode_freqs_y])
                if (len(mode_freqs_x) + len(mode_freqs_y)) else np.array([]),
                "Imaginärteil": np.concatenate([mode_vals_x, mode_vals_y])
                if (len(mode_freqs_x) + len(mode_freqs_y)) else np.array([]),
            }).sort_values("Frequenz_Hz", ignore_index=True)

            self.fill_table(modes_df)

            # ------------------------------------------------------------
            # 7) Plot neu zeichnen
            # ------------------------------------------------------------
            self.fig.clear()
            axp = self.fig.add_subplot(111)

            # Grundkurven
            axp.plot(fx, ax, label="Übertragungsfunktion in x")
            axp.plot(fy, ay, label="Übertragungsfunktion in y")

            # Moden als Marker (Punkte)
            axp.plot(mode_freqs_x, mode_vals_x, "o", label="Moden X")
            axp.plot(mode_freqs_y, mode_vals_y, "o", label="Moden Y")

            # Beschriftungen wären hier möglich (auskommentiert in deinem Code).
            # Wenn ich das wieder aktivieren will, kann ich mit axp.annotate(...)
            # die Frequenzen über Pfeile an die Peaks schreiben.

            axp.set_xlabel("Frequenz [Hz]")
            axp.set_ylabel("Imaginärteil")
            axp.set_title("Plot der berechneten Übertragungsfunktionen")
            axp.grid(True)

            # x-Achse passend zu f_max begrenzen
            axp.set_xlim(0, f_max)

            axp.legend()

            # tight_layout verhindert, dass Labels abgeschnitten werden
            self.fig.tight_layout()

            # canvas.draw() aktualisiert das eingebettete Matplotlib-Widget im GUI
            self.canvas.draw()

        except Exception as e:
            # Wenn irgendwo ein Fehler passiert, zeige ich ihn als Dialog.
            # Das ist benutzerfreundlicher als ein Crash im Terminal.
            QMessageBox.critical(self, "Fehler", str(e))


if __name__ == "__main__":
    # ============================================================
    # Programmstart (Qt Eventloop)
    # ============================================================
    app = QApplication(sys.argv)          # Qt Anwendung initialisieren
    win = UebertragungsfunktionGUI()      # mein Fenster/GUI erzeugen
    win.show()                            # GUI anzeigen
    sys.exit(app.exec())                  # Eventloop starten (Programm läuft)