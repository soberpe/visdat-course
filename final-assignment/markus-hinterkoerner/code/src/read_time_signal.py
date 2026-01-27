def read_time_signal(filepath):
    """
    Liest Zeitbereichsdaten aus einer Datei ein (z. B. Beschleunigung oder Kraft).

    Erwartetes Dateiformat:
    - Zwei Spalten
        1. Zeit
        2. Amplitude (z. B. Beschleunigung, Kraft, Weg)
    - Tabulator als Spaltentrennzeichen
    - Dezimaltrennzeichen: Komma
    """

    # Pandas wird für das komfortable Einlesen der Textdatei verwendet
    import pandas as pd

    # -----------------------------
    # Existenzprüfung der Datei
    # -----------------------------

    # Prüfen, ob der übergebene Dateipfad existiert
    # Falls nicht, wird ein klarer Fehler ausgegeben
    if not filepath.exists():
        raise FileNotFoundError(f"Datei nicht gefunden: {filepath}")

    # -----------------------------
    # Einlesen der Zeitbereichsdaten
    # -----------------------------

    # Einlesen der Datei:
    # - sep="\t": Tabulator als Trennzeichen
    # - decimal=",": Komma als Dezimaltrennzeichen
    # - header=0: Erste Zeile enthält die Spaltenüberschriften
    df = pd.read_csv(
        filepath,
        sep="\t",
        decimal=",",
        header=0
    )

    # -----------------------------
    # Extraktion der Spalten
    # -----------------------------

    # Erste Spalte: Zeitwerte
    time = df.iloc[:, 0].values

    # Zweite Spalte: Amplitudenwerte
    amplitude = df.iloc[:, 1].values

    # Rückgabe der Zeit- und Amplitudensignale als NumPy-Arrays
    return time, amplitude