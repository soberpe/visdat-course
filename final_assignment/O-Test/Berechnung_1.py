import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import subprocess
from pathlib import Path

# Eigene Module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'src')))
import Module as M

# Laden der Eigenen Funktionen von den Eigenen Modulen
#from Module import (pink_noise_time_signal, read_mrf)

def main():
    # -----------------------------------------------------------------------------------------------------
    # Verzeichnisse definieren
    # definieren Pfad FreeDyn-Eingabedatei (FDS)
    ## Typ: str 
    fdsFilePath = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'data_2/EFS2'))
    ## Typ: pathlib.Path
    #fdsFilePath = Path(__file__).resolve().parent / "data" / "EFS2.fds"
    
    # ------------------------------------------------------------
    # Parameterdefinition
    
    fs = 100.0  # Abtastfrequenz [Hz]

    T1 = 0.1
    T2 = 7.0
    T3 = 8.0

    dt = 0.01
    t_vec = np.arange(0.0, 10.0 + dt, dt)
    dim = len(t_vec)

    # ------------------------------------------------------------
    # 1) Erzeugen des rosa Rauschsignals
    
    x_noise = M.pink_noise_time_signal(fs, t_vec, T1, T2, T3)

    plt.figure()
    plt.plot(t_vec, x_noise)
    plt.xlabel("Zeit [s]")
    plt.ylabel("Kraft [N]")
    plt.title("Eingangssignal (Rosa Rauschen)")
    plt.grid(True)

    # ------------------------------------------------------------
    # 2) FFT des Eingangssignals

    X = (1.0 / dim) * np.fft.fft(x_noise)

    # Speichern des Eingangssignals
    Kraftpfad = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"data_2","Kraft.txt"))
    np.savetxt(
        Kraftpfad,
        np.column_stack((t_vec, x_noise)),
    )

    # ------------------------------------------------------------
    # 3) Simulation mit FreeDyn

    # Pfad für free_dyn_exe anpassen !!!!!!!!!!!!!!!
    free_dyn_exe = Path(r"C:\FreeDyn_Release_2024_9\FreeDyn_2024.9\bin\FreeDyn.exe")

    command = [str(free_dyn_exe), fdsFilePath + ".fds"]

    # Aufruf der Simulation
    subprocess.run(command, shell=True)

    # ------------------------------------------------------------
    # Statusprüfung
    
    status_file = Path(fdsFilePath).with_suffix(".status")

    if status_file.exists():
        status_text = status_file.read_text(encoding="utf-8", errors="ignore")
        if "Computation has been successfully finished" in status_text:
            print("Simulation erfolgreich")
        else:
            print("Simulation gescheitert")
    else:
        print("Statusdatei nicht gefunden")

    # ------------------------------------------------------------
    # Einlesen der Messdaten
    
    measure_file = Path(fdsFilePath).with_suffix(".mrf")
    t_mes, y = M.read_mrf(measure_file, measure_id=1)

    plt.figure()
    plt.plot(t_mes, y)
    plt.xlabel("Zeit [s]")
    plt.ylabel("Auslenkung [mm]")
    plt.title("Simulationsergebnis")
    plt.grid(True)

    # ------------------------------------------------------------
    # 4) FFT des Ausgangssignals
    
    Y = (1.0 / dim) * np.fft.fft(y)

    # ------------------------------------------------------------
    # 5) Berechnung der Übertragungsfunktion H
    
    H = np.zeros(dim, dtype=complex)
    for i in range(dim):
        if X[i] != 0:
            H[i] = Y[i] / X[i]

    f_vec = np.arange(0.0, dim * dt, dt)

    # ------------------------------------------------------------
    # 6) Impulsantwort mittels IFFT
    
    h = dim * np.fft.ifft(H)

# Speichern der Übertragungsfunktion
    hpfad = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"data_2","Uebertragungsfunktion.txt"))
    np.savetxt(
        hpfad,
        np.column_stack((t_mes[: len(h)], h.real)),
        header="Zeit [s]\tImpulsantwort",
    )

    plt.figure()
    plt.subplot(2, 1, 1)
    plt.plot(f_vec, np.abs(H))
    plt.ylabel("|H(f)|")
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(t_mes[: len(h)], h.real)
    plt.xlabel("Zeit [s]")
    plt.ylabel("h(t)")
    plt.grid(True)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
