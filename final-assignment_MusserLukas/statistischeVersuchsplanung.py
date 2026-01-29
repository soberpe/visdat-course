# ==============================
# Statistische Versuchsplanung
# ==============================


# ================ Imports =================
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QMessageBox, QLabel, QDialog, QHBoxLayout, QTableWidget,
     QTableWidgetItem, QGroupBox, QComboBox, QCheckBox, QPushButton,
     QTextBrowser, QDockWidget
    )
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt

import sys
import os
import numpy as np

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


# =============== Hauptklasse =================
class statistischeVersuchsplanung(QMainWindow):
    
    # ---------------- Initializialisierung der GUI und Datenstrukturen -----------------
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Statistische Versuchsplanung")
        self.resize(1200, 800)

        # Lookup-Tabelle für t-Werte (für Signifikanztest)
        # Format: Freiheitsgrad: {0.05: t-Wert, 0.01: t-Wert, 0.001: t-Wert}
        self.t_value_table = {
            8: {0.05: 2.306, 0.01: 3.355, 0.001: 5.041},
            16: {0.05: 2.12, 0.01: 2.921, 0.001: 4.015},
            32: {0.05: 2.037, 0.01: 2.738, 0.001: 3.622},
            36: {0.05: 2.028, 0.01: 2.719, 0.001: 3.582},
            64: {0.05: 1.998, 0.01: 2.655, 0.001: 3.449},
            72: {0.05: 1.993, 0.01: 2.646, 0.001: 3.431},
            116: {0.05: 1.981, 0.01: 2.619, 0.001: 3.376},
            128: {0.05: 1.979, 0.01: 2.615, 0.001: 3.368},
            144: {0.05: 1.977, 0.01: 2.61, 0.001: 3.359},
            196: {0.05: 1.972, 0.01: 2.601, 0.001: 3.341},
            232: {0.05: 1.97, 0.01: 2.597, 0.001: 3.333},
            256: {0.05: 1.969, 0.01: 2.595, 0.001: 3.329},
            288: {0.05: 1.968, 0.01: 2.593, 0.001: 3.325},
            392: {0.05: 1.966, 0.01: 2.588, 0.001: 3.316},
            396: {0.05: 1.966, 0.01: 2.588, 0.001: 3.315},
            464: {0.05: 1.965, 0.01: 2.586, 0.001: 3.312},
            576: {0.05: 1.964, 0.01: 2.584, 0.001: 3.307},
            784: {0.05: 1.963, 0.01: 2.582, 0.001: 3.303},
            928: {0.05: 1.963, 0.01: 2.581, 0.001: 3.301},
            1568: {0.05: 1.961, 0.01: 2.579, 0.001: 3.297},
            1584: {0.05: 1.961, 0.01: 2.579, 0.001: 3.297},
            1856: {0.05: 1.961, 0.01: 2.578, 0.001: 3.296},
            3136: {0.05: 1.961, 0.01: 2.577, 0.001: 3.294},
            3168: {0.05: 1.961, 0.01: 2.577, 0.001: 3.294},
            6336: {0.05: 1.961, 0.01: 2.577, 0.001: 3.292},
        }

        # Zentrales Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Hauptlayout (links Controls, rechts Tabelle/Plots)
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Control panel
        controls = self.create_controls()
        main_layout.addWidget(controls)

        # Tabelle für Versuchsplan
        exptable = QGroupBox("Versuchsplan")
        self.table = QTableWidget(central_widget)
        exptable.setLayout(QVBoxLayout())
        exptable.layout().addWidget(self.table)
        main_layout.addWidget(exptable)

        # Dock-Bereiche (Plots und Bericht)
        self.setup_dockwidgets()

        # Menüleiste
        self.create_menus()
        self.statusBar().showMessage("Ready")

        # Datenstrukturen für Messwerte und Berechnungsergebnisse initialisieren
        self.experimental_data = None
        self.calculation_results = None

    # ---------------- Dock-Bereiche (Plots und Bericht) ----------------- 
    def setup_dockwidgets(self):
        # Haupteffekte
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.figure_effect = Figure(figsize=(5, 4))
        self.canvas_effect = FigureCanvas(self.figure_effect)
        layout.addWidget(NavigationToolbar(self.canvas_effect, self))
        layout.addWidget(self.canvas_effect)
        self.dock_haupteffekte = self.create_dock("Haupteffekte", widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock_haupteffekte)

        # Signifikanz
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.figure_significance = Figure(figsize=(5, 4))
        self.canvas_significance = FigureCanvas(self.figure_significance)
        layout.addWidget(NavigationToolbar(self.canvas_significance, self))
        layout.addWidget(self.canvas_significance)
        self.dock_signifikanz = self.create_dock("Signifikanz", widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock_signifikanz)

        # Wechselwirkungen
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.figure_interaction = Figure(figsize=(5, 4))
        self.canvas_interaction = FigureCanvas(self.figure_interaction)
        layout.addWidget(NavigationToolbar(self.canvas_interaction, self))
        layout.addWidget(self.canvas_interaction)        
        self.dock_wechselwirkungen = self.create_dock("Wechselwirkungen", widget)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.dock_wechselwirkungen)

        # Bericht
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.report_text = QTextBrowser()
        layout.addWidget(self.report_text)
        self.dock_bericht = self.create_dock("Bericht", widget)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.dock_bericht)

        # Dock-Anordnung
        self.splitDockWidget(self.dock_haupteffekte, self.dock_signifikanz, Qt.Orientation.Horizontal) 
        self.splitDockWidget(self.dock_haupteffekte, self.dock_wechselwirkungen, Qt.Orientation.Vertical) 
        self.splitDockWidget(self.dock_signifikanz, self.dock_bericht, Qt.Orientation.Vertical)

        # Checkbox-Synchronisition
        self.dock_haupteffekte.visibilityChanged.connect( lambda visible: self.effect_combo.setChecked(visible) )
        self.dock_signifikanz.visibilityChanged.connect( lambda visible: self.significance_combo.setChecked(visible) )
        self.dock_wechselwirkungen.visibilityChanged.connect( lambda visible: self.interaction_combo.setChecked(visible) )
        self.dock_bericht.visibilityChanged.connect( lambda visible: self.report_combo.setChecked(visible) )

    # ---------------- Dock-Erstellung -----------------
    def create_dock(self, title, widget): 
        dock = QDockWidget(title, self) 
        dock.setWidget(widget) 
        dock.setFeatures( QDockWidget.DockWidgetFeature.DockWidgetMovable | 
                            QDockWidget.DockWidgetFeature.DockWidgetFloatable | 
                            QDockWidget.DockWidgetFeature.DockWidgetClosable 
                            ) 
        return dock
    
    # ---------------- Menüleiste -----------------
    def create_menus(self):
        menubar = self.menuBar()

        # File-Menü
        file_menu = menubar.addMenu("&File")
        exit_action = QAction("&Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
        reset_action = QAction("&Reset", self)
        reset_action.setShortcut("Ctrl+R")
        reset_action.triggered.connect(self.reset)
        edit_menu.addAction(reset_action)
 
        # Help menu
        help_menu = menubar.addMenu("&Help")
        overview_action = QAction("&Overview", self)
        overview_action.setShortcut("Ctrl+H")
        overview_action.triggered.connect(self.overview)
        help_menu.addAction(overview_action)

    # ---------------- Control panel -----------------
    def create_controls(self):        
        controls = QGroupBox("Controls")
        layout = QVBoxLayout()
        controls.setLayout(layout)

        # Anzahl der Einflussfaktoren
        line = QHBoxLayout()
        line.addWidget(QLabel("Einflussfaktoren"))
        self.factor_combo = QComboBox()
        self.factor_combo.addItems(["2", "3", "4", "5", "6"])
        self.factor_combo.setCurrentText("3")
        self.factor_combo.setFixedWidth(70)
        line.addWidget(self.factor_combo)
        layout.addLayout(line)

        # Anzahl der Stufen
        line = QHBoxLayout()
        line.addWidget(QLabel("Stufen"))
        self.level_combo = QComboBox()
        self.level_combo.addItems(["2"])
        self.level_combo.setCurrentText("2")
        self.level_combo.setFixedWidth(70)
        line.addWidget(self.level_combo)
        layout.addLayout(line)

        # Anzahl der Wiederholungen
        line = QHBoxLayout()
        line.addWidget(QLabel("Wiederholungen"))
        self.repet_combo = QComboBox()
        self.repet_combo.addItems(["3", "5", "10","30", "50", "100"])
        self.repet_combo.setCurrentText("3")
        self.repet_combo.setFixedWidth(70)
        line.addWidget(self.repet_combo)
        layout.addLayout(line)

        # Experimental-design-Button
        button = QPushButton("Create experimental design")
        button.clicked.connect(self.CreateTable)
        layout.addWidget(button)

        # Run-experimental-Button
        button = QPushButton("Run experimental")
        button.clicked.connect(self.run_experimental)
        layout.addWidget(button)

        # Checkbox Haupeffekte
        line = QHBoxLayout()
        line.addWidget(QLabel("Haupteffekte"))
        self.effect_combo = QCheckBox()
        self.effect_combo.setChecked(True)
        self.effect_combo.setFixedWidth(70)
        self.effect_combo.stateChanged.connect(self.toggle_haupteffekte)
        line.addWidget(self.effect_combo)
        layout.addLayout(line)

        # Checkbox Wechselwirkungen
        line = QHBoxLayout()
        line.addWidget(QLabel("Wechselwirkungen"))
        self.interaction_combo = QCheckBox()
        self.interaction_combo.setChecked(True)
        self.interaction_combo.setFixedWidth(70)
        self.interaction_combo.stateChanged.connect(self.toggle_wechselwirkungen)
        line.addWidget(self.interaction_combo)
        layout.addLayout(line)
        
        # Checkbox Signifikanztest
        line = QHBoxLayout()
        line.addWidget(QLabel("Signifikanztest"))
        self.significance_combo = QCheckBox()
        self.significance_combo.setChecked(True)
        self.significance_combo.setFixedWidth(70)
        self.significance_combo.stateChanged.connect(self.toggle_signifikanz) 
        line.addWidget(self.significance_combo)
        layout.addLayout(line)

        # Checkbox Bericht
        line = QHBoxLayout()
        line.addWidget(QLabel("Bericht"))
        self.report_combo = QCheckBox()
        self.report_combo.setChecked(True)
        self.report_combo.setFixedWidth(70)
        self.report_combo.stateChanged.connect(self.toggle_bericht)
        line.addWidget(self.report_combo)
        layout.addLayout(line)
        
        # Calculate-Button
        button = QPushButton("Calculate")
        button.clicked.connect(self.calculate)
        layout.addWidget(button)

        # Show-calculation-Button
        button = QPushButton("Show calculation")
        button.clicked.connect(self.show_calculation)
        layout.addWidget(button)

        # Push controls to top
        layout.addStretch()       
        # Fixed width for control panel
        controls.setFixedWidth(200)

        return controls

    # ---------------- Dock-Visivilität -----------------
    def toggle_haupteffekte(self, state): 
        self.dock_haupteffekte.setVisible(bool(state))
    def toggle_signifikanz(self, state): 
        self.dock_signifikanz.setVisible(bool(state))
    def toggle_wechselwirkungen(self, state): 
        self.dock_wechselwirkungen.setVisible(bool(state))
    def toggle_bericht(self, state): 
        self.dock_bericht.setVisible(bool(state))

    # ---------------- Hilfe / Overview -----------------    
    def overview(self):
        
        # Ordner der aktuellen .py Datei ermitteln
        base_path = os.path.dirname(os.path.abspath(__file__))
        
        # help_overview-txt im selben Ordner suchen 
        file_path = os.path.join(base_path, "help_overview.txt")
        
        # Datei prüfen ob vorhanden
        if not os.path.exists(file_path):
            QMessageBox.warning(self, "Error", f"Help file '{file_path}' not found.")
            return
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fehler beim Lesen der Datei:\n{e}")
            return

        # Dialog erstellen
        dialog = QDialog(self)
        dialog.setWindowTitle("Overview / Help")
        dialog.setMinimumSize(800, 400)

        layout = QVBoxLayout(dialog)
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setText(text)
        layout.addWidget(text_edit)

        dialog.exec()

    # ---------------- Versuchsplan erzeugen -----------------
    def CreateTable(self):
        #table = QGroupBox("Table")
        #layout = QVBoxLayout()
        #table.setLayout(layout)

        num_factors = int(self.factor_combo.currentText())
        num_levels = int(self.level_combo.currentText())

        num_rows = num_levels ** num_factors
        num_cols = num_factors

        self.table.clear()
        self.table.setRowCount(num_rows)
        self.table.setColumnCount(num_cols)
        self.table.setFixedWidth(min(num_cols*58+20, 200))

        headers = [f"Factor {i+1}" for i in range(num_cols)]
        self.table.setHorizontalHeaderLabels(headers)
        self.table.resizeColumnsToContents()
        
        # Fill the table with design combinations
        for row in range(num_rows):
            for col in range(num_cols):
                level = (row // (num_levels ** col)) % num_levels
                # Normalize levels to range [-1, +1]
                normalized_level = -1 + 2 * level / (num_levels - 1)
                item = QTableWidgetItem(f"{normalized_level:.0f}")
                self.table.setItem(row, col, item)

    # ---------------- Wahl der Dateneingabe -----------------
    def run_experimental(self):
        if self.table.rowCount() == 0:
            QMessageBox.warning(self, "Error", "Bitte zuerst einen Versuchsplan erzeugen.")
            return 
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Insert Data")
        msg.setText("How do you want to insert the data?")
        import_button = msg.addButton("Import", QMessageBox.ButtonRole.AcceptRole)
        manual_button = msg.addButton("Manuell", QMessageBox.ButtonRole.AcceptRole)
        cancel_button = msg.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
        msg.exec()
        
        if msg.clickedButton() == import_button:
            QMessageBox.information(self, "Info", "Demo version cannot import data")
            #self.importData
            pass
        elif msg.clickedButton() == manual_button:
            self.manualData()
            pass
        elif msg.clickedButton() == cancel_button:
            QMessageBox.close

    # ---------------- Manuelle Dateneingabe -----------------
    def manualData(self):
        dialog = QDialog(self)       
        dialog.setWindowTitle("Manuelle Dateneingabe")
        dialog.setMinimumSize(600, 400)
        
        layout = QVBoxLayout(dialog)

        num_factors = int(self.factor_combo.currentText())
        num_levels = int(self.level_combo.currentText())
        num_repet = int(self.repet_combo.currentText())
        
        num_rows = self.table.rowCount()
        num_cols = num_repet

        self.data_table = QTableWidget(num_rows, num_cols)
        self.data_table.setHorizontalHeaderLabels([f"Messung {i+1}" for i in range(num_cols)])
        layout.addWidget(QLabel("Bitte Messwerte eingeben:"))
        layout.addWidget(self.data_table)

        save_btn = QPushButton("Speichern")
        layout.addWidget(save_btn)
        load_btn = QPushButton("Vorhandene Daten laden")
        layout.addWidget(load_btn)

        # Daten speichern
        def save_data():
            data = []
            for r in range(num_rows):
                row_values = []
                for c in range(num_cols):
                    item = self.data_table.item(r, c)
                    row_values.append(item.text() if item else "")
                data.append(row_values)

            self.experimental_data = {
                "factors": num_factors,
                "levels": num_levels,
                "repetitions": num_repet,
                "data": data
            }
            QMessageBox.information(self, "Info", "Daten wurden gespeichert.")
        # Daten laden    
        def load_existing_data():
            if self.experimental_data is None:
                QMessageBox.warning(self, "Error", "Keine gespeicherten Daten gefunden.")
                return False

            for r in range(num_rows):
                for c in range(num_cols):
                    val = self.experimental_data["data"][r][c]
                    if val is not None:
                        self.data_table.setItem(r, c, QTableWidgetItem(str(val)))

        
        save_btn.clicked.connect(save_data)
        load_btn.clicked.connect(load_existing_data)
            
        dialog.exec()
    
    # ---------------- Import Dateneingabe -----------------
    #def importData(self):   

    # ---------------- Berechnung der Effekte und Wechselwirkungen -----------------
    def calculate(self):
        if self.experimental_data is None:
            QMessageBox.warning(self, "Error", "No experimental data available.")
            return

        num_factors = self.experimental_data["factors"]

        # Messdaten in numpy-Array umwandeln
        data = np.array(self.experimental_data["data"], dtype=float)
        # Mittelwerte pro Versuch berechnen (über alle Wiederholungen)
        means = data.mean(axis=1)
        
        # Haupteffekte berechnen
        effects = {}
        if self.effect_combo.isChecked():
            for i in range(num_factors):
                effect_sum = 0
                for j in range(self.table.rowCount()):
                    factor_level = float(self.table.item(j, i).text())
                    effect_sum += factor_level * means[j]
                effects[i] = round(effect_sum / (self.table.rowCount()/2), 4)

        # Wechselwirkungen berechnen
        interactions = {}
        if self.interaction_combo.isChecked():
            for i in range(num_factors):
                for j in range(i+1, num_factors):
                    interaction_sum = 0
                    for k in range(self.table.rowCount()):
                        level_i = float(self.table.item(k, i).text())
                        level_j = float(self.table.item(k, j).text())
                        interaction_sum += level_i * level_j * means[k]
                    interactions[(i, j)] = round(float(interaction_sum / (self.table.rowCount()/2)), 4)

        # Ergebnisse speichern
        self.calculation_results = {
            "overall_mean": float(means.mean()),
            "effects": effects,
            "interactions": interactions,
            "effect_significance": {},
            "interaction_significance": {}
        }

        QMessageBox.information(self, "Info", "Berechnung abgeschlossen.")

    # ---------------- t-Wert Interpolation -----------------
    def get_t_values(self, df):
        # Direkter Treffer (Immer der Fall bei Standardversuchsplan)
        if df in self.t_value_table:
            t = self.t_value_table[df]
            return (t[0.05],t[0.01],t[0.001])
        
        # Lookup-Tabelle nach Freihietsgraden sortieren
        sorted_df = sorted(self.t_value_table.keys())
        lower_df = None
        upper_df = None

        # Nachbarn suchen
        for d in sorted_df:
            if d < df:
                lower_df = d
            elif d > df:
                upper_df = d
                break
        
        # Falls nur ein Nachbar vorhanden
        if lower_df is None:
            t_low = self.t_value_table[upper_df]
            return (t_low[0.05], t_low[0.01], t_low[0.001])
        elif upper_df is None:
            t_up = self.t_value_table[lower_df]
            return (t_up[0.05], t_up[0.01], t_up[0.001])

        # Lineare Interpolation
        ratio = (df - lower_df) / (upper_df - lower_df)

        def interp(alpha): 
            return round( 
                self.t_value_table[lower_df][alpha] 
                + ratio * (self.t_value_table[upper_df][alpha] 
                - self.t_value_table[lower_df][alpha]), 4 )
        
        return interp(0.05), interp(0.01), interp(0.001)

    # ---------------- Anzeige der Berechnungsergebnisse -----------------
    def show_calculation(self):
        if self.calculation_results is None:
            QMessageBox.warning(self, "Error", "Bitte zuerst Berechnungen durchführen")
            return
        
        if self.effect_combo.isChecked():
            self.show_effekt()
        else:
            self.figure_effect.clear()
            self.canvas_effect.draw()

        if self.interaction_combo.isChecked():
            self.show_interaction()
        else:
            self.figure_interaction.clear()
            self.canvas_interaction.draw()

        if self.significance_combo.isChecked():
            self.show_significance()
        else:
            self.figure_significance.clear()
            self.canvas_significance.draw()
        
        if self.report_combo.isChecked():
            self.show_report()
        else:
            self.report_text.clear()
            self.report_text.setPlainText("")

    # ---------------- Haupteffekte anzeigen -----------------
    def show_effekt(self):
  
        num_factors = self.experimental_data["factors"]
        effects = self.calculation_results["effects"]
        overall_mean = self.calculation_results["overall_mean"]

        mean_low = np.zeros(num_factors)
        mean_high = np.zeros(num_factors)
        
        # Berechnung der Mittelwerte für niedrige und hohe Stufe
        for i in range(num_factors):
            e = effects[i]
            mean_low[i] = overall_mean - e/2
            mean_high[i] = overall_mean + e/2

        self.figure_effect.clear()
        ax = self.figure_effect.add_subplot(111)
        
        x = [0, 1]
        for i in range(num_factors):
            y = [mean_low[i], mean_high[i]]
            ax.plot(x, y, marker="x", linewidth=2, label=f"F{i+1}")
        
        ax.set_ylabel("Zielwert")
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["-", "+"])
        ax.set_ylim(min(0, min(mean_low), min(mean_high)), max(0, max(mean_low), max(mean_high)))
        ax.set_xlabel("Faktorstufen")
        ax.legend(loc="best", fontsize=6)
        ax.grid(True)

        self.figure_effect.tight_layout()
        self.canvas_effect.draw()

    # ---------------- Wechselwirkungen anzeigen -----------------
    def show_interaction(self):
       
        num_factors = self.experimental_data["factors"]
        data = np.array(self.experimental_data["data"], dtype=float)
        means = data.mean(axis=1)
        
        self.figure_interaction.clear()
        
        num_rows = num_factors - 1
        num_cols = num_factors - 1
        
        # Untere Dreiecksmatrix der Interaktionsplots
        for f1 in range(1, num_factors):  # Faktor auf x-Achse (ab 1)
            for f2 in range(f1):  # Legende-Faktor (0 bis f1-1)
                ax = self.figure_interaction.add_subplot(num_rows, num_cols, (f1 - 1) * num_cols + f2 + 1)
                
                # Stufenwerte für die Faktoren
                levels_f1 = np.array([float(self.table.item(r, f1).text()) for r in range(self.table.rowCount())])
                levels_f2 = np.array([float(self.table.item(r, f2).text()) for r in range(self.table.rowCount())])
                
                # Berechne Mittelwerte für jede Kombination
                mask_low_low = (levels_f1 == -1) & (levels_f2 == -1)
                mask_high_low = (levels_f1 == 1) & (levels_f2 == -1)
                mask_low_high = (levels_f1 == -1) & (levels_f2 == 1)
                mask_high_high = (levels_f1 == 1) & (levels_f2 == 1)
                
                # Plot
                x = [0, 1]
                y_f2_low = [means[mask_low_low].mean(), means[mask_high_low].mean()]
                y_f2_high = [means[mask_low_high].mean(), means[mask_high_high].mean()]
                
                ax.plot(x, y_f2_low, color=("#303030"), marker="o", linewidth=1, label=f"F{f2+1}: −")
                ax.plot(x, y_f2_high, color=("#8F8F8F"), marker="o", linewidth=1, label=f"F{f2+1}: +")
                
                ax.set_xlabel(f"Faktor {f1+1}")
                ax.set_ylabel("Zielwert")
                ax.set_xticks([0, 1])
                ax.set_xticklabels(["−", "+"])
                ax.set_title(f"F{f1+1}×F{f2+1}")
                ax.legend(loc="best", fontsize=6)
                ax.grid(True, alpha=0.3)
        
        self.figure_interaction.tight_layout()
        self.canvas_interaction.draw()

    # ---------------- Signifikanztest anzeigen -----------------
    def show_significance(self):
        
        num_factors = self.experimental_data["factors"]
        num_levels = self.experimental_data["levels"]
        data = np.array(self.experimental_data["data"], dtype=float)
        variances = data.var(axis=1)

        lendata = len(self.experimental_data["data"])
        lenexp = num_factors ** num_levels

        # Standardfehler der Effekte      
        standardfehler = (4/lendata*variances.mean())**0.5

        # Freiheitsgrade
        df = lendata - lenexp

        # t-Werte
        t5, t1, t01 = self.get_t_values(df)

        # Schwellenwerte
        schwellwertal5 = t5 * standardfehler
        schwellwertal1 = t1 * standardfehler
        schwellwertal01 = t01 * standardfehler

        self.calculation_results["schwellwert"]={
            "5%": schwellwertal5,
            "1%": schwellwertal1,
            "0.1%": schwellwertal01
        }

        # Klassifikation der Haupteffekte
        for fak, eff in self.calculation_results['effects'].items():
            abs_eff = abs(eff)
            if abs_eff >= schwellwertal01:
                self.calculation_results["effect_significance"][fak] = "hochsignifikant"
            elif abs_eff >= schwellwertal1:
                self.calculation_results["effect_significance"][fak] = "signifikant"
            elif abs_eff >= schwellwertal5:
                self.calculation_results["effect_significance"][fak] = "moderat signifikant"
            else:
                self.calculation_results["effect_significance"][fak] = "nicht signifikant"

        # Klassifiziere alle Wechselwirkungen
        for (f1, f2), int in self.calculation_results['interactions'].items():
            abs_int = abs(int)
            if abs_int >= schwellwertal01:
                self.calculation_results["interaction_significance"][(f1, f2)] = "hochsignifikant"
            elif abs_int >= schwellwertal1:
                self.calculation_results["interaction_significance"][(f1, f2)] = "signifikant"
            elif abs_int >= schwellwertal5:
                self.calculation_results["interaction_significance"][(f1, f2)] = "moderat signifikant"
            else:
                self.calculation_results["interaction_significance"][(f1, f2)] = "nicht signifikant"

        # Plot erstellen
        self.figure_significance.clear()
        ax = self.figure_significance.add_subplot(111)
        
        labels = []
        values = []
        colors = []
        
        # Haupteffekte
        for fac, eff in self.calculation_results['effects'].items():
            labels.append(f"F{fac+1}")
            abs_eff = abs(eff)
            values.append(abs_eff)
            sig = self.calculation_results["effect_significance"].get(fac, "nicht signifikant")
            colors.append(self._sig_color(sig))

        # Wechselwirkungen
        for (f1, f2), interaction in self.calculation_results['interactions'].items():
            labels.append(f"F{f1+1}×F{f2+1}")
            abs_interaction = abs(interaction)
            values.append(abs_interaction)
            sig  = self.calculation_results["interaction_significance"].get((f1, f2), "nicht signifikant")
            colors.append(self._sig_color(sig))

        # Create bar chart
        x_pos = np.arange(len(labels))
        ax.bar(x_pos, values, color=colors, edgecolor='black', linewidth=1.2)
        
        # Add threshold lines        
        ax.axhline(y=schwellwertal01, color=self._sig_color("hochsignifikant"), linestyle='--', linewidth=2, 
                   label=f'Hochsignifikant (99.9%) {round(schwellwertal01, 4)}')
        ax.axhline(y=schwellwertal1, color=self._sig_color("signifikant"), linestyle='--', linewidth=2, 
                   label=f'Signifikant (99.0%) {round(schwellwertal1, 4)}')
        ax.axhline(y=schwellwertal5, color=self._sig_color("moderat signifikant"), linestyle='--', linewidth=2, 
                   label=f'Moderat signifikant (95.0%) {round(schwellwertal5, 4)}')
        
        # Set labels and title
        ax.set_xlabel("Einflussgröße", fontsize=10)
        ax.set_ylabel("Effekte", fontsize=10)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(labels)
        ax.legend(loc='best', fontsize=6)
        ax.grid(True, alpha=0.3, axis='y')
        
        self.figure_significance.tight_layout()
        self.canvas_significance.draw()

    # ---------------- Signifikanzfarbe bestimmen -----------------
    def _sig_color(self, significance):
        if significance == "hochsignifikant":
            return '#2ca02c'
        elif significance == "signifikant":
            return '#ff7f0e'
        elif significance == "moderat signifikant":
            return '#d62728'
        else:
            return '#808080'
        
    # ---------------- Bericht anzeigen -----------------
    def show_report(self):
        
        txt = []
        
        txt.append(f"=== Berechnungsergebnisse ===\n\n")
        txt.append(f"Gesamtmittelwert: {round(self.calculation_results['overall_mean'], 4)}\n\n")
        
        txt.append("Haupteffekte:\n")
        for fak, eff in self.calculation_results['effects'].items():
            sig = self.calculation_results["effect_significance"].get(fak, "nicht berechnet")
            txt.append(f"  Faktor {fak+1}: {round(eff, 4)} -> {sig}\n")
        txt.append("\n")

        txt.append("Wechselwirkungen:\n")
        for (f1, f2), interaction in self.calculation_results['interactions'].items():
            sig = self.calculation_results["interaction_significance"].get((f1, f2), "nicht berechnet")
            txt.append(f"  Faktoren {f1+1} & {f2+1}: {round(interaction, 4)} -> {sig}\n")
        txt.append("\n")

        txt.append("Signifikant anhand der folgenden Schwellenwerte:\n")
        schwellwerte = self.calculation_results.get("schwellwert", {})
        txt.append(f"   Moderat signifikant: {round(schwellwerte.get('5%', 0), 4)}\n")
        txt.append(f"   Signifikant: {round(schwellwerte.get('1%', 0), 4)}\n")
        txt.append(f"   Hochsignifikant: {round(schwellwerte.get('0.1%', 0), 4)}\n")
        txt.append("\n")

        self.report_text.setText("".join(txt))
        self.report_text.setReadOnly(True)
        self.report_text.setStyleSheet("QTextBrowser { background-color: white; color: black; font-size: 10pt; }")

    # ---------------- Reset-Funktion -----------------
    def reset(self):
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        self.experimental_data = None
        self.calculation_results = None
        self.report_text.clear()
        
        self.figure_effect.clear()
        self.canvas_effect.draw()

        self.figure_interaction.clear()
        self.canvas_interaction.draw()

        self.figure_significance.clear()
        self.canvas_significance.draw()

        QMessageBox.information(self, "Reset", "Application has been reset.")

    # ---------------- Schließen der Anwendung -----------------
    def close(self, event):
        reply = QMessageBox.question(
            self,
            "Unsaved Changes",
            "Do you want to save your data before closing?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
        )

        if reply == QMessageBox.StandardButton.Cancel:
            QMessageBox.close

        elif reply == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "Info", "Demo version cannot be saved")
            QMessageBox.close
            pass

        elif reply == QMessageBox.StandardButton.No:
            sys.exit()  # Close without saving
            pass


# =============== Programmstart =================
def main():
    app = QApplication(sys.argv)
    window = statistischeVersuchsplanung()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

