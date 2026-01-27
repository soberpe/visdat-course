---
marp: true
theme: default
paginate: true
---

# Final Assignment – Hochhaus FRF & 3D
**Alois Schmalwieser**  
Visualization & Data Processing

---

## Motivation
- Zeitdaten aus Prüfstandstechnik: **Kraft** + **Beschleunigung**
- Ziel: Moden extrahieren und darstellen (GUI + 3D)
- Messaufbau: Response nur an **Punkt 1**, Anregung variiert **Punkt 1…6**

---

## Pipeline (Überblick)
1. `.lvm` Import (Zeit, Beschl., Kraft)
2. Samplingrate aus Zeitvektor bestimmen
3. FRF (H1): Welch + CSD
4. Peak-Picking auf Mittelwert \|H\| → Moden 1…N
5. Participation je Anregungspunkt am Peak
6. 3D Darstellung + Export

---

## FRF-Berechnung (H1)
- Detrend von Kraft und Beschleunigung
- Spektren:
  - Auto-Spektrum der Kraft: \(S_{ff}(f)\) (Welch)
  - Kreuzspektrum Beschl./Kraft: \(S_{af}(f)\) (CSD)
- H1-Estimator:
  \[
  H(f)=\frac{S_{af}(f)}{S_{ff}(f)}
  \]

---

## Peak Picking
- Gemittelter Betrag über alle 6 FRFs:
  \[
  M(f)=\frac{1}{6}\sum_{i=1}^{6}|H_i(f)|
  \]
- Peaks in \([0,f_{max}]\) über `scipy.signal.find_peaks`
- Filter über **Prominence** (relativ zu max(M))

---

## Stabilisierung am Peak (Peak-Band)
- Problem: "ein FFT-Bin" am Peak ist empfindlich (Rauschen, Raster)
- Lösung: komplexes Mittel in Fenster **± Peak-Band** um \(f_0\)
  \[
  v_i = \frac{1}{N}\sum_{f\in[f_0-\Delta f,\,f_0+\Delta f]} H_i(f)
  \]
- Ergebnis: stabilere Participation und weniger Jitter

---

## 3D-Visualisierung (Stickmodell)
- 16 Knoten: 6 vorne + 6 hinten (3 Ebenen)
- Participation wird auf Knoten gemappt:
  - v(1..6) → vorn
  - v(1..6) → hinten (gespiegelt)
- Animation: harmonische Bewegung in einer Richtung

---

## Export
- FRF Plot als PNG
- 3D Screenshot als PNG
- 3D Animation als GIF
- Exportpfad: `assets/screenshots/`

---

## Hinweis / Limitation
- Response wird nur an **einem** Punkt gemessen
- Daher:
  - Modenfrequenzen sind zuverlässig auffindbar
  - Participation je Anregungspunkt ist sinnvoll
  - **keine vollständigen räumlichen Eigenformen** der Response rekonstruierbar

---

## Entfernt
- Kohärenz-Berechnung und Kohärenz-Plot wurden entfernt (nicht benötigt)


## 3D view
- 16-node stick-model high-rise
- Ground grid for better motion perception
- Lowest 4 nodes (ground floor) fixed
