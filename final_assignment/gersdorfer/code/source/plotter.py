import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_transfer_function(ax, freq, H, f_max, title):
    """
    Plottet den Betrag der Übertragungsfunktion in ein bestehendes Axes-Objekt.
    """
    f_range = (freq >= 0) & (freq <= f_max)

    ax.clear()
    ax.plot(freq[f_range], np.abs(H[f_range]))
    ax.set_xlabel("Frequenz [Hz]")
    ax.set_ylabel("Amplitude")
    ax.set_title(title)
    ax.grid(True)


def plot_imaginary_comparison(ax, freq, H, freq_imag, f_max):
    """
    Vergleich Imaginärteil FFT vs. CSV/LabVIEW
    """
    f_range = (freq >= 0) & (freq <= f_max)
    H_imag = np.imag(H)

    ax.clear()
    ax.plot(freq[f_range], freq_imag[f_range], label="CSV / LabVIEW")
    ax.plot(freq[f_range], H_imag[f_range], "--", label="FFT")
    ax.set_xlabel("Frequenz [Hz]")
    ax.set_ylabel("Im")
    ax.set_title("Imaginärteil Vergleich")
    ax.legend()
    ax.grid(True)
