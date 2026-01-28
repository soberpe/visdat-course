# Final Assignment – Hochhaus FRF & 3D (Schmalwieser)
## Projektbeschreibung
Dieses Projekt lädt **6 Zeitmessungen** (LabVIEW `.lvm`) eines Hochhaus‑Versuchsaufbaus
(Anregung Punkte 1…6, Response immer Punkt 1), berechnet daraus **FRFs (H1)** und
visualisiert die gefundenen Moden als **Participation** auf einem einfachen
**16‑Knoten‑Stickmodell** (8 vorne + 8 hinten).


## Features
- `.lvm` Parser (Zeit, Beschleunigung, Kraft)
- FRF‑Berechnung (H1): Welch + CSD
- Peak‑Picking auf gemitteltem \|H\| (bis `fmax`, mit `prominence`)
- **Peak‑Band (±)**: komplexer Mittelwert um die Modefrequenz → stabilere Participation
- 3D‑Visualisierung (PyVista) + Animation
- Export:
  - FRF Plot (PNG)
  - 3D Screenshot (PNG)
  - 3D Animation (GIF)

## Verwendete Technologien

- **NumPy** – numerische Berechnungen, FFT-Auswertung
- **Pandas** – Einlesen und Verarbeiten von CSV-Daten
- **Matplotlib** – Visualisierung der Analyseergebnisse
- **PyQt6** – grafische Benutzeroberfläche
- **Pyvista** – 2d Darstellung


## Projektstruktur
```
final-assignment-schmalwieser/
  README.md
  slides.md
  requirements.txt
  assets/screenshots/         
  code/
    main.py                   # Startpunkt
    ui_mainwindow.py          # GUI (PyQt6)
    ui_canvases.py            # Matplotlib Canvas
    io_lvm.py                 # .lvm Import
    frf_analysis.py           # FRF + Peak-Picking + Participation
    geometry.py               # 16-Knoten-Stickmodell
    viewer3d.py               # PyVista Helper
    exporting.py              # PNG/GIF Export
    data/sample/              # Messdaten
```

## Installation & Run
```bash
cd final-assignment-schmalwieser/code
pip install -r requirements.txt
python main.py
```

## Daten
Dateien liegen in:
`final-assignment-schmalwieser/code/data/sample`


## Export
Exports landen in:
`final-assignment-schmalwieser/assets/screenshots/`
