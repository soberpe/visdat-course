---
marp: true
theme: default
paginate: true
---

# FFT Analyse Tool für LabVIEW-Messdaten
**Simon Gersdorfer**
Visualization & Data Processing - Final Project

---

## Problem / Motivation
- Teilweise fehlende Informationen in LabVIEW CSV Daten ergänzen und Darstellung der Übertragungsfuktion
- Dient als Werkzeug zur Laborprotokollerstellung

---

## Vorgehensweise
- Implementierung der Grundfunktionen im Main File ohne GUI
- Auslagern der Grundfunktionen in eigene Module
- Erstellung einer Grafischen Oberfläche mit Verwendung der bereits implementierten Module
- Zusätzlich noch der Einbau der Export Funktion
- Standardpakete analog zu Vorlesung


---

## Implementation Highlights
- GUI greift auf viele Funktionen zu
- Funktionen können auch aus main File aufgerufen und bedient werden
-Matplotlib Toolbar mit eingebaut
-Flexibler CSV Import

---

## Demo
Live demonstration

---

## Results
- Die Anwendung funktioniert zuverlässig für den vorgesehenen Anwendungsfall (LabVIEW-Exportdaten)
- Übertragungsfunktion und Imaginärteil werden korrekt berechnet und dargestellt
- CSV-Export ermöglicht flexible Weiterverarbeitung der Mess- und Auswertedaten
- Für stark abweichende CSV-Layouts sind manuelle Anpassungen erforderlich

---

## Challenges & Solutions
- Strukturierung des Codes in klar getrennte Module
- Fehlersuche - zeitintensiv
- Fehlersuche durch schrittweises testen ist am effizientesten


---

## Lessons Learned
- besseres Verständnis für modulare Softwarestruktur 
- KI-gestützte Tools (z. B. ChatGPT) sind sehr hilfreich bei Fehlersuche und Architekturüberlegungen
- erste Erfahrungen mit einer GUI Programmierung
---

## Thank You
Fragen?