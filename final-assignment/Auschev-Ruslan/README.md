# Visualisierung & Datenaufbereitung Final Assignment - FEM Viewer

## 1 Einleitung
```
Der FEM viewer wurde zuerst laut Übungsanleitung durchgearbeitet und erstellt. In weiterer Folge wurde der FEM viewer mit multiple views, animation und slice plane erweitert.  
```

## 2 Struktur
- `final-assignment/` — Ordner wo die finale Abgabe stattfindet 
- `assets/` — hier sind einige screenshot enthalten die im Zuge der Entstehung des erweiterten FEM - viewers gemacht wurden
- `code/` — hier sind die .vtu Datei, src, python run_application.py und requirements.txt enthalten
- `Readme.md` — hier ist eine Beschreibung des gesamten Projekts enthalten
- `slides.md` — ist die finale Präsentation des Projekts

## 3 Student

### Ruslan Auschev
- **GitHub:** [@auschev](https://github.com/auschev)
- **Program:** Master Mechanical Engineering
- **Interests:** creating documents, creating structures, optimizing workflows, visualizing data
- **Background:** First and Second semester VBA and C++, also Raspberry Pi and Arduino
``
## 4 Verwendete Module

Für dieses Projekt wurden folgende Module mithilfe "pip install" Befehl in die Umgebung .venv installiert.

- PyQt6==6.10.1
- pyvista==0.46.4
- pyvistaqt==0.11.3
- NumPy==2.3.5

Weiters wurde für die virtuelle Umgebung 

- python==3.13.0

verwendet.

## 5 Data

Die verwendete Datei für die Visualisierung ist:

- beam_stress.vtu

wurde direkt aus der Übung übernommen. Die Datei befindet sich im Ordner "Data". Es sind Spannungen, Deformationen und das Netz enthalten.

## 6 Implementierung und Details

### 6.1 Änderungen am FEM Viewer für Multiple Views

Um den FEM Viewer für die gleichzeitige Anzeige von zwei Plottern („Multiple Views“) lauffähig zu machen, wurden folgende Änderungen durchgeführt:

- Einführung mehrerer plotter
- Anpassung der Mesh-Darstellung
- Edge-Visibility und Scalar Bar wurden für beide plots erzeugt
- Deformationen wurden auf bei plots übertragen
- Reset View und Screenshots wurden so geändert, dass ein Reset ohne abstürzen möglich ist und Screeshots für beide plotter möglich sind.

Der FEM Viewer kann nun zwei nebeneinanderliegende 3D-Ansichten darstellen, bei denen alle bestehenden Funktionen wie Deformation, Edge-Visibility, Scalar Bar, Reset View und Screenshot weiterhin korrekt funktionieren. Die Benutzeroberfläche bleibt stabil, und das reine Mesh kann ebenfalls angezeigt werden.

![Zwei-Plots](assets/screenshots//zwei_plots.png)

### 6.2 Animation der Deformation

- Eine neue Checkbox „Animate Deformation“ wurde hinzugefügt.

- Wird sie aktiviert, bewegt der Viewer automatisch den Deformations-Slider in einer Schleife, wodurch das Mesh kontinuierlich deformiert wird.

- Die Animation läuft zwischen minimalem und maximalem Wert des Sliders.

- Deaktivieren der Checkbox stoppt die Animation sofort, GUI und andere Funktionen bleiben aber weiterhin nutzbar

Hierfür wurde eine neue Funktion definiert, der eben diese Slider für die Deformation in vorgegebenen Zeitschritten ansteuert.

Unten im Bild rechts sieht man ein Kästchen mit "Animate Deformation" damit kann die Animation aktiviert und deaktiviert werden.

![Animation](assets/screenshots//Animation.png)

### 6.3 Beschreibung der Slice-Plane-Funktion

Zur Erweiterung des FEM-Viewers wurde eine Slice-Plane-Funktion implementiert, mit der Schnitte durch das 3D-Modell interaktiv dargestellt werden können.
Dazu wurden zunächst UI-Elemente (Checkbox, Slider und Achsenauswahl) in das Control-Panel integriert. Die Checkbox aktiviert bzw. deaktiviert die Slice-Ansicht, während der Slider die Position der Schnittfläche relativ zu den Mesh-Bounds (0–100 %) steuert. Über eine ComboBox kann die Schnittebene entlang der X-, Y- oder Z-Achse gewählt werden.

Die eigentliche Schnittberechnung erfolgt in der Methode update_slice(). Dort wird aus den aktuellen Mesh-Bounds die reale Position der Schnittebene berechnet und mit der PyVista-Funktion mesh.slice() ein neues Slice-Mesh erzeugt. Dieses Slice-Mesh wird anschließend in allen Plottern angezeigt.

Unten im Bild ist zu sehen, wie man durch setzen von Häckchen "Show Slice Plane" aktiviert wird und anschließend mit dem Slider die Schnittebene entlang der gewählten Achse verschoben wird. 

![Slide_Plane](assets/screenshots//Slice_Plane.png)

## 7 Future Improvements

- Mehrere Farb-Mappings / Colormaps
- Vektorpfeile anzeigen
- Von VTK erzeugte Videos exportieren
- Mehrere Meshes gleichzeitig laden
- Unterschiedliche Ansichten z.B. Spannung & Verschiebung
- Koordinatensystem im Eck usw.

## 8 SRC - Ordner

Der src - Ordner enthält die wichtigsten zusatz Änderungen, die für die Implementierung von Zustatzfunktionen relevant sind.

Der main - code befindet sich im "python run_application.py" dort sind alle Funktionen enthalten, das heißt, dort werden die Funktionen aus src - Odner nicht aufgerufen!

Der src - Ordner wurde genutzt, um die wichtigsten Änderung einzeln aufzulisten.




