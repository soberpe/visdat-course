---
marp: true
theme: default
paginate: true
---

# Visualisierung einer Üertragungsfunktion und Darstellen der Moden
**Marco Hutterer**
Visualization & Data Processing - Final Project

---

## Problem / Motivation
- Durchführung einer **Modalanalyse an einem Prüfstand**
- Messung von Systemantworten in **X- und Y-Richtung**
- Bereits berechnete **Übertragungsfunktionen** liegen vor  
  → dargestellt als **Imaginärteil über der Frequenz**
- Ziel:
  - Moden (Eigenfrequenzen) **identifizieren**
  - Ergebnisse **verständlich visualisieren**
  - Moden **numerisch auswertbar** darstellen (Tabelle)

---

## Datengrundlage
- Messdaten aus einem **experimentellen Prüfstand**
- Dateiformat: **LVM**
- Enthaltene Größen:
  - `X_Value` → Frequenz
  - `Comment` → Imaginärteil der Übertragungsfunktion
- Zwei Datensätze:
  - Übertragungsfunktion in **X-Richtung**
  - Übertragungsfunktion in **Y-Richtung**

---

## Vorgehensweise
1. Einlesen der Messdaten (X / Y)
2. Skalierung und Filterung der Frequenzen
3. Berechnung des Betrags der Übertragungsfunktion
4. Peak-Erkennung zur Modenbestimmung
5. Visualisierung:
   - Übertragungsfunktionen
   - Markierung der Moden
6. Ausgabe der Moden in Tabellenform

---

## Verwendete Pakete
- **Python**
- **NumPy / Pandas**
  - Datenverarbeitung
  - Numerische Operationen
- **SciPy (`find_peaks`)**
  - Robuste Peak- / Modenerkennung
- **Matplotlib**
  - Plotten der Übertragungsfunktionen
- **PyQt6**
  - Graphisches User Interface
  - Interaktive Bedienung

---

## Fazit

- Erfolgreiche Umsetzung einer **Modalanalyse-Visualisierung**
- Kombination aus:
  - Numerischer Auswertung
  - Interaktiver Darstellung
- Tool ist:
  - Verständlich
  - Erweiterbar
  - Praktisch für experimentelle Auswertung

---

## Thank You
**Vielen Dank für Ihre Aufmerksamkeit!** 
Fragen?