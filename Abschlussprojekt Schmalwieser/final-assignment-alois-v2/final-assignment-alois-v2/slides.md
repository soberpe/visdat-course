---
marp: true
theme: default
paginate: true
---

# Hochhaus – Moden (FRF) & 3D (V2)
**Alois**  
Final Assignment – Visualization & Data Processing

---

## Motivation
- Zeitdaten aus Prüfstandstechnik (Kraft + Beschleunigung)
- Ziel: Moden robust extrahieren + anschaulich darstellen (GUI + 3D)

---

## Pipeline
- `.lvm` Parser (Zeitreihe)
- FRF (H1): Welch + CSD
- Kohärenz γ²(f): Qualitätsmaß
- Peak-Picking auf Mittelwert |H| → Moden 1..N

---

## Stabilisierung am Peak (V2)
- Nicht nur ein FFT-Bin
- Komplexer Mittelwert in Fenster **± Peak-Band**
- Ergebnis: weniger Rauschen, stabilere Participation

---

## Visualisierung & Export
- FRF-Plot (bis fmax skaliert)
- Kohärenz-Plot
- 3D Stickmodell (12 Knoten) + Animation
- Export: PNG + GIF
