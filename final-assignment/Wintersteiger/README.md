# Mode Visualizer – Qualitative Modendarstellung aus FRF-Daten

## Project Title

**Mode Visualizer – Qualitative Modendarstellung aus FRF-Messdaten**

Dieses Projekt dient zur **anschaulichen Visualisierung von Eigenmoden** eines Prüfstands auf Basis gemessener Frequenzgangfunktionen (FRF).  
Aus mehreren Messdateien werden automatisch **Resonanzfrequenzen (Moden)** erkannt und als **deformierte Rahmenstruktur** dargestellt.

Das Ziel ist **keine vollständige experimentelle Modalanalyse**, sondern eine **verständliche, qualitative Darstellung** der dominanten Schwingungsformen.

---

## Features

- Auswahl von **16 LVM-Messdateien**
  - 4 Ecken des Prüfstands
  - 2 Anregungsrichtungen (X / Y)
  - 2 Messrichtungen (x / y)
- Einstellbarer **Analyse-Frequenzbereich**
- **Peak-Erkennung** im Imaginärteil der FRF
  - positive und negative Peaks
- **Clustering** der Peaks zu gemeinsamen Modenfrequenzen
- Unterdrückung von Rauschpeaks durch Mindestanzahl an Peaks
- Grafische Darstellung:
  - Links: Imaginärteil aller FRFs über Frequenz
  - Rechts: **qualitative Modeform** als deformierter Rahmen
- Optionale **Animation** der Modeformen
- Auswahl der Moden über ein Dropdown-Menü

---

## Technologies Used

- **Python**
- **NumPy** – numerische Berechnungen
- **Pandas** – Einlesen und Verarbeitung der Messdaten
- **PyQt6** – grafische Benutzeroberfläche (GUI)
- **Matplotlib** – Plotten und Animation

**Besondere Techniken:**
- Peak-Erkennung über lokale Maxima und Minima
- Frequenz-Clustering zur Modenbestimmung
- Qualitative Modendarstellung ohne vollständige Modalanalyse

---

## Installation & Setup

```bash
cd final-assignment/Wintersteiger/code/ModeVisualizerRun.py
pip install -r requirements.txt
```

## GUI Workflow

1. Auswahl aller **16 LVM-Dateien**  
   (4 Ecken × 2 Anregungsrichtungen × 2 Messrichtungen)
2. Einstellen des **Analyse-Frequenzbereichs** (`f_min`, `f_max`)
3. Festlegen des **Peak-Schwellwerts** (`|imag| ≥ Level`)
4. Setzen der **Clustering-Parameter**  
   (Frequenz-Toleranz und minimale Peak-Anzahl)
5. Start der Analyse über **„Analyse starten“**
6. Auswahl einer Mode im **Dropdown-Menü**
7. Anzeige der **qualitativen Modeform**  
   (optional animiert)

---

## Data

**Verwendete Daten:**
- Frequenzgangfunktionen (FRF) im **.lvm-Format**

**Erwartete Dateistruktur:**
- Tab-getrennte Textdatei
- Erste Zeile: Metadaten (wird ignoriert)
- Spalte 1: Frequenz (intern als 10·Hz gespeichert)
- Spalte 2: Imaginärteil der FRF
- Dezimaltrennzeichen: Komma


---

 ## Screenshots
 ![h:600](assets/screenshots/Programm.png)
