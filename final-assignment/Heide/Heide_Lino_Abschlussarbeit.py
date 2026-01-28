import pyvista as pv
import numpy as np
import json
import urllib.request
from pathlib import Path
import warnings
import matplotlib.path as mpath

# --- EXTERNE BIBLIOTHEKEN PRÜFEN ---
# Wir versuchen die SciPy-Bibliothek für die schnelle räumliche Suche (KDTree) zu laden.
# Falls sie nicht installiert ist, nutzen wir später eine langsamere NumPy-Variante.
try:
    from scipy.spatial import KDTree
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

# --- SYSTEM-EINSTELLUNGEN ---
# Hier unterdrücken wir unnötige Warnmeldungen in der Konsole, um die Ausgabe
# während des Programmlaufs für das Masterprojekt sauber zu halten.
warnings.filterwarnings('ignore')

# ---------------------------------------------------------
# 1. FUNKTIONEN ZUM LADEN UND CACHEN DER GEODATEN
# ---------------------------------------------------------

# Link zur GeoJSON-Datei von Natural Earth (110m Auflösung für gute Performance)
WORLD_SIMPLE_URL = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson"

def lade_welt_geojson():
    # Wir erstellen einen versteckten Ordner im Benutzerverzeichnis, um die 
    # Geodaten lokal zu speichern. So muss die Datei nicht jedes Mal neu geladen werden.
    cache_verzeichnis = Path.home() / ".globus_cache"
    cache_verzeichnis.mkdir(exist_ok=True)
    cache_datei = cache_verzeichnis / "laender.geojson"
    
    # Zuerst prüfen wir, ob die Datei bereits im lokalen Cache-Ordner liegt.
    # Wenn ja, lesen wir sie direkt von der Festplatte ein.
    if cache_datei.exists():
        try:
            with open(cache_datei, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception: pass
    
    # Falls die Datei nicht lokal existiert, laden wir sie über eine HTTP-Anfrage
    # aus dem Repository von Natural Earth herunter.
    try:
        anfrage = urllib.request.Request(WORLD_SIMPLE_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(anfrage, timeout=15) as antwort:
            daten = json.loads(antwort.read().decode('utf-8'))
            # Nach dem Download speichern wir die Daten sofort lokal für den nächsten Start.
            with open(cache_datei, 'w', encoding='utf-8') as f:
                json.dump(daten, f)
            return daten
    except Exception as e:
        print(f"❌ Fehler beim Laden der Daten: {e}")
        return {"type": "FeatureCollection", "features": []}

# ---------------------------------------------------------
# 2. HAUPTKLASSE FÜR DEN INTERAKTIVEN GLOBUS
# ---------------------------------------------------------

class InteraktiverGlobus:
    def __init__(self, radius=1.0):
        # Grundlegende Initialisierung der Variablen für den Plotter und die Geometrien.
        self.radius = radius
        self.laender_geometrien = {}
        self.plotter = None
        self.aktuelles_highlight = None
        self.namens_anzeige = None
        
        # DEFINITION DER HÖHEN-LEVEL (OFFSETS):
        # BASIS: Die grüne Landmasse schwebt leicht über dem blauen Ozean.
        # GRENZEN: Die schwarzen Linien liegen minimal über dem Land.
        # HIGHLIGHT: Das rote gewählte Land liegt ganz oben, um Überlappungen zu vermeiden.
        self.OFFSET_BASIS = 1.025     
        self.OFFSET_GRENZEN = 1.027
        self.OFFSET_HIGHLIGHT = 1.035 
        
        # Hier werden die Rohdaten geladen und in ein Python-Format umgewandelt.
        self.daten = lade_welt_geojson()
        self._verarbeite_geojson()
        
        # Initialisierung der Such-Strukturen für die Klick-Erkennung auf dem Globus.
        self.index_punkte = []
        self.index_namen = []
        self.kd_tree = None

    def _verarbeite_geojson(self):
        # Wir gehen alle Features (Länder) in der GeoJSON-Datei einzeln durch.
        # Dabei extrahieren wir den Namen und die geografischen Koordinaten.
        for feature in self.daten.get('features', []):
            name = feature['properties'].get('NAME', 'Unbekannt')
            geometrie = feature['geometry']
            polygone = []
            
            # Da Länder entweder aus einem Polygon oder mehreren Teilen (Inseln) bestehen,
            # sortieren wir diese hier korrekt in unsere Liste ein.
            if geometrie['type'] == 'Polygon':
                polygone.append(geometrie['coordinates'][0])
            elif geometrie['type'] == 'MultiPolygon':
                for p in geometrie['coordinates']: 
                    polygone.append(p[0])
            
            # Wenn Geometrien vorhanden sind, speichern wir sie unter dem Ländernamen ab.
            if polygone:
                self.laender_geometrien[name] = polygone

    def _baue_suche_index(self):
        # Damit wir wissen, welches Land angeklickt wurde, erstellen wir eine
        # unsichtbare Punktwolke, die über der gesamten Weltkarte liegt.
        alle_punkte = []
        namen = []
        print("\n[1/2] ⚙️  Erzeuge Präzisions-Index... (bitte warten)")
        
        for name, polygone in self.laender_geometrien.items():
            for poly in polygone:
                poly_np = np.array(poly)
                
                # Schritt 1: Wir erzeugen Punkte entlang der Küstenlinien jedes Landes.
                # Das sorgt dafür, dass die Grenzen besonders präzise anklickbar sind.
                for i in range(len(poly_np)-1):
                    p1, p2 = poly_np[i], poly_np[i+1]
                    distanz = np.linalg.norm(p1 - p2)
                    anzahl_zwischenpunkte = max(2, int(distanz / 0.15))
                    zwischenpunkte = np.linspace(p1, p2, anzahl_zwischenpunkte)
                    pts_3d_kante = self.projiziere_auf_kugel(zwischenpunkte, self.OFFSET_BASIS)
                    alle_punkte.extend(pts_3d_kante)
                    namen.extend([name] * len(pts_3d_kante))
                
                # Schritt 2: Wir füllen das Innere der Länder mit einem Gitter aus Punkten.
                # Nur Punkte, die innerhalb der Landesgrenzen liegen, werden in den Index aufgenommen.
                lon_min, lat_min = np.min(poly_np, axis=0)
                lon_max, lat_max = np.max(poly_np, axis=0)
                lons = np.arange(lon_min, lon_max, 0.4)
                lats = np.arange(lat_min, lat_max, 0.4)
                
                if len(lons) > 0 and len(lats) > 0:
                    grid_lon, grid_lat = np.meshgrid(lons, lats)
                    gitter_punkte = np.column_stack((grid_lon.ravel(), grid_lat.ravel()))
                    maske = mpath.Path(poly_np).contains_points(gitter_punkte)
                    innen_punkte = gitter_punkte[maske]
                    
                    if len(innen_punkte) > 0:
                        pts_3d_innen = self.projiziere_auf_kugel(innen_punkte, self.OFFSET_BASIS)
                        alle_punkte.extend(pts_3d_innen)
                        namen.extend([name] * len(pts_3d_innen))

        # Die gesammelten Punkte werden für eine extrem schnelle Suche in einen KD-Tree geladen.
        self.index_punkte = np.array(alle_punkte)
        self.index_namen = namen
        if HAS_SCIPY:
            self.kd_tree = KDTree(self.index_punkte)
        print(f"[2/2] ✅ Index fertiggestellt. {len(self.index_punkte)} Referenzpunkte aktiv.")

    def projiziere_auf_kugel(self, punkte_2d, r_faktor):
        # Diese mathematische Funktion rechnet flache Längen- und Breitengrade
        # unter Berücksichtigung des Radius in ein kartesisches 3D-Koordinatensystem um.
        if len(punkte_2d.shape) == 1: 
            punkte_2d = punkte_2d.reshape(1, 2)
        
        lon = np.radians(punkte_2d[:, 0])
        lat = np.radians(punkte_2d[:, 1])
        r = self.radius * r_faktor
        
        # Berechnung der X, Y und Z Komponenten für die Position im 3D-Raum.
        x = r * np.cos(lat) * np.cos(lon)
        y = r * np.cos(lat) * np.sin(lon)
        z = r * np.sin(lat)
        return np.column_stack((x, y, z))

    def _erstelle_land_mesh(self, name, hoehen_faktor):
        # Hier wandeln wir die 2D-Grenzlinien eines Landes in ein echtes 3D-Objekt (Mesh) um.
        polygone = self.laender_geometrien.get(name, [])
        meshes = []
        for poly in polygone:
            if len(poly) < 3: continue
            pts_2d = np.array(poly)
            faces = np.hstack([[len(pts_2d)], np.arange(len(pts_2d))])
            
            # Wir triangulieren die Fläche und unterteilen sie mehrfach (Subdivide), 
            # damit sich die eigentlich flache Karte sauber an die Kugelform anschmiegt.
            temp_2d = pv.PolyData(np.column_stack((pts_2d, np.zeros(len(pts_2d)))), faces=faces)
            unterteilt = temp_2d.triangulate().subdivide(1, subfilter='linear')
            
            # Schließlich projizieren wir alle generierten Dreiecke auf die Kugeloberfläche.
            pts_3d = self.projiziere_auf_kugel(unterteilt.points[:, :2], hoehen_faktor)
            meshes.append(pv.PolyData(pts_3d, faces=unterteilt.faces))
            
        return meshes[0].merge(meshes[1:]) if len(meshes) > 1 else (meshes[0] if meshes else None)

    def _callback_rechtsklick(self, punkt):
        # Diese Funktion wird ausgelöst, sobald der Nutzer die rechte Maustaste drückt.
        if punkt is None: return
        
        # Wir stellen sicher, dass man nur Länder anklicken kann, die der Kamera zugewandt sind.
        if np.dot(punkt, np.array(self.plotter.camera.position)) <= 0: return 

        # Wir suchen den Punkt in unserem Index, der dem Mausklick am nächsten liegt.
        if HAS_SCIPY and self.kd_tree:
            distanz, index = self.kd_tree.query(punkt)
            if distanz < 0.15: 
                self.waehle_land(self.index_namen[index], zoom=False)
        else:
            distanzen = np.linalg.norm(self.index_punkte - punkt, axis=1)
            index = np.argmin(distanzen)
            if distanzen[index] < 0.15: 
                self.waehle_land(self.index_namen[index], zoom=False)

    def waehle_land(self, name, zoom=True):
        # Wenn ein Land gewählt wird, suchen wir den exakten Namen in unserer Datenbank.
        if not name: return
        name_korrekt = next((n for n in self.laender_geometrien if name.lower() in n.lower()), None)
        if not name_korrekt: return

        # Falls bereits ein Land rot markiert ist, entfernen wir die alte Markierung.
        if self.aktuelles_highlight:
            self.plotter.remove_actor(self.aktuelles_highlight)
        
        # Wir erstellen ein neues rotes Mesh für das gewählte Land auf dem höchsten Offset-Level.
        mesh = self._erstelle_land_mesh(name_korrekt, self.OFFSET_HIGHLIGHT)
        if mesh:
            self.aktuelles_highlight = self.plotter.add_mesh(mesh, color='red', name="highlight", pickable=False)
            # Falls Zoom aktiv ist (z.B. beim Start), fliegt die Kamera zum Land.
            if zoom:
                pos = np.mean(mesh.points, axis=0)
                self.plotter.camera.position = (pos / np.linalg.norm(pos)) * 3.5
                self.plotter.camera.focal_point = (0, 0, 0)
        
        # Der Name des gewählten Landes wird als permanenter Text oben links eingeblendet.
        if self.namens_anzeige:
            self.plotter.remove_actor(self.namens_anzeige)
        self.namens_anzeige = self.plotter.add_text(f"📍 Land: {name_korrekt}", position='upper_left', color='black', font_size=18)

    def focus_europa(self):
        # Hilfsfunktion, um die Kamera per Tastendruck sofort wieder auf Europa auszurichten.
        self.plotter.camera.position = self.projiziere_auf_kugel(np.array([[10.0, 45.0]]), 3.8)[0]
        self.plotter.camera.focal_point = (0, 0, 0)
        self.plotter.camera.up = (0, 0, 1)
        self.plotter.render()
        print("🌍 Fokus zurück auf Europa gesetzt.")

    def anzeigen(self, start_land):
        # Hier wird das Hauptfenster mit allen grafischen Elementen initialisiert.
        self.plotter = pv.Plotter(window_size=(1100, 850), title="VIS Masterprojekt - Interaktiver Globus")
        self.plotter.background_color = 'white'
        
        # Zuerst erstellen wir die blaue Kugel für den Ozean.
        self.plotter.add_mesh(pv.Sphere(radius=self.radius, theta_resolution=100, phi_resolution=100), color='skyblue', pickable=True)
        
        # Danach zeichnen wir jedes Land in Grün und fügen die schwarzen Grenzlinien hinzu.
        print("🗺️  Zeichne Weltkarte...")
        for name in self.laender_geometrien.keys():
            mesh = self._erstelle_land_mesh(name, self.OFFSET_BASIS)
            if mesh:
                self.plotter.add_mesh(mesh, color='forestgreen', smooth_shading=True, pickable=False)
                kanten = mesh.extract_feature_edges(boundary_edges=True, feature_edges=False, manifold_edges=False)
                self.plotter.add_mesh(kanten, color='black', line_width=1, pickable=False)

        # Die Klick-Erkennung (Punktwolke) wird nun im Hintergrund aufgebaut.
        self._baue_suche_index()

        # Wir fügen die Bedienungsanleitung als Text direkt in das 3D-Fenster ein.
        legende_text = (
            "🎮 STEUERUNG:\n"
            "   - LMB: Globus drehen\n"
            "   - RMB: Land auswählen\n"
            "   - MMB: Globus verschieben\n"
            "   - STRG + LMB: Globus kippen\n"
            "   - R: Kamera zurücksetzen\n"
            "   - Mausrad: Zoomen"
        )
        self.plotter.add_text(legende_text, position='lower_left', color='black', font_size=11)

        # Tasten-Events (z.B. 'R' für Reset) und das Klick-System werden aktiviert.
        self.plotter.add_key_event('r', self.focus_europa)
        self.plotter.enable_point_picking(callback=self._callback_rechtsklick, show_message=False, show_point=False, left_clicking=False)

        # Das beim Start eingegebene Land wird sofort markiert und herangezoomt.
        self.waehle_land(start_land)
        
        # Ausgabe der Steuerung im Terminal für zusätzliche Übersicht.
        print("\n------------------------------------------------")
        print("🎮 STEUERUNG BEREIT (siehe 3D-Fenster)")
        print("------------------------------------------------\n")
        
        self.plotter.show()

# ---------------------------------------------------------
# 3. PROGRAMMSTART
# ---------------------------------------------------------

if __name__ == "__main__":
    # Startbildschirm im Terminal.
    print("================================================")
    print("🌍 WILLKOMMEN ZUM INTERAKTIVEN GLOBUS")
    print("================================================")
    
    # Erstellen der Globus-Instanz und Abfrage des Startlandes.
    globus = InteraktiverGlobus()
    eingabe = input("👉 Bitte ein Startland auf Englisch eingeben: ").strip()
    
    # Validierung der Eingabe: Existiert das Land? Wenn nicht, wird Deutschland gewählt.
    if eingabe:
        start_name = next((n for n in globus.laender_geometrien if eingabe.lower() in n.lower()), None)
        if start_name:
            globus.anzeigen(start_name)
        else:
            print(f"❌ Land '{eingabe}' wurde nicht gefunden. Starte mit Standardansicht.")
            globus.anzeigen("Germany")
    else:
        globus.anzeigen("Germany")