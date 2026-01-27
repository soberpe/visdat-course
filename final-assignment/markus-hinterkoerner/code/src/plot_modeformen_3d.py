def plot_modeformen_3d(mesh_orig, mode_shapes, mode_freqs, knoten_hoehen, haus, plot_path,
                       interaktiv=True, subdivide_n=2):
    """
    Plottet alle Modeformen eines Hochhauses in einer 3D-Darstellung.

    Koordinatensystem:
    - y-Richtung: Höhe des Gebäudes
    - x-Richtung: Breite (rein geometrisch)
    - z-Richtung: Auslenkung der Modeform
    """

    # Import für glatte, monotone Interpolation der Modeformen
    # PCHIP vermeidet unphysikalische Überschwinger
    from scipy.interpolate import PchipInterpolator

    # PyVista wird für die 3D-Visualisierung und das Warping des Meshes verwendet
    import pyvista as pv

    # NumPy für numerische Operationen
    import numpy as np

    # Schleife über alle Modeformen
    # mode_idx: Index der Mode (0-basiert)
    # mode_shape: Auslenkungen der Knoten für diese Mode
    for mode_idx, mode_shape in enumerate(mode_shapes):

        # -----------------------------
        # Vorbereitung des Meshes
        # -----------------------------

        # Kopie des Original-Meshes erstellen,
        # damit das Ursprungsmesh unverändert bleibt
        mesh = mesh_orig.copy()

        # Optional: Unterteilung des Meshes für eine glattere Darstellung
        # "linear" bedeutet lineare Unterteilung der Elemente
        if subdivide_n > 0:
            mesh = mesh.subdivide(subdivide_n, "linear")

        # -----------------------------
        # Berechnung der Verschiebungen
        # -----------------------------

        # Initialisieren eines Verschiebungsarrays
        # gleiche Dimension wie die Mesh-Punkte (x, y, z)
        displacement = np.zeros_like(mesh.points)

        # Interpolationsfunktion für die Modeform:
        # - knoten_hoehen[::-1]: Fundament zuerst
        # - mode_shape[::-1]: passende Reihenfolge der Auslenkungen
        spline = PchipInterpolator(
            knoten_hoehen[::-1],
            mode_shape[::-1]
        )

        # Z-Auslenkung (Querbewegung) wird abhängig von der y-Position berechnet
        # mesh.points[:, 1] entspricht der Höhe jedes Mesh-Punktes
        displacement[:, 2] = spline(mesh.points[:, 1])

        # Speichern der Verschiebungen im Mesh
        # "U" ist der Standardname für Verschiebungsvektoren in PyVista
        mesh["U"] = displacement

        # -----------------------------
        # Skalierung der Modeform
        # -----------------------------

        # Maximale absolute Auslenkung der Mode
        max_auslenkung = np.max(np.abs(mode_shape))

        # Gesamthöhe des Hochhauses
        hoehe_hh = knoten_hoehen.max() - knoten_hoehen.min()

        # Skalierungsfaktor:
        # Die Modeform wird so skaliert, dass die maximale Auslenkung
        # etwa 10 % der Gebäudehöhe beträgt (rein visuell)
        factor = hoehe_hh / max_auslenkung * 0.1

        # Ausgabe des verwendeten Skalierungsfaktors zur Kontrolle
        # print(f"{haus} – Mode {mode_idx+1}: Warping-Faktor = {factor:.2f}")

        # -----------------------------
        # Warping des Meshes
        # -----------------------------

        # Anwendung der Verschiebungen auf das Mesh
        # Die Verschiebungen werden mit dem Faktor skaliert
        warped_mesh = mesh.warp_by_vector("U", factor=factor)

        # -----------------------------
        # Darstellung
        # -----------------------------

        if interaktiv:
            # -----------------------------
            # Interaktive Darstellung (Fenster öffnet sich)
            # -----------------------------

            plotter = pv.Plotter()

            # Hinzufügen des verformten Meshes
            plotter.add_mesh(
                warped_mesh,
                color='lightblue',
                show_edges=True,
                opacity=1.0
            )

            # Koordinatenachsen anzeigen
            plotter.add_axes()

            # Gitternetz zur Orientierung
            plotter.show_grid()

            # Kamerablick:
            # Blick von der Seite, Hochrichtung nach oben
            plotter.view_vector(
                vector=(-1, 0, 0),
                viewup=(0, 1, 0)
            )

            # Anzeigen des Plots
            plotter.show(title=f"{haus} – 3D Auslenkung Mode {mode_idx+1}")

            # Plotter schließen
            plotter.close()

        else:
            # -----------------------------
            # Off-Screen Rendering (nur Screenshot)
            # -----------------------------

            # Plotter ohne Fenster (z. B. für automatisierte Auswertung)
            plotter_off = pv.Plotter(off_screen=True)

            plotter_off.add_mesh(
                warped_mesh,
                color='lightblue',
                show_edges=True,
                opacity=1.0
            )

            plotter_off.add_axes()
            plotter_off.show_grid()

            plotter_off.view_vector(
                vector=(-1, 0, 0),
                viewup=(0, 1, 0)
            )

            # Pfad für die Bilddatei
            full_path = plot_path / f"{haus}_Mode{mode_idx+1}_3D.png"

            # Screenshot speichern
            plotter_off.screenshot(
                full_path,
                window_size=(1600, 900)
            )

            # Plotter schließen, um Ressourcen freizugeben
            plotter_off.close()