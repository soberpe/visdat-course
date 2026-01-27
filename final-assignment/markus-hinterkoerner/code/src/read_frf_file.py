def read_frf_file(filepath):
    """
    Liest eine FRF-Datei ein (z. B. Real- oder Imaginärteil der Frequenzantwort).
    
    Erwartetes Dateiformat:
    - Tabulator-getrennte Werte
    - Dezimalzeichen: Komma (',')
    - Zwei Spalten: 
        1. f: Frequenz
        2. val: Messwert (Re- oder Im-Teil)
    
    Parameter
    ----------
    filepath : Path
        Pfad zur FRF-Datei, die eingelesen werden soll.
    
    Returns
    -------
    pandas.DataFrame
        DataFrame mit den Spalten ["f", "val"]
    
    Raises
    ------
    FileNotFoundError
        Wenn die angegebene Datei nicht existiert.
    """

    import pandas as pd

    # -----------------------------
    # Existenzprüfung der Datei
    # -----------------------------
    if not filepath.exists():
        raise FileNotFoundError(f"Datei nicht gefunden: {filepath}")

    # -----------------------------
    # Einlesen der FRF-Datei
    # -----------------------------
    # - sep="\t": Tabulator als Spaltentrennzeichen
    # - decimal=",": Komma als Dezimaltrennzeichen
    # - names=["f","val"]: Spaltennamen festlegen
    # - header=0: Erste Zeile als Header interpretieren
    df = pd.read_csv(
        filepath,
        sep="\t",
        decimal=",",
        names=["f", "val"],
        header=0
    )

    # -----------------------------
    # Rückgabe
    # -----------------------------
    return df