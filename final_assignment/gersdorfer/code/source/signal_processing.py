import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq          #Benötigt man für FFT Befehler


def compute_fft(acc_timedata, force_timedata, fs):

    #fs = 12800              #Gewählte Abtastrate der Messung
    #N = len(data)           #Länge der Daten
    N = len(acc_timedata)           #Länge der Daten
    #tmeas = (1/fs)*N        #Messdauer


    U = fft(force_timedata) / N             
    Y = fft(acc_timedata) / N

    H = Y / U                               #Übertragungsfunktion

    freq = fftfreq(N, d=1/fs)               #Erstellung der Frequenzachse

    return freq, H