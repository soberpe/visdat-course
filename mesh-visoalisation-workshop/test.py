import pyvista as pv
import numpy as np

# Load mesh
mesh = pv.read("data/beam_stress.vtu")

# --- Explore structure ---

# Print mesh summary
print(mesh)
print("Fields: ", mesh.array_names)
print("Points: ", mesh.points)
print("Cells: ", mesh.cells)

# Spannungen
stress=mesh["S_Mises"]
print("Stress range: ", stress.min(), " to ", stress.max(),"MPa")

# Verschiebungen
displacements=mesh["U"]
print("Displacement range: ", displacements.min(), " to ", displacements.max(),"mm")
print("Displacement shape: ", displacements.shape)

# --- Visualisierung ---

pl=pv.Plotter(shape=(1,1), window_size=[1200,800])
pl.add_mesh(mesh,show_edges=False, scalars="S_Mises", cmap="coolwarm",clim=(0,100), opacity=1,scalar_bar_args={"title":"Von Mises Stress [MPa]"})
'pl.save_graphic("beam_stress.png")'
'pl.background_color="white"'
light = pv.Light(position=(10, 10, 10), focal_point=(0, 0, 0), color="white", intensity=0.5)
pl.add_light(light)
pl.camera_position = 'iso'
'pl.camera_position=[(1000, 1000, 1000), (0, 0, 0), (0, 0, 1)]'
## Mark max stress point
max_idx=np.argmax(stress)
print("Max stress at point:", mesh.points[max_idx], "with value:", stress[max_idx],"MPa")

high_stress=mesh.threshold(value=stress[max_idx]*0.7, scalars="S_Mises")
'pl.add_mesh(high_stress, color="red", opacity=1.0, render_points_as_spheres=True)'

## Slice through the mesh
slice = mesh.slice(normal='x', origin=(300, 0, 0))
pl.add_mesh(slice, scalars=slice["S_Mises"], cmap="coolwarm", opacity=0.3,clim=(0,100) )
clip_mesh = mesh.clip(normal='x', origin=(300, 0, 0))
pl.add_mesh(clip_mesh, scalars=clip_mesh["S_Mises"], cmap="coolwarm", opacity=0.3,clim=(0,100))

## Warped mesh by displacement
warped_mesh = mesh.warp_by_vector("U", factor=1000.0)
pl.add_mesh(warped_mesh, scalars=warped_mesh["S_Mises"], cmap="coolwarm", opacity=0.5,clim=(0,100))

## Add displacement vectors
arrows=mesh.glyph(orient="U", scale="U",tolerance=0.05,factor=50)
pl.add_mesh(arrows, color="black")


pl.show()





