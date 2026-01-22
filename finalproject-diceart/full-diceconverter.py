import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image
import traceback

# --- KONFIGURATION ---
COMPARE_RES = 32      # Auflösung für den Vergleich (Qualität)

# --- DATENSTRUKTUREN ---
class DiceData:
    """ Speichert die Infos für einen einzelnen Würfel """
    def __init__(self, x, y, value, rotation_deg, direction_char):
        self.x = x
        self.y = y
        self.value = value           # 1-6
        self.rotation = rotation_deg # 0, 90, 180, 270
        self.direction = direction_char # N, O, S, W

class DiceVariant:
    """ Hilfsklasse zum Vergleichen der Bilder """
    def __init__(self, image, value, rotation, direction_char):
        self.image = image
        self.value = value
        self.rotation = rotation
        self.direction_char = direction_char
        # Cache für schnellen Vergleich
        self.compare_data = list(image.resize((COMPARE_RES, COMPARE_RES)).getdata())

# --- HELFER FUNKTIONEN ---
def get_difference(pixels_a, pixels_b):
    """ Berechnet Mean Squared Error zwischen zwei Bild-Chunks """
    diff = 0
    for a, b in zip(pixels_a, pixels_b):
        d = a - b
        diff += d * d
    return diff

# --- HAUPTLOGIK ---
def process_dice_art(input_image_path, horizontal_dice, vertical_dice=None):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dice_source_folder = os.path.join(script_dir, "dice")
    
    # Ausgabe Ordner
    output_folder = os.path.join(script_dir, "diceconverter-output")
    blueprint_folder = os.path.join(script_dir, "blueprints-output")

    # Ordner Checks
    for f in [output_folder, blueprint_folder]:
        if not os.path.exists(f): os.makedirs(f)
    
    if not os.path.exists(dice_source_folder):
        print(f"FEHLER: Ordner '{dice_source_folder}' fehlt!")
        return None

    # 1. Bild laden
    try:
        original_img = Image.open(input_image_path).convert('L')
    except Exception as e:
        print(f"Fehler beim Laden des Bildes: {e}")
        return None

    width, height = original_img.size
    if vertical_dice is None:
        aspect_ratio = height / width
        vertical_dice = int(horizontal_dice * aspect_ratio)

    print(f"--- Starte Berechnung ({horizontal_dice}x{vertical_dice}) ---")

    # 2. Varianten laden (0°, 90°, 180°, 270°)
    dice_variants = {}
    rot_map = {0: 'N', 90: 'W', 180: 'S', 270: 'O'}
    dice_render_size = 50 

    for i in range(1, 7):
        path = os.path.join(dice_source_folder, f"{i}.png")
        if not os.path.exists(path):
            print(f"Fehler: Bild {i}.png fehlt im dice Ordner!")
            return None
            
        base_img = Image.open(path).resize((dice_render_size, dice_render_size)).convert('L')
        dice_variants[i] = []
        for rot in [0, 90, 180, 270]:
            # PIL rotiert CCW (Counter Clockwise)
            dice_variants[i].append(DiceVariant(base_img.rotate(rot), i, rot, rot_map[rot]))

    # 3. Analyse & Matrix Aufbau
    target_w = horizontal_dice * COMPARE_RES
    target_h = vertical_dice * COMPARE_RES
    analyze_img = original_img.resize((target_w, target_h), resample=Image.Resampling.LANCZOS)
    
    # Output Bild (2D Vorschau)
    preview_img = Image.new('L', (horizontal_dice * dice_render_size, vertical_dice * dice_render_size))

    matrix = [] 
    blueprint_lines = []
    total_dice = horizontal_dice * vertical_dice
    count = 0

    for y in range(vertical_dice):
        row_data = []
        row_txt = []
        for x in range(horizontal_dice):
            # A. Ausschnitt holen
            box = (x * COMPARE_RES, y * COMPARE_RES, (x + 1) * COMPARE_RES, (y + 1) * COMPARE_RES)
            chunk_data = list(analyze_img.crop(box).getdata())
            
            # B. Helligkeit bestimmt Zahl
            val = int((sum(chunk_data) / len(chunk_data)) / 256 * 6)
            if val > 5: val = 5
            target_val = 6 - val 
            
            # C. Beste Rotation finden
            best_variant = None
            min_diff = float('inf')
            for variant in dice_variants[target_val]:
                diff = get_difference(chunk_data, variant.compare_data)
                if diff < min_diff:
                    min_diff = diff
                    best_variant = variant
            
            # D. Daten speichern
            # 1. In Matrix (Objekt)
            d_obj = DiceData(x, y, target_val, best_variant.rotation, best_variant.direction_char)
            row_data.append(d_obj)
            
            # 2. In Blueprint Text (String)
            row_txt.append(f"{target_val}{best_variant.direction_char}")
            
            # 3. In 2D Bild (Pixel)
            pos = (x * dice_render_size, y * dice_render_size)
            preview_img.paste(best_variant.image, pos)

            count += 1
            if count % 500 == 0:
                print(f"Fortschritt: {int(count/total_dice*100)}%", end="\r")
        
        matrix.append(row_data)
        blueprint_lines.append("\t".join(row_txt))

    print("\nBerechnung fertig. Speichere Dateien...")

    # 4. Speichern
    base_name = os.path.splitext(os.path.basename(input_image_path))[0]
    
    # A. Bild
    img_out = os.path.join(output_folder, f"dice_{base_name}.png")
    preview_img.save(img_out)
    
    # B. Text
    txt_out = os.path.join(blueprint_folder, f"plan_{base_name}.txt")
    with open(txt_out, "w", encoding="utf-8") as f:
        f.write(f"Bauplan: {base_name} ({horizontal_dice}x{vertical_dice})\n")
        f.write("-" * 40 + "\n")
        for line in blueprint_lines:
            f.write(line + "\n")

    print(f"Bild gespeichert: {img_out}")
    print(f"Plan gespeichert: {txt_out}")
    
    return matrix

# --- START ---
def select_file():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    return filedialog.askopenfilename(filetypes=[("Bilder", "*.jpg *.png *.jpeg *.webp")])

if __name__ == "__main__":
    print("--- DICE CONVERTER (2D Generator & Bauplan) ---")
    
    f = select_file()
    
    if f:
        print(f"Datei: {os.path.basename(f)}")
        
        valid_input = False
        h = 0
        while not valid_input:
            raw_input = input("Breite (Anzahl Würfel, z.B. 80): ")
            if raw_input.strip().isdigit():
                h = int(raw_input)
                valid_input = True
            else:
                print("Bitte eine gültige ganze Zahl eingeben!")

        try:
            process_dice_art(f, h)
            print("Vorgang abgeschlossen.")
                
        except Exception as e:
            print("\n" + "!"*40)
            print("ES IST EIN FEHLER AUFGETRETEN:")
            traceback.print_exc()
            print("!"*40)
    else:
        print("Abbruch.")