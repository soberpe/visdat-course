---
marp: true
theme: default
paginate: true
---

# Mode Visualizer
**David wintersteiger**
Visualization & Data Processing - Final Project

---

## Problem / Motivation
- Das Grundproblem liegt darin die Moden eines Prüfstands für einen Modellautoprüfstand zu analysieren und anschließend qualtitaiv zu visualisieren. 
Viele FRF-Messkurven → Resonanzen schwer übersichtlich zu erkennen

- Peaks liegen nicht exakt bei gleicher Frequenz

- Ziel: Moden schnell finden und anschaulich darstellen

- Why is this useful?
Schnellere Auswertung, weniger “manuelles Suchen” nach Peaks, nachvollziehbare und präsentationsfähige Darstellung der Moden.
---

## Prüfstand

![h:560 center](assets/screenshots/Gestell5.jpeg)



## Daten

- Messdaten von Prüfstand
- Dateiformat .lvm
- 2 Spalten pro Datensatz
    - 'X_Value' → Frequenz in 10*Hz
    - 'Comment' → Imaginärteil
---
## Approach

- LVM-Dateien einlesen (Imaginärteil über Frequenz)

- Analysebereich festlegen (`f_min / f_max`)

- Positive & negative Peaks erkennen

- Peaks aus allen Kurven clustern → Modenfrequenzen

- Moden visuell als Verformung darstellen

---
## Verwendete Pakete

 - PyQt6 (GUI) 
 - Matplotlib (Plots + Animation)
 - Pandas (Datenverarbeitung)
 - Numpy (Datenverarbeitung)
---

## Implementation Highlights


- stabile Moden statt Rauschpeaks `Tol [Hz]`
    - Sind diese Peaks nahe genug, um dieselbe Mode zu sein?
    - Ziel: Modenfrequenzen finden

- robuste Amplitudenbestimmung bei Modefrequenz `Fenster +/- df`
    - Wo ist der Peak in der Nähe dieser Modefrequenz?
    - Ziel: Amplitude für die Verformung bestimmen

- GUI + Animation

- Auto-Skalierung verhindert Abschneiden


---

## Results

- Gute Darstellung der Moden
- Moden werden qualitativ visualisiert
- Zur genaueren Analyse einzelner Moden → ModeAnalyzer.py


---

## Results Foto


![h:600](assets/screenshots/Programm.png)

---

## Challenges & Solutions
- Frequenzen wurden im Endeffekt falsch aufgenommen. 
- Erkannt durch ersten Plot
- Lösung indem `X_Value` Daten beim Einlesen mit *0,1 multipliziert werden 

---

## Lessons Learned
- Python super alternative zu Paid Software
- Software so anpassbar wie man sie braucht
- frei zugängliche KI gute Unterstützung
- KI zwar gute Hilfe allerdings, bei weitem nicht fehlerfrei!

---

## Thank You
Questions?