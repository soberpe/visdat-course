import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image

def create_dice_art(input_image_path, horizontal_dice, vertical_dice=None):
    
    # --- PFAD-LOGIK FIX ---
    # Wir ermitteln den genauen Pfad, in dem dieses Python-Script liegt
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Der Output-Ordner und der dice-Ordner werden nun relativ zum Script gesucht
    output_folder = os.path.join(script_dir, "diceconverter-output")
    dice_source_folder = os.path.join(script_dir, "dice")

    # --- 1. Output-Ordner vorbereiten ---
    if not os.path.exists(output_folder):
        try:
            os.makedirs(output_folder)
            print(f"Ordner erstellt: {output_folder}")
        except OSError as e:
            print(f"Fehler beim Erstellen des Ordners: {e}")
            return

    # Dateiname für Output generieren
    base_name = os.path.basename(input_image_path)
    file_name_without_ext = os.path.splitext(base_name)[0]
    output_path = os.path.join(output_folder, f"dice_{file_name_without_ext}.png")

    # --- 2. Bild öffnen & Transparenz behandeln ---
    try:
        img = Image.open(input_image_path)
        if img.mode in ('RGBA', 'LA'):
            background = Image.new('L', img.size, 255)
            background.paste(img.convert('L'), mask=img.getchannel('A'))
            img = background
        else:
            img = img.convert('L')
    except Exception as e:
        print(f"Fehler beim Öffnen des Bildes: {e}")
        return

    # Proportionale Berechnung
    width, height = img.size
    if vertical_dice is None:
        aspect_ratio = height / width
        vertical_dice = int(horizontal_dice * aspect_ratio)

    print(f"Verarbeite Bild... Zielgröße: {horizontal_dice}x{vertical_dice} Würfel.")

    # --- 3. Skalieren ---
    small_img = img.resize((horizontal_dice, vertical_dice), resample=Image.Resampling.LANCZOS)
    
    # --- 4. Würfel laden (FIXED) ---
    dice_size = 50 
    dice_images = []
    
    # Wir prüfen nun den absoluten Pfad zum dice-Ordner
    if not os.path.exists(dice_source_folder):
        print("\n" + "!"*40)
        print(f"FEHLER: Der Ordner 'dice' wurde nicht gefunden!")
        print(f"Das Skript sucht hier: {dice_source_folder}")
        print("Bitte stelle sicher, dass der Ordner exakt 'dice' heißt (Kleinschreibung).")
        print("!"*40 + "\n")
        return

    try:
        for i in range(1, 7):
            # Wir bauen den Pfad: Script-Ordner -> dice -> 1.png
            path = os.path.join(dice_source_folder, f"{i}.png")
            
            d_img = Image.open(path).resize((dice_size, dice_size)).convert('L')
            dice_images.append(d_img)
    except FileNotFoundError:
        print(f"FEHLER: Bild '{path}' fehlt im 'dice'-Ordner.")
        return
    except Exception as e:
        print(f"Unbekannter Fehler beim Laden der Würfel: {e}")
        return

    # --- 5. Mosaik erstellen ---
    output_img = Image.new('L', (horizontal_dice * dice_size, vertical_dice * dice_size))
    pixels = small_img.load()

    for y in range(vertical_dice):
        for x in range(horizontal_dice):
            brightness = pixels[x, y]
            val = int(brightness / 256 * 6)
            if val > 5: val = 5
            dice_index = 5 - val 
            output_img.paste(dice_images[dice_index], (x * dice_size, y * dice_size))

    # --- 6. Speichern ---
    try:
        output_img.save(output_path)
        print("\n" + "="*40)
        print(f"FERTIG!")
        print(f"Output gespeichert unter:\n{output_path}")
        print("="*40)
        output_img.show()
    except Exception as e:
        print(f"Fehler beim Speichern: {e}")

def select_file():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    file_path = filedialog.askopenfilename(
        title="Wähle ein Bild für den Dice-Converter aus",
        filetypes=[("Bilder", "*.jpg *.jpeg *.png *.bmp *.webp")]
    )
    root.destroy()
    return file_path

if __name__ == "__main__":
    print("--- Python Dice Art Converter ---")
    input_file = select_file()
    
    if input_file:
        print(f"Ausgewählte Datei: {os.path.basename(input_file)}")
        try:
            h_input = input("Anzahl Würfel horizontal (z.B. 80): ")
            if not h_input.isdigit():
                print("Bitte eine ganze Zahl eingeben.")
            else:
                h_count = int(h_input)
                v_input = input("Anzahl Würfel vertikal (Enter für automatisch): ")
                v_count = int(v_input) if v_input.strip() else None
                create_dice_art(input_file, h_count, v_count)
        except ValueError:
            print("Fehler: Ungültige Eingabe.")
    else:
        print("Keine Datei ausgewählt.")