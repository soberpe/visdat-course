import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv
from pyvistaqt import BackgroundPlotter
from PyQt6 import QtWidgets


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


# Korrigierte Flugbahn

def simulate_corrected_trajectory(v0, alpha_deg, z_wind, target_carry, target_side, max_iter=10, tol=0.1):
    dv = 0.0
    dz = 0.0
    for _ in range(max_iter):
        x_hist, y_hist, z_hist = simulate_trajectory(v0 + dv, alpha_deg, z_wind + dz)
        carry_end = x_hist[-1]
        side_end = z_hist[-1]

        err_carry = target_carry - carry_end
        err_side = target_side - side_end

        if abs(err_carry) < tol and abs(err_side) < tol:
            break

        dv += 0.1 * err_carry
        dz += 0.1 * err_side

    return simulate_trajectory(v0 + dv, alpha_deg, z_wind + dz), dv, dz


# CSV einlesen

df = pd.read_csv('final-assignment/Zierler/Code/data/Schlagdaten.csv', sep=';')
for col in ["Carry (m)", "Side (m)", "Ball Speed (m/s)", "start Ang. (Deg)", "max. Hight (m)"]:
    df[col] = df[col].str.replace(',', '.').astype(float)


# Club-Auswahl

class TrajectoryApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Schlaegerauswahl für Flugbahnrekonstruktion")
        self.setGeometry(100, 100, 400, 120)
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        # Dropdown für Clubs
        self.club_selector = QtWidgets.QComboBox()
        self.club_selector.addItems(sorted(df["Club"].unique()))
        layout.addWidget(self.club_selector)

        # Button
        self.run_button = QtWidgets.QPushButton("Flugbahnen rekonstruieren")
        layout.addWidget(self.run_button)
        self.run_button.clicked.connect(self.run_simulation)

    def run_simulation(self):
        club_name = self.club_selector.currentText()
        df_club = df[df["Club"] == club_name]

        trajectories = []
        labels = []
        colors = ["blue", "orange", "purple", "cyan", "magenta", "yellow", "brown", "pink", "gray", "green", "red"]

        
        # 2D Plot
        
        plt.figure(figsize=(10,5))
        for i, row in df_club.iterrows():
            v0 = row["Ball Speed (m/s)"]
            alpha_deg = row["start Ang. (Deg)"]
            target_carry = row["Carry (m)"]
            target_side = row["Side (m)"]

            (x_hist, y_hist, z_hist), dv, dz = simulate_corrected_trajectory(
                v0, alpha_deg, 0.0, target_carry, target_side
            )

            trajectories.append((x_hist, y_hist, z_hist))
            labels.append(f"Shot {i+1}: Carry {target_carry:.1f}, Side {target_side:.1f}")
            plt.plot(x_hist, y_hist, label=labels[-1])

        plt.xlabel("x [m] (Carry)")
        plt.ylabel("y [m] (Höhe)")
        plt.title(f"Rekonstruierte Flugbahnen für {club_name} [m]")
        plt.grid(True)
        plt.legend()
        plt.show()

       
        # 3D Visualisierung
        
        plotter = BackgroundPlotter()
        mesh_objects = []

        for (x_hist, y_hist, z_hist), label, color in zip(trajectories, labels, colors*10):
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

        # Boden
        ground = pv.Plane(center=((x_min_all + x_max_all)/2,0,(z_min_all+z_max_all)/2),
                          direction=(0,1,0),
                          i_size=(z_max_all - z_min_all),
                          j_size=(x_max_all - x_min_all))
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

        # Rasterbeschriftung
        labels_raster = []
        label_points = []
        for xg in x_main:
            labels_raster.append(f"{int(xg)} m")
            label_points.append((xg,0.1,0))
        for zg in z_main:
            labels_raster.append(f"{int(zg)} m")
            label_points.append((0,0.1,zg))
        plotter.add_point_labels(label_points, labels_raster, font_size=12, text_color="black", always_visible=True)

       
        # Achsenlinien + Beschriftung
       
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

        
        # Checkboxen für jede Flugbahn
       
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
            plotter.add_text(label, position=(40, 30 + 30*i), font_size=12, color="black")

        # Titel + parallele Projektion
        plotter.add_text(f"3D-Rekonstruktion aller Flugbahnen für {club_name}", font_size=20)
        plotter.enable_parallel_projection()
        plotter.app.exec_()


app = QtWidgets.QApplication(sys.argv)
window = TrajectoryApp()
window.show()
sys.exit(app.exec())
