import numpy as np


def pink_noise_time_signal(fs, t_vec, T1, T2, T3):
    """
    Erzeugt ein zeitabhängiges rosa Rauschsignal mit Ein- und Ausblendung.

    Parameter:
    fs    : Abtastfrequenz [Hz]
    t_vec : Zeitvektor
    T1    : Ende Ramp-Up
    T2    : Beginn Ramp-Down
    T3    : Ende Ramp-Down

    Rückgabe:
    xnoise : Rauschsignal
    """

    # ------------------------------------------------------------
    # Grundparameter
    # ------------------------------------------------------------
    dim = len(t_vec)
    T = t_vec[-1]

    N = int(np.round(fs * T))
    if N % 2 == 1:
        N += 1

    time = np.arange(N) / fs

    # ------------------------------------------------------------
    # Weißes Rauschen erzeugen
    # ------------------------------------------------------------
    s = np.random.normal(0.0, 1.0, N)

    # ------------------------------------------------------------
    # Frequenzgewichtung für rosa Rauschen
    # ------------------------------------------------------------
    a = fs / 10.0
    F = np.zeros(N // 2)

    for i in range(N // 2):
        F[i] = 1.0 / (1.0 + (a * i / N) ** 2) ** 0.25

    F = np.concatenate([F, F[::-1]])

    # ------------------------------------------------------------
    # FFT → Gewichtung → IFFT
    # ------------------------------------------------------------
    S = np.fft.fft(s)
    S *= F
    sig = np.real(np.fft.ifft(S))

    # ------------------------------------------------------------
    # Normierung
    # ------------------------------------------------------------
    sig /= np.max(np.abs(sig))

    # ------------------------------------------------------------
    # Interpolation auf gewünschten Zeitvektor
    # (Ersatz für Scilab interp / splin)
    # ------------------------------------------------------------
    xnoise = np.interp(t_vec, time, sig)

    # ------------------------------------------------------------
    # Ein- und Ausblendung (Ramp-Up / Ramp-Down)
    # ------------------------------------------------------------
    for i, t_cur in enumerate(t_vec):
        if t_cur <= T1:
            xnoise[i] *= max(0.0, t_cur / T1)
        elif T2 <= t_cur <= T3:
            xnoise[i] *= max(0.0, 1.0 - (t_cur - T2) / (T3 - T2))
        elif t_cur > T3:
            xnoise[i] = 0.0

    return xnoise


def read_mrf(measure_file_name: str, measure_id: int):
    """
    Liest eine FD *.mrf (Measure Result File) Datei und extrahiert
    das Measure mit der gewünschten ID.

    Parameter
    ----------
    measure_file_name : str
        Vollständiger Pfad zur *.mrf Datei (inklusive Endung)
    measure_id : int
        ID des gewünschten Measures (1-basiert)

    Rückgabewerte
    -------------
    t : numpy.ndarray
        Zeitvektor
    y : numpy.ndarray
        Signalvektor (ausgewähltes Measure)
    """

    try:
        file = open(measure_file_name, "r", encoding="utf-8")
    except OSError:
        raise RuntimeError(
            "ERROR: Datei konnte in Funktion read_mrf nicht geöffnet werden"
        )

    # Initialisierung der Ergebnisarrays (Blockweise Erweiterung wie im Scilab-Code)
    block_size = 100000
    t = np.zeros(block_size)
    y = np.zeros(block_size)

    # ------------------------------------------------------------------
    # Header lesen bis der Eintrag 'Topology' gefunden wird
    # ------------------------------------------------------------------
    while True:
        line = file.readline()
        if not line:
            file.close()
            raise RuntimeError("ERROR: 'Topology' nicht im Header gefunden")

        line = line.strip()
        if line.startswith("Topology"):
            break

    # Zwei weitere Header-Zeilen überspringen
    line = file.readline().strip()
    line = file.readline().strip()

    # Anzahl der Measures bestimmen
    num_measures = len(line.split())

    if measure_id > num_measures or measure_id < 1:
        file.close()
        raise ValueError(
            "ERROR: Measure-ID überschreitet die Anzahl verfügbarer Measures"
        )

    # ------------------------------------------------------------------
    # Suchen des Datenbereichs
    # ------------------------------------------------------------------
    while True:
        line = file.readline()
        if not line:
            file.close()
            raise RuntimeError("ERROR: 'Data'-Bereich nicht gefunden")

        line = line.strip()
        if line.startswith("Data"):
            break

    # Eine Zeile überspringen (laut Dateiformat)
    file.readline()

    # ------------------------------------------------------------------
    # Einlesen der Messdaten
    # ------------------------------------------------------------------
    index = 0

    while True:
        line = file.readline()
        if not line:
            break

        # Zeitwert lesen
        try:
            t[index] = float(line.strip())
        except ValueError:
            continue

        # Alle Measures zu diesem Zeitwert lesen
        for i in range(1, num_measures + 1):
            measure_line = file.readline()
            if not measure_line:
                break

            if i == measure_id:
                try:
                    y[index] = float(measure_line.strip())
                except ValueError:
                    y[index] = 0.0

        index += 1

        # Speicher dynamisch erweitern
        if index % block_size == 0:
            t = np.concatenate((t, np.zeros(block_size)))
            y = np.concatenate((y, np.zeros(block_size)))

    file.close()

    # Arrays auf tatsächlich gelesene Länge kürzen
    t = t[:index]
    y = y[:index]

    return t, y
