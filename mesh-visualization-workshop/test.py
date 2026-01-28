import pyvista as pv
import numpy as np

mesh = pv.read("data/beam_stress.vtu")
print(mesh)
print("Fields: ", mesh.array_names)
print("Points: ", mesh.points, "\nCells: ",mesh.cells)

stress = mesh["S_Mises"]
displacement = mesh["U"]

pl = pv.Plotter(shape=(1, 2), window_size=[800, 600])
pl.subplot(1, 1)
pl.add_mesh(mesh, show_edges=True, 
            scalars=stress, 
            cmap="coolwarm", 
            opacity=0.3,
            scalar_bar_args={"title": "Von Mises Stress"})

light = pv.Light(position=(1, 1, 1), focal_point=(0, 0, 0), color='white', intensity=0.8)
pl.add_light(light)

max_idx = np.argmax(stress)
print("Maximum stress at point:", mesh.points[max_idx], "with value:", stress[max_idx])

# high_stress = mesh.threshold(value = stress[max_idx]*0.5, scalars="S_Mises")
# pl.add_mesh(high_stress, color='red', opacity=1, label='High Stress Regions')

# slice_mesh = mesh.slice(normal='x', origin=(300, 0, 0))
# pl.add_mesh(slice_mesh, scalars=slice_mesh["S_Mises"], cmap="coolwarm", opacity=1, show_scalar_bar=False)

# warped_mesh = mesh.warp_by_vector("U", factor=1000)
# pl.add_mesh(warped_mesh, 
            # scalars=warped_mesh["S_Mises"], 
            # cmap="coolwarm", opacity=1, 
            # show_scalar_bar=False)

arrow = mesh.glyph(orient="U", scale="S_Mises", tolerance=0.05, factor=50)
pl.add_mesh(arrow, color='black', label='Displacement Vectors')
pl.add_text("Beam Stress Visualization", font_size=14)
pl.show()  