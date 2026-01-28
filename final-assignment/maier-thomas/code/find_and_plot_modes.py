#File welches funktinen zum Finden und Plotten der Eigenmoden beinhaltet
#File soll als input in das Hauptprogramm verwendet werden

import numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.signal import find_peaks

# ======================================================
# Funktion zum Finden der Eigenfrequenzen
# ======================================================
def find_eigenfrequencies(
    frequency,
    tf,
    height_ratio=0.15,      #  Einstellparameter Peakhöhe für die Suche
    min_distance=1,         #Einstellparameter für die Suche
):
    
    peaks, props = find_peaks(
        np.abs(tf),                                 
        height=np.max(np.abs(tf)) * height_ratio,  #Definieren der Höhe der peaks welche berücksichtigt werden sollen 
        distance=min_distance,
    )

    return frequency[peaks], peaks


# ======================================================
# Funktion zum finden der Moden
# ======================================================
def build_mode(z_nodes, z_meas, u_meas):


    # Sortieren der Messwerte nach der z-Koordinate des Geometriefiles über die Zuordnungsmatrix bei chaotishcer Messreihenanordnung
    order = np.argsort(z_meas)
    z_meas = z_meas[order]
    u_meas = u_meas[order]

    # Doppelte Höhen entfernen
    z_meas, idx = np.unique(z_meas, return_index=True)
    u_meas = u_meas[idx]

    # Zu wenige Punkte → nichts darstellen
    if len(z_meas) < 2:
        return np.zeros_like(z_nodes)
    
    # Fundament festhalten
    if z_meas[0] > 0:
        z_meas = np.insert(z_meas, 0, 0.0)
        u_meas = np.insert(u_meas, 0, 0.0)

    interp = PchipInterpolator(z_meas, u_meas, extrapolate=True)    
    u_all = interp(z_nodes)

    # außerhalb Messbereich (nur Sicherheit)
    u_all[np.isnan(u_all)] = 0.0

    return u_all

# ======================================================
# Universielle funktion zum Plotten von moden (qualitativ)
# ======================================================
def plot_mode(
    ax,
    node_ids,
    nodes,          
    edges,
    plot_lines,     
    axis_a="x",
    axis_b="z",
    disp_axis="x",
    scale=0.4,          #Einstellparameter für die Ausprägung der Moden im Plot
):
    ax.clear()

    A = nodes[axis_a]
    B = nodes[axis_b]
    D = nodes[disp_axis]

    for e in edges:
        i1 = np.where(node_ids == e["n1"])[0][0]
        i2 = np.where(node_ids == e["n2"])[0][0]

        # Geometrie
        ax.plot(
            [A[i1], A[i2]],
            [B[i1], B[i2]],
            color="0.8",
            lw=0.8,
        )

        # Modeform(en)
        for color, u in plot_lines:
            ax.plot(
                [A[i1] + scale * u[i1],
                 A[i2] + scale * u[i2]],
                [B[i1], B[i2]],
                color,
                lw=1.4,
            )

    ax.set_aspect("equal")
    ax.set_xlabel(axis_a)
    ax.set_ylabel(axis_b)
    ax.grid(True)
