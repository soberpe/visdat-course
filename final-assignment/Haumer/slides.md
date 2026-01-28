---
marp: true
theme: default
paginate: true
---

# Weiterentwicklung des FEM-Viewers
**Tobias Haumer**  
Visualization & Data Processing – Final Project

---

## Problem / Motivation
- FEM-Simulationen liefern oft große, komplexe Datensätze
- Ergebnisse (z. B. Verschiebungen, Spannungen) sind ohne Visualisierung schwer interpretierbar
- Statische Darstellungen reichen nicht aus, um Deformationsverläufe zu verstehen  
- Ziel: **interaktiver FEM-Viewer mit animierter Deformation**

---

## Approach
- Entwicklung einer Desktop-Anwendung mit Python
- Kombination aus:
  - **PyQt6** für das GUI
  - **PyVista / VTK** für 3D-Visualisierung
- Fokus auf:
  - Interaktive Feld- und Farbwahl
  - Skalierbare Geometriedarstellung
  - Zeitabhängige Deformationsanimation (Play-Button)

---

## Key Features
- Laden von FEM-Meshes
- Anzeige von Skalar- und Vektorfeldern
- Automatische oder manuelle Skalierung
- Umschaltbare Darstellung:
  - undeformiert
  - deformiert
- Clipping-Ebene zur Analyse innerer Strukturen
- Animation der Deformation ähnlich einem Video

---

## Implementation Highlights – GUI
- Zentrales `QMainWindow` mit:
  - Control Panel (links)
  - 3D-Renderfenster (`QtInteractor`) rechts
- Wichtige GUI-Elemente:
  - `QComboBox` für Feldauswahl & Colormap
  - `QSlider` für Deformationsskalierung
  - `QCheckBox` für Optionen (Edges, Scalar Bar, Deformation)
  - Play-/Pause-Button für Animation

---

## Results
- Grundsätzlich eine nutzbare Lösung für FEM-Visoalisierungen
- vor allem für eine Masterarbeit ein Tool um einheitliche Grafiken zu erstellen

---

## Challenges & Solutions
- ein- und ausblenden des ausgegrauten Körpers zur richtigen Zeit 
- Das Video der Deformation
- darf Szene nicht jedes mal löschen und neu laden

---

## Lessons Learned
- wie schnell man mit relativ wenig python Erfahrung Projekte umsetzen kann
- oft einfacher selber Daten zu visoalisieren als mit standard Softwaretools

---

## Thank You