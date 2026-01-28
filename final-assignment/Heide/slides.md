---
marp: true
theme: default
paginate: true
---

# Interaktiver 3D-Globus
Lino Heide 
Visualization & Data Processing – Final Project

---

## Problem / Motivation

- Geographische Daten liegen meist 2-Dimensional vor
- Klassische Karten sind:
  - verzerrt und daher unrealistisch
  - schlecht zur Darstellung von tatsächlicher geographischer Entfernung
- Ziel:
  - Länder direkt im 3D-Raum auswählen
  - Globale Zusammenhänge räumlich verständlich machen

➡️ Motivation: Interaktive Visualisierung globaler 3D Daten

---

## Approach

- Darstellung der Erde als 3D-Kugel
- Projektion von Ländergrenzen (Lon/Lat → 3D)
- Interaktion:
  - Drehen, Zoomen, Klicken
  - Auswahl eines Landes per Maus

## Software

- Python
- PyVista (3D-Visualisierung)
- NumPy
- SciPy (KD-Tree, optional)
- matplotlib

---

## Implementation Highlights

- Projektion von GeoJSON-Polygonen auf eine Kugel
- Triangulation für glatte Darstellung
- Mehrere Höhenebenen:
  - Ozean
  - Länder
  - Grenzen
  - Hervorhebung

Picking-Algorithmus
- Unsichtbare Punktwolke pro Land
- KD-Tree für schnelle Zuordnung

---

## Demo

- Live-Demo der Anwendung  


---

## Results

- Flüssige Interaktion
- Teilweise Präzise Länder-Auswahl
- Klare visuelle Trennung Geometrien

**Performance**
- Sehr schnelle Klick-Erkennung (KD-Tree)
- Fallback auf NumPy ohne SciPy möglich
- 110m-Datensatz → gutes Detail/Performance-Verhältnis
- Schnelles Laden der Mesh-Daten mithilfe von Mergen
- Crashes treten manchmal auf

---

## Challenges & Solutions

Herausforderungen:
- Länderflächen statt Grenzen
- Komplexe Multi-Polygon-Geometrien
- Präzises Picking bei beweglicher Kamera
- Z-Fighting zwischen Layern
- Eliminierung der Deadzones

Lösungen:
- Sampling von Grenzen + Innenpunkten
- Front-Facing-Check
- Höhen-Offsets für jede Ebene

---

## Lessons Learned

- Umgang mit realen Geodaten (GeoJSON)
- 3D-Projektion und Kamerasteuerung
- Häufig eigene Lösungsinitiative nötig
- Inkrementelles "Bauen" und "Manipulieren" führt zum Ziel


---

## Thank You

Danke für die Aufmerksamkeit  
Fragen?
