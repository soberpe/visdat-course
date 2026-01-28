# ======================================================
# SCHWINGUNGSANALYSE MAIN
# File zur Visualisierung von Übertragungsfunktionen, bestimmen von Eigenfrequenzen und qualitatives darstellen von Moden
# Benötigte Files:
# - Übertragungsfunktion FFT Imaginärteil (TSV)
# - Übertragungsfunktion FFT Betrag (TSV)
# - Geometrie File (HDF5)
# Passende Dateien zum qualitativen Testen werden im Ordner  final-assignment/maier-thomas/data/ bereitgestellt


# Konkret wird der Code an messungen eines Legohochhauses angewendet, welches mit Roofing Hammer angeregt wurde.
# Die Beschleunigungen wurden durch 2 Beschleunigungssensoren aufgenommen.
# Weietre infos sowie Messwerte sind dem Prüfstandslabor zu entnehmen.
# ======================================================


# IMPORT der benötigten Libraries
import sys
import numpy as np
import pandas as pd
import h5py

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel,
    QFileDialog, QGroupBox, QComboBox,
    QPushButton, QListWidget, QListWidgetItem, QDoubleSpinBox
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from find_and_plot_modes import (       #   Importieren der Funktionen aus find_and_plot_modes.py
    build_mode,
    plot_mode,
    find_eigenfrequencies
)

# ======================================================
# MEASUREMENT-MAP zum Zuordnen von Anregungspunkten und Messnummer auf Knoten des Geometriefiles; 
# ======================================================
MEASUREMENT_MAP = { # Die Darstellung wird auf eine Kante pro Richtung beschränkt, um die Übersichtlichkeit zu gewährleisten
    "X": {
        "LEFT": [(8, 45, +1), (10, 33, +1), (12, 21, +1)],              # Linke vordere Kante des Hochhauses 
        #"RIGHT": [(0, 34, -1), (3, 22, -1), (5, 46, -1)],              # Rechte vordere Kante des Hochhauses
        #"BACK_RIGHT": [(6, 47, -1), (14, 35, -1), (16, 23, -1)],       # Rechte hintere Kante des Hochhauses
                                                                        # Aufnahme der linken hinteren Kante wurde vernachlässigt
    },
    "Y": {
        "FRONT_LEFT": [(7, 45, +1), (9, 33, +1), (11, 21, +1)],
        #"FRONT_RIGHT": [(1, 34, +1), (4, 22, -1), (12, 46, +1)],
        #"BACK_RIGHT": [(13, 47, -1), (15, 35, -1), (17, 23, -1)],
        # Aufnahme der linken hinteren Kante wurde vernachlässigt
    }
}


class Plott_UEfkt_Modes(QMainWindow):               # Hauptfensterklasse der Applikation
    def __init__(self):                             # Initialisierung der GUI
        super().__init__()                          # Aufruf des Konstruktors der Basisklasse
        self.setWindowTitle("Schwingungsanlyse")    # Setzen des Fenstertitels
        self.resize(1200, 800)                      # Setzen der Fenstergröße

        # Datencontainer
        self.frequency = None
        self.node_ids = None
        self.edges = None
        self.tf_imag = None
        self.tf_mag = None
        self.kanalnamen = []
        self.nodes = {}

        # =========================
        # Zentrales Widget
        # =========================
        central = QWidget()                 #Zentrales Widget erstellen
        self.setCentralWidget(central)      #Setzen des zentralen Widgets
        main_layout = QHBoxLayout(central)     #Hauptlayout des zentralen Widgets erstellen

        #Bedienungungselemente erstellen
        controls = self.create_controls()
        main_layout.addWidget(controls)

        # Matplotlib Canvas
        self.figure = Figure(figsize=(6, 8))
        self.canvas = FigureCanvasQTAgg(self.figure)
        main_layout.addWidget(self.canvas, stretch=3)
        
        # Leeren Plot erstellen zur Anzeige von Info-Texten am Anfang
        ax = self.figure.add_subplot(111)
        ax.text(
            0.5, 0.5, 
            "Zum Start den gewünschten Button drücken", 
            ha='center', va='center', fontsize=14,
            wrap=True
        )
        ax.set_xticks([])               # keine x-Achse
        ax.set_yticks([])               # keine y-Achse
        ax.set_frame_on(False)          # Rahmen aus
        self.canvas.draw()

        # Menüleiste
        self.create_menus()
        self.statusBar().showMessage("Laden Sie das FFT-File")

    # ======================================================
    # Funktion zum erstellen der Menüleiste
    # ======================================================
    def create_menus(self):
        menubar = self.menuBar()                        
        file_menu = menubar.addMenu("&Load File")       # Menü zum Laden der benötigten Files
        image_menu = menubar.addMenu("&Bild")           # Menü zum Speichern des aktuellen Plots als Bilddatei

        open_fft = QAction("Öffne Üfkt FFT Imaginärteil File", self)    # Untermenüaktion zum Öffnen des Imaginär-FFT-Files
        open_fft.triggered.connect(self.open_fft_file)
        file_menu.addAction(open_fft)

        open_uefkt = QAction("Öffne Üfkt FFT Betrag File", self)        # Untermenüaktion zum Öffnen des Betrag-FFT-Files
        open_uefkt.triggered.connect(self.open_uefkt_file)
        file_menu.addAction(open_uefkt)

        open_geom = QAction("Öffne &Geometry File", self)           # Untermenüaktion zum Öffnen des Geometrie-Files
        open_geom.triggered.connect(self.open_geometry_file)
        file_menu.addAction(open_geom)

        file_menu.addSeparator()                                    # Trennlinie im Menü

        exit_action = QAction("Exit", self)                  # Untermenüaktion zum Beenden der Applikation      
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        save_image = QAction("Bild Speichern", self)        # Untermenüaktion zum Speichern des aktuellen Plots als Bilddatei
        save_image.triggered.connect(self.save_image)  
        image_menu.addAction(save_image)

    # ======================================================
    # Funktion zum erstellen der Bedienungselemente im linken Bereich des Fensters
    # ======================================================
    def create_controls(self):
        main_box = QVBoxLayout()                     #Hauptlayout für die Bedienungselemente

        # ==========================
        # Einstellmöglichkeiten für den Plot der Übertragungsfunktion
        # ==========================
        tf_box = QGroupBox("Übertragungsfunktion")
        tf_layout = QVBoxLayout(tf_box)
        tf_layout.addWidget(QLabel("Analysebereich Max [Hz]:"))
        self.freq_input = QDoubleSpinBox()
        self.freq_input.setMinimum(0.0)         
        self.freq_input.setMaximum(1e6)
        self.freq_input.setValue(0.0)
        self.freq_input.setSingleStep(1.0)
        tf_layout.addWidget(self.freq_input)

        # Plot-Button für Übertragungsfunktion
        self.plot_tf_btn = QPushButton("Übertragungsfunktion plotten")
        self.plot_tf_btn.clicked.connect(self.plot_transfer_function)
        tf_layout.addWidget(self.plot_tf_btn)

        # Eigenfrequenzen-Button
        self.find_eigenfreqs_btn = QPushButton("Eigenfrequenzen bestimmen")
        self.find_eigenfreqs_btn.clicked.connect(
          lambda: (
            self.show_info("Laden Sie das Betrag-FFT-File.")        #Info-Text anzeigen, falls Betrag-FFT File nicht geladen ist
            if self.tf_mag is None 
            else self.find_and_fill_eigenfreqs(
                np.mean(self.tf_mag, axis=1) if self.tf_mag.ndim > 1 else self.tf_mag,
                xmax=self.freq_input.value()
                )
            )
        )
        # Darstellen der Eigenfrequenzen-Liste
        tf_layout.addWidget(self.find_eigenfreqs_btn)                  #
        tf_layout.addWidget(QLabel("Gefundene Eigenfrequenzen:"))   #Label für die Liste der Eigenfrequenzen
        self.eigenfreq_list = QListWidget()
        self.eigenfreq_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        tf_layout.addWidget(self.eigenfreq_list)

        main_box.addWidget(tf_box)

        # ==========================
        # Einstellmöglichkeiten für den Plot der Modes
        # ==========================
        mode_box = QGroupBox("Mode Control")
        mode_layout = QVBoxLayout(mode_box)

        # Mode auswählen
        mode_layout.addWidget(QLabel("Mode auswählen:"))
        self.mode_combo = QComboBox()
        mode_layout.addWidget(self.mode_combo)

        # Richtung wählen
        mode_layout.addWidget(QLabel("Richtung:"))
        self.dir_combo = QComboBox()
        self.dir_combo.addItems(["X", "Y"])
        mode_layout.addWidget(self.dir_combo)

        # Kanal wählen
        mode_layout.addWidget(QLabel("Kanal:"))
        self.channel_combo = QComboBox()
        mode_layout.addWidget(self.channel_combo)

        # Mode-Plot Button
        self.plot_mode_btn = QPushButton("Mode plotten")
        self.plot_mode_btn.clicked.connect(self.plot_selected_mode_from_button)
        mode_layout.addWidget(self.plot_mode_btn)

        # Reset Button zum zurücksetzen der Ansicht
        reset_btn = QPushButton("Reset View")
        reset_btn.clicked.connect(self.reset_view)
        mode_layout.addWidget(reset_btn)

        main_box.addWidget(mode_box)    
        container = QWidget()
        container.setLayout(main_box)
        container.setFixedWidth(300)
        return container

    # ======================================================
    # Funktion zum zurücksetzen der Ansicht, damit kein Plot mehr angezeigt wird
    # ======================================================
    def reset_view(self):
        self.figure.clear()
        self.canvas.draw()


    # ======================================================
    # Funktion zum öffnen des Übertragungsfunktion Betrag Files
    # ======================================================
    def open_uefkt_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Übertragungsfunktion FFT Betrag",
            "",
            "TSV Files (*.tsv)"
        )
        if not path:
            return

        df = pd.read_csv(path, sep="\t", comment="#", decimal=",")
        self.frequency = df["frequency"].astype(float).values

        kanalnamen = [c for c in df.columns if "UEBERTRAGUNGSFUNKTION" in c]    #Filtern der Spaltennamen für die Kanäle
        kanalnamen = sorted(kanalnamen, key=lambda s: int(s.split("_")[-1]))      #Sortieren der Kanalnamen nach der Kanalnummer

        self.tf_mag = df[kanalnamen].astype(float).values       #Speichern der Übertragungsfunktion Betragswerte als numpy Array
        self.kanalnamen = kanalnamen                            #Speichern der Kanalnamen

        self.channel_combo.clear()
        self.channel_combo.addItems(self.kanalnamen)

        self.statusBar().showMessage(f"Betrag-FFT geladen ({len(self.kanalnamen)} Kanäle)", 5000)

    # ======================================================
    # Funktion zum öffnen des Geometrie Files
    # ======================================================
    def open_geometry_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Geometry HDF5", "", "HDF5 Files (*.h5)"
        )
        if not path:        #Abbrechen, falls kein Pfad ausgewählt wurde
            return

        with h5py.File(path, "r") as f:        #Öffnen des HDF5 Files
            nodes = f["nodes"][:]
            self.edges = f["edges"][:]

        self.node_ids = nodes["id"]        # Knotenpositionen extrahieren   
        self.nodes = {
            "x": nodes["x"],
            "y": nodes["y"] if "y" in nodes.dtype.names else np.zeros(len(nodes)),
            "z": nodes["z"],
        }

        self.statusBar().showMessage("Geometry loaded")

    # ======================================================
    # Funktion zum Öffnen des Übertragungsfunktion Imaginär Files
    # ======================================================
    def open_fft_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Übertragungsfunktion FFT Imaginärteil",
            "",
            "TSV Files (*.tsv)"
        )
        if not path:            #Abbrechen, falls kein Pfad ausgewählt wurde
            return

        df = pd.read_csv(path, sep="\t", comment="#", decimal=",")      #Einlesen der TSV Datei mit Pandas
        self.frequency = df["frequency"].values                         #Speichern der Frequenzwerte

        kanalnamen = sorted(                                            #Filtern und Sortieren der Spaltennamen für die Kanäle aufgrund chaotischer messabfolge
            [c for c in df.columns if "Imaginaer" in c],                
            key=lambda s: int(s.split("_")[-1])                        
        )

        self.tf_imag = df[kanalnamen].values
        self.statusBar().showMessage("Imaginär-FFT geladen", 5000)


    # ======================================================
    # Funktion zum Speichern des aktuellen Plots als Bilddatei
    # ======================================================
    def save_image(self):
        path, _ = QFileDialog.getSaveFileName(          #Öffnen des Datei-Dialogs zum Speichern
            self,
            "Save Image",
            "",
            "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)"
        )
        if not path:                                #Abbrechen, falls kein Pfad ausgewählt wurde
            return

        self.figure.savefig(path)
        self.statusBar().showMessage(f"Bild gespeichert: {path}", 5000)


    # ======================================================
    # Eigenfrequenzen bestimmen
    # ======================================================
    def find_and_fill_eigenfreqs(self, tf_mag, xmax=None):
        if not isinstance(tf_mag, np.ndarray):                  #Überprüfen, ob tf_mag ein numpy Array ist
            self.show_info("Fehler: tf_mag ist kein Array.")     
            return

        if xmax is not None and xmax > 0:                   #Beschränken des Frequenzbereichs auf xmax, falls angegeben
            mask = self.frequency <= xmax                      #Maske für Frequenzen ≤ xmax erstellen
            freq = self.frequency[mask]                        
            tf_mag = tf_mag[mask]
        else:
            freq = self.frequency

        self.eigenfreqs, self.peak_indices = find_eigenfrequencies(freq, tf_mag)           #Aufrufen der Funktion aus find_and_plot_modes.py

         # Liste aktualisieren

        self.eigenfreq_list.clear()                             #Liste der Eigenfrequenzen sicherhaeitshalber leeren
        if hasattr(self, "mode_combo"): 
            self.mode_combo.clear()                             #ComboBox der Modes leeren
            for i, f in enumerate(self.eigenfreqs):             #Hinzufügen der Modes zur ComboBox
                self.mode_combo.addItem(f"Mode {i + 1}") 

        for f in self.eigenfreqs:
            self.eigenfreq_list.addItem(f"{f:.2f} Hz")          #Hinzufügen der Eigenfrequenzen zur Liste

    # ======================================================
    # Funktion zum Extrahieren eines Mode aus der Imaginär-FFT über die Höhe der Entsprechenden Kante aus der Measurement-Map
    # ======================================================
    @staticmethod                                       #Statische Methode, da kein Zugriff auf Instanzvariablen benötigt wird
    def extract_mode_from_measurement_map(              
        tf_imag,
        freq_idx,
        measurement_maps,
        node_ids,
        nodes,
        normalize=True,
    ):
        z_meas = []
        u_meas = []

        #print("\n================ MODE DEBUG =================")  #Debug-Ausgaben zur Überprüfung der Funktion bei Bedarf aktivieren
        #print(f"Frequenzindex: {freq_idx}")                       #Debug-Ausgaben zur Überprüfung der Funktion bei Bedarf aktivieren

        
        #print("\nMesspunkte (z, u_imag):")
        # Messwerte sammeln
        for measurement_map in measurement_maps:
            for meas_idx, node_id, sign in measurement_map:
                node_pos = np.where(node_ids == node_id)[0][0]      #Finden der Position des Knotens im Knoten-Array
                z = nodes["z"][node_pos]                            #Extrahieren der z-Koordinate des Knotens   
                u = sign * tf_imag[freq_idx, meas_idx]              #Extrahieren des Imaginärteils der Übertragungsfunktion und Anwenden des Vorzeichens

                z_meas.append(z)                                    #Hinzufügen der z-Koordinate zur Messpunktliste
                u_meas.append(u)                                    #Hinzufügen der Auslenkung zur Messpunktliste
                #print(                                     #Debug-Ausgaben zur Überprüfung der Funktion bei Bedarf aktivieren
                    #f"  Node {node_id:>3} | "   
                    #f"z = {z:6.2f} | "
                    #f"TF[{meas_idx}] = {u:+.4e}"
                #)
        z_meas = np.asarray(z_meas)                       #Umwandeln der Messpunktlisten in numpy Arrays
        u_meas = np.asarray(u_meas)                 #Umwandeln der Messpunktlisten in numpy Arrays

        # Mode über Höhe aufbauen
        z_nodes = nodes["z"]
        u_all = build_mode(z_nodes, z_meas, u_meas)

        # Normieren

        if normalize:                               #Normieren der Auslenkungen, falls gewünscht= True, Flase abfrage
            max_val = np.max(np.abs(u_all))
            if max_val > 0:
                u_all /= max_val

        # -------------------------                 #Debug-Ausgaben zur Überprüfung der Modeauslenkung bei Bedarf aktivieren
        # Knoten-Auslenkungen
        # -------------------------
        #print("\nInterpolierte Knoten-Auslenkungen:")
        #for nid, z, u in zip(node_ids, nodes["z"], u_all):
            #print(f"  Node {nid:>3} | z = {z:6.2f} | u = {u:+.4f}")

        #print("============================================\n")

        return u_all

    # ======================================================
    # Funktion zum plotten eines ausgewählten Modes
    # ======================================================
    def plot_selected_mode(self, mode_idx):

        if self.nodes is None or "z" not in self.nodes:         #Überprüfen, ob Geometrie File geladen ist
            self.show_info("Laden Sie das Geometry-File.")
            return

        if self.tf_imag is None:                            #Überprüfen, ob Imaginär-FFT File geladen ist
            self.show_info("Laden Sie das Imaginär-FFT-File.")
            return

        if not hasattr(self, "peak_indices"):               #Überprüfen, ob Eigenfrequenzen bestimmt wurden
            self.show_info("Eigenfrequenzen fehlen.")
            return

        freq_idx = self.peak_indices[mode_idx]

        direction = "X"  # "X" oder "Y"                 #Richtung normalerweise aus der ComboBox auswählen, für bessere Darstellung aktuell fest auf "X" gesetzt

        # alle Kanten dieser Richtung verwenden
        measurement_maps = list(MEASUREMENT_MAP[direction].values())    #Extrahieren der Messpunkt-Maps für die gewählte Richtung

        u_all = self.extract_mode_from_measurement_map(     #Aufrufen der statischen Methode zum Extrahieren des Modes entsprechend der Messpunkt-Map
            tf_imag=self.tf_imag,
            freq_idx=freq_idx,
            measurement_maps=measurement_maps,
            node_ids=self.node_ids,
            nodes=self.nodes,
            normalize=True,
        )


        self.figure.clear()
        ax = self.figure.add_subplot(111)

        plot_mode(                              #Aufrufen der plot_mode Funktion aus find_and_plot_modes.py
            ax=ax,
            node_ids=self.node_ids,
            nodes=self.nodes,
            edges=self.edges,
            plot_lines=[("b", u_all)],
            axis_a="x",
            axis_b="z",
            disp_axis="x",  # "x" oder "y"
            scale=0.4,
        )

        ax.set_title(f"Mode {mode_idx + 1} ({direction})")
        self.canvas.draw()


    # ======================================================
    # Funktion zum plotten des ausgewählten Modes sobald der entsprechende Button gedrückt wird
    # ======================================================
    def plot_selected_mode_from_button(self):
        idx = self.mode_combo.currentIndex()
        if self.nodes is None or "z" not in self.nodes or self.node_ids is None or self.edges is None:   # Überprüfen, ob Geometrie File geladen ist
            self.show_info("Laden Sie das Geometry-File, um Modes zu plotten.")
            return
        if not hasattr(self, "peak_indices"):                                   # Überprüfen, ob Eigenfrequenzen bestimmt wurden
            self.show_info("Die Eigenfrequenzen wurden noch nicht bestimmt.")
            return
        if idx < 0:                                 # Überprüfen, ob ein Mode ausgewählt wurde              
            self.show_info("Wählen Sie einen Mode aus.")
            return
        self.plot_selected_mode(idx)


    # ======================================================
    # Funktion zum plotten der Übertragungsfunktion
    # ======================================================
    def plot_transfer_function(self):
        if self.tf_mag is None:
            self.show_info("Laden Sie das Betrag-FFT-File.")        #Info-Text anzeigen, falls Betrag-FFT File nicht geladen ist
            return

        xmax = float(self.freq_input.value())                   #Maximalen Frequenzbereich aus dem Input-Feld auslesen
        if xmax <= 0.0:
            xmax = self.frequency.max()                         #Falls 0 bzw kein gültiger Wert eingegeben wurde, auf das Maximum der Frequenzen setzen

        self.figure.clear()                                     #Betsehenden Plot löschen damit neu geplottet werden kann   
        ax = self.figure.add_subplot(111)
        for i, kanal in enumerate(self.kanalnamen):                 #Schleife über alle Kanäle zum Plotten
            tf = self.tf_mag[:, i]                                  #Extrahieren der Übertragungsfunktion des aktuellen Kanals
            ax.plot(self.frequency, tf, label=f"{kanal}")           #Plotten der Übertragungsfunktion

        ax.set_xlabel("Frequenz [Hz]")              #Achsenbeschriftungen setzen
        ax.set_ylabel("Betrag")
        #ax.set_xticks(np.arange(0, xmax, 1))       #x-Achsen Ticks setzen, bei Bedarf aktivieren
        #ax.set_yticks(np.arange(0, 1500, 1))       #y-Achsen Ticks setzen, bei Bedarf aktivieren
        ax.grid(True)
        if len(self.kanalnamen) > 0:                
            ax.set_xlim(0, xmax)
            ax.set_ylim(np.min(self.tf_mag), 10)

        ax.set_title("Übertragungsfunktion (alle Kanäle)")
        self.canvas.draw()

    # ======================================================
    # Funktion zum Anzeigen von Info-Texten im Plot-Bereich
    # ======================================================
    def show_info(self, text):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.text(0.5, 0.5, text, ha='center', va='center', fontsize=14, wrap=True)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_frame_on(False)
        self.canvas.draw()


# ======================================================
# MAIN
# ======================================================
def main():
    app = QApplication(sys.argv)
    win = Plott_UEfkt_Modes()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
