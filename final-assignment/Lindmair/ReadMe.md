---
marp: true
theme: default
paginate: true
backgroundColor: #f0f0f0
---

# Interaktiver FEM Viewer

**Autor:** Gregor Lindmair  
**Projekt:** Abschlussarbeit Visualisierung & Datenaufbereitung (VIS3)

---
## Was ist der FEM - Viewer?
Das Tool ist ein Viewer zum Visualisieren von FEM-Ergebnissen. Anstatt teure Software für die Visalisierung und Speicherung zu nutzen, können FEM - Daten einfach manipuliert, aufbereitet und angezeigt werden. 

--- 
## Funktionen (1)
* **Dateien laden:** Öffnen von Datei - Formaten wie `.vtu` und `.vtk` über ein Menü.
* **Verformung anzeigen:** Die berechnete Verformung kann mit einem Schieberegler verstärkt dargestellt werden, um sie besser sichtbar zu machen.
* **Datenfelder wählen:** Man kann auswählen, welches Ergebnis (z. B. Spannung oder Verschiebung) farbig auf dem Bauteil angezeigt werden soll.
* **Filter (Threshold):** Bereiche mit niedrigen Werten lassen sich prozentuell mit einem Schieberegler ausblenden, um sich auf die kritischen Stellen zu konzentrieren.
---
## Funktionen (2)
* **Kamera-Steuerung:** 
    * Schnelle Ansichten von oben, vorne oder in 3D (Isometrisch).
    * Eine "Rückgängig"-Funktion für die Kamera, falls man sich im Modell verirrt hat.
    * Speichern einer Ansicht und einfaches zurückkehren auf die gespeicherte Ansicht.
* **Vergleich:** Das ursprüngliche, undeformierte Bauteil kann bei Bedarf als Gittermodell eingeblendet werden.
* **Bild-Export:** Die aktuelle Ansicht kann als PNG-Bild gespeichert werden.

---
## Funktionen (3)
* **Einstellen einer Colormap:** Es werden unterschiedliche Colormaps zur Verfügung gestellt, die eingestellt werden können.

    Diese sind: 
    * viridis", "plasma", "inferno", "magma", "cividis", "jet","coolwarm"
---

## Technik
* **Python 3.13**
* **PyQt6:** Für das komplette UI-Design.
* **PyVista & PyVistaQT:** Das Herzstück für das 3D-Rendering. Ist die Brücke zwischen PyVista (3D-Rendering mit VTK) und Qt (GUI-Framework) – einbetten von interaktiven 3D-Grafiken in Python-Apps.
* **NumPy:** Für die schnelle Berechnung der verformten Knotenpunkte.
* **Matplotlib:** Python-Bibliothek zur Datenvisualisierung.
Sie ermöglicht es, statische, interaktive und animierte Diagramme zu erstellen.
* **VTK:** DBibliothek im Hintergrund für die wissenschaftliche Grafik.

---

## Verwendete Technologien
* **Python:** Die Programmiersprache.
* **PyQt6:** Erstellt die Benutzeroberfläche (Fenster, Knöpfe, Regler).
* **PyVista:** Kümmert sich um die Darstellung der 3D-Modelle.
* **NumPy:** Berechnet die mathematischen Verschiebungen der Punkte.

---

## Besondere Merkmale der Umsetzung
* **Schnelle Berechnung:** Die Verformung wird direkt über Vektorrechnung (NumPy) berechnet, damit das Programm auch bei größeren Modellen flüssig läuft.
* **Fehlerschutz:** Das Programm erkennt automatisch, wenn Daten unvollständig sind (z. B. 2D-Daten in einer 3D-Umgebung) und korrigiert dies, um Abstürze zu verhindern.
* **Sicherheitsabfrage:** Beim Schließen wird geprüft, ob noch Änderungen aktiv sind, damit keine Arbeit verloren geht. Bei vorhandenen Änderungen wird gefragt, ob gespeichert werden soll oder nicht. 

---

## Installation und Start



*Benötigte Bibliotheken installieren und Starten des Programms:*
   ```bash
   pip install PyQt6 pyvista pyvistaqt numpy matplotlib
   
   cd final-assignment/FEM_Lindmair.py


Starte das Programm mit python FEM_Lindmair.py.

Gehe auf File -> Open Mesh und wähle eine VTU- oder VTK-Datei aus.

Nutze die Regler auf der linken Seite, um das Feld zu wählen oder den Threshold (Filter) anzuwenden.

Aktiviere "Show Deformed", um die Verformung zu sehen, und nutze den Scale Factor Slider zur Skalierung.

Über das Menü Camera kannst du Ansichten speichern oder zurücksetzen.

Über das Menü View oder die Zahlen 1 2 3 kannst du die Ansicht auf top, front oder isometric setzen