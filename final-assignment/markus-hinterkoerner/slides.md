---
marp: true
theme: default
paginate: true
---

# Hochhaus-Modeformen Visualisierung
**Markus Hinterkörner**  
Visualization & Data Processing - Final Project

---

## Problem / Motivation
- Analysieren und Visualisieren von Hochhaus-Schwingungen basierend auf FRF-Daten.
- Ziel: Verständnis des Schwingungsverhaltens bei Erdbeben oder Windlasten.
- Nützlich für Ingenieure und Forschung, um kritische Eigenfrequenzen und Modeformen zu identifizieren.

---

## Vorgehensweise
- Einlesen von FRF- und optional Zeitbereichsdaten für mehrere Hochhäuser und Knoten.
- Berechnung von Eigenfrequenzen durch Peak-Analyse des Imaginärteils.
- Berechnung der Modeformen für alle Knoten.
- 2D- und 3D-Visualisierung:
  - 2D: Fundament bei Null, Knoten vertikal, Modeformen überlagert.
  - 3D: STL-Mesh wird gemäß Modeform verformt (Warping), glatte Interpolation via `PchipInterpolator`.
- Flexibler Modus für 3D-Plots: interaktiv oder nur Screenshots speichern.
- Technologien: Python 3.13, `numpy`, `scipy`, `pandas`, `matplotlib`, `pyvista`.

---

## Implementation Highlights
- Automatisches Einlesen der Daten aus strukturierter Ordnerhierarchie.
- Verwendung von Peak-Erkennung für präzise Eigenfrequenzen innerhalb definierter Frequenzfenster.
- Interpolation der Modeformen auf beliebigen 3D-Meshes für realistische Visualisierung.
- Flexibles Plot-System: Unterordner pro Hochhaus, Offscreen Rendering für Screenshots.

---

## Screenshots 2D Modeformen Hochhaus 1 & Hochhaus 2
<div style="display:flex; justify-content:space-around; align-items:center;">
  <img src="assets/screenshots/Hochhaus_1/Hochhaus_1_Modeformen_2d.png">
  <img src="assets/screenshots/Hochhaus_2/Hochhaus_2_Modeformen_2d.png">
</div>

<style>
img {
  max-height: 80vh;
  max-width: 85vw; /* jeweils max 85% Breite für zwei Bilder nebeneinander */
  object-fit: contain;
}
</style>

---

## Screenshots 3D Modeform von Mode 1 und Hochhaus 1

<div style="display:flex; justify-content:space-around; align-items:center;">
  <img src="assets/screenshots/Hochhaus_1/Hochhaus_1_Mode1_3d.png">
  <img src="assets/screenshots/Hochhaus_1/Hochhaus_1_Mode2_3d.png">
</div>

<style>
img {
  max-height: 80vh;
  max-width: 85vw; /* jeweils max 85% Breite für zwei Bilder nebeneinander */
  object-fit: contain;
}
</style>

---

## Demo
- Live-Demonstration des Skripts:  
  - `python main.py`  
  - Anzeige und Speicherung von 2D- und 3D-Modeformen.

---

## Ergebnisse
- Eigenfrequenzen pro Hochhaus identifiziert und ausgegeben.
- 2D-Modeformen visualisiert mit Fundament und allen Knoten.
- 3D-Modeformen auf STL-Mesh sichtbar, wahlweise interaktiv.
- Performance: Datenmengen moderat, Offscreen-Rendering für schnelle Plot-Erstellung.

---

## Herausforderungen & Lösungen
- Synchronisation der FRF-Daten über mehrere Knoten und Hochhäuser gelöst durch strukturierte Dictionaries.
- Interpolation auf 3D-Meshes gelöst mit `PchipInterpolator`.
- Flexible Plotstruktur für interaktive und statische Visualisierung umgesetzt.
- Abweichungen zwischen 2D- und 3D-Darstellung höherer Moden:
  Glättende Interpolation auf dem 3D-Mesh führt zu kurvenförmigen Modeformen,
  während die 2D-Darstellung diskrete Knoten („Zick-Zack“) zeigt.

---

## Lessons Learned
- Praktische Erfahrung in der Verarbeitung von Messdaten und Modeformenanalyse.
- Umgang mit 3D-Visualisierung in Python (`pyvista`) und Offscreen Rendering.
- Strukturierung von Code, Daten und Plots für wiederholbare Analysen.
- Erfahrung mit Peak-Erkennung, Interpolation und Plot-Optimierung.

---

## Thank You
Questions?