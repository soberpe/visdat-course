# ======================================================
# Standardbibliotheken
# ======================================================

import sys                                   # Zugriff auf Systemfunktionen wie Argumente, Exit etc.
import numpy as np                           # Numerische Berechnungen, Arrays, lineare Algebra
import pandas as pd                          # CSV-Daten lesen, Tabellen verarbeiten
import pyvista as pv                         # 3D-Visualisierung

# PyVista-Qt Integration
from pyvistaqt import QtInteractor           # Qt-Widget für PyVista-Rendering, ermöglicht interaktive 3D-Ansicht

# Qt Widgets
from PyQt6.QtWidgets import (
    QApplication,                            # Die Haupt-Qt-Anwendung
    QMainWindow,                             # Hauptfenster, in dem Widgets platziert werden
    QWidget,                                 # Basisklasse für alle Widgets
    QVBoxLayout,                             # Vertikales Layout für Widgets
    QFileDialog,                             # Öffnet Dialoge zur Dateiauswahl
    QPushButton,                             # Buttons für Aktionen
    QHBoxLayout,                             # Horizontales Layout für Widgets
    QMessageBox,                             # Zeigt Meldungsboxen (Fehler, Warnungen)
    QSizePolicy,                             # Steuerung der Widget-Größenanpassung
    QInputDialog                             # Dialog für einfache Benutzereingaben (Zahlen, Text)
)

# ======================================================
# Hauptklasse für das CFD-Ergebnis-Viewer-Fenster
# ======================================================

class CFDResultsViewer(QMainWindow):
    def __init__(self):
        super().__init__()                     # Initialisiert das QMainWindow

        self.setWindowTitle("CFD Viewer")  # Fenstertitel
        self.resize(1400, 800)                 # Fenstergröße

        # ==================================================
        # Daten
        # ==================================================

        self.df = None                         # DataFrame für CFD-Daten aus CSV
        self.stl_mesh = None                   # STL-Datei für 3D-Modell
        self.current_mode = None               # Aktueller Modus: 3D-Modell, Velocity, Pressure, Vector

        # Button
        self.scalar_ranges = {
            "Velocity": None,
            "Pressure": None,
            "Vector": None
        }

        # ==================================================
        # Zentrales Layout
        # ==================================================

        central_widget = QWidget()             # Haupt-Widget für QMainWindow
        self.setCentralWidget(central_widget) # Setzt das zentrale Widget
        main_layout = QHBoxLayout(central_widget)  

        # ==================================================
        # PyVista Plotter
        # ==================================================

        self.plotter = QtInteractor(central_widget)  # Interaktives 3D-Plot-Widget
        main_layout.addWidget(self.plotter, stretch=10)  # Füge Plot hinzu, größer als Seitenleiste

        # ==================================================
        # Skalen-Seitenleiste
        # ==================================================

        self.scale_panel = QWidget()           
        self.scale_layout = QVBoxLayout(self.scale_panel)  # Vertikales Layout
        self.scale_panel.setFixedWidth(200)    # Feste Breite der Seitenleiste
        main_layout.addWidget(self.scale_panel) # Füge Seitenleiste ins Hauptlayout

        # ==================================================
        # Skalen-Buttons
        # ==================================================

        self.btn_scale_velocity = QPushButton("Skala Ändern Geschwindigkeit")  # Button für Velocity-Skala
        self.btn_scale_pressure = QPushButton("Skala Ändern Druck")            # Button für Pressure-Skala
        self.btn_scale_vector   = QPushButton("Skala Ändern Vektor")           # Button für Vector-Skala

        for btn in [
            self.btn_scale_velocity,
            self.btn_scale_pressure,
            self.btn_scale_vector
        ]:
            btn.setEnabled(False)            # Anfangs deaktiviert, bis Daten geladen
            self.scale_layout.addWidget(btn) # Fügt Button dazu hinzu

        # Verbindungen: Klick → Skala ändern
        self.btn_scale_velocity.clicked.connect(lambda: self.change_scale("Velocity"))
        self.btn_scale_pressure.clicked.connect(lambda: self.change_scale("Pressure"))
        self.btn_scale_vector.clicked.connect(lambda: self.change_scale("Vector"))

        # ==================================================
        # Top Buttons
        # ==================================================

        top_widget = QWidget()                # Container für obere Aktionsbuttons
        top_layout = QHBoxLayout(top_widget)  # Horizontales Layout
        top_layout.setContentsMargins(10, 10, 10, 10)  # Abstand
        top_layout.setSpacing(20)             # Abstand zwischen Buttons

        self.btn_3d     = QPushButton("3D Modell")     # Button für STL-Anzeige
        self.btn_geschw = QPushButton("Geschwindigkeit")  # Button für Velocity-Plot
        self.btn_druck  = QPushButton("Druck")         # Button für Pressure-Plot
        self.btn_vector = QPushButton("Vektor Plot")   # Button für Vektor-Plot

        self.top_buttons = [                         # Liste aller Top-Buttons
            self.btn_3d,
            self.btn_geschw,
            self.btn_druck,
            self.btn_vector
        ]

        for btn in self.top_buttons:
            btn.setEnabled(False)                     # Anfangs deaktiviert
            btn.setMinimumWidth(120)                  # Minimale Breite
            btn.setMaximumWidth(200)                  # Maximale Breite
            btn.setSizePolicy(
                QSizePolicy.Policy.Expanding,        # Horizontal vergrößerbar
                QSizePolicy.Policy.Fixed             # Vertikal fix
            )
            btn.clicked.connect(self.button_clicked)  # Klick → zentrale Handler-Funktion
            top_layout.addWidget(btn)                  # Zum Layout hinzufügen

        self.addToolBar("Controls").addWidget(top_widget)  # Toolbar hinzufügen
        self.update_button_styles()                       # Setzt initiale Farben der Buttons

        self.create_menu()                                # Menü erstellen

    # ==================================================
    # Menü
    # ==================================================

    def create_menu(self):
        menubar = self.menuBar()                          # Menubar des Fensters
        file_menu = menubar.addMenu("File")              # File-Menü hinzufügen
        file_menu.addAction("Import CSV", self.import_csv)   # CSV Import-Action
        file_menu.addAction("STL-Datei einlesen", self.import_stl) # STL Import-Action
        file_menu.addSeparator()                          # Trennlinie
        file_menu.addAction("Exit", self.close)          # Exit-Action

    # ==================================================
    # CSV Import (funktioniert wieder)
    # ==================================================

    def import_csv(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Import CSV", "", "CSV Files (*.csv)" # Öffnet Dateidialog für CSV
        )
        if not path:                                     # Abbruch, wenn keine Datei gewählt
            return

        try:
            self.df = pd.read_csv(path, header=None)     # CSV-Datei einlesen ohne Header
            self.df.columns = ["X", "Y", "Z", "Pressure", "Velocity"]  # Spalten benennen

            # Buttons aktivieren
            self.btn_geschw.setEnabled(True)
            self.btn_druck.setEnabled(True)
            self.btn_vector.setEnabled(True)
            self.btn_scale_velocity.setEnabled(True)
            self.btn_scale_pressure.setEnabled(True)
            self.btn_scale_vector.setEnabled(True)

            self.show_geschwindigkeit()  # Zeigt Standardplot (Velocity)

        except Exception as e:
            QMessageBox.critical(self, "Fehler", str(e)) # Fehlermeldung bei Fehler

    # ==================================================
    # STL Import
    # ==================================================

    def import_stl(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "STL-Datei einlesen", "", "STL Files (*.stl)"  # Dateidialog für STL
        )
        if not path:
            return

        self.stl_mesh = pv.read(path)  # STL-Datei einlesen als PyVista Mesh
        self.btn_3d.setEnabled(True)   # 3D Button aktivieren
        self.update_button_styles()    # Buttons neu einfärben

    # ==================================================
    # Skalarplots
    # ==================================================

    def show_geschwindigkeit(self):
        self.current_mode = "Velocity"          # Modus setzen
        self.update_button_styles()             # Buttons einfärben
        self.plot_scalar("Velocity", "Geschwindigkeit [m/s]", "Velocity")  # Plot erstellen

    def show_druck(self):
        self.current_mode = "Pressure"
        self.update_button_styles()
        self.plot_scalar("Pressure", "Druck [Pa]", "Pressure")

    def plot_scalar(self, scalar_name, title, key):
        self.plotter.clear()                    # Vorherigen Plot löschen

        points = self.df[["X", "Y", "Z"]].to_numpy()  # Punkte in NumPy-Array
        mesh = pv.PolyData(points)             # PyVista PolyData Mesh
        mesh[scalar_name] = self.df[scalar_name].to_numpy() # Skalarwerte zuweisen

        clim = self.scalar_ranges[key]         # Farbskala ggf. vom Nutzer gesetzt

        self.plotter.add_mesh(
            mesh,
            scalars=scalar_name,
            cmap="jet",
            point_size=5,
            render_points_as_spheres=True,
            clim=clim,
            scalar_bar_args={"title": title}   # Farblegende
        )

        self.plotter.show_grid()               # Gitter anzeigen
        self.plotter.view_xy()                 # Ansicht auf XY-Ebene
        self.plotter.reset_camera()            # Kamera auf alle Punkte anpassen

    # ==================================================
    # Vektorplot
    # ==================================================

    def show_vectors(self):
        self.current_mode = "Vector"           # Modus setzen
        self.update_button_styles()             # Buttons einfärben
        self.plotter.clear()                    # Alten Plot löschen

        points = self.df[["X", "Y", "Z"]].to_numpy()  # Punkte extrahieren
        velocity = self.df["Velocity"].to_numpy()     # Geschwindigkeit extrahieren

        slope, _ = np.polyfit(points[:, 0], points[:, 1], 1)  # mittlere Strömungsrichtung XY
        flow_dir = np.array([1.0, slope, 0.0])                # Richtungsvektor
        flow_dir /= np.linalg.norm(flow_dir)                  # Normieren

        vectors = np.tile(flow_dir, (len(points), 1))         # Kopieren für alle Punkte

        mesh = pv.PolyData(points)
        mesh["Velocity"] = velocity
        mesh["Vectors"] = vectors
        mesh.set_active_vectors("Vectors")                    # Vektoren aktiv setzen

        sampled = mesh.extract_points(np.arange(0, len(points), 10))  # jeden 10. Punkt
        glyphs = sampled.glyph(
            orient="Vectors",         # Richtung
            scale="Velocity",         # Pfeillänge proportional zur Geschwindigkeit
            factor=0.18,              # globaler Skalierungsfaktor
            geom=pv.Arrow()           # Pfeil
        )

        clim = self.scalar_ranges["Vector"]  # Benutzerdefinierte Farbschale

        self.plotter.add_mesh(
            glyphs,
            scalars="Velocity",
            cmap="jet",
            clim=clim,
            scalar_bar_args={"title": "Geschwindigkeit [m/s]"}
        )

        self.plotter.show_grid()
        self.plotter.view_xy()
        self.plotter.reset_camera()

    # ==================================================
    # STL Anzeige
    # ==================================================

    def show_3d_model(self):
        self.current_mode = "STL"
        self.update_button_styles()
        self.plotter.clear()

        self.plotter.set_background("#eeeeee")   # Heller grauer Hintergrund

        self.plotter.add_mesh(
            self.stl_mesh,
            color="#8b5a2b",       # Braun für Modell
            show_edges=True,
            edge_color="#2f2f2f",  # Dunkelgrau für Kanten
            line_width=1.0,
            smooth_shading=True
        )

        self.plotter.reset_camera()

    # ==================================================
    # Skala ändern
    # ==================================================

    def change_scale(self, key):
        min_val, ok1 = QInputDialog.getDouble(
            self, "Min Wert", f"Min Wert für {key} eingeben:", decimals=3
        )
        if not ok1:
            return

        max_val, ok2 = QInputDialog.getDouble(
            self, "Max Wert", f"Max Wert für {key} eingeben:", decimals=3
        )
        if not ok2:
            return

        if min_val >= max_val:
            QMessageBox.warning(
                self, "Fehler", "Min Wert muss kleiner als Max Wert sein!"
            )
            return

        self.scalar_ranges[key] = (min_val, max_val)  # Skala speichern

        if key == "Velocity":
            self.show_geschwindigkeit()
        elif key == "Pressure":
            self.show_druck()
        elif key == "Vector":
            self.show_vectors()

    # ==================================================
    # Button Styles (3 Zustände)
    # ==================================================

    def update_button_styles(self):
        colors = {
            "enabled":  "#5dade2",  # aktiv, aber nicht ausgewählt
            "active":   "#21618c",  # aktuell ausgewählt
            "disabled": "#95a5a6"   # inaktiv
        }

        for btn in self.top_buttons:
            if not btn.isEnabled():
                color = colors["disabled"]
            elif (
                (btn == self.btn_3d     and self.current_mode == "STL") or
                (btn == self.btn_geschw and self.current_mode == "Velocity") or
                (btn == self.btn_druck  and self.current_mode == "Pressure") or
                (btn == self.btn_vector and self.current_mode == "Vector")
            ):
                color = colors["active"]
            else:
                color = colors["enabled"]

            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 8px 16px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: #2980b9;
                }}
            """)

    # ==================================================
    # Button Klick Handler
    # ==================================================

    def button_clicked(self):
        sender = self.sender()  # Herausfinden, welcher Button gedrückt wurde

        if sender == self.btn_3d:
            self.show_3d_model()
        elif sender == self.btn_geschw:
            self.show_geschwindigkeit()
        elif sender == self.btn_druck:
            self.show_druck()
        elif sender == self.btn_vector:
            self.show_vectors()

# ======================================================
# Programmstart
# ======================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)      # Qt-Anwendung erstellen
    viewer = CFDResultsViewer()       # Hauptfenster erstellen
    viewer.show()                     # Fenster anzeigen
    sys.exit(app.exec())              # Qt-Eventloop starten und sauber beenden
