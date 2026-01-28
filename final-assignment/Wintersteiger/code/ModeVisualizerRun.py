"""
Mode Visualizer – 16 LVM Dateien (PyQt6)
Peaks + qualitative Moden als deformierter Prüfstand

IDEA / ZIEL:
- Du wählst 16 .lvm Dateien aus (4 Ecken * 2 Anregungsrichtungen X/Y * 2 Messrichtungen x/y).
- Du wählst einen Frequenzbereich (f_min .. f_max).
- Du definierst einen Schwellwert (Level): |imag| >= level.
- In jeder Kurve werden lokale Peaks (positive UND negative) erkannt.
- Alle Peak-Frequenzen aus allen Kurven werden zusammengefasst ("Clustering") -> Modenfrequenzen.
- Links wird der Imaginärteil über Frequenz geplottet.
- Rechts wird eine qualitative Verformung des "Prüfstandsrahmens" bei einer ausgewählten Mode gezeigt (Animation).

WICHTIG:
- Die Modeform ist qualitativ (anschaulich), keine vollständige experimentelle Modalanalyse.
- Wir nutzen nur den Imaginärteil als "Auslenkungsmaß" an den 4 Ecken.
"""

# -------------------------------------------------
# Imports
# -------------------------------------------------
import os
import sys
import numpy as np
import pandas as pd

# PyQt6 Widgets: Bausteine der grafischen Oberfläche
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog, QDoubleSpinBox,
    QSpinBox, QMessageBox, QPlainTextEdit, QComboBox, QCheckBox,
    QGroupBox
)

# Matplotlib: Figure (Zeichenfläche), Animation, und Qt-Einbettung
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar


# -------------------------------------------------
# Funktion: LVM-Datei einlesen
# -------------------------------------------------
def load_lvm_as_df(path: str, freq_scale: float = 1.0) -> pd.DataFrame:
    """
    Liest eine .lvm Datei (tab-getrennt) ein und gibt einen DataFrame zurück.

    Erwartung:
    - Datei enthält zwei Spalten (ohne Header):
      Spalte 1: Frequenz
      Spalte 2: Imaginärteil
    - erste Zeile wird übersprungen (z.B. allgemeiner Header in LVM)

    freq_scale:
    - Skaliert Frequenzwerte (hier fix auf 0.1 gesetzt, weil Messsystem in 10*Hz ausgibt).

    Rückgabe:
    - DataFrame mit Spalten: "freq", "imag"
    """
    df = pd.read_csv(
        path,
        sep="\t",        # Tab als Trennzeichen
        skiprows=1,      # erste Zeile überspringen
        header=None,     # Datei hat keinen Spaltenheader
        decimal=",",     # Dezimaltrennzeichen ist Komma
        engine="python"  # robuster Parser
    )

    # Spalten benennen
    df.columns = ["freq", "imag"]

    # -------- Frequenz direkt skalieren --------
    # In deinen Messdaten wird die Frequenz offenbar als 10*Hz gespeichert.
    # Daher multiplizieren wir mit 0.1, um echte Hz zu erhalten.
    freq_scale = 0.1
    df["freq"] = df["freq"] * freq_scale

    # Sortieren nach Frequenz ist wichtig für Peak-Suche
    df = df.sort_values("freq").reset_index(drop=True)
    return df


# -------------------------------------------------
# Peaks: positive / negative (wie im Plotter)
# -------------------------------------------------
def find_positive_peaks(df: pd.DataFrame, level: float):
    """
    Findet POSITIVE Peaks (lokale Maxima) der Imaginärteil-Kurve.

    Peak-Bedingung:
    - y[i-1] < y[i] > y[i+1]   -> lokales Maximum
    - y[i] >= level            -> Peak muss über Schwellwert liegen

    Rückgabe:
    - Liste von (freq, imag) Tupeln für jedes gefundene Maximum.
    """
    # Wenn df leer/zu kurz ist, kann man keine lokalen Maxima finden
    if df is None or df.empty or len(df) < 3:
        return []

    # Umwandlung in numpy Arrays für schnellen Zugriff
    x = df["freq"].to_numpy()
    y = df["imag"].to_numpy()

    peaks = []
    # Wir starten bei i=1 und enden bei len-2,
    # weil wir i-1 und i+1 brauchen.
    for i in range(1, len(df) - 1):
        if y[i - 1] < y[i] and y[i] > y[i + 1] and y[i] >= level:
            peaks.append((float(x[i]), float(y[i])))
    return peaks


def find_negative_peaks(df: pd.DataFrame, level: float):
    """
    Findet NEGATIVE Peaks (lokale Minima).

    Peak-Bedingung:
    - y[i-1] > y[i] < y[i+1]   -> lokales Minimum
    - y[i] <= -level           -> Minimum muss unter -level liegen

    Rückgabe:
    - Liste von (freq, imag) Tupeln für jedes gefundene Minimum.
    """
    if df is None or df.empty or len(df) < 3:
        return []

    x = df["freq"].to_numpy()
    y = df["imag"].to_numpy()

    peaks = []
    for i in range(1, len(df) - 1):
        if y[i - 1] > y[i] and y[i] < y[i + 1] and y[i] <= -level:
            peaks.append((float(x[i]), float(y[i])))
    return peaks


def peaks_from_df(df: pd.DataFrame, level: float):
    """
    Kombiniert positive und negative Peaks (Maxima + Minima) in einer Liste.

    Danach wird nach Frequenz sortiert, damit:
    - die Ausgabe übersichtlich ist
    - Clustering später einfacher ist
    """
    peaks = find_positive_peaks(df, level) + find_negative_peaks(df, level)
    peaks = sorted(peaks, key=lambda t: t[0])  # Sortieren nach freq
    return peaks


# -------------------------------------------------
# Clustering (Moden aus vielen Peaks)
# -------------------------------------------------
def cluster_modes(all_peak_freqs: list[np.ndarray], tol: float, min_count: int) -> np.ndarray:
    """
    Aus den Peak-Frequenzen vieler Kurven werden "Moden" gebildet.

    Grundproblem:
    - Jede Kurve hat ihre Peaks bei leicht unterschiedlichen Frequenzen
      (Messrauschen, unterschiedliche FRF, etc.)
    - Trotzdem gehört ein Peak bei z.B. 46.05 Hz und 46.30 Hz oft zur selben Mode.

    Lösung:
    - "clustern" aller Peakfrequenzen:
      Peaks, die näher als tol Hz beieinander liegen, kommen in denselben Cluster.
    - Cluster, die weniger als min_count Peaks enthalten, werden verworfen
      (Rauschpeaks sollen keine Mode erzeugen).

    Rückgabe:
    - Array von Modenfrequenzen = Mittelwert jedes gültigen Clusters.
    """
    flat_list = []

    # Alle nicht-leeren Peak-Frequenzarrays sammeln
    for arr in all_peak_freqs:
        if arr is not None and len(arr) > 0:
            flat_list.append(arr)

    # Wenn überhaupt keine Peaks gefunden wurden:
    if not flat_list:
        return np.array([])

    # Alles zu einem großen Array zusammenfügen
    flat = np.concatenate(flat_list)
    if flat.size == 0:
        return np.array([])

    # Sortieren ermöglicht einfaches "Durchgehen" von links nach rechts
    flat.sort()

    # erster Cluster startet mit erstem Peak
    clusters = [[flat[0]]]

    # alle weiteren Peaks einsortieren
    for f in flat[1:]:
        # Vergleich mit Mittelwert des letzten Clusters
        if abs(f - np.mean(clusters[-1])) <= tol:
            clusters[-1].append(f)
        else:
            # neuer Cluster
            clusters.append([f])

    # Aus jedem Cluster die Modefrequenz bestimmen (Mittelwert)
    # Nur Cluster mit genug "Stimmen" (min_count) werden akzeptiert.
    modes = [float(np.mean(c)) for c in clusters if len(c) >= int(min_count)]
    return np.array(modes, dtype=float)


def value_at(freq: np.ndarray, y: np.ndarray, f0: float, df: float) -> float:
    """
    Liefert einen y-Wert in der Nähe der Frequenz f0.

    Problem:
    - f0 liegt nicht immer exakt auf einem Messpunkt
    - und der Peak kann leicht neben f0 liegen

    Lösung:
    - wir nehmen das Maximum im Bereich [f0-df, f0+df]
      -> robust, weil wir so den Peak "treffen", auch wenn er leicht verschoben ist

    Wenn in dem Fenster keine Punkte liegen:
    - wir nehmen den nächstgelegenen Frequenzpunkt.
    """
    m = (freq >= f0 - df) & (freq <= f0 + df)
    if np.any(m):
        return float(np.max(y[m]))

    # fallback: nächster Punkt
    idx = int(np.argmin(np.abs(freq - f0)))
    return float(y[idx])


# -------------------------------------------------
# GUI Klasse (auf Basis des Plotter-Layouts)
# -------------------------------------------------
class ModeVisualizer16(QWidget):
    """
    Diese Klasse ist das Hauptfenster.

    Sie enthält:
    - Dateiauswahl (16 Dateien)
    - Parameter (Frequenzbereich, Peak-Level, Clustering, Fenster, Scale)
    - Plotbereich (Matplotlib, 2 Achsen)
    - Log-/Ergebnisfeld
    """

    def __init__(self):
        super().__init__()

        # Titel + Fenstergröße
        self.setWindowTitle("Mode Visualizer (16 LVM) – Peaks & Verformung")
        self.resize(1900, 1000)

        # Erzeuge die 16 Dateischlüssel:
        # P{1..4}_{X/Y}_{x/y}
        self.keys = [f"P{p}_{ex}_{m}"
                     for p in range(1, 5)
                     for ex in ("X", "Y")
                     for m in ("x", "y")]

        # Hier wird gespeichert, welche Datei zu welchem Key gehört
        self.paths: dict[str, str] = {k: "" for k in self.keys}

        # Hier werden die geladenen Daten (als DataFrames) gespeichert
        self.dfs: dict[str, pd.DataFrame] = {}

        # Hier werden Peaks pro Kurve gespeichert
        self.peaks: dict[str, list[tuple[float, float]]] = {}

        # Hier werden die gefundenen Modefrequenzen gespeichert
        self.modes = np.array([], dtype=float)

        # Geometrie für die Darstellung: ein Quadrat (4 Ecken)
        self.pts = np.array([
            [0, 0],
            [1, 0],
            [1, 1],
            [0, 1]
        ], dtype=float)

        # Animation-Handle: muss gespeichert werden, sonst stoppt Animation
        self.anim = None

        # UI aufbauen (Buttons, Spinboxen, etc.)
        self._build_ui()

        # Matplotlib Setup:
        # Figure = Zeichenfläche, Canvas = Qt-Einbettung, Toolbar = Zoom/Pan/etc.
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Zwei Achsen: links FRF, rechts Verformung
        self.ax_frf = self.figure.add_subplot(1, 2, 1)
        self.ax_def = self.figure.add_subplot(1, 2, 2)

        # Matplotlib Widgets ins Layout einfügen
        self.plot_area.addWidget(self.toolbar)
        self.plot_area.addWidget(self.canvas, 1)

    # -------------------------------------------------
    # UI Aufbau
    # -------------------------------------------------
    def _build_ui(self):
        """
        Erstellt die komplette Benutzeroberfläche.
        - Outer Layout: links Steuerung, rechts Plotbereich.
        """
        outer = QHBoxLayout(self)

        # linke und rechte Spalte
        left = QVBoxLayout()
        right = QVBoxLayout()
        outer.addLayout(left, 1)
        outer.addLayout(right, 4)

        # -------- Dateien --------
        file_box = QGroupBox("16 Dateien auswählen")
        grid = QGridLayout(file_box)

        # labels speichert die LineEdits, in denen die Pfade angezeigt werden
        self.labels = {}
        row = 0

        # Für jede Ecke P1..P4 werden 4 Dateien angelegt (X/Y * x/y)
        for p in range(1, 5):
            grid.addWidget(QLabel(f"<b>P{p}</b>"), row, 0)
            row += 1

            for ex in ("X", "Y"):
                for m in ("x", "y"):
                    key = f"P{p}_{ex}_{m}"

                    # Button: Datei auswählen
                    btn = QPushButton(key)
                    btn.clicked.connect(lambda _, k=key: self.select_file(k))

                    # Anzeige des Pfads
                    le = QLineEdit()
                    le.setReadOnly(True)
                    le.setPlaceholderText("keine Datei gewählt")
                    self.labels[key] = le

                    # Button: Datei wieder löschen
                    clr = QPushButton("löschen")
                    clr.clicked.connect(lambda _, k=key: self.clear_file(k))

                    grid.addWidget(btn, row, 0)
                    grid.addWidget(le, row, 1)
                    grid.addWidget(clr, row, 2)
                    row += 1

            row += 1  # Leerzeile nach jedem P-Block

        left.addWidget(file_box)

        # -------- Parameter --------
        pbox = QGroupBox("Analyseparameter")
        pg = QGridLayout(pbox)

        # Frequenzbereich f_min und f_max
        self.spin_fmin = QDoubleSpinBox()
        self.spin_fmin.setRange(0, 1e9)
        self.spin_fmin.setDecimals(2)
        self.spin_fmin.setValue(0.5)

        self.spin_fmax = QDoubleSpinBox()
        self.spin_fmax.setRange(0, 1e9)
        self.spin_fmax.setDecimals(2)
        self.spin_fmax.setValue(120.0)

        # Peak-Level
        self.spin_level = QDoubleSpinBox()
        self.spin_level.setDecimals(6)
        self.spin_level.setRange(0, 1e9)
        self.spin_level.setSingleStep(0.001)
        self.spin_level.setValue(0.01)

        # Clustering-Toleranz
        self.spin_tol = QDoubleSpinBox()
        self.spin_tol.setDecimals(3)
        self.spin_tol.setRange(0, 1e9)
        self.spin_tol.setValue(0.8)

        # Min. Anzahl Peaks im Cluster
        self.spin_minc = QSpinBox()
        self.spin_minc.setRange(1, 16)
        self.spin_minc.setValue(4)

        # Fensterbreite für value_at: ±df
        self.spin_win = QDoubleSpinBox()
        self.spin_win.setDecimals(3)
        self.spin_win.setRange(0, 1e9)
        self.spin_win.setValue(0.8)

        # Skalierung der Verformung
        self.spin_scale = QDoubleSpinBox()
        self.spin_scale.setRange(0, 1000)
        self.spin_scale.setDecimals(3)
        self.spin_scale.setSingleStep(0.05)
        self.spin_scale.setValue(0.25)

        # Beschriftungen + Widgets in Grid-Layout
        items = [
            ("f_min [Hz]", self.spin_fmin),
            ("f_max [Hz]", self.spin_fmax),
            ("Peak-Level |imag| ≥", self.spin_level),
            ("Tol [Hz]", self.spin_tol),
            ("Min Peaks", self.spin_minc),
            ("Fenster ±df [Hz]", self.spin_win),
            ("Scale", self.spin_scale),
        ]
        for i, (t, w) in enumerate(items):
            pg.addWidget(QLabel(t), i, 0)
            pg.addWidget(w, i, 1)

        left.addWidget(pbox)

        # -------- Buttons/Controls --------
        # Analyse Start
        self.btn_run = QPushButton("Analyse starten")
        self.btn_run.clicked.connect(self.run_analysis)

        # Animation ein/aus
        self.cb_anim = QCheckBox("Animation")
        self.cb_anim.setChecked(True)

        # Dropdown für Moden
        self.combo_modes = QComboBox()
        self.combo_modes.currentIndexChanged.connect(self.on_mode_changed)

        left.addWidget(self.btn_run)
        left.addWidget(self.cb_anim)
        left.addWidget(QLabel("Mode auswählen:"))
        left.addWidget(self.combo_modes)

        # Log-Ausgabe / Ergebnisse
        self.results_box = QPlainTextEdit()
        self.results_box.setReadOnly(True)
        self.results_box.setMaximumHeight(260)
        left.addWidget(self.results_box)

        left.addStretch()

        # Plotbereich rechts (Toolbar + Canvas kommen später rein)
        self.plot_area = QVBoxLayout()
        right.addLayout(self.plot_area)

    # -------------------------------------------------
    # Datei Handling
    # -------------------------------------------------
    def select_file(self, key: str):
        """
        Öffnet einen Dateidialog und speichert den gewählten Pfad.
        """
        f, _ = QFileDialog.getOpenFileName(self, f"{key} wählen", "", "*.lvm")
        if f:
            self.paths[key] = f
            self.labels[key].setText(f)

    def clear_file(self, key: str):
        """
        Löscht die Dateiwahl für den Key.
        """
        self.paths[key] = ""
        self.labels[key].setText("")

    # -------------------------------------------------
    # Analyse starten
    # -------------------------------------------------
    def run_analysis(self):
        """
        Analyse-Workflow:
        1) check: alle 16 Dateien gewählt?
        2) Daten laden und auf fmin..fmax filtern
        3) Peaks in jeder Kurve finden
        4) Peaks clustern -> Modenfrequenzen
        5) Plot links zeichnen
        6) erste Mode rechts zeichnen
        """
        if not all(self.paths[k] for k in self.keys):
            QMessageBox.warning(self, "Fehler", "Bitte alle 16 Dateien auswählen (oder fehlende löschen/anpassen).")
            return

        # Zustände zurücksetzen
        self.results_box.setPlainText("")
        self.combo_modes.clear()
        self.dfs.clear()
        self.peaks.clear()
        self.modes = np.array([], dtype=float)

        # Parameter aus GUI lesen
        fmin = float(self.spin_fmin.value())
        fmax = float(self.spin_fmax.value())
        level = float(self.spin_level.value())

        # 1) Daten laden + Filtern auf Frequenzbereich
        for k, path in self.paths.items():
            df = load_lvm_as_df(path)
            df = df[(df["freq"] >= fmin) & (df["freq"] <= fmax)].reset_index(drop=True)
            self.dfs[k] = df

        # 2) Peaks finden in jeder Kurve
        all_peak_freqs = []
        for k, df in self.dfs.items():
            pk = peaks_from_df(df, level)   # Liste (freq, imag)
            self.peaks[k] = pk

            # Frequenzen extrahieren für Clustering
            pf = np.array([f for f, _ in pk], dtype=float)
            all_peak_freqs.append(pf)

        # 3) Moden clustern
        self.modes = cluster_modes(
            all_peak_freqs,
            tol=float(self.spin_tol.value()),
            min_count=int(self.spin_minc.value())
        )

        # Wenn keine Mode gefunden
        if self.modes.size == 0:
            self.results_box.setPlainText("Keine Moden gefunden. (Level/Tol/Min Peaks anpassen)\n")
            self.draw_frf()
            self.clear_def_plot()
            return

        # Log-Text erstellen + Dropdown befüllen
        txt = []
        txt.append(f"Analysebereich: {fmin:.2f} .. {fmax:.2f} Hz")
        txt.append(f"Peak-Level: |imag| ≥ {level:g}")
        txt.append("")
        txt.append("Gefundene Modenfrequenzen (Cluster):")

        for m in self.modes:
            txt.append(f" - {m:.2f} Hz")
            self.combo_modes.addItem(f"{m:.2f} Hz")

        self.results_box.setPlainText("\n".join(txt))

        # Plots aktualisieren
        self.draw_frf()
        self.draw_mode(self.modes[0])

    # -------------------------------------------------
    # Plot: FRF links
    # -------------------------------------------------
    def draw_frf(self):
        """
        Zeichnet links:
        - alle 16 Imaginärteilkurven
        - X-Achse = fmin..fmax
        - Y-Achse automatisch passend zu den Daten (mit Sicherheitsrand)

        Peak-Markierungen sind aktuell AUSKOMMENTIERT.
        """
        self.ax_frf.clear()
        self.ax_frf.set_title("Imaginärteil + Peaks (|imag| ≥ Level)")
        self.ax_frf.set_xlabel("Frequenz [Hz]")
        self.ax_frf.set_ylabel("Imaginärteil")
        self.ax_frf.grid(True)

        # X-Limit setzen
        fmin = float(self.spin_fmin.value())
        fmax = float(self.spin_fmax.value())
        if fmax > fmin:
            self.ax_frf.set_xlim(fmin, fmax)

        all_y = []

        # Kurven plotten
        for k, df in self.dfs.items():
            self.ax_frf.plot(df["freq"], df["imag"], lw=0.7)

            yy = df["imag"].to_numpy()
            if yy.size > 0:
                all_y.append(yy)

        # Peaks als Punkte plotten (deaktiviert)
        # for k, pk in self.peaks.items():
        #     if not pk:
        #         continue
        #     pf = [f for f, _ in pk]
        #     py = [im for _, im in pk]
        #     self.ax_frf.plot(pf, py, marker="o", linestyle="None")

        # Y-Limit automatisch mit Rand
        if all_y:
            ycat = np.concatenate(all_y)
            ymin = float(np.min(ycat))
            ymax = float(np.max(ycat))
            yr = ymax - ymin
            pad = 0.10 * yr if yr > 1e-12 else 1e-3
            self.ax_frf.set_ylim(ymin - pad, ymax + pad)

        self.canvas.draw()

    # -------------------------------------------------
    # Mode Plot rechts
    # -------------------------------------------------
    def clear_def_plot(self):
        """Leert rechten Plot."""
        self.ax_def.clear()
        self.ax_def.set_title("Mode")
        self.ax_def.grid(True)
        self.canvas.draw()

    def corner_vector(self, p: int, f0: float) -> np.ndarray:
        """
        Bestimmt den 2D-Vektor (mx, my) für Ecke p bei Frequenz f0.
        mx = x-Komponente, my = y-Komponente

        Dazu:
        - nehme ex = X und Y (zwei Anregungsrichtungen)
        - hole bei f0 (±df) den Imaginärteil für x- und y-Messung
        - addiere und am Ende mitteln wir (0.5 * Summe)
        """
        v = np.zeros(2, dtype=float)
        dfw = float(self.spin_win.value())

        for ex in ("X", "Y"):
            dfx = self.dfs[f"P{p}_{ex}_x"]
            fx = dfx["freq"].to_numpy()
            yx = dfx["imag"].to_numpy()

            dfy = self.dfs[f"P{p}_{ex}_y"]
            fy = dfy["freq"].to_numpy()
            yy = dfy["imag"].to_numpy()

            mx = value_at(fx, yx, f0, dfw)
            my = value_at(fy, yy, f0, dfw)

            v += np.array([mx, my], dtype=float)

        return 0.5 * v

    def _set_auto_view(self, u_norm: np.ndarray, scale: float):
        """
        Setzt den Sichtbereich rechts automatisch abhängig vom Scale,
        damit bei großen Auslenkungen nichts abgeschnitten wird.
        """
        max_def = scale * float(np.max(np.linalg.norm(u_norm, axis=1)))
        margin = max(0.25, 1.2 * max_def)
        self.ax_def.set_xlim(-margin, 1.0 + margin)
        self.ax_def.set_ylim(-margin, 1.0 + margin)

    def draw_mode(self, f0: float):
        """
        Zeichnet rechts die deformierte Form (Quadrat).
        - u = Verschiebungsvektoren an den 4 Ecken
        - u_norm = normiert, damit scale sinnvoll wirkt
        - Animation: sinusförmiges Ein-/Auslenken
        """
        self.ax_def.clear()
        self.ax_def.set_aspect("equal", adjustable="box")
        self.ax_def.grid(True)
        self.ax_def.set_title(f"Mode bei {f0:.2f} Hz")
        self.ax_def.set_xlabel("x")
        self.ax_def.set_ylabel("y")

        # Verschiebungsvektoren an 4 Ecken berechnen
        u = np.array([self.corner_vector(i, f0) for i in range(1, 5)], dtype=float)

        # Normieren
        denom = float(np.max(np.linalg.norm(u, axis=1)))
        if denom < 1e-12:
            denom = 1.0
        u_norm = u / denom

        # Scale aus GUI
        s = float(self.spin_scale.value())
        self._set_auto_view(u_norm, s)

        # Undeformierten Rahmen zeichnen
        base = np.vstack([self.pts, self.pts[0]])
        self.ax_def.plot(base[:, 0], base[:, 1], lw=2)

        # Linie für deformierte Form (wird in update angepasst)
        (line,) = self.ax_def.plot([], [], lw=3)

        def update(k):
            # sinusförmiger Faktor
            a = np.sin(2 * np.pi * k / 60.0)

            # deformierte Punkte
            d = self.pts + s * u_norm * a

            # Polygon schließen (letzter Punkt = erster Punkt)
            poly = np.vstack([d, d[0]])

            # Linien-Daten setzen
            line.set_data(poly[:, 0], poly[:, 1])
            return (line,)

        # alte Animation überschreiben
        self.anim = None

        # Animation an/aus
        if self.cb_anim.isChecked():
            self.anim = FuncAnimation(self.figure, update, frames=120, interval=30, blit=False)
        else:
            # wenn keine Animation: einmalig zeichnen
            update(15)

        self.canvas.draw()

    # -------------------------------------------------
    # Dropdown: andere Mode auswählen
    # -------------------------------------------------
    def on_mode_changed(self, idx: int):
        """
        Wenn der Benutzer im Dropdown eine andere Mode auswählt,
        wird die rechte Darstellung neu gezeichnet.
        """
        if idx >= 0 and idx < len(self.modes):
            self.draw_mode(float(self.modes[idx]))


# -------------------------------------------------
# Programmstart
# -------------------------------------------------
if __name__ == "__main__":
    # QApplication = Qt "Hauptanwendung" / Event-Loop
    app = QApplication(sys.argv)

    # Fenster erzeugen und anzeigen
    w = ModeVisualizer16()
    w.show()

    # Event-Loop starten
    sys.exit(app.exec())
