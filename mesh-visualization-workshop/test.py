import pyvista as pv
import numpy as np

mesh = pv.read("data/beam_stress.vtu")
print(mesh)
print("Fields: ", mesh, mesh.array_names)
print("Points: ", mesh.points)
print("Cells: ", mesh.cells)

stress = mesh["S_Mises"]
displacment = mesh["U"]

# print("Stress range: ",stress.min(), " to ", stress.max(),"MPa")
# print("Displacment range: ",displacment.min(), " to ", displacment.max(),"mm")
# print("Displacment shape: ", displacment.shape)

# # Erste Variante Plot (kurz)
# #mesh.plot(show_edges=True)
# # Zweite Variante Plot (ausführlich)
# pl = pv.Plotter()
# pl.add_mesh(mesh,show_edges=True,scalars=stress, cmap="coolwarm", scalar_bar_args={"title": "Von Mises Stress (MPa)"})
# #pl.savefig('mesh-visualization-workshop/beam_stress.png', dpi=300)

# pl.camera_position ="xy"
# pl.show()
pl = pv.Plotter(shape=(1,2), window_size=[1200,600])
pl.subplot(0,0)
pl.add_mesh(
    mesh,
    scalars=stress,
    cmap="coolwarm",
    opacity=0.3,
    clim=[0,7],
    show_scalar_bar=True,
    scalar_bar_args={"title": "Von Mises Stress"},
)

#Maximum anzeigen: -------------------------------------------------
# max_idx = np.argmax(stress)
# print("Maximum stress at point:", mesh.points[max_idx], "with value:", stress[max_idx])

# high_stress = mesh.threshold(value=stress[max_idx] * 0.9, scalars="S_Mises")
# pl.add_mesh(
#     high_stress,
#     cmap="coolwarm",
#     color="red",
#     opacity=1.0,
#     label="High Stress Label",
# )

#Schnitt -------------------------------------------------
# slice_mesh = mesh.slice(normal="Z", origin=(300,0,0))
# clip_mesh = mesh.clip(normal="X", origin=(300,0,0))
# pl.add_mesh(
#     clip_mesh,
#     scalars=clip_mesh["S_Mises"],
#     cmap="coolwarm",
#     opacity=1.0,
#     clim=[0,7],
#     show_scalar_bar=True,
#     scalar_bar_args={"title": "Von Mises Stress"},
# )

# Deformiert: ------------------------------------------------
# warped_mesh = mesh.warp_by_vector("U", factor=1000.0)
# pl.add_mesh(
#     warped_mesh,
#     scalars=stress,
#     cmap="coolwarm",
#     opacity=1.0,
#     clim=[0,7],
#     show_scalar_bar=False,
# )

# Pfeile einfügen: ---------------------------------------
arrows = mesh.glyph(scale="S_Mises", orient="U", tolerance=0.05, factor=10.)
pl.subplot(0,1)
pl.add_mesh(arrows,color="black")
pl.add_text("Test", font_size=24, position="upper_edge")
pl.show()