import os
import numpy as np
from PIL import Image
import pyvista as pv

# --- KONFIGURATION ---
DICE_SIZE = 1.0

def create_texture_atlas(dice_folder):
    """ Erstellt die Textur aus den 6 Bildern """
    images = []
    try:
        for i in range(1, 7):
            path = os.path.join(dice_folder, f"{i}.png")
            img = Image.open(path).convert("RGB")
            images.append(img)
    except Exception as e:
        print(f"Fehler: Konnte Bilder in '{dice_folder}' nicht laden: {e}")
        return None

    w, h = images[0].size
    atlas = Image.new("RGB", (w * 6, h))
    for i, img in enumerate(images):
        if img.size != (w, h): img = img.resize((w, h))
        atlas.paste(img, (i * w, 0))
    
    atlas_np = np.array(atlas)
    # WICHTIG: Textur muss für VTK vertikal gespiegelt werden
    atlas_np = np.flipud(atlas_np) 
    return pv.Texture(atlas_np)

def create_manual_die_mesh():
    """ 
    Erstellt einen Würfel komplett manuell über PolyData.
    Dies umgeht alle Fehler mit fehlenden Texture-Coordinates.
    """
    s = DICE_SIZE / 2.0

    # 1. Wir definieren 24 Punkte (4 pro Seite), damit jede Seite eigene UVs haben kann.
    # Reihenfolge: Left, Right, Back, Front, Bottom, Top
    points = np.array([
        # Left (-X)
        [-s, -s, -s], [-s, -s,  s], [-s,  s,  s], [-s,  s, -s],
        # Right (+X)
        [ s, -s, -s], [ s,  s, -s], [ s,  s,  s], [ s, -s,  s],
        # Back (-Y)
        [ s, -s, -s], [-s, -s, -s], [-s, -s,  s], [ s, -s,  s],
        # Front (+Y)
        [-s,  s, -s], [ s,  s, -s], [ s,  s,  s], [-s,  s,  s],
        # Bottom (-Z)
        [-s, -s, -s], [ s, -s, -s], [ s,  s, -s], [-s,  s, -s],
        # Top (+Z)
        [-s, -s,  s], [ s, -s,  s], [ s,  s,  s], [-s,  s,  s],
    ])

    # 2. Flächen definieren (Jedes Quad nutzt 4 Punkte)
    # Format: [4, p0, p1, p2, p3, 4, p4, p5...]
    # Das '4' am Anfang sagt: "Das nächste Polygon hat 4 Ecken"
    faces = np.array([
        4, 0, 1, 2, 3,      # Left
        4, 4, 5, 6, 7,      # Right
        4, 8, 9, 10, 11,    # Back
        4, 12, 13, 14, 15,  # Front
        4, 16, 17, 18, 19,  # Bottom
        4, 20, 21, 22, 23   # Top
    ])

    # 3. Textur-Koordinaten (UVs) berechnen
    # Atlas Indices: Left(4)->3, Right(3)->2, Back(5)->4, Front(2)->1, Bottom(6)->5, Top(1)->0
    atlas_indices = [3, 2, 4, 1, 5, 0]
    step = 1.0 / 6.0
    
    uvs = []
    for idx in atlas_indices:
        u_min = idx * step
        u_max = (idx + 1) * step
        # UVs passend zu den Punkten oben (CCW Order)
        # (0,0), (0,1), (1,1), (1,0) innerhalb des Atlas-Streifens
        face_uvs = [
            [u_min, 0.0], # Punkt 0 (Unten Links)
            [u_min, 1.0], # Punkt 1 (Oben Links)
            [u_max, 1.0], # Punkt 2 (Oben Rechts)
            [u_max, 0.0]  # Punkt 3 (Unten Rechts)
        ]
        uvs.extend(face_uvs)
    
    # 4. Mesh erstellen
    mesh = pv.PolyData(points, faces)
    mesh.active_texture_coordinates = np.array(uvs)
    
    return mesh

if __name__ == "__main__":
    print("--- 3D Textur Test (Manual Mesh) ---")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dice_dir = os.path.join(script_dir, "dice")
    
    if not os.path.exists(dice_dir):
        print(f"FEHLER: Ordner nicht gefunden: {dice_dir}")
        exit()

    print("Lade Texturen...")
    texture = create_texture_atlas(dice_dir)
    
    if texture is None:
        print("Abbruch: Textur Fehler.")
        exit()

    print("Erstelle Mesh (Manuell)...")
    base_mesh = create_manual_die_mesh()

    pl = pv.Plotter()
    pl.set_background("white")

    # Rotationen (Zahl nach oben)
    rotations_to_top = {
        1: [], 6: [('x', 180)], 2: [('x', -90)], 
        5: [('x', 90)], 3: [('y', 90)], 4: [('y', -90)]
    }

    test_dice = [
        (1, 0, 0.0),   
        (6, 0, 1.2),   
        (3, 90, 2.4),  
        (5, 45, 3.6)   
    ]

    print("Platziere Würfel...")
    for val, z_rot, x_pos in test_dice:
        mesh = base_mesh.copy()
        
        # A. Richtige Zahl nach oben
        for axis, angle in rotations_to_top[val]:
            if axis == 'x': mesh.rotate_x(angle, point=mesh.center, inplace=True)
            elif axis == 'y': mesh.rotate_y(angle, point=mesh.center, inplace=True)
        
        # B. Eigene Rotation (Z-Achse)
        mesh.rotate_z(z_rot, point=mesh.center, inplace=True)
        
        # C. Verschieben
        mesh.translate([x_pos, 0, 0], inplace=True)
        
        pl.add_mesh(mesh, texture=texture, show_edges=False)

    pl.camera_position = 'xy'
    print("Starte Visualisierung...")
    pl.show()