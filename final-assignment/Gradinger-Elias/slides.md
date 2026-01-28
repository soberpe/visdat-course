---
marp: true
theme: default
paginate: true


---

# Bau eines FEM-Viewer
**Elias Gradinger**  
VIS3UE Projekt WS 25/26

---

## Problem / Motivation

Spannungen und/oder Verschiebungen die ohne grafische Darstellung nur schwer zu interpretieren sind, mittels einem für diesen Anwendungsfall entworfenen Code welcher Dateiformate wie .vtu, .vtk, .vti Daten auslesen kann, darstellen zu lassen und mit verschiedenen Parametern noch zu spielen und Effekte etc. zu verstärken.
Mein Ziel war deswegen ein einfaches Programm zu erstellen, um eben diese FEM-Ergebnisse in 3D zu visualisieren.

---

## Approach - Was ist die Anforderung

- Entwicklung einer einfachen Benutzeroberfläche
- das laden von FEM-Meshs aus .vtu, .vtk, .vti-Dateien zu ermöglichen
- den Balken durch verschiedenste Einstellmöglichkeiten bezüglich U,S, von Mises darstellen zu lassen
- auch die Deformation und Clipping mittels Verschieberegler selbstständig einstellen zu können

---

## Screenshot der 1. Erweiterung um die Deformation
![Deformation 1000](assets/screenshots//Def1000.png)

---

## Screenshot der 2. Erweiterung um die Clipping Plane inkl. Deformation
![Deformation 1000 + schneiden](assets/screenshots//Def1000_y_geschnitten.png)

---


## Implementation Highlights

- Laden von .vtu, .vtk, .vti-FEM-Dateien
- Auswahl von verschiendenen Color-Maps
- Automatische Berechnung der Betragswerte bei Vektorfeldern mittels NumPy
- Deformationsdarstellung über Verschieberegler
- Clipping Plane zum schneiden des Ballens in der x,y,z-Achse
- "Export-Screenshot" von der aktuellen Ansicht

---


## Demo


---


## Results
- Programm lädt FEM-Meshes zuverlässig
- Ergebnisse werden korrekt visualisiert
- der Anwender kann:
  - die verschiedenen Felder wechseln
  - die Deformation skalieren
  - Schnitte durch das Modell erzeugen
- Performance ist ausreichend und stürzt nicht ab
- Gute Basis für weitere Erweiterungen (Challange 3-6)

---

## Challenges & Solutions
### Herausforderung:
- PyVista & PyQt6 richtig anzuwenden
- Abstürze des Programms beim Verschieben von den Reglern zu unterbinden
- der Umgang mit Vektor- vs. Skalarfeldern
- Skalierbare Deformation
- Clipping entlang X/Y/Z-Achse

### Lösung:
- Schrittweises Debugging und Testen


---


## Lessons Learned
- Grundlagen in Hinsicht auf das Programmieren
- Arbeiten mit 3D-Mesh-Daten
- Schrittweises Vorgehen und nicht aufzugeben auch wenn nichts funktioniert

---

## Thank You

Thank you for your attention.  
**Questions?**
