from pathlib import Path  # Für Pfadoperationen
import numpy as np        # Für numerische Operationen
import pyvista as pv      # Für 3D-Visualisierung
from scipy.signal import find_peaks  # Für Peak-Erkennung

# =====================================================
# 0. EINSTELLUNGEN
# =====================================================
INTERAKTIV_3D = True  # True = interaktive 3D-Plots anzeigen, False = nur Screenshots speichern

# =====================================================
# 1. HILFSFUNKTIONEN IMPORTIEREN
# =====================================================
from src.read_time_signal import read_time_signal       # Zeitbereichsdaten einlesen
from src.read_frf_file import read_frf_file             # FRF-Dateien einlesen
from src.plot_frf_im import plot_frf_im                 # FRF Imaginärteil Plots
from src.compute_mode_shapes import compute_mode_shapes # Modeformen-Berechnung
from src.plot_modeformen_2d import plot_modeformen_2d   # 2D Modeformen Plots
from src.plot_modeformen_3d import plot_modeformen_3d   # 3D Modeformen Plots

# =====================================================
# 2. HAUPTPROGRAMM
# =====================================================
if __name__ == "__main__":

    base_path = Path(__file__).parent / "data"  # Basisverzeichnis für Messdaten
    plot_path = Path(__file__).parent.parent / "assets/screenshots"
    plot_path.mkdir(parents=True, exist_ok=True)

    hochhaeuser = ["Hochhaus_1", "Hochhaus_2", "Hochhaus_3"]
    knoten_liste = ["E1", "E2", "E3"]
    T = 10
    delta_f = 1 / T  # Frequenzauflösung

    # Unterordner für jedes Hochhaus im Plot-Verzeichnis anlegen
    plot_paths = {}
    for haus in hochhaeuser:
        haus_plot_path = plot_path / haus
        haus_plot_path.mkdir(exist_ok=True)
        plot_paths[haus] = haus_plot_path

    # -------------------------------------------------
    # Daten einlesen
    # -------------------------------------------------
    data = {}
    for haus in hochhaeuser:
        data[haus] = {}

        for knoten in knoten_liste:

            # Pfade zu den FRF-Dateien
            im_file = base_path / haus / f"{knoten}_Im.txt"
            # re_file = base_path / haus / f"{knoten}_Re.txt"

            # Prüfen, ob Dateien existieren
            if not im_file.exists():
                raise FileNotFoundError(f"FRF-Dateien fehlen für {haus}, {knoten}")

            # FRF-Dateien einlesen
            df_im = read_frf_file(im_file)
            # df_re = read_frf_file(re_file)

            # Frequenzachse erzeugen
            N = len(df_im)
            f_phys = np.arange(N) * delta_f

            # Daten strukturiert speichern
            data[haus][knoten] = {
                "f": f_phys,
                "Im": df_im["val"].values
            }

    # -------------------------------------------------
    # FRF Imaginärteil Plots (2D)
    # -------------------------------------------------
    for haus in hochhaeuser:
        plot_frf_im(
            data_haus=data[haus],      # Nur das aktuelle Hochhaus
            haus=haus,
            knoten_liste=knoten_liste,
            plot_path=plot_paths[haus] # Speichern im jeweiligen Unterordner
        )

    # -------------------------------------------------
    # Eigenfrequenzen bestimmen
    # -------------------------------------------------
    referenz_knoten = "E1"
    print("=== Gefundene Eigenfrequenzen ===\n")
    for haus in hochhaeuser:
        f_ref = data[haus][referenz_knoten]["f"]
        im_ref = np.abs(data[haus][referenz_knoten]["Im"])
        height_thr = 0.25 * np.max(im_ref)  # Peak-Threshold
        min_distance_pts = int(1.5 / delta_f)  # Mindestabstand der Peaks

        peaks, _ = find_peaks(im_ref, height=height_thr, distance=min_distance_pts)
        eigenfrequenzen = f_ref[peaks]

        print(f"{haus}:")
        if len(eigenfrequenzen) == 0:
            print("  Keine Peaks über Threshold gefunden")
        else:
            for i, freq in enumerate(eigenfrequenzen):
                print(f"  Mode {i+1}: {freq:.3f} Hz")
        print()

    # -------------------------------------------------
    # Modeformen 2D Plot
    # -------------------------------------------------
    mode_windows_all = {
        "Hochhaus_1": [(2,4),(8,10),(15,17),(30,36)],
        "Hochhaus_2": [(2,4),(8,10),(15,17),(30,36)],
        "Hochhaus_3": [(2,4),(8,10),(15,17),(30,36)]
    } # Frequenzfenster für Moden

    for haus in hochhaeuser:
        mode_freqs, mode_shapes = compute_mode_shapes(
            data, haus, knoten_liste, mode_windows_all[haus], referenz_knoten, delta_f
        )
        plot_modeformen_2d(
            mode_freqs,
            mode_shapes,
            haus,
            knoten_liste,
            plot_paths[haus]
        )

    # -------------------------------------------------
    # 3D Modeformen
    # -------------------------------------------------
    stl_file = base_path / "Hochhaus.stl"
    if not stl_file.exists():
        raise FileNotFoundError(f"STL-Datei nicht gefunden: {stl_file}")

    mesh_orig = pv.read(stl_file) # Original-Mesh des Hochhauses laden

    # Knotenhöhen für die Modeform-Interpolation
    y_min = mesh_orig.points[:,1].min() # Fundament
    y_max = mesh_orig.points[:,1].max() # Oben
    knoten_hoehen = np.array([y_max, (y_min + y_max)/2, y_min]) # E1, E2, E3

    for haus in hochhaeuser:
        mode_freqs, mode_shapes = compute_mode_shapes(
            data, haus, knoten_liste, mode_windows_all[haus], referenz_knoten, delta_f
        )
        plot_modeformen_3d(
            mesh_orig,
            mode_shapes,
            mode_freqs,
            knoten_hoehen,
            haus,
            plot_paths[haus],
            interaktiv=INTERAKTIV_3D,
            subdivide_n=2
        )