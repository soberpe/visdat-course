def plot_modeformen_2d(mode_freqs, mode_shapes, haus, knoten_liste, plot_path):
    """
    Plottet die berechneten Modeformen eines Hochhauses in einer 2D-Darstellung.

    Darstellung:
    - y-Achse: Geschosse (inkl. Fundament)
    - x-Achse: Auslenkung der Modeform
    - Fundament wird als feste Referenz bei Auslenkung = 0 dargestellt
    """

    # Import der benötigten Bibliotheken (lokal innerhalb der Funktion)
    # matplotlib: für die grafische Darstellung
    # numpy: für numerische Operationen und Arrays
    import matplotlib.pyplot as plt
    import numpy as np

    # Erstellen einer neuen Figur mit definierter Größe
    # Größere Höhe, damit die Geschosse gut unterscheidbar sind
    plt.figure(figsize=(7, 8))

    # Erzeugen der y-Positionen für die Darstellung
    # +1, da zusätzlich zum obersten Knoten auch das Fundament dargestellt wird
    # Beispiel: 3 Knoten → y = [0, 1, 2, 3]
    y_positions = np.arange(len(knoten_liste) + 1)

    # -----------------------------
    # Ursprungsform (unverformtes System)
    # -----------------------------

    # Darstellung der unverformten Struktur als senkrechte Linie bei x = 0
    # Diese Linie dient als Referenz für die Modeformen
    plt.plot(
        np.zeros(len(y_positions)),   # x-Werte = 0 (keine Auslenkung)
        y_positions,                  # y-Werte = Geschosshöhen
        color='red',
        linewidth=2,
        label='Ursprüngliche Form'
    )

    # -----------------------------
    # Modeformen plotten
    # -----------------------------

    # Schleife über alle berechneten Eigenfrequenzen
    # i = Index der Mode (0-basiert)
    # f_mode = Eigenfrequenz der jeweiligen Mode
    for i, f_mode in enumerate(mode_freqs):

        # Sicherheitsabfrage:
        # Falls keine gültige Eigenfrequenz vorhanden ist, wird diese Mode übersprungen
        if f_mode is None or np.isnan(f_mode):
            continue

        # Zugehörige Modeform aus dem Array holen
        # mode_shapes[i] enthält die Auslenkungen der einzelnen Knoten
        mode_shape = mode_shapes[i]

        # Fundament zur Modeform hinzufügen:
        # - Fundament hat immer Auslenkung 0
        # - Reihenfolge wird umgedreht ([::-1]),
        #   damit die Darstellung von unten (Fundament) nach oben korrekt ist
        mode_shape_with_fundament = np.append(0, mode_shape[::-1])

        # Plot der aktuellen Modeform
        plt.plot(
            mode_shape_with_fundament,  # x-Achse: Auslenkungen
            y_positions,                # y-Achse: Geschosse
            marker='o',                 # Marker an den Knoten
            linewidth=2,
            label=f"Mode {i+1} ({f_mode:.2f} Hz)"  # Beschriftung mit Modennummer und Frequenz
        )

    # -----------------------------
    # Achsenbeschriftungen und Layout
    # -----------------------------

    # Beschriftung der y-Achse:
    # Fundament unten, darüber die Knoten in umgekehrter Reihenfolge
    y_labels = ["Fundament"] + knoten_liste[::-1]
    plt.yticks(y_positions, y_labels)

    # Achsenbeschriftungen
    plt.xlabel("Auslenkung")
    plt.ylabel("Knoten")

    # Titel des Plots mit Hausbezeichnung
    plt.title(f"Modeformen – {haus}")

    # Legende anzeigen
    plt.legend()

    # Gitter zur besseren Lesbarkeit
    plt.grid(True)

    # -----------------------------
    # Speichern und Aufräumen
    # -----------------------------

    # Speichern des Plots als PNG-Datei im angegebenen Plot-Verzeichnis
    # dpi=300 für drucktaugliche Qualität
    plt.savefig(plot_path / f"{haus}_Modeformen_2D.png", dpi=300)

    # Schließen der Figur, um Speicher freizugeben
    plt.close()