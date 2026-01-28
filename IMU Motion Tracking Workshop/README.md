---
marp: true
paginate: true
footer: "VIS3VO · IMU Workshop · Simon Gersdorfer"
---

# IMU Workshop Ausarbeitung
## Simon Gersdorfer

Master Maschinenbau · 3 Semester  
FH OÖ Wels

---

## Inhalte

- Bewegungsbeschreibung
- Berechnete Entfernung der Bewegung
- Beobachtungen
- Herausforderungen

---

## Bewegungsbeschreibung

- **Bewegungsbahn:** vertikal gespiegeltes U
- **horizontal zurückgelegte Distanz:** ca. 0,4m
- **vertikal zurückgelegte Distanz:** ca. 0,5m
- oszillierende Bewegung während Zurücklegung der Kurvenbahn
- ca. 2 Sekunden in Ruhe am Beginn und Ende der Messung 

---

## Berechnete Entfernung der Bewegung
- Vergleich zwischen realer Bewegung und Messung nicht möglich, da keine Messmittel vorhanden
- Berechnete Distanz: 1,49m

---

## Beobachtungen
- Bewegung in x-Richtung ca 0,2m und in y-Richtung ca 0,4m --> deckt sich inetwa mit der realen Bewegung (visuelles Schätzen der Distanzen)
siehe fig 06

- relative Bewegung in z-Richtung vom Startpunkt zum Endpunkt ca 1,5m --> deckt sich nicht mit der realen Bewegung --> soll: ca 0,5m (visuelles Schätzen der Distanzen)
siehe fig 06

- Drift wird bei länger dauernder Messung höher (siehe Bewegung in z-Richtung gegen Ende der Bewegung --> massive Änderung der Höhe)
siehe fig 07


---

## Herausforderungen
MATLAB mobile speichert bei langer Messdauer die Werte nicht in einer CSV Datei

Abspeichern als CSV Datei durch Befehle in Matlab

Weiters muss dabei das MATLAB Zeitformat in UNIX konvertiert werden, dass es für das bestehende Pyton Script lesbar ist.

