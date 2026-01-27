---
marp: true
theme: default
paginate: true
---

# FEM - Viewer Erweiterung
**Auschev Ruslan**
Visualization & Data Processing - Final Project

---

## Motivation
- Erweiterung von FEM - Viewer um die Daten besser analysieren zu können.

    - Zwei Ansichten
    - Animation von Deformation
    - Schnittebene durch 3D - Modell

---

## Used Technologies

- Verwendete Module
    - PyQt6==6.10.1
    - pyvista==0.46.4
    - pyvistaqt==0.11.3
    - NumPy==2.3.5
- Virtuelle Umgebung mit Python 3.13.0


---
## Implementation Highlights
- Erzeugung  von zwei Ansichten
    - Variable "self.plotters" initialisiert
    - Erzeugung der Ansichten in init "for i in range(2):"
    - In Funktion "display_mesh()" werden diese Ansichten verwendet 

- Animation von Deformation
    - AN / AUS von checkbox prüfen "self.animation_checkbox"
    - Nur dieser Parameter wird geändert "self.deform_slider"
    - Wird aufgerufen wenn Checkbox AN ist " def run_animation(self):

---

- Schnittebene
    - AN / AUS von checkbox prüfen "self.slice_checkbox"
    - Schieber Position wählbar zw. 0 -100 % "self.slice_slider
    - Schnittebene entlang der Achsen X, Y, Z wählbar "self.slice_axis_combo
    Die Funktion "update_slice()" zeigt falls Checkbox aktiviert ist den Schnitt an 


---
###### Screenshot: Zwei Ansichten

![Zwei-Plots](assets/screenshots//zwei_plots.png)

---
###### Screenshot: Animation von Deformation
![Animation](assets/screenshots//Animation.png)

---

###### Screenshot: Schnittebene
![Slice_Plane](assets/screenshots//Slice_Plane.png)

---

## Demo
Live Demonstration

---

## Results
- Was funktioniert gut?
    - alles was implementiert wurde funktioniert zuverlässig

- Um die Performance für die Animation der Deformation zu verbessern werden nur die Beträge der Deformationsvektoren berechnet und an Knotenpunkten angewendet, anstatt das gesamte Mesh neu zu erzeugen

---

## Challenges & Solutions
- Was war schwer?
    - Grundaufbau vom Code zu verstehen war Herausforderung
    - Richtige Einrückung der Funktionen
    - Definition der Variablen an den richtigen Stellen
- Wie habe ich es gelöst
    - Code studiert
    - Chatgpt  

---

## Lessons Learned
- Was habe ich gelernt?
    - Wie man Funktionen mit und ohne Rückgabewert deklariert in Python
    - Einrückung ist bei Python wichtig
    - for- und while Schleifen, If - Verzweigung und Funktionen enden mit ":" zum Schluss


---

## Vielen Dank für eure Aufmerksamkeit