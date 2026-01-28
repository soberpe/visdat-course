import pyvista as pv
import numpy as np

mesh = pv.read("data/beam_stress.vtu")
print(mesh)
print("Fields: ", mesh.array_names)
print("Points: ", mesh.points)
print("Cells: ", mesh.cells)

stress = mesh["S_Mises"]
displacement = mesh["U"]

pl = pv.Plotter(shape=(1,2), window_size=(1200,600))
pl.subplot(0,0)
pl.add_mesh(mesh,
             scalars="S_Mises", 
             cmap="coolwarm",
             opacity=0.3, 
             clim=[0,5],
             show_scalar_bar=True, 
             scalar_bar_args={"title": "Von Mises Stress"},
             )

arrows = mesh.glyph(scale="S_Mises", orient="U", tolerance=0.05, factor=10.0)

pl.subplot(0,1)
pl.add_mesh(arrows, color="black", label="Displacement Vectors")
pl.add_text("Displacement Vectors", font_size=12, position="upper_edge")

pl.show()



# max_idx = np.argmax(stress)
# print("Max Stress at point: ", mesh.points[max_idx], "with value: ", stress[max_idx], "MPA")

# high_stress = mesh.threshold(value=stress[max_idx]*0.6, scalars="S_Mises")
# pl.add_mesh(high_stress, 
#             color="red", 
#             opacity=1.0, 
#             label="High Stress Regions")

# slice_mesh = mesh.slice(normal='x', origin=(300,0,0))
# pl.add_mesh(slice_mesh, 
#             scalars=slice_mesh["S_Mises"], 
#             cmap="coolwarm", 
#             opacity=1.0, 
#             show_scalar_bar=False)

# clip_mesh = mesh.clip(normal='x', origin=(300,0,0))
# pl.add_mesh(clip_mesh, 
#             scalars=clip_mesh["S_Mises"], 
#             cmap="coolwarm", 
#             opacity=1.0, 
#             show_scalar_bar=False)

# warped_mesh = mesh.warp_by_vector("U", factor=1000.0)
# pl.add_mesh(warped_mesh, 
#             scalars=warped_mesh["S_Mises"], 
#             cmap="coolwarm", 
#             opacity=1.0,
#             clim=[0,1], 
#             show_scalar_bar=False,
#             label="Deformed Shape")