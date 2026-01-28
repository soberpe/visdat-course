import pyvista as pv
import numpy as np

mesh = pv.read("data/beam_stress.vtu")
print(mesh)
print("Fields:",mesh.array_names)
print("Points:",mesh.points)
print("Cells:",mesh.cells)

print(mesh["S_Mises"])
stress = mesh["S_Mises"]
print("Stress range: ", stress.min(), "to", stress.max(), "MPa")

displacement = mesh["U"]
print("Displacement range: ", displacement.min(), "to", displacement.max(), "mm")
print("Displacement shape: ", displacement.shape)

pl = pv.Plotter()
pl.add_mesh(
    mesh,
    show_scalar_bar=True,
    scalars=stress, cmap="bwr",
    scalar_bar_args={"title": "Von Mises Stress (MPa)"})

max_idx = np.argmax(stress)
print("Max stress at point index:", mesh.points[max_idx], "with value: ", stress[max_idx])

'''high_stress = mesh.threshold(value=stress[max_idx] * 0.8, scalars="S_Mises")
pl.add_mesh(
    high_stress,
    color="red",
    opacity=1.0,
    label="High Stress Regions")'''


clip_mesh = mesh.slice(normal='x', origin=(300,0,0))
pl.add_mesh(
    clip_mesh,
    scalars=clip_mesh["S_Mises"],
    cmap="jet",
    opacity=1.0,
    label="V'Mises Stress",
    show_scalar_bar=False)

warped_mesh = mesh.warp_by_vector("U", factor = 100)
pl.add_mesh(
    warped_mesh,
    scalars = stress,
    cmap = "jet",
    opacity = 0.3, 
    clim = [0,1],
    show_scalar_bar=False
)

arrows = mesh.glyph(orient="U", scale="S_Mises", factor=50, tolerance = 0.05)
pl.add_mesh(arrows, color="black")
'''pl.subplot(0,1)'''
pl.add_text("Test01", font_size=24, position="upper_edge")
pl.show()

print("Programm Ende")