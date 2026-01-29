---
marp: true
theme: default
paginate: true
---

# Statistische Versuchsplanung  
**Lukas**  
Visualization & Data Processing – Final Project

---

## Problem / Motivation
- In technischen und wissenschaftlichen Experimenten ist es oft unklar, **welche Einflussfaktoren wirklich relevant sind**.  
- Vollfaktorielle Versuchspläne sind mächtig, aber **manuelle Berechnung ist fehleranfällig und zeitaufwendig**.  
- Ziel: Ein Tool, das **Versuchspläne automatisch generiert**, **Messwerte verwaltet**, **Effekte berechnet** und **grafisch darstellt**.  
- Dadurch können Anwender schneller erkennen:
  - Welche Faktoren wirken stark?
  - Welche Wechselwirkungen existieren?
  - Welche Effekte sind statistisch signifikant?

---

## Approach
- Entwicklung einer **interaktiven Desktop‑Anwendung** mit PyQt6  
- Vollfaktorielle Designs mit 2 Stufen pro Faktor  
- Automatische Berechnung von:
  - Haupteffekten  
  - Wechselwirkungen  
  - Signifikanztests (t‑Test basierend auf Lookup‑Tabelle)  
- Visualisierung über Matplotlib  
- Klar strukturierte GUI mit vier Ausgabebereichen

---

## Key Technologies
- **Python 3.11**
- **PyQt6** – GUI‑Framework  
- **NumPy** – numerische Berechnungen  
- **Matplotlib** – Diagramme  
- **OOP‑Struktur** für saubere Erweiterbarkeit  
- Dynamische Dock‑Widgets für flexible Layouts

---

## Implementation Highlights
- Automatische Generierung eines vollfaktoriellen Designs  
- Berechnung der Effekte über gewichtete Mittelwerte  
- Interpolationsfunktion für t‑Werte bei beliebigen Freiheitsgraden  
- Vier parallele Visualisierungen:
  - Haupteffekte  
  - Wechselwirkungen  
  - Signifikanzdiagramm  
  - Textbasierter Bericht  
- Benutzerfreundliche Dateneingabe über Dialogfenster

---

## Screenshots
*(Hier fügst du später Bilder deiner Anwendung ein)*  
- Control‑Panel  
- Versuchsplan‑Tabelle  
- Haupteffekte‑Plot  
- Interaktionsmatrix  
- Signifikanz‑Balkendiagramm  
- Bericht‑Fenster

---

## Demo
- Live‑Demonstration der Anwendung  
- Erstellung eines Versuchsplans  
- Eingabe von Messwerten  
- Berechnung & Visualisierung  
- Interpretation der Ergebnisse

---

## Results
- Voll funktionsfähige Anwendung zur statistischen Versuchsplanung  
- Klare und intuitive Benutzeroberfläche  
- Aussagekräftige Diagramme  
- Signifikanztest ermöglicht schnelle Bewertung der Relevanz  
- Gute Performance auch bei vielen Faktoren und Wiederholungen

---

## Challenges & Solutions
### Herausforderung:
- Dynamische GUI‑Layouts mit mehreren Dock‑Widgets  
- Korrekte Berechnung der Effekte und Interaktionen  
- Interpolation der t‑Werte  
- Übersichtliche Darstellung vieler Diagramme

### Lösungen:
- Strukturierung der GUI in modulare Komponenten  
- Mathematische Berechnungen mit NumPy  
- Eigene Interpolationsfunktion  
- Automatische Layout‑Optimierung (tight_layout)

---

## Lessons Learned
- Vertiefung in statistische Methoden der Versuchsplanung  
- Umgang mit komplexen GUI‑Strukturen in PyQt6  
- Matplotlib‑Integration in interaktive Anwendungen  
- Bedeutung sauberer Code‑Struktur und Modularität  
- Praktische Erfahrung mit Software‑Engineering im wissenschaftlichen Kontext

---

## Thank You
Fragen?
