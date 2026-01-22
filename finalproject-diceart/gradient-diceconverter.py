import os
import math
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageOps

# --- KONFIGURATION ---
# Falls das Skript zu langsam ist, setze diesen Wert kleiner (z.B. 16).
# Das ist die Auflösung, in der der Vergleich "Original vs. Würfel" stattfindet.
COMPARE_RES = 32 

class DiceVariant:
    def __init__(self, image, value, rotation):
        self.image = image
        self.value = value
        self.rotation = rotation
        # Für den schnellen Vergleich erstellen wir eine kleine, verwaschene Version
        self.compare_data = list(image.resize((COMPARE_RES, COMPARE_RES)).getdata())

def get_difference(pixels_a, pixels_b):
    """
    Berechnet den Unterschied zwischen zwei Bild-Daten-Listen (Mean Squared Error).
    Je kleiner der Rückgabewert, desto ähnlicher sind sich die Bilder.
    """
    diff = 0
    # Wir iterieren durch die Pixel und summieren die Unterschiede
    for a, b in zip(pixels_a, pixels_b):
        d = a - b
        diff += d * d
    return diff

def create_smart_dice_art(input_image_path, horizontal_dice, vertical_dice=None):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_folder = os.path.join(script_dir, "diceconverter-output")
    dice_source_folder = os.path.join(script_dir, "dice")

    # --- 1. Ordner Checks ---
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    if not os.path.exists(dice_source_folder):
        print(f"FEHLER: Ordner '{dice_source_folder}' nicht gefunden!")
        return

    # --- 2. Input Bild laden ---
    try:
        original_img = Image.open(input_image_path)
        # Transparenz fixen
        if original_img.mode in ('RGBA', 'LA'):
            bg = Image.new('L', original_img.size, 255)
            bg.paste(original_img.convert('L'), mask=original_img.getchannel('A'))
            original_img = bg
        else:
            original_img = original_img.convert('L')
    except Exception as e:
        print(f"Fehler beim Bildladen: {e}")
        return

    # --- 3. Dimensionen berechnen ---
    width, height = original_img.size
    if vertical_dice is None:
        aspect_ratio = height / width
        vertical_dice = int(horizontal_dice * aspect_ratio)

    print(f"Modus: Smart Rotation | Grid: {horizontal_dice}x{vertical_dice}")

    # --- 4. Würfel laden & Rotationen cachen ---
    # Wir laden jeden Würfel und erstellen 4 rotierte Versionen im Speicher
    dice_variants = {} # Dictionary: Key = Augenzahl (1-6), Value = Liste von DiceVariant Objekten
    dice_render_size = 50 # Größe im finalen Bild

    print("Generiere Rotations-Varianten...")
    for i in range(1, 7):
        path = os.path.join(dice_source_folder, f"{i}.png")
        if not os.path.exists(path):
            print(f"Fehler: {i}.png fehlt!")
            return
        
        base_img = Image.open(path).resize((dice_render_size, dice_render_size)).convert('L')
        dice_variants[i] = []

        # Erstelle 4 Rotationen (0, 90, 180, 270 Grad)
        for rot in [0, 90, 180, 270]:
            # rotate dreht gegen den Uhrzeigersinn
            rotated_img = base_img.rotate(rot)
            variant = DiceVariant(rotated_img, i, rot)
            dice_variants[i].append(variant)

    # --- 5. Das Originalbild vorbereiten ---
    # Wir brauchen das Originalbild in der exakten Größe, damit wir Ausschnitte ("Crops") machen können
    # Zielgröße in Pixeln für das interne Raster
    target_w = horizontal_dice * COMPARE_RES
    target_h = vertical_dice * COMPARE_RES
    
    # Skalieren für die Analyse (nicht für den Output!)
    analyze_img = original_img.resize((target_w, target_h), resample=Image.Resampling.LANCZOS)
    
    # Output Leinwand
    output_img = Image.new('L', (horizontal_dice * dice_render_size, vertical_dice * dice_render_size))

    # --- 6. Der Algorithmus ---
    print("Berechne optimale Ausrichtung (das kann einen Moment dauern)...")
    
    total_dice = horizontal_dice * vertical_dice
    count = 0

    for y in range(vertical_dice):
        for x in range(horizontal_dice):
            # 1. Ausschnitt (Chunk) aus dem Analyse-Bild holen
            box = (x * COMPARE_RES, y * COMPARE_RES, (x + 1) * COMPARE_RES, (y + 1) * COMPARE_RES)
            chunk = analyze_img.crop(box)
            chunk_data = list(chunk.getdata()) # Pixelwerte als Liste
            
            # 2. Durchschnittshelligkeit berechnen -> Bestimmt die Augenzahl
            avg_brightness = sum(chunk_data) / len(chunk_data)
            
            # Mapping: 0=Dunkel(6), 255=Hell(1)
            val = int(avg_brightness / 256 * 6)
            if val > 5: val = 5
            target_value = 6 - val # Das ist die Würfelzahl (1-6), die wir brauchen
            
            # 3. Die beste Rotation für DIESE Augenzahl finden
            # Wir holen uns die 4 rotiertern Varianten für die ermittelte Zahl
            candidates = dice_variants[target_value]
            
            best_variant = None
            min_diff = float('inf')

            # Vergleiche den Original-Ausschnitt mit den 4 Rotationen
            for variant in candidates:
                diff = get_difference(chunk_data, variant.compare_data)
                if diff < min_diff:
                    min_diff = diff
                    best_variant = variant
            
            # 4. Besten Würfel in das Output-Bild kleben
            pos = (x * dice_render_size, y * dice_render_size)
            output_img.paste(best_variant.image, pos)
            
            # Fortschrittsanzeige in der Konsole
            count += 1
            if count % 500 == 0:
                print(f"Fortschritt: {int(count/total_dice*100)}%", end="\r")

    # --- 7. Speichern ---
    base_name = os.path.basename(input_image_path)
    file_name_without_ext = os.path.splitext(base_name)[0]
    output_path = os.path.join(output_folder, f"gradient_dice_{file_name_without_ext}.png")
    
    output_img.save(output_path)
    print(f"\nFertig! Gespeichert: {output_path}")
    output_img.show()

# --- UI & START ---
def select_file():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    file_path = filedialog.askopenfilename(
        title="Wähle Bild", filetypes=[("Bilder", "*.jpg *.png *.bmp *.webp")]
    )
    root.destroy()
    return file_path

if __name__ == "__main__":
    print("--- Python Smart Dice Art (mit Rotation) ---")
    f = select_file()
    if f:
        try:
            h = int(input("Breite in Würfeln (z.B. 80): "))
            v_in = input("Höhe (Enter für Auto): ")
            v = int(v_in) if v_in.strip() else None
            create_smart_dice_art(f, h, v)
        except ValueError:
            print("Ungültige Eingabe.")