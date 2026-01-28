# FFT Analyse Tool für LabVIEW-Messdaten

## Projektbeschreibung

Dieses Projekt ist ein Analyse-Tool zur Auswertung von Messdaten aus LabVIEW.  
Es ermöglicht das Einlesen zeitdiskreter Messsignale (z. B. Beschleunigung und Kraft), die Berechnung der Übertragungsfunktion mittels FFT, sowie deren grafische Darstellung und den Export ausgewählter Signale.

Ziel des Projekts ist es, eine GUI-gestützte Auswertungsumgebung zu schaffen, in der Messdaten interaktiv analysiert und berechnete Daten strukturiert exportiert und anschließend weiterverwendet werden können.

---

## Features

- Einlesen von Messdaten aus CSV-Dateien (LabVIEW-Export)
- Konfigurierbare CSV-Struktur (Header-Zeilen, Spaltennamen)
- FFT-basierte Berechnung der Übertragungsfunktion
- Darstellung des Betrags der Übertragungsfunktion
- Vergleich des Imaginärteils zur Plausibilitätsprüfung  
  (FFT-Ergebnis vs. Referenzdaten aus LabVIEW)
- Eingebettete Matplotlib-Plots in einer PyQt6-GUI
- Interaktive Plot-Navigation
- Export frei wählbarer Signale als CSV-Datei

---

## Verwendete Technologien

- **NumPy** – numerische Berechnungen, FFT-Auswertung
- **Pandas** – Einlesen und Verarbeiten von CSV-Daten
- **Matplotlib** – Visualisierung der Analyseergebnisse
- **PyQt6** – grafische Benutzeroberfläche

---

## Installation & Setup

```bash
cd final-assignment/gersdorfer/code
pip install -r requirements.txt
```

---

## Daten


Das Projekt verarbeitet zeitdiskrete Messdaten aus LabVIEW, die als CSV-Dateien exportiert wurden.  
Die Dateien befinden sich im Ordner `code/data/`

Header-Zeilen und relevante Spalten (Acceleration, Force, ...) sind über die GUI frei konfigurierbar.

---

## Implementation Details

- Die Übertragungsfunktion wird als Quotient der FFT von Beschleunigung und Kraft berechnet.  
- Alle Funktionen sind in eigenen Modulen
- Der CSV-Export ist so aufgebaut, sodass beliebige Signale ausgewählt, benannt und gespeichert werden können.


