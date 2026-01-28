#import pyvista as pv
#import numpy as np

#mesh = pv.read("data/beam_stress.vtu")
#print(mesh)
#print("Fields:", mesh.array_names)
#print("Points:", mesh.points)
#print("Cells:", mesh.cells)

#stress = mesh["S_Mises"]
#displacement = mesh["U"]

#pl = pv.Plotter(shape=(2,2).window_size=[1200,600])
#pl.sublot(0,1)
#pl.add_mesh(
#    mesh,
#    scalars=stress,
#    cmap="coolwarm",
#    opacity=0.3,
#    clim=[0,100],
#    show_scalar_bar=True,
#    scalar_bar_args={"title": "Von Mises Stress [MPa]"},
#)

#max_idx = np.argmax(stress)
#print("Maximum stress at point:", mesh.points[max_idx], "with value:", stress[max_idx])

#high_stress = mesh.threshold(value=stress[max_idx] * 0.9, scalars="S_Mises")
#pl.add_mesh(
#    high_stress,
#    color="red",
#    opacity=1,
#    label="High Stress Regions",
#)

#slice_mesh = mesh.slice(normal="Z",origin=(0,0,0))

#clip_mesh = mesh.clip(normal="X",origin=(300,0,0))
#pl.add_mesh(
#    clip_mesh,
#    scalars=clip_mesh["S_Mises"],
#    cmap="coolwarm",
#    opacity=1,
#    show_scalar_bar=True,
#    scalar_bar_args={"title": "Von Mises Stress [MPa]"},
#)

#warped_mesh = mesh.warp_by_vector("U", factor=1000.0)
#pl.add_mesh(
#    warped_mesh,
#    scalars=warped_mesh["S_Mises"],
#    cmap="coolwarm",
#    opacity=1,
#    clim=[0,1],
#    show_scalar_bar=True,
#    scalar_bar_args={"title": "Von Mises Stress [MPa]"},
#)

#arrows = mesh.glyph(scale="S_Mises", orient="U", tolerance=0.05, factor=50.)
#pl.sublot(0,1)
#pl.add_mesh(arrows, color="black")
#pl.show()