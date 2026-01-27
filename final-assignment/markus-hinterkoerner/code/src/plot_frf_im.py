def plot_frf_im(data_haus, haus, knoten_liste, plot_path):
    """
    Plottet den Imaginärteil der FRF-Daten für EIN Hochhaus.

    Parameter
    ----------
    data_haus : dict
        Enthält die FRF-Daten eines Hochhauses (alle Knoten)
        Struktur:
        data_haus["E1"]["f"]  -> Frequenzarray
        data_haus["E1"]["Im"] -> Imaginärteil
    haus : str
        Name des Hochhauses (z.B. "Hochhaus 1")
    knoten_liste : list[str]
        Liste der Messpunkte/Knoten (z.B. ["E1", "E2", "E3"])
    plot_path : Path
        Zielordner, in dem der Plot gespeichert wird
    """

    import matplotlib.pyplot as plt
    import numpy as np

    # ---------------------------------------------------------
    # Sicherheitsprüfung: Sind überhaupt Daten vorhanden?
    # ---------------------------------------------------------
    if not data_haus:
        print(f"WARNUNG: Keine Daten für {haus} vorhanden – Plot wird übersprungen.")
        return

    # Neue Figure erzeugen
    plt.figure(figsize=(16, 9))

    # Merker, ob mindestens ein gültiger Knoten geplottet wurde
    plotted_anything = False

    # ---------------------------------------------------------
    # Schleife über alle gewünschten Knoten
    # ---------------------------------------------------------
    for knoten in knoten_liste:

        # Prüfen, ob der Knoten im Datensatz existiert
        if knoten not in data_haus:
            print(f"Hinweis: Knoten '{knoten}' existiert nicht in {haus} – wird übersprungen.")
            continue

        # Plotten des Imaginärteils über der Frequenz
        plt.plot(
            data_haus[knoten]["f"],
            data_haus[knoten]["Im"],
            label=knoten
        )

        plotted_anything = True

    # ---------------------------------------------------------
    # Falls kein einziger Knoten geplottet wurde → Abbruch
    # ---------------------------------------------------------
    if not plotted_anything:
        print(f"WARNUNG: Für {haus} konnte kein gültiger Knoten geplottet werden.")
        plt.close()
        return

    # Achsenbeschriftung und Titel
    plt.xlabel("Frequenz [Hz]")
    plt.ylabel("Imaginärteil")
    plt.title(f"Imaginärteil aller Knoten – {haus}")

    # Darstellung
    plt.legend()
    plt.grid(True)

    # ---------------------------------------------------------
    # x-Achse sinnvoll rastern (1 Hz Schritte)
    # Wir nehmen den ersten gültigen Knoten als Referenz
    # ---------------------------------------------------------
    erster_knoten = next(iter(data_haus))
    f_min = int(data_haus[erster_knoten]["f"][0])
    f_max = int(data_haus[erster_knoten]["f"][-1]) + 1
    plt.xticks(np.arange(f_min, f_max, 1))

    # ---------------------------------------------------------
    # Plot speichern
    # ---------------------------------------------------------
    plot_path.mkdir(parents=True, exist_ok=True)
    plt.savefig(plot_path / f"{haus}_Imaginaerteil.png", dpi=100)
    plt.close()