#Standard-Bibliotheken
import os
import sys

#Third-Party Bibliotheken
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# Projektpfade
# ============================================================

#Basisverzeichnis (dient zur Vermeidung von Absolutpfaden)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))      #Bestimmung des Basisverzeichnis

# Python-Module (Datenverarbeitung/PLots etc.)
SOURCE_DIR = os.path.join(BASE_DIR, "source")
sys.path.insert(0, SOURCE_DIR)                              #Zugriff auf meine Module/Funktionen in Source

# Datenverzeichnis
DATA_DIR = os.path.join(BASE_DIR, "data")                   #Zugriff auf meine CSV- Daten in data




# ============================================================
# Eigene Module importieren
# ============================================================
import data_loader as dl
import signal_processing as sp
import plotter as plo


# ============================================================
# Konfiguration / Parameter
# ============================================================

#Messdatei
FILE_NAME = "P2b_OhneTilger.csv"
file_path = os.path.join(DATA_DIR, FILE_NAME)   

#CSV-Parameter
header_rows = 22
acc_col = ("Acceleration")
force_col = ("Force")
freq_imag_col = ("Untitled")

#Messparameter
fs = 12800              #Gewählte Abtastrate der Messung

#Plotparameter
f_max = 40                              #Maximale Frequenz der Visualisierung


# ============================================================
# Daten einlesen
# ============================================================

# Ausführung der Einlese Funktion
freq_imag, acc_timedata, force_timedata  = dl.load_measurement_csv(file_path, header_rows, acc_col, force_col, freq_imag_col)


# ============================================================
# Signalverarbeitung
# ============================================================

# Ausführung der FFT Funktion
freq, H = sp.compute_fft(acc_timedata, force_timedata, fs)



# ============================================================
# Visualisierung
# ============================================================


f_range= (freq>=0) & (freq <=f_max)     #Dargestellter Frequenzbereich

# Plots

# Erzeugung einer Figure mit zwei untereinanderliegenden Achsen:
# ax1 Betrag der Übertragungsfunktion |H(f)|
# ax2 Vergleich des Imaginärteils (FFT vs. CSV/LabVIEW)
# sharex=True sorgt für eine gemeinsame Frequenzachse

fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(10, 8), sharex=True)

# Betrag der Übertragungsfunktion
plo.plot_transfer_function(ax1, freq, H, f_max, "Übertragungsfunktion Betrag")

# Imaginärteil-Vergleich
plo.plot_imaginary_comparison(ax2, freq, H, freq_imag, f_max)

plt.tight_layout()      # Automatische Anpassung der Abstände zwischen Subplots sonst überlappen sich manche Texte
plt.show()

