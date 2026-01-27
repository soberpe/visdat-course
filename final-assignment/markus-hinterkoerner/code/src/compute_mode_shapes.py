def compute_mode_shapes(data, haus, knoten_liste, mode_windows, referenz_knoten, delta_f):
    """
    Bestimmt die Modeformen eines Hochhauses aus den FRF-Daten (Imaginärteil).
    
    Beschreibung
    ------------
    Die Funktion durchsucht definierte Frequenzfenster nach Peaks im Imaginärteil des Referenzknotens.
    Jeder Peak entspricht einer Eigenfrequenz (Mode). Für jede Mode wird die Auslenkung
    an allen Knoten als Modeform bestimmt.

    Parameter
    ----------
    data : dict
        Messdaten aller Hochhäuser und Knoten. Struktur:
        data[haus][knoten] = {"f": Frequenzen, "Im": Imaginärteil, "Re": Realteil}
    haus : str
        Name des Hochhauses, z.B. "Hochhaus 1"
    knoten_liste : list of str
        Liste der Knoten/Messpunkte, z.B. ["E1","E2","E3"]
    mode_windows : list of tuples
        Liste von Frequenzfenstern [(f_min1, f_max1), ...], in denen Peaks gesucht werden
    referenz_knoten : str
        Knoten, dessen Imaginärteil als Referenz für die Peaks dient
    delta_f : float
        Frequenzauflösung (1 / Messdauer T)

    Returns
    -------
    mode_freqs : list of float
        Gefundene Eigenfrequenzen der Moden
    mode_shapes : list of np.array
        Modeformen als Arrays mit Werten für jeden Knoten
    """

    import numpy as np
    from scipy.signal import find_peaks

    # -----------------------------
    # Listen zur Speicherung
    # -----------------------------
    mode_freqs = []    # Gefundene Eigenfrequenzen
    mode_shapes = []   # Modeformen

    # -----------------------------
    # Referenzknoten
    # -----------------------------
    f_ref = data[haus][referenz_knoten]["f"]         # Frequenzen des Referenzknotens
    im_ref = np.abs(data[haus][referenz_knoten]["Im"])  # Imaginärteil (absolut) des Referenzknotens

    # -----------------------------
    # Schleife über alle Frequenzfenster
    # -----------------------------
    for f_min, f_max in mode_windows:
        # Maske für Frequenzen innerhalb des aktuellen Fensters
        mask = (f_ref >= f_min) & (f_ref <= f_max)

        rel_threshold = 0.15  # Minimal-Prominenz für Peaks (15% des Maximums im Fenster)

        # Peaks im Imaginärteil des Referenzknotens suchen
        peaks, props = find_peaks(
            im_ref[mask],
            prominence=rel_threshold * np.max(im_ref[mask])
        )

        # Wenn kein Peak gefunden, Fenster überspringen
        if len(peaks) == 0:
            continue

        # Höchster Peak im Fenster
        peak_idx = peaks[np.argmax(im_ref[mask][peaks])]
        f_mode = f_ref[mask][peak_idx]  # Eigenfrequenz
        mode_freqs.append(f_mode)       # Eigenfrequenz speichern

        # -----------------------------
        # Modeform für alle Knoten bestimmen
        # -----------------------------
        shape = []
        for knoten in knoten_liste:
            f = data[haus][knoten]["f"]      # Frequenzen des Knotens
            im = data[haus][knoten]["Im"]    # Imaginärteil
            # Index, der am nächsten zur Eigenfrequenz liegt
            idx = np.argmin(np.abs(f - f_mode))
            shape.append(im[idx])            # Imaginärwert zur Modeform hinzufügen

        shape = np.array(shape)             # In NumPy-Array umwandeln
        mode_shapes.append(shape)           # Modeform speichern

    # -----------------------------
    # Rückgabe
    # -----------------------------
    return mode_freqs, mode_shapes