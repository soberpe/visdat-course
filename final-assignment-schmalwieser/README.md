# Final Assignment – Hochhaus FRF & 3D (Schmalwieser)

Dieses Projekt lädt **6 Zeitmessungen** (LabVIEW `.lvm`) eines Hochhaus‑Versuchsaufbaus
(Anregung Punkte 1…6, Response immer Punkt 1), berechnet daraus **FRFs (H1)** und
visualisiert die gefundenen Moden als **Participation** auf einem einfachen
**16‑Knoten‑Stickmodell** (6 vorne + 6 hinten).

> Hinweis: Aus dem Messaufbau (Response nur an einem Punkt) kann man **keine echten
> räumlichen Eigenformen** rekonstruieren. Die 3D‑Ansicht zeigt daher **Participation
> pro Anregungspunkt** (komplex, auf Amplitude normiert), nicht eine vollständige Modenform.

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

**Entfernt (auf Wunsch):** Kohärenz‑Berechnung und ‑Plot.

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

## Export
Exports landen in:
`final-assignment-schmalwieser/assets/screenshots/`
