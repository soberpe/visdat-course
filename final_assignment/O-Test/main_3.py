# ------------------------------------------------------------
# Importieren der Standardbibliotheken
import sys
import os
from pathlib import Path
import subprocess

# ------------------------------------------------------------
# Importieren der externen Pakete
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import (FigureCanvasQTAgg, NavigationToolbar2QT)
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QFileDialog,
    QLabel, QPushButton, QLineEdit,
    QGroupBox, QComboBox
)
from PyQt6.QtGui import QAction

# ------------------------------------------------------------
# Importieren der eigene Module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'src')))
import Module as M

class Fenster(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Übertragungsfunktions Berechnung über Freedyn")
        self.setGeometry(100, 100, 1000, 600)

        # ------------------------------------------------------------
        # Anfangs Parameter Rauschen
        self.noise_params = {
            "fs": 100.0,
            "T1": 0.1,
            "T2": 7.0,
            "T3": 8.0,
            "dt": 0.01
        }

        # ------------------------------------------------------------
        # Erstellen Menü BAR
        self.create_menue()

        # ------------------------------------------------------------
        # STATUS BAR
        self.statusBar().showMessage("Bereit")

        # ------------------------------------------------------------
        # Zentrales WIDGET
        Zentrales_widget = QWidget()
        self.setCentralWidget(Zentrales_widget)
        main_layout = QHBoxLayout(Zentrales_widget)

        # ------------------------------------------------------------
        #  BEDIENFELD (LINKS)
        BEDIENFELD = self.Bedienfeld_erstellen()
        main_layout.addWidget(BEDIENFELD)

        # ------------------------------------------------------------
        # Grafikbereich (Rechts)
        plot_widget = QWidget()
        plot_layout = QVBoxLayout(plot_widget)
        plot_layout.setContentsMargins(0, 0, 0, 0)
        plot_layout.setSpacing(5)

        # Figure
        self.fig, self.ax = plt.subplots()
        self.ax.set_title("Warten auf Daten...")
        self.ax.grid(True)

        self.canvas = FigureCanvasQTAgg(self.fig)
        plot_layout.addWidget(self.canvas, 1)

        # Toolbar (UNTER dem Plot)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        plot_layout.addWidget(self.toolbar, 0)

        # Plotbereich zum Hauptlayout hinzufügen
        main_layout.addWidget(plot_widget, 4)


    # ------------------------------------------------------------
    def create_menue(self):
        """Anwendungsmenüs erstellen"""
        menü_bar = self.menuBar()
        file_menu = menü_bar.addMenu("Datei")

        # Simulationsdatei laden 
        open_action = QAction("&Öffnen Simulations-file...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        # Beenden
        exit_action = QAction("Beenden", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
    
    # ------------------------------------------------------------
    # Definition der Funktion Datei öfnnen
    def open_file(self):
        """Öffnet die fds-Datei über den Dateidialog."""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Auswählen Freedyn Simulations Datei", 
            os.path.join(os.path.dirname(__file__), "data_2"),
            "VTK Files (*.fds);;All Files (*.*)"
        )
        
        if not filename:
            return
        
        try:
            self.filefds = filename

            self.statusBar().showMessage(f"Ladet: {filename}", 3000)

            self.setWindowTitle(
                f"Übertragungsfunktion für - {os.path.basename(filename)}"
            )

            self.fdsFilePath = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.filefds))

        except Exception as e:
            self.statusBar().showMessage(
                f"Error Laden Datei: {str(e)}", 5000
            )

    
    # ------------------------------------------------------------
    # Bedienfeld_Erstellen
    def Bedienfeld_erstellen(self):
        """Erstellet ein Bedienfeld mit Feldauswahl und Anzeigeoptionen."""
        Bedienfeld = QGroupBox("Bedienfeld")
        control_layout = QVBoxLayout()
        Bedienfeld.setLayout(control_layout)
                    
        # Field selection
        control_layout.addWidget(QLabel("Thema:"))
        self.field_combo = QComboBox()
        self.field_combo.addItem("Rauschen", userData=1)
        self.field_combo.addItem("Simulation", userData=2)
        self.field_combo.addItem("Übertragungsfunktion", userData=3)
        self.field_combo.currentIndexChanged.connect(self.on_field_changed)
        control_layout.addWidget(self.field_combo)

        # --------------------------------------------
        # Parameter Gruppe – Rauschen
        self.noise_param_group = QGroupBox("Rauschparameter")
        param_layout = QVBoxLayout()
        self.noise_param_group.setLayout(param_layout)

        self.input_fs = QLineEdit(str(self.noise_params["fs"]))
        param_layout.addWidget(QLabel("Abtastfrequenz fs [Hz]"))
        param_layout.addWidget(self.input_fs)

        self.input_T1 = QLineEdit(str(self.noise_params["T1"]))
        param_layout.addWidget(QLabel("T1 – Ramp-Up Ende [s]"))
        param_layout.addWidget(self.input_T1)

        self.input_T2 = QLineEdit(str(self.noise_params["T2"]))
        param_layout.addWidget(QLabel("T2 – Ramp-Down Start [s]"))
        param_layout.addWidget(self.input_T2)

        self.input_T3 = QLineEdit(str(self.noise_params["T3"]))
        param_layout.addWidget(QLabel("T3 – Ramp-Down Ende [s]"))
        param_layout.addWidget(self.input_T3)

        self.input_dt = QLineEdit(str(self.noise_params["dt"]))
        param_layout.addWidget(QLabel("Zeitschritt dt [s]"))
        param_layout.addWidget(self.input_dt)

        control_layout.addWidget(self.noise_param_group)

        # --------------------------------------------
        # Tasten – einmal erzeugen
        self.btn_noise_clalc = QPushButton("Rauschen erzeugen")
        self.btn_noise_clalc.clicked.connect(self.generate_noise)
        control_layout.addWidget(self.btn_noise_clalc)

        self.btn_noise_plot = QPushButton("Rauschen darstellen")
        self.btn_noise_plot.clicked.connect(self.plot_noise)
        control_layout.addWidget(self.btn_noise_plot)

        self.btn_F_safe = QPushButton("Rauschsignal exportieren")
        self.btn_F_safe.clicked.connect(self.safe_Force_function)
        control_layout.addWidget(self.btn_F_safe)

        self.btn_sim_run = QPushButton("Simulation durchführen")
        self.btn_sim_run.clicked.connect(self.run_simulation)
        control_layout.addWidget(self.btn_sim_run)

        self.btn_sim_plot = QPushButton("Grafik darstellen")
        self.btn_sim_plot.clicked.connect(self.plot_simulation)
        control_layout.addWidget(self.btn_sim_plot)

        self.btn_tf_calc = QPushButton("Übertragungsfunktion berechnen")
        self.btn_tf_calc.clicked.connect(self.calc_transfer_function)
        control_layout.addWidget(self.btn_tf_calc)

        self.btn_tf_plot = QPushButton("Übertragungsfunktion darstellen")
        self.btn_tf_plot.clicked.connect(self.plot_transfer_function)
        control_layout.addWidget(self.btn_tf_plot)

        self.btn_tf_safe = QPushButton("Übertragungsfunktion speichern")
        self.btn_tf_safe.clicked.connect(self.safe_transfer_function)
        control_layout.addWidget(self.btn_tf_safe)

        # Alle Buttons ausblenden
        self.btn_sim_run.setVisible(False)
        self.btn_sim_plot.setVisible(False)
        self.btn_tf_calc.setVisible(False)
        self.btn_tf_plot.setVisible(False)
        self.btn_tf_safe.setVisible(False)

        # --------------------------------------------
        # Fixed width for control panel
        Bedienfeld.setFixedWidth(280)

        control_layout.addStretch()  # schiebt alles nach oben
                                
        return Bedienfeld

    # ------------------------------------------------------------
    # Thema Wahl
    def on_field_changed(self, index):
        field_id = self.field_combo.itemData(index)

        # Sichtbarkeit korrekt steuern
        self.noise_param_group.setVisible(False)

        # Alle Buttons ausblenden
        self.btn_noise_clalc.setVisible(False)
        self.btn_noise_plot.setVisible(False)
        self.btn_F_safe.setVisible(False)
        self.btn_sim_run.setVisible(False)
        self.btn_sim_plot.setVisible(False)
        self.btn_tf_calc.setVisible(False)
        self.btn_tf_plot.setVisible(False)
        self.btn_tf_safe.setVisible(False)

        if field_id == 1:
            # Rauschen
            self.noise_param_group.setVisible(True)
            self.btn_noise_clalc.setVisible(True)
            self.btn_noise_plot.setVisible(True)
            self.btn_F_safe.setVisible(True)

        elif field_id == 2:
            # Simulation
            self.btn_sim_run.setVisible(True)
            self.btn_sim_plot.setVisible(True)

        elif field_id == 3:
            # Übertragungsfunktion
            self.btn_tf_calc.setVisible(True)
            self.btn_tf_plot.setVisible(True)
            self.btn_tf_safe.setVisible(True)

    
    # ------------------------------------------------------------
    # Definition Funktion Rauschen erzeugen
    def generate_noise(self):
        try:
            # ------------------------------------------------------------
            # Parameter (aus Eingabefeldern oder Defaults)
            fs = float(self.input_fs.text())
            T1 = float(self.input_T1.text())
            T2 = float(self.input_T2.text())
            T3 = float(self.input_T3.text())
            dt = float(self.input_dt.text())

            # ------------------------------------------------------------
            # Zeitvektor
            t_vec = np.arange(0.0, 10.0 + dt, dt)
            dim = len(t_vec)

            # ------------------------------------------------------------
            # Rauschen erzeugen
            x_noise = M.pink_noise_time_signal(fs, t_vec, T1, T2, T3)

            # ------------------------------------------------------------
            # Als Klassenattribute speichern
            self.dt = dt
            self.t_vec = t_vec
            self.x_noise = x_noise
            self.dim = dim

            self.statusBar().showMessage(
                "Rauschsignal erfolgreich erzeugt",
                3000
            )

        except Exception as e:
            self.statusBar().showMessage(
                f"Fehler bei Rauscherzeugung: {str(e)}",
                6000
            )
    # ------------------------------------------------------------
    # Definition Funktion Rauschen darstellen
    def plot_noise(self):
        # ------------------------------------------------------------
        # Sicherheitsprüfung
        if not hasattr(self, "t_vec") or not hasattr(self, "x_noise"):
            self.statusBar().showMessage(
                "Fehler: Kein Rauschsignal vorhanden",
                5000
            )
            return

        # ------------------------------------------------------------
        # Plot aktualisieren
        self.reset_figure()
        self.ax.plot(self.t_vec, self.x_noise)
        self.ax.set_xlabel("Zeit [s]")
        self.ax.set_ylabel("Kraft [N]")
        self.ax.set_title("Eingangssignal – Rosa Rauschen")
        self.ax.grid(True)

        self.canvas.draw()

        self.statusBar().showMessage(
            "Rauschsignal dargestellt",
            3000
        )

    # ------------------------------------------------------------
    def safe_Force_function(self,Kraft):
            # ------------------------------------------------------------
            # Sicherheitsprüfung
            if not hasattr(self, "t_vec") or not hasattr(self, "x_noise"):
                self.statusBar().showMessage(
                    "Fehler: Rauschsignal noch nicht berechnet (zuerst Rauschen erzeugen)",
                    5000
                )
                return

            # ------------------------------------------------------------
            # Eingangssignal (Kraft) exportieren
            Rauschsignal = np.column_stack((self.t_vec, self.x_noise))

            # Vorschlagsverzeichnis
            default_dir = Path(__file__).parent / "data_2"
            default_dir.mkdir(exist_ok=True)

            filename, _ = QFileDialog.getSaveFileName(
                self,  # Parent = Hauptfenster
                "Exportieren der Rauschsignal-Datei",
                str(default_dir / "Kraft.txt"),
                "Textdatei (*.txt)"
            )

            if not filename:
                return  # Benutzer hat abgebrochen

            np.savetxt(
                filename,
                Rauschsignal,
                header="Zeit [s]\tKraft [N]",
                comments=""
            )

            self.statusBar().showMessage(
                f"Rauschsignal gespeichert",
                6000
            )

            # Für Sicherheitsüberprüfung bei der Funktion run_simulation
            self.F_safe = 1
           
    # ------------------------------------------------------------
    # Definition Funktion Simulation durchführen
    def run_simulation(self):
        try:
            # ------------------------------------------------------------
            # 1) Sicherheitsprüfung
            if not hasattr(self, "F_safe"):
                self.statusBar().showMessage(
                    "Fehler: Kein Eingangssignal vorhanden (zuerst Rauschsignal speichern)",
                    5000
                )
                return

            if not hasattr(self, "fdsFilePath"):
                self.statusBar().showMessage(
                    "Fehler: Keine FreeDyn-Datei geladen",
                    5000
                )
                return

            # ------------------------------------------------------------
            # 3) Simulation mit FreeDyn

            # Muss für den PC angepasst werden.             !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            free_dyn_exe = Path(r"C:\FreeDyn_Release_2024_9\FreeDyn_2024.9\bin\FreeDyn.exe")

            if not free_dyn_exe.exists():
                raise FileNotFoundError("FreeDyn.exe nicht gefunden")

            # Sicherstellen: fdsFilePath OHNE Endung
            fds_base = Path(self.fdsFilePath).with_suffix("")

            command = [str(free_dyn_exe), str(fds_base) + ".fds"]

            self.statusBar().showMessage("Simulation läuft ...")
            subprocess.run(command, check=False)

            # ------------------------------------------------------------
            # Statusprüfung
            status_file = fds_base.with_suffix(".status")

            if not status_file.exists():
                raise FileNotFoundError("Statusdatei nicht gefunden")

            status_text = status_file.read_text(
                encoding="utf-8", errors="ignore"
            )

            if "Computation has been successfully finished" in status_text:
                self.statusBar().showMessage(
                    "Simulation erfolgreich abgeschlossen",
                    4000
                )
            else:
                self.statusBar().showMessage(
                    "Simulation beendet – Fehler im Solver",
                    5000
                )
                return

            # ------------------------------------------------------------
            # Einlesen der Messdaten
            measure_file = fds_base.with_suffix(".mrf")

            if not measure_file.exists():
                raise FileNotFoundError("Messdatei (*.mrf) nicht gefunden")

            self.t_mes, self.y = M.read_mrf(measure_file, measure_id=1)

        except Exception as e:
            self.statusBar().showMessage(
                f"Fehler Simulation: {str(e)}",
                6000
            )

    # ------------------------------------------------------------
    # Definition Funktion Simulation darstellen
    def plot_simulation(self):
        # ------------------------------------------------------------
        # Sicherheitsprüfung
        if not hasattr(self, "t_mes") or not hasattr(self, "y"):
            self.statusBar().showMessage(
                "Fehler: Keine Simulationsdaten vorhanden",
                5000
            )
            return

        # ------------------------------------------------------------
        # Plot aktualisieren (bestehende Achse!)
        self.reset_figure()
        self.ax.plot(self.t_mes, self.y)
        self.ax.set_xlabel("Zeit [s]")
        self.ax.set_ylabel("Auslenkung [mm]")
        self.ax.set_title("Simulationsergebnis (FreeDyn)")
        self.ax.grid(True)

        self.canvas.draw()

        # ------------------------------------------------------------
        self.statusBar().showMessage(
            "Simulationsergebnis dargestellt",
            3000
        )

    # ------------------------------------------------------------
    # Definition Funktion Übertragungsfunktion berechnen
    def calc_transfer_function(self):
        try:
            # ------------------------------------------------------------
            # Sicherheitsprüfungen
            if not hasattr(self, "x_noise"):
                self.statusBar().showMessage(
                    "Fehler: Eingangssignal x_noise nicht vorhanden",
                    5000
                )
                return

            if not hasattr(self, "y"):
                self.statusBar().showMessage(
                    "Fehler: Kein Ausgangssignal vorhanden",
                    5000
                )
                return

            # ------------------------------------------------------------
            # Dimension absichern
            dim = min(len(self.x_noise), len(self.y))

            x = self.x_noise[:dim]
            y = self.y[:dim]

            # ------------------------------------------------------------
            # FFT Eingang / Ausgang
            X = (1.0 / dim) * np.fft.fft(x)
            Y = (1.0 / dim) * np.fft.fft(y)

            # ------------------------------------------------------------
            # Übertragungsfunktion
            H = np.zeros(dim, dtype=complex)

            for i in range(dim):
                if X[i] != 0:
                    H[i] = Y[i] / X[i]

            # Frequenzachse
            f_vec = np.arange(0.0, dim * self.dt, self.dt)

            # ------------------------------------------------------------
            # Impulsantwort
            h = dim * np.fft.ifft(H)

            # ------------------------------------------------------------
            # Als Klassenattribute speichern
            self.X = X
            self.Y = Y
            self.H = H
            self.h = h
            self.f_vec = f_vec
            self.dim = dim

            self.statusBar().showMessage(
                "Übertragungsfunktion erfolgreich berechnet",
                4000
            )

        except Exception as e:
            self.statusBar().showMessage(
                f"Fehler bei Übertragungsfunktion: {str(e)}",
                6000
            )

    # ------------------------------------------------------------
    # Definition Funktion Übertragungsfunktion darstellen
    def plot_transfer_function(self):
        # ------------------------------------------------------------
        # Sicherheitsprüfung
        if not hasattr(self, "H") or not hasattr(self, "h"):
            self.statusBar().showMessage(
                "Fehler: Übertragungsfunktion noch nicht berechnet",
                5000
            )
            return

        # ------------------------------------------------------------
        # Plot vorbereiten
        # Figure zurücksetzen (aber NICHT neu erstellen!)
        self.reset_figure()

        ax1 = self.fig.add_subplot(2, 1, 1)
        ax1.plot(self.f_vec, np.abs(self.H))
        ax1.set_xlabel("Frequenz")
        ax1.set_ylabel("|H(f)|")
        ax1.set_title("Übertragungsfunktion")
        ax1.grid(True)

        ax2 = self.fig.add_subplot(2, 1, 2)
        ax2.plot(self.t_mes[: len(self.h)], self.h.real)
        ax2.set_xlabel("Zeit [s]")
        ax2.set_ylabel("h(t)")
        ax2.grid(True)

        self.fig.tight_layout()
        self.canvas.draw()

        # ------------------------------------------------------------
        self.statusBar().showMessage(
            "Übertragungsfunktion dargestellt",
            3000
        )
    
    # ------------------------------------------------------------
    # Definition Funktion Übertragungsfunktion speichern
    def safe_transfer_function(self):
            # ------------------------------------------------------------
            # Sicherheitsprüfung
            if not hasattr(self, "t_mes") or not hasattr(self, "h"):
                self.statusBar().showMessage(
                    "Fehler: Übertragungsfunktion noch nicht berechnet",
                    5000
                )
                return

            # ------------------------------------------------------------
            # Übertragungsfunktion exportieren
            h = np.column_stack((self.t_mes[: len(self.h)], self.h.real))

            # Vorschlagsverzeichnis
            default_dir = Path(__file__).parent / "data_2"
            default_dir.mkdir(exist_ok=True)

            filename, _ = QFileDialog.getSaveFileName(
                self,  # Parent = Hauptfenster
                "Exportieren der Uebertragungsfunktion",
                str(default_dir / "Uebertragungsfunktion.txt"),
                "Textdatei (*.txt)"
            )

            if not filename:
                return  # Benutzer hat abgebrochen

            np.savetxt(
                filename,
                h,
                header="Zeit [s]\tKraft [N]",
                comments=""
            )

            self.statusBar().showMessage(
                f"Kraftsignal gespeichert: {filename}",
                4000
            )

            # ------------------------------------------------------------
            self.statusBar().showMessage(
                "Übertragungsfunktion gespeichert",
                3000
            )

    # ------------------------------------------------------------
    # Definition Funktion Figure zurücksetzen
    def reset_figure(self):
        self.fig.clear()
        self.ax = self.fig.add_subplot(111)
    # ------------------------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Fenster()
    window.show()
    sys.exit(app.exec())
