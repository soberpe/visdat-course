import pandas as pd
import matplotlib.pyplot as plt

# ===== DATEIPFADE =====
measfile_x = r"C:\Users\david\OneDrive - FH OOe (1)\3.Semester\VIS\visdat-course\final-assignment\Wintersteiger\code\data\Messung Gestell Anregung Y1\Imaginaerteil_uber_Freq_Uebertragungsfunktion_x.lvm"
measfile_y = r"C:\Users\david\OneDrive - FH OOe (1)\3.Semester\VIS\visdat-course\final-assignment\Wintersteiger\code\data\Messung Gestell Anregung Y1\Imaginaerteil_uber_Freq_Uebertragungsfunktion_y.lvm"

# ===== FREQUENZBEREICH (HIER EINSTELLEN!) =====
f_min = 0.0      # untere Grenze [Hz]
f_max = 200.0   # obere Grenze [Hz]

# ===== EINLESEN (TAB + Dezimalkomma + 1 Headerzeile) =====
df_x = pd.read_csv(measfile_x, sep="\t", skiprows=1, header=None, decimal=",", engine="python")
df_y = pd.read_csv(measfile_y, sep="\t", skiprows=1, header=None, decimal=",", engine="python")

# ===== SPALTEN =====
df_x.columns = ["freq", "imag"]
df_y.columns = ["freq", "imag"]

# ===== FREQUENZBEREICH FILTERN =====
df_x = df_x[(df_x["freq"] >= f_min) & (df_x["freq"] <= f_max)]
df_y = df_y[(df_y["freq"] >= f_min) & (df_y["freq"] <= f_max)]

# ===== PLOT =====
plt.figure(figsize=(8, 5))
plt.plot(df_x["freq"], df_x["imag"], label="X-Richtung")
plt.plot(df_y["freq"], df_y["imag"], label="Y-Richtung")

plt.xlabel("Frequenz [Hz]")
plt.ylabel("Imaginärteil")
plt.title(f"Imaginärteil über Frequenz ({f_min}–{f_max} Hz)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()