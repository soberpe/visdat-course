# Höhenprofilanalyse mit Hochwasser-Simulation

Das Tool wandelt 2D-Graustufenbilder in 3D-Geländemodelle um und ermöglicht eine Hochwassersimulation sowie eine Querschnittsanalysen.




## Features

* 2D zu 3D Konvertierung: Echtzeit-Generierung von 3D-Meshes aus Bildern.
* Split-View: Synchronisierte Ansicht von 2D-Profilschnitt (Matplotlib) und 3D-Modell (PyVista).
* Interaktives Slicing: Dynamische Schnittebene durch das Gelände (X- oder Y-Achse).
* Hochwassersimulation: Visuelle Simulation von Wasserpegeln mit korrekter Überlagerung.
* Performance-Modus: Optionales Downsampling für flüssige Darstellung großer Bilder.
* Kalibrierung: Manuelle Eingabe der Maximalhöhe in Metern.

## Voraussetzungen

Das Projekt benötigt Python 3.13.9

### Benötigte Bibliotheken
Die Abhängigkeiten sind in requirements.txt definiert:
* PyQt6 (GUI Framework)
* pyvista & pyvistaqt (3D Rendering)
* matplotlib (2D Plotting)
* numpy (Datenverarbeitung)
* imageio (Bildimport)

## Installation & Start

Folgen Sie diesen Schritten, um die Anwendung einzurichten:

1. Virtuelle Umgebung erstellen (Empfohlen)
Öffnen Sie ein Terminal (PowerShell/CMD) im Ordner:
python -m venv venv
.\venv\Scripts\activate

2. Abhängigkeiten installieren
pip install -r requirements.txt

3. Anwendung starten
python main.py

## Bedienung

Die Benutzeroberfläche ist in zwei Bereiche unterteilt:

### Linkes Panel (Controls)

1. Operation Mode:
* Terrain Analysis: Fokus auf Topologie und Slicing.
* Flood Simulation: Aktiviert die WasserSpiegel-Regler und die blaue bewegliche Wasserebene.

2. Data Source:
* Import Image: Laden eigener Heightmaps (PNG/JPG). Bilder werden automatisch in den data/ Ordner kopiert.
* High Performance (Downsample): Aktivieren, um nur jeden 2. Pixel zu laden (bessere Performance bei großen Bildern).
* Reset Camera: Setzt die Ansicht auf die Draufsicht (Top-Down) zurück.

3. Calibration:
* Setzen Sie hier die echte Höhe des höchsten Punktes (weißester Pixel) in Metern (z.B. Welt:8848

4. Visual Exaggeration:
* Überhöht das Gelände visuell, um flache Strukturen besser erkennbar zu machen und um die Hochwassersimulation besser erkenntlich zu machen

5. Profile Slice Control:
* Wählen Sie die Schnittachse (X oder Y).
* Der Slider bewegt die rote Schnittebene durch das Modell.
* Checkbox: Blendet die rote Ebene im 3D-Bild ein/aus.

### Rechtes Panel (Visualisierung)
* Oben: 2D-Querschnitt des Geländes an der aktuellen Slider-Position.
* Unten: Interaktives 3D-Modell.
* Linke Maustaste: Drehen
* Rechte Maustaste: Zoomen
* Mittlere Maustaste / Shift+Links: Verschieben (Pannen)

## Implementation Details & Probleme

### 1. Synchronisation der 3D-Schnittebene
Eine der größten technischen Hürden war die korrekte Visualisierung der Schnittebene im 3D-Raum, die exakt mit dem 2D-Profil übereinstimmen muss.

* Problem: Eine einfache Ebene war oft visuell schwer zu erkennen oder verdeckte die Sicht auf das Gelände. Zudem musste die Ebene bei Änderung der Höhenskalierung (Visual Exaggeration) dynamisch mitwachsen.
* Lösung: Die Ebene wurde in zwei separate geometrische Objekte getrennt:
    * Ein Rahmen als dicke rote Linie für die Sichtbarkeit.
    * Eine Füllung als Mesh mit hoher Transparenz.
* Logik: Eine Event-Loop berechnet die 4 Eckpunkte der Ebene bei jeder Slider-Bewegung neu aklualisiert wird.

### 2. Performance-Optimierung (Downsampling)
* Problem: Das Rendering und Live-Warping von hochauflösenden Heightmaps erzeugt Millionen von Vertices, was zu niedrigen Framerates führt.
* Lösung: Implementierung eines Downsampling-Algorithmus.
* Technik: Es wird beim Einlesen jedes zweite Pixel übersprungen. Dies reduziert die zu verarbeitende Datenmenge auf 25%, wodurch die Interaktion auch auf Standard-Hardware flüssig bleibt.

## Datenformat

Das Tool erwartet Graustufenbilder (Heightmaps):https://tangrams.github.io/heightmapper/
* Schwarz (0): Tiefster Punkt (0m).
* Weiß (255): Höchster Punkt
* Unterstützte Formate: .png, .jpg, .jpeg, .bmp.

Beispielbilder befinden sich im Ordner data/.

## Bekannte Limitierungen

* Manuell maximale Höhe eingeben
* Bei hochauflösenden Bildern ohne Downsampling kann die Framerate sinken.

## Bilder der Anwendung

Bilder der Anwendung

Terrain Analyse
![final-assignment Huemer/assets/screenshots/VisDat-1.png](assets/screenshots/VisDat-1.png)

Flood Simulation
![alt text](assets/screenshots/VisDat-2.png)

## Autor

Huemer Lukas
Visualisierung & Datenverarbeitung
29.01.2026