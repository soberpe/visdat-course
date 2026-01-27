# Hochhaus-Modeformen Visualisierung

## Projektbeschreibung
Dieses Projekt analysiert und visualisiert Schwingungen von Hochhäusern anhand von FRF-Daten (Frequency Response Functions/Übetragungsfunktionen).  
Es ermöglicht die Berechnung von Eigenfrequenzen und Modeformen, sowie deren Darstellung in 2D- und 3D-Plots.  
Ziel ist es, ein besseres Verständnis der Schwingungsverhalten von Hochhäusern zu erhalten, z. B. bei Erdbeben oder Windlasten.

---

## Features
- Einlesen von Zeitbereichs- und FRF-Daten aus Textdateien
- Berechnung von Eigenfrequenzen und Modeformen
- 2D-Visualisierung der Modeformen mit Fundament und Knotenauslenkungen
- 3D-Visualisierung der Modeformen auf STL-Gebäudemodell
- Flexibler Modus: interaktive 3D-Ansicht oder Screenshots
- Automatische Erstellung von Ordnern für Hochhäuser und Plots

---

## Technologien
- Python 3.13
- Numerik & Signalverarbeitung: `numpy`, `scipy`
- Datenhandling: `pandas`
- 2D-Plotting: `matplotlib`
- 3D-Visualisierung: `pyvista` (optional `pyvistaqt` für interaktive Plots)
- STL-Dateien für 3D-Mesh (Solidworks)

---

## Installation und Setup
```bash
cd final-assignment/markus-hinterkoerner/code
pip install -r requirements.txt
```
---

## Usage
```python
main.py
```

---

## Data

### Eingabedaten
- FRF-Dateien: Tab-getrennte Textdateien mit Dezimalzeichen `,`
- `<Knoten>_Re.txt` – Realteil der FRF
- `<Knoten>_Im.txt` – Imaginärteil der FRF
- Zeitbereichsdaten: Zwei Spalten: Zeit [s], Amplitude
- 3D-Modell: STL-Datei des Hochhauses: `Hochhaus.stl`

### Hinweis zu Zeitbereichs- und Realteildaten

Im Rahmen einer Laborübung (Prüfstandstechnik) wurden zusätzlich Zeitbereichsdaten 
(Beschleunigungs- und Kraftsignale) sowie der Realteil der FRFs verwendet 
und geplottet.

Für das vorliegende Final Assignment wurden diese Funktionalitäten bewusst 
nicht mehr in die Auswertung integriert, da:

- die Modenanalyse und Peak-Erkennung ausschließlich auf dem Imaginärteil der FRFs basiert,
- der Realteil der FRF für die hier betrachteten Fragestellungen keinen zusätzlichen Mehrwert liefert,
- Zeitbereichsplots für dieses Projekt nicht erforderlich sind und den Fokus von der
  frequenzbasierten Analyse ablenken würden.

Der Code ist jedoch modular aufgebaut, sodass eine erneute Integration von
Zeitbereichsdaten oder des Realteils der FRFs ohne strukturelle Änderungen möglich wäre.

---

### Ordnerstruktur der Daten

```text
code/data/
├── Hochhaus 1/
│   ├── E1_Im.txt
│   ├── E1_Re.txt
│   └── ...
├── Hochhaus 2/
├── E1_Im.txt
│   ├── E1_beschleunigung.txt
│   ├── E1_Im.txt
│   ├── E1_kraft.txt
│   ├── E1_Re.txt
│   └── ...
├── Hochhaus 3/
├── Hochhaus.SLDPRT
└── Hochhaus.stl
```

---

### Format / Struktur
- FRF-Dateien: 2 Spalten (Frequenz, Wert)
- Zeitbereichsdaten: 2 Spalten (Zeit, Amplitude)
- STL-Datei: Standard 3D-Mesh

---

## Implementation Details

### Algorithmen und Ansätze
- Eigenfrequenzen: Peaks des Imaginärteils der FRFs werden innerhalb definierter Frequenzfenster gefunden.
- Modeformen: Werte an den Frequenzen der Peaks werden für alle Knoten gesammelt und interpoliert.
- 2D-Plot: Fundament als Linie bei Null, Knoten vertikal angeordnet, Modeformen überlagert.
- 3D-Plot: STL-Mesh wird gemäß Modeform verformt (Warping), glatte Interpolation via PchipInterpolator.
- Die bewusste Beschränkung auf den Imaginärteil der FRFs ermöglicht eine robuste 
und übersichtliche Modenanalyse mit klar identifizierbaren Eigenfrequenzen.

### Herausforderungen
- Synchronisation von Daten aus mehreren Knoten und Hochhäusern
- Interpolation der Modeformen auf 3D-Meshes
- Flexible Plotstruktur: interaktiv oder Screenshots, Unterordner pro Hochhaus

### Performance
- Verarbeitung erfolgt sequentiell; Datenmengen moderat, daher keine Parallelisierung notwendig
- PyVista Offscreen Rendering für Screenshots verhindert Blockierung der Hauptausführung

---

## Screenshots
Beispiele aus der Anwendung (gespeichert in `assets/screenshots/`):
- 2D Modeformen
- 3D Modeformen

Screenshots zeigen typische Auslenkungen für die Moden eines Hochhauses

---

## Future Improvements
- GUI zur interaktiven Auswahl von Hochhäusern, Moden oder Frequenzfenstern
- Erweiterung auf beliebig viele Knoten
- Automatische Normalisierung oder Vergleich zwischen Hochhäusern
- Integration von Echtzeit-Messdaten
- Erweiterte Visualisierungen (Animation der Modeformen über Zeit)

## Test auf Clean Environment

```powershell
# 1️⃣ Temporär Python zum PATH hinzufügen
$env:Path += ";C:\Users\hinte\AppData\Local\Programs\Python\Python313\"

# Überprüfen, ob Python gefunden wird
python --version

# 2️⃣ In Projektordner wechseln
cd C:\visdat-course\final-assignment\markus-hinterkoerner\code

# 3️⃣ Virtuelles Environment erstellen
python -m venv test_env

# 4️⃣ Virtual Environment aktivieren
.\test_env\Scripts\Activate.ps1

# 5️⃣ Pip aktualisieren und Abhängigkeiten installieren
pip install --upgrade pip
pip install -r requirements.txt

# 6️⃣ Code testen
python main.py

# 7️⃣ Optional: Virtual Environment verlassen
deactivate