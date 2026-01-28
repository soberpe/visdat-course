---
marp: true
theme: default
paginate: true
---

# File für Schwingungsanalyse
Thomas Maier
Visualization & Data Processing - Final Project

---

## Problem / Motivation
- Für das Labor Prüfstandstechnik galt es von einem Modellhochhaus die Eigenfrequenzen und Übertragungsfunktion zu ermitteln. Weiters sollen die Moden qualitativ dargestellt werden.


- Nachdem nach ersten Versuchen mit Excel klar war das hier die Performance mit diesen rießigen Datenmassen sehr nachließ, lag die Idee nahe dies mittels einem Python code zu bewerkstelligen.

    - Schnell, einfach, gute Performance
    - einfaches plotten von Graphen/Darstellungen inklusive Export
---

## Approach
- Plotten der Übertragungsfunktion durch Auftragen von Betrag über Frequenz
- Finden der Eigenfrequenzen durch Peakfinding mit anpassbarer Parameter hinsichtlich Feinheit
- Qualitatives Plotten der Modeformen gemappt auf geladene Geometrie. Auswerten des Imaginärteiles an der jeweiligen Eigenfrequenz (also Mode abhängig) und ploten dieses. Verbinden der Punkte durch Extra-/ bzw. Interpolation dazwischen.
---

## Implementation Highlights
- ![Menü](assets\screenshots\File_menu.png){width =50%}
---
## Implementation Highlights
- ![Menü](assets\screenshots\Bild_menu.png){width =50%}
---
## Implementation Highlights
- ![Menü](assets\screenshots\uefkt.png){width = 50%}
---
## Implementation Highlights
- ![Menü](assets\screenshots\Eigenfreq.png){width =50%}
---
## Implementation Highlights
- ![Menü](assets\screenshots\Moden.png){width =50%}
---

## Demo
Live demonstration or video/GIF

---

## Results
- Plausible Eigenfrequenzen und Modeformen werden detektiert und geplottet.
- Abgleich mit screenshoots aus LabView
---

## Challenges & Solutions
- Modeplott war nicht sehr einfach da unplausible Plots ausgegeben wurden- im Code auch noch ein auskommentierter Debug Code mit Ausgabe der extra-/interpolierten Verschiebungswerte am jeweilgen Knoten
- Anfangs Dateiausgabe der Testdateien in h5 files, dies wurde aber verworfen, da ich für diese einen eigen "Reader" (erneut eigenes Skript) brauche, daher Umstellung auf tsv damit ich diese auch im Editor lesen kann.

---

## Lessons Learned
- Grundsätzlich ist für mich selbst der Eindruck entstanden, dass man sich sehr einfach und schnell ein Pytonscript "basteln" kann. Z.B. Skript welches 17 Messfiles in eines zusammenfügt, bzw. Skript welches ein Drahtmodell des Hochhauses macht, für eine schöne Skizze (=das Verwendete h5 Geometriefile) 
- Aktuell probiere ich interessehalber noch eine Datenauswerter von Messdaten aus einem Arduino 
- Vermutlich werde ich ähnliches für meine Masterarbeit brauchen
---

## Thank You