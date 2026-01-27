import numpy as np
import pyvista as pv
import matplotlib.pyplot as plt
from pyvistaqt import BackgroundPlotter
# #für 3 Flugbahnen!!!!!


# # Physikalische Konstanten

# g = 9.81
# rho = 1.225
# m_ball = 0.043
# A = 0.00143
# c_D = 0.25
# c_L = 0.20
# dt = 0.01
# k = rho * A * c_D / (2.0 * m_ball)


# #Flugbahnsimulation

# def simulate_trajectory(v0, alpha_deg, v_wind_z):
#     alpha = np.deg2rad(alpha_deg)
#     v_x = v0 * np.cos(alpha)
#     v_y = v0 * np.sin(alpha)
#     v_z = 0.0
#     x, y, z = 0.0, 0.0, 0.0
#     x_hist, y_hist, z_hist = [x], [y], [z]

#     while y >= 0.0:
#         v_rel_x = v_x
#         v_rel_y = v_y
#         v_rel_z = v_z - v_wind_z
#         v_rel = np.sqrt(v_rel_x**2 + v_rel_y**2 + v_rel_z**2)

#         v_n = np.sqrt(v_x**2 + v_y**2)
#         a_x = -k * v_n * (v_x * c_D + v_y * c_L)
#         a_y = -k * v_n * (v_y * c_D - v_x * c_L) - g
#         a_z = -k * v_rel * v_rel_z

#         v_x += a_x * dt
#         v_y += a_y * dt
#         v_z += a_z * dt

#         x += 1.25*(v_x * dt + 0.5 * a_x * dt**2)
#         y += 2*(v_y * dt + 0.5 * a_y * dt**2)
#         z += v_z * dt + 0.5 * a_z * dt**2

#         if y < 0:
#             y_old, x_old, z_old = y_hist[-1], x_hist[-1], z_hist[-1]
#             lam = y_old / (y_old - y)
#             x = x_old + lam * (x - x_old)
#             y = 0.0
#             z = z_old + lam * (z - z_old)
#             x_hist.append(x); y_hist.append(y); z_hist.append(z)
#             break

#         x_hist.append(x)
#         y_hist.append(y)
#         z_hist.append(z)

#     return np.array(x_hist), np.array(y_hist), np.array(z_hist)


# # Flugbahnen

# trajectories = [
#     simulate_trajectory(45.0, 16.0, 3.0),
#     simulate_trajectory(50.0, 20.0, -2.0),
#     simulate_trajectory(40.0, 10.0, 5.0)
# ]

# colors = ["blue", "orange", "purple"]
# labels = ["Flugbahn 1", "Flugbahn 2", "Flugbahn 3"]



# # Berechnungen für alle Flugbahnen

# for i, (x_hist, y_hist, z_hist) in enumerate(trajectories, start=1):
#     x_impact = x_hist[-1]
#     y_impact = y_hist[-1]   # sollte 0 sein
#     z_impact = z_hist[-1]

#     y_max_traj = np.max(y_hist)
#     z_drift_impact = z_impact
#     flugzeit = len(x_hist) * dt

#     print(f"===== Flugbahn {i} Aufschlagdaten =====")
#     print(f"Wurfweite x       : {x_impact:.2f} m")
#     print(f"Seitliche Drift z : {z_impact:.2f} m")
#     print(f"Gesamte Flugzeit  : {flugzeit:.2f} s")
#     print(f"Maximale Flughöhe : {y_max_traj:.2f} m")
#     print(f"Seitliche Drift am Aufschlag : {z_drift_impact:.2f} m\n")





# # Visualisierung

# plotter = pv.Plotter()

# # Flugbahnen + Aufschlagpunkte
# for (x_hist, y_hist, z_hist), color, label in zip(trajectories, colors, labels):
#     points = np.column_stack((x_hist, y_hist, z_hist))
#     traj = pv.lines_from_points(points)
#     plotter.add_mesh(traj, color=color, line_width=3, label=label)
#     impact = pv.Sphere(radius=0.3, center=(x_hist[-1], y_hist[-1], z_hist[-1]))
#     plotter.add_mesh(impact, color=color)


# # Raster/Boden

# x_max = max([np.max(t[0]) for t in trajectories]) * 1.1
# x_min = 0.0
# z_max = max([np.max(np.abs(t[2])) for t in trajectories]) * 1.3
# z_min = -z_max
# y_max = max([np.max(t[1]) for t in trajectories]) * 1.1

# # Boden
# ground = pv.Plane(
#     center=((x_min + x_max)/2, 0.0, (z_min + z_max)/2),
#     direction=(0,1,0),
#     i_size=(z_max - z_min),
#     j_size=(x_max - x_min)
# )
# plotter.add_mesh(ground, color="forestgreen", opacity=0.7)

# # Raster alle 5 m (dünn)
# grid_spacing = 5.0
# x_lines = np.arange(x_min, x_max + 1e-6, grid_spacing)
# z_lines = np.arange(z_min, z_max + 1e-6, grid_spacing)
# for xg in x_lines:
#     plotter.add_mesh(pv.Line(pointa=(xg,0,z_min), pointb=(xg,0,z_max)), color="black", line_width=1)
# for zg in z_lines:
#     plotter.add_mesh(pv.Line(pointa=(x_min,0,zg), pointb=(x_max,0,zg)), color="black", line_width=1)

# # Hauptraster alle 25 m (dick)
# main_grid_spacing = 25.0
# x_main = np.arange(x_min, x_max + 1e-6, main_grid_spacing)
# z_main = np.arange(z_min, z_max + 1e-6, main_grid_spacing)
# for xg in x_main:
#     plotter.add_mesh(pv.Line(pointa=(xg,0,z_min), pointb=(xg,0,z_max)), color="black", line_width=3)
# for zg in z_main:
#     plotter.add_mesh(pv.Line(pointa=(x_min,0,zg), pointb=(x_max,0,zg)), color="black", line_width=3)

# # ---- Dicke Begrenzungslinien an den Enden ----
# plotter.add_mesh(pv.Line(pointa=(x_min,0,z_max), pointb=(x_max,0,z_max)), color="black", line_width=6)
# plotter.add_mesh(pv.Line(pointa=(x_min,0,z_min), pointb=(x_max,0,z_min)), color="black", line_width=6)
# plotter.add_mesh(pv.Line(pointa=(x_min,0,z_min), pointb=(x_min,0,z_max)), color="black", line_width=6)
# plotter.add_mesh(pv.Line(pointa=(x_max,0,z_min), pointb=(x_max,0,z_max)), color="black", line_width=6)

# # Hauptraster-Beschriftung (x- und z-Achse)
# labels = []
# label_points = []
# for xg in x_main:
#     labels.append(f"{int(xg)} m")
#     label_points.append((xg, 0.1, 0.0))
# for zg in z_main:
#     labels.append(f"{int(zg)} m")
#     label_points.append((0.0, 0.1, zg))
# plotter.add_point_labels(label_points, labels, font_size=12, text_color="black", always_visible=True)


# # Achsen

# axis_scale = 1.1
# x_axis = pv.Line(pointa=(0,0,0), pointb=(axis_scale*x_max,0,0))
# y_axis = pv.Line(pointa=(0,0,0), pointb=(0,axis_scale*y_max,0))
# z_axis = pv.Line(pointa=(0,0,0), pointb=(0,0,axis_scale*z_max))
# plotter.add_mesh(x_axis, color="red", line_width=3)
# plotter.add_mesh(y_axis, color="green", line_width=3)
# plotter.add_mesh(z_axis, color="blue", line_width=3)
# plotter.add_point_labels(
#     [(axis_scale*x_max,0,0), (0,axis_scale*y_max,0), (0,0,axis_scale*z_max)],
#     ["x","y","z"], font_size=20, text_color="black"
# )


# plotter.show_axes()
# plotter.add_title("3D-Flugbahnen mit Raster, Beschriftung und dicken Begrenzungslinien")
# plotter.enable_parallel_projection()
# plotter.show()


#################################################################################################

# für alle 8 Flugbahnen


# Physikalische Konstanten

g = 9.81
rho = 1.225
m_ball = 0.043
A = 0.00143
c_D = 0.25
c_L = 0.20
dt = 0.01
k = rho * A * c_D / (2.0 * m_ball)


# Flugbahnsimulation

def simulate_trajectory(v0, alpha_deg, v_wind_z):
    alpha = np.deg2rad(alpha_deg)
    v_x = v0 * np.cos(alpha)
    v_y = v0 * np.sin(alpha)
    v_z = 0.0
    x, y, z = 0.0, 0.0, 0.0
    x_hist, y_hist, z_hist = [x], [y], [z]

    while y >= 0.0:
        v_rel_x = v_x
        v_rel_y = v_y
        v_rel_z = v_z - v_wind_z
        v_rel = np.sqrt(v_rel_x**2 + v_rel_y**2 + v_rel_z**2)

        v_n = np.sqrt(v_x**2 + v_y**2)
        a_x = -k * v_n * (v_x * c_D + v_y * c_L)
        a_y = -k * v_n * (v_y * c_D - v_x * c_L) - g
        a_z = -k * v_rel * v_rel_z

        v_x += a_x * dt
        v_y += a_y * dt
        v_z += a_z * dt

        x += 1.25*(v_x * dt + 0.5 * a_x * dt**2)
        y += 2*(v_y * dt + 0.5 * a_y * dt**2)
        z += v_z * dt + 0.5 * a_z * dt**2

        if y < 0:
            y_old, x_old, z_old = y_hist[-1], x_hist[-1], z_hist[-1]
            lam = y_old / (y_old - y)
            x = x_old + lam * (x - x_old)
            y = 0.0
            z = z_old + lam * (z - z_old)
            x_hist.append(x); y_hist.append(y); z_hist.append(z)
            break

        x_hist.append(x)
        y_hist.append(y)
        z_hist.append(z)

    return np.array(x_hist), np.array(y_hist), np.array(z_hist)


# Acht Flugbahnen

start_conditions = [
    (45.0, 16.0, 3.0),
    (50.0, 20.0, -2.0),
    (40.0, 10.0, 5.0),
    (48.0, 18.0, 0.0),
    (42.0, 15.0, -3.0),
    (46.0, 12.0, 2.0),
    (43.0, 14.0, 1.0),
    (49.0, 17.0, -1.0)
]

colors = ["blue", "orange", "purple", "cyan", "magenta", "yellow", "brown", "pink"]
labels = [f"Flugbahn {i}" for i in range(1, 9)]
trajectories = [simulate_trajectory(v0, alpha, wind) for (v0, alpha, wind) in start_conditions]


# Numerische Auswertung

for i, (x_hist, y_hist, z_hist) in enumerate(trajectories, start=1):
    x_impact = x_hist[-1]
    y_impact = y_hist[-1]
    z_impact = z_hist[-1]
    y_max_traj = np.max(y_hist)
    z_drift_impact = z_impact
    flugzeit = len(x_hist) * dt

    print(f"===== Flugbahn {i} Aufschlagdaten =====")
    print(f"Wurfweite x       : {x_impact:.2f} m")
    print(f"Seitliche Drift z : {z_impact:.2f} m")
    print(f"Gesamte Flugzeit  : {flugzeit:.2f} s")
    print(f"Maximale Flughöhe : {y_max_traj:.2f} m")
    print(f"Seitliche Drift am Aufschlag : {z_drift_impact:.2f} m\n")


# 2D Höhenplots mit Matplotlib

plt.figure(figsize=(10,5))
for i, (x_hist, y_hist, _) in enumerate(trajectories, start=1):
    plt.plot(x_hist, y_hist, label=f"Flugbahn {i}")
plt.xlabel("x [m]")
plt.ylabel("y [m]")
plt.title("Höhenkurven aller Flugbahnen")
plt.legend()
plt.grid(True)
plt.show()


# 3D-Visualisierung

plotter = BackgroundPlotter()
plotter.set_background("white")

# Flugbahn-Meshes speichern, um sichtbar/unsichtbar zu machen
mesh_objects = []

for (x_hist, y_hist, z_hist), color, label in zip(trajectories, colors, labels):
    points = np.column_stack((x_hist, y_hist, z_hist))
    traj_mesh = pv.lines_from_points(points)
    traj_actor = plotter.add_mesh(traj_mesh, color=color, line_width=3, label=label)
    impact_actor = plotter.add_mesh(pv.Sphere(radius=0.3, center=(x_hist[-1], y_hist[-1], z_hist[-1])), color=color)
    mesh_objects.append((traj_actor, impact_actor))


# Boden + Raster + Begrenzungslinien

x_max_all = max([np.max(t[0]) for t in trajectories]) * 1.1
x_min_all = 0.0
z_max_all = max([np.max(np.abs(t[2])) for t in trajectories]) * 1.3
z_min_all = -z_max_all
y_max_all = max([np.max(t[1]) for t in trajectories]) * 1.1

ground = pv.Plane(
    center=((x_min_all + x_max_all)/2, 0.0, (z_min_all + z_max_all)/2),
    direction=(0,1,0),
    i_size=(z_max_all - z_min_all),
    j_size=(x_max_all - x_min_all)
)
plotter.add_mesh(ground, color="forestgreen", opacity=0.7)

# Dünnes Raster 5 m
grid_spacing = 5.0
x_lines = np.arange(x_min_all, x_max_all + 1e-6, grid_spacing)
z_lines = np.arange(z_min_all, z_max_all + 1e-6, grid_spacing)
for xg in x_lines:
    plotter.add_mesh(pv.Line(pointa=(xg,0,z_min_all), pointb=(xg,0,z_max_all)), color="black", line_width=1)
for zg in z_lines:
    plotter.add_mesh(pv.Line(pointa=(x_min_all,0,zg), pointb=(x_max_all,0,zg)), color="black", line_width=1)

# Hauptraster 25 m
main_grid_spacing = 25.0
x_main = np.arange(x_min_all, x_max_all + 1e-6, main_grid_spacing)
z_main = np.arange(z_min_all, z_max_all + 1e-6, main_grid_spacing)
for xg in x_main:
    plotter.add_mesh(pv.Line(pointa=(xg,0,z_min_all), pointb=(xg,0,z_max_all)), color="black", line_width=3)
for zg in z_main:
    plotter.add_mesh(pv.Line(pointa=(x_min_all,0,zg), pointb=(x_max_all,0,zg)), color="black", line_width=3)

# Dicke Begrenzungslinien
plotter.add_mesh(pv.Line(pointa=(x_min_all,0,z_max_all), pointb=(x_max_all,0,z_max_all)), color="black", line_width=6)
plotter.add_mesh(pv.Line(pointa=(x_min_all,0,z_min_all), pointb=(x_max_all,0,z_min_all)), color="black", line_width=6)
plotter.add_mesh(pv.Line(pointa=(x_min_all,0,z_min_all), pointb=(x_min_all,0,z_max_all)), color="black", line_width=6)
plotter.add_mesh(pv.Line(pointa=(x_max_all,0,z_min_all), pointb=(x_max_all,0,z_max_all)), color="black", line_width=6)

# Raster-Beschriftung
labels_raster = []
label_points = []
for xg in x_main:
    labels_raster.append(f"{int(xg)} m")
    label_points.append((xg, 0.1, 0.0))
for zg in z_main:
    labels_raster.append(f"{int(zg)} m")
    label_points.append((0.0, 0.1, zg))
plotter.add_point_labels(label_points, labels_raster, font_size=12, text_color="black", always_visible=True)

# Achsen
axis_scale = 1.1
x_axis = pv.Line(pointa=(0,0,0), pointb=(axis_scale*x_max_all,0,0))
y_axis = pv.Line(pointa=(0,0,0), pointb=(0,axis_scale*y_max_all,0))
z_axis = pv.Line(pointa=(0,0,0), pointb=(0,0,axis_scale*z_max_all))
plotter.add_mesh(x_axis, color="red", line_width=3)
plotter.add_mesh(y_axis, color="green", line_width=3)
plotter.add_mesh(z_axis, color="blue", line_width=3)
plotter.add_point_labels(
    [(axis_scale*x_max_all,0,0), (0,axis_scale*y_max_all,0), (0,0,axis_scale*z_max_all)],
    ["x","y","z"], font_size=20, text_color="black"
)

# Titel
plotter.add_text("3D-Flugbahnen (8 Bahnen)",
                 font_size=20, color="black", position='upper_edge')


# Checkboxen für jede Flugbahn mit Label

def toggle_visibility(checked, index):
    traj_actor, impact_actor = mesh_objects[index]
    traj_actor.SetVisibility(checked)
    impact_actor.SetVisibility(checked)

for i, label in enumerate(labels):
    plotter.add_checkbox_button_widget(
        callback=lambda checked, i=i: toggle_visibility(checked, i),
        value=True,
        position=(10, 30 + 30*i),
        size=20,
        color_on="green",
        color_off="red"
    )
    # Text neben Checkbox
    plotter.add_text(
        label,
        position=(40, 30 + 30*i),
        font_size=12,
        color="black"
    )

plotter.enable_parallel_projection()
plotter.app.exec_()
