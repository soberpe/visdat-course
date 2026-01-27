import pyvista as pv
import numpy as np

mesh = pv.read("data/beam_stress.vtu")
print(mesh)
print("Fields: ", mesh.array_names)
print("Points: ", mesh.points, "\nCells: ",mesh.cells)

print("Mieses Spannung:", mesh["S_Mises"])

stress = mesh["S_Mises"]

print("Stress range:"  , stress.min(),"to", stress.max(), "MPa")

displacement = mesh["U"]
print("Displacement range:", displacement.min(),"to", displacement.max(), "mm")
print("Displacement shape:", displacement.shape)

pl=pv.Plotter(shape=(1,2), window_size=[1200,600])

pl.add_mesh(mesh, show_edges=True, scalars=stress, cmap="coolwarm", opacity=0.3,show_scalar_bar=True, scalar_bar_args={"title": "Mises Stress (MPa)"})
pl.background_color = "white"
pl.title = "Beam Stress Visualization"

max_idx = np.argmax(stress)
max_point = mesh.points[max_idx]
print("Maximum stress point:", max_point, "with stress:", stress[max_idx], "MPa")

high_stress = mesh.threshold(value=stress[max_idx] * 0.7, scalars="S_Mises")
pl.add_mesh(high_stress, color="red", opacity=0.5, label="High Stress Regions")

warped_mesh = mesh.warp_by_vector("U", factor=1000.0)
arrows = mesh.glyph(orient="U", scale="U", factor=500.0, geom=pv.Arrow())
pl.subplot(0,1)
pl.add_mesh(arrows, color="blue", label="Displacement Vectors")
pl.add_mesh(warped_mesh, scalars=stress, cmap="coolwarm", opacity=1,show_scalar_bar=False, label="Deformed Shape")

pl.show()
