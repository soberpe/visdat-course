import numpy as np
import matplotlib.pyplot as plt    
import pyvista as pv                 
#import time
from pyvistaqt import BackgroundPlotter
from PyQt6 import QtWidgets


# Physikalische Konstanten und Berechnungskonstanten


g = 9.81            # Erdbeschleunigung [m/s^2]
rho = 1.225         # Luftdichte [kg/m^3]
m_ball = 0.043       # Masse des Balls [kg]
A = 0.00143           # Querschnittsfläche [m^2]
c_D = 0.25          # Widerstandsbeiwert
c_L = 0.20          # Auftriebsbeiwert (Spin / Magnus)

dt = 0.01           # Zeitschritt [s]

# Luftwiderstands-Konstante:
# k = rho * A * c_D / (2 * m)
k = rho * A * c_D / (2.0 * m_ball)


# Anfangsbedingungen


v0 = 45.0                           # Anfangsgeschwindigkeit [m/s]
alpha = np.deg2rad(16.0)            # Abflugwinkel [rad]

# Anfangsgeschwindigkeit (3D)
v_x = v0 * np.cos(alpha)
v_y = v0 * np.sin(alpha)
v_z = 0.0                           # Kein seitlicher Startimpuls

# Anfangsposition
x = 0.0
y = 0.0
z = 0.0

# Zeit
t = 0.0


# Seitenwind in z-Richtung (ABweichung in z-Richtung)


v_wind_z = 3.0      # Konstanter Seitenwind [m/s]


# Speicherung der Flugbahn


x_hist = [x]
y_hist = [y]
z_hist = [z]
t_hist = [t]

# Zeitintegration


while y >= 0.0:

    
    # Relative Geschwindigkeit zur Luft
    

    v_rel_x = v_x
    v_rel_y = v_y
    v_rel_z = v_z - v_wind_z

    # Betrag der Relativgeschwindigkeit
    v_rel = np.sqrt(
        v_rel_x**2 +
        v_rel_y**2 +
        v_rel_z**2
    )

   


    
    # Berechnung der Beschleunigungen
    

    # Betrag der Geschwindigkeit
    v_n = np.sqrt(v_x**2 + v_y**2)

    # Beschleunigung in x-Richtung
    a_x = -k * v_n * (v_x * c_D + v_y * c_L)

    # Beschleunigung in y-Richtung
    a_y = -k * v_n * (v_y * c_D - v_x * c_L) - g


    # Beschleunigung in z-Richtung
    a_z = -k * v_rel * v_rel_z

    
    # Geschwindigkeitsupdate (explizites Euler-Verfahren)
    

    v_x += a_x * dt
    v_y += a_y * dt
    v_z += a_z * dt

    
    # Ortsupdate
    

    
    x += 1.25*(v_x * dt + 0.5 * a_x * dt**2)
    y += 2*(v_y * dt + 0.5 * a_y * dt**2)
    z += v_z * dt + 0.5 * a_z * dt**2




    
    # Abbruchbedingung: exakter Bodenkontakt y = 0
    

    if y < 0.0:
        # Lineare Interpolation zwischen letztem gültigen Punkt
        # (y_old > 0) und aktuellem Punkt (y < 0)
        y_old = y_hist[-1]
        x_old = x_hist[-1]
        z_old = z_hist[-1]

        # Interpolationsfaktor (0 < lambda < 1)
        lam = y_old / (y_old - y)

        # Exakt interpolierter Aufschlagpunkt
        x = x_old + lam * (x - x_old)
        y = 0.0
        z = z_old + lam * (z - z_old)

        # Speichern des physikalisch korrekten Endpunkts
        x_hist.append(x)
        y_hist.append(y)
        z_hist.append(z)

        break


    # Zeitupdate & Speicherung


    t += dt

    x_hist.append(x)
    y_hist.append(y)
    z_hist.append(z)
    t_hist.append(t)


# Umwandlung in NumPy-Arrays

x_hist = np.array(x_hist)
y_hist = np.array(y_hist)
z_hist = np.array(z_hist)



# 6.1 Berechnungen : 
# Aufschlagpunkt (letzter Punkt der Flugbahn)


x_impact = x_hist[-1]
y_impact = y_hist[-1]   # = 0
z_impact = z_hist[-1]


#Berechnungen der maximalen Flughöhe und ABweichung seitlich (z-Richtung)

# Maximale Flughöhe
y_max = max(y_hist)

# Seitliche Abweichung beim Aufschlag (z-Richtung)
z_drift_impact = z_impact



# Numerische Auswertung


print("===== Aufschlagdaten =====")
print(f"Wurfweite x       : {x_impact:.2f} m")
print(f"Seitliche Drift z : {z_impact:.2f} m")
print(f"Gesamte Flugzeit  : {len(x_hist) * dt:.2f} s")
print(f"Maximale Flughöhe : {y_max:.2f} m")
print(f"Seitliche Drift am Aufschlag : {z_drift_impact:.2f} m")



# 3D Visualisierung


points = np.column_stack((x_hist, y_hist, z_hist))
trajectory = pv.lines_from_points(points)

plotter = pv.Plotter()
plotter.add_mesh(
    trajectory,
    color="blue",
    line_width=3,
    label="3D-Flugbahn mit Seitenwind"
)

# Aufschlagpunkt als Kugel (3D)
impact_point = pv.Sphere(
    radius=0.3,
    center=(x_impact, y_impact, z_impact)
)

plotter.add_mesh(
    impact_point,
    color="Red",
    label="Aufschlagpunkt"
)

# Bodenfläche (grün)


x_min = 0.0
x_max = 1.1 * np.max(x_hist)

z_min = -1.25 * abs(z_impact)
z_max =  1.25 * abs(z_impact)


# Ausdehnungen der Flugbahn
x_extent = 1.1 * np.max(x_hist)
z_extent = 1.3 * z_impact


ground = pv.Plane(
    center=((x_min + x_max) / 2.0, 0.0, (z_min + z_max) / 2.0),
    direction=(0.0, 1.0, 0.0),   # Normale nach oben → Plane liegt in x–z
    i_size=(z_max - z_min),      
    j_size=(x_max - x_min) 
)

plotter.add_mesh(
    ground,
    color="forestgreen",
    opacity=0.8
)



# Bodenraster (5 m Abstand in x–z-Ebene)


grid_spacing = 5.0

x_lines = np.arange(x_min, x_max + 1e-6, grid_spacing)
z_lines = np.arange(z_min, z_max + 1e-6, grid_spacing)


grid_actors_5m = []



# Linien parallel zur z-Achse (konstantes x)
for xg in x_lines:
    line = pv.Line(
        pointa=(xg, 0.0, z_min),
        pointb=(xg, 0.0, z_max)
    )
    actor = plotter.add_mesh(line, color="black", line_width=2)
    grid_actors_5m.append(actor)


# Linien parallel zur x-Achse (konstantes z)
for zg in z_lines:
    line = pv.Line(
        pointa=(x_min, 0.0, zg),
        pointb=(x_max, 0.0, zg)
    )
    actor = plotter.add_mesh(line, color="black", line_width=2)
    grid_actors_5m.append(actor)



# Liste für Raster-Actors (für spätere GUI-Steuerung)

actor = plotter.add_mesh(line, color="darkgray", line_width=2)
grid_actors_5m.append(actor)


# Hauptraster (alle 25 m, stärker hervorgehoben)


main_grid_spacing = 25.0

x_main = np.arange(x_min, x_max + 1e-6, main_grid_spacing)
z_main = np.arange(z_min, z_max + 1e-6, main_grid_spacing)

grid_actors_25m = []

# Linien parallel zur z-Achse (Hauptraster)
for xg in x_lines:
    line = pv.Line(
        pointa=(xg, 0.0, z_min),
        pointb=(xg, 0.0, z_max)
    )
    actor = plotter.add_mesh(line, color="black", line_width=4)
    grid_actors_25m.append(actor)


# Linien parallel zur x-Achse (Hauptraster)
for zg in z_lines:
    line = pv.Line(
        pointa=(x_min, 0.0, zg),
        pointb=(x_max, 0.0, zg)
    )
    actor = plotter.add_mesh(line, color="black", line_width=4)
    grid_actors_25m.append(actor)




# Beschriftung des Hauptrasters (25 m)


labels = []
label_points = []

# x-Beschriftung entlang der x-Achse
for xg in x_main:
    labels.append(f"{int(xg)} m")
    label_points.append((xg, 0.01, 0.0))  # minimal über Boden

plotter.add_point_labels(
    label_points,
    labels,
    font_size=12,
    text_color="black",
    always_visible=True
)



# Koordinatenachsen im Ursprung 


# Maximale Ausdehnungen der Flugbahn
x_max = np.max(x_hist)
y_max = np.max(y_hist)
z_max = np.max(np.abs(z_hist))

axis_scale = 1.1  # kleiner Sicherheitsfaktor

# x-Achse
x_axis = pv.Line(
    pointa=(0.0, 0.0, 0.0),
    pointb=(axis_scale * x_max, 0.0, 0.0)
)

# y-Achse
y_axis = pv.Line(
    pointa=(0.0, 0.0, 0.0),
    pointb=(0.0, axis_scale * y_max, 0.0)
)

# z-Achse
z_axis = pv.Line(
    pointa=(0.0, 0.0, 0.0),
    pointb=(0.0, 0.0, axis_scale * z_max)
)

# Achsen zur Szene hinzufügen
plotter.add_mesh(x_axis, color="red", line_width=3)
plotter.add_mesh(y_axis, color="green", line_width=3)
plotter.add_mesh(z_axis, color="blue", line_width=3)


# Achsenbeschriftung


plotter.add_point_labels(
    [
        (axis_scale * x_max, 0.0, 0.0),
        (0.0, axis_scale * y_max, 0.0),
        (0.0, 0.0, axis_scale * z_max)
    ],
    ["x", "y", "z"],
    font_size=20,
    text_color="black"
)



plotter.show_axes()
plotter.add_title("3D-Flugbahn")

# Parallelprojektion für technisch saubere Ansicht
plotter.enable_parallel_projection()

plotter.show()




# Zeitverläufe der Koordinaten


t_hist = np.arange(len(x_hist)) * dt

plt.figure(figsize=(10, 6))

plt.plot(t_hist, x_hist, label="x(t)")
plt.plot(t_hist, y_hist, label="y(t)")
plt.plot(t_hist, z_hist, label="z(t)")

plt.xlabel("Zeit [s]")
plt.ylabel("Position [m]")
plt.title("Zeitverlauf der Koordinaten")
plt.legend()
plt.grid(True)
plt.show()




# 2D-Diagnoseplots mit matplotlib


plt.figure(figsize=(12, 4))


# Flugbahn: x–y (Höhe über Weite)

plt.subplot(1, 2, 1)
plt.plot(x_hist, y_hist, label="Flugbahn")
plt.scatter(x_impact, y_impact, color='red', s=50, zorder=5, label="Aufschlagpunkt")  # rot + etwas größer
plt.xlabel("x [m]")
plt.ylabel("y [m]")
plt.title("Flugbahn (x–y)")
plt.grid(True)
plt.legend()



# Bodenprojektion: x–z (seitliche Drift)

plt.subplot(1, 2, 2)
plt.plot(x_hist, z_hist, label="Bodenprojektion")
plt.scatter(x_impact, z_impact, color='red', s=50, zorder=5, label="Aufschlagpunkt")
plt.xlabel("x [m]")
plt.ylabel("z [m]")
plt.title("Bodenprojektion (x–z)")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()































# # ============================================================
# # 12. Reine PyVista-Animation der Flugbahn (ohne Qt)
# # ============================================================

# print("Starte PyVista-Animation (ohne Qt)...")

# # Neuer Plotter nur für die Animation
# anim_plotter = pv.Plotter()

# # Boden
# anim_plotter.add_mesh(ground, color="forestgreen", opacity=0.8)

# # Achsen
# anim_plotter.add_mesh(x_axis, color="red", line_width=3)
# anim_plotter.add_mesh(y_axis, color="green", line_width=3)
# anim_plotter.add_mesh(z_axis, color="blue", line_width=3)

# anim_plotter.show_axes()
# anim_plotter.enable_parallel_projection()

# # Fenster sofort öffnen (wichtig!)
# anim_plotter.show(auto_close=False, interactive_update=True)


# # ============================================================
# # Kameraeinstellung für sichtbare Flugbahn (ADD-ONLY)
# # ============================================================

# anim_plotter.camera_position = [
#     (0.5 * x_max, 0.6 * x_max, 1.2 * x_max),  # Kamera-Position
#     (0.5 * x_max, 0.0, 0.0),                  # Blickpunkt
#     (0.0, 1.0, 0.0)                           # Up-Vektor
# ]

# anim_plotter.update()


# # ------------------------------------
# # Animierte Flugbahn
# # ------------------------------------
# trajectory_actor = None
# animation_delay = 0.04  # Sekunden (größer = langsamer)

# for i in range(2, len(x_hist)):
#     partial_points = np.column_stack((
#         x_hist[:i],
#         y_hist[:i],
#         z_hist[:i]
#     ))

#     partial_line = pv.lines_from_points(partial_points)

#     if trajectory_actor is not None:
#         anim_plotter.remove_actor(trajectory_actor)

#     trajectory_actor = anim_plotter.add_mesh(
#         partial_line,
#         color="blue",
#         line_width=3
#     )

#     anim_plotter.render()
#     time.sleep(animation_delay)

# # ------------------------------------
# # Aufschlagpunkt am Ende
# # ------------------------------------
# impact_sphere = pv.Sphere(
#     radius=0.3,
#     center=(x_impact, y_impact, z_impact)
# )

# anim_plotter.add_mesh(impact_sphere, color="red")
# anim_plotter.render()

# print("Animation abgeschlossen.")
