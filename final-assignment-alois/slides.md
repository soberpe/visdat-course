---
marp: true
theme: default
paginate: true
---

# Hochhaus Modal Viewer  
**Alois**  
Final Assignment – Visualization & Data Processing

---

## Motivation
- Modalanalyse eines „Hochhauses“ im Prüfstand
- Messdaten liegen als LabVIEW `.lvm` Zeitreihen (Kraft + Beschleunigung) vor
- Ziel: Moden automatisch extrahieren und verständlich visualisieren

---

## Daten & Pipeline
- Input: 6 Messfiles (Anregung Punkt 1..6, Beschleunigung Punkt 1)
- Preprocessing: Detrend
- FRF: H1-Schätzer (Welch/CSD)
- Peak-Picking auf Mittelwert |H(f)| → Moden 1..N

---

## Visualisierung
- 2D: |H(f)| aller FRFs + Mittelwert, Phase
- Modes-List: Frequenzen der Peaks
- 3D: Stickmodell des Hochhauses + Animation

---

## Hinweis zur Interpretation
- Nur ein Response-Messpunkt (Punkt 1)
- 3D zeigt **Anregungs-Teilnahme** (participation) je Punkt, nicht die echte räumliche Modeform der Response.

---

## Demo
- Files auswählen → Load & Analyze
- Mode auswählen → 3D Animation + Amplituden

---

## Lessons Learned
- robuste Daten-Parser für LabVIEW
- FRF-Schätzung (H1) + Peak-Picking
- Kombination PyQt6 + Matplotlib + PyVistaQt
