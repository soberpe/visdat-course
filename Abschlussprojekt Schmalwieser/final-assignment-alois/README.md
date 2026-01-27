# Hochhaus Modal Viewer (FRF → Moden → 3D)

Dieses Projekt lädt **LabVIEW .lvm** Zeitbereichsdaten (Kraft + Beschleunigung), berechnet daraus **FRFs** (H1-Schätzer), findet automatisch **Modenfrequenzen** (Peak-Picking) und visualisiert das Ergebnis inklusive einer **3D-Animation** eines vereinfachten Hochhaus-Modells.

**Wichtig:** Da in den Messdaten die **Beschleunigung nur an Punkt 1** gemessen wurde und die **Anregung über Punkt 1–6** variiert wurde, kann aus diesen 6 Dateien **keine räumliche Modeform der Gebäuderesponse** rekonstruiert werden.  
Die 3D-Ansicht zeigt daher eine **„Anregungs-Teilnahme“ (participation)**: wie stark die Anregung an jedem Punkt die Response an Punkt 1 bei der gewählten Modefrequenz beeinflusst.

## Run

```bash
cd final-assignment/alois/code
pip install -r requirements.txt
python main.py
```

## Datenformat

- `.lvm` mit Spalten: `X_Value` (Zeit), `Acceleration`, `Force`
- Tab-separiert, Dezimal-Komma wird unterstützt.

## Features

- 6× File-Auswahl (Punkt 1..6)
- FRF-Berechnung (H1)
- Peak-Picking: wähle Anzahl Moden, fmax, Prominence
- 2D-Plot: |H(f)| (alle + Mittelwert), Phase
- 3D-Viewer: vereinfachtes Hochhaus (6 Knoten) mit Animation

## Nächste Verbesserungen (optional)

- Interpolation falls Frequenzraster nicht identisch
- Kohärenz-Plot zur Qualitätsbewertung
- Bessere Modalfitting-Parameter (Dämpfung, Peak-Band)
- Unterstützung für echte Multi-Output Messungen → echte Modeformen
