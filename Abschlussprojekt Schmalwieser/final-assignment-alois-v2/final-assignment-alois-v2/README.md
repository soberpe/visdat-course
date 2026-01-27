# Hochhaus – Moden (FRF) & 3D (Version 2)

**Upgrades in V2**
1. **Kohärenz-Plot** (Qualität / Linearität / Rauschen sichtbar)
2. **Peak-Fenster (± Peak-Band)**: komplexer Mittelwert um Modefrequenz → stabilere Participation
3. **Export**: FRF Plot (PNG), 3D Screenshot (PNG), 3D Animation (GIF)

## Wichtige Interpretation
Messaufbau:
- Response: Beschleunigung **nur an Punkt 1**
- Anregung: variiert Punkt **1..6**

Damit kann man:
- Modenfrequenzen zuverlässig finden
- Participation je Anregungspunkt bestimmen

Damit kann man NICHT:
- echte räumliche Modeformen der Response rekonstruieren (dafür bräuchte man Responses an den anderen Punkten)

Die 3D Ansicht zeigt deshalb **Participation** auf einem 12-Knoten-Stickmodell (6 vorne + 6 hinten).

## Run
```bash
cd final-assignment/alois_v2/code
pip install -r requirements.txt
python main.py
```

## Export
Exports landen in:
`final-assignment/alois_v2/assets/screenshots/`
