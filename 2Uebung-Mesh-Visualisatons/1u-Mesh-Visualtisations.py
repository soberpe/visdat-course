import pyvista as pv   
import numpy as np 
mesh = pv.read("data/beam_stress.vtu")
print(mesh)
print("Fields: ", mesh.array_names)
print("Points: ", mesh.points)
print("Cells: ", mesh.cells)

stress = mesh["S_Mises"]
print("Stress range: ", stress.min(), "to", stress.max())

displacement = mesh["U"]
print("Displacement range: ", displacement.min(), "to", displacement.max()) 
print("Displacement shape: ", displacement.shape)

pl = pv.Plotter(window_size=[1024, 768], shape=(1, 2))
pl.add_mesh(mesh, scalars=stress, 
            cmap="viridis", 
            opacity=0.3,
            show_scalar_bar=True , 
             clim=(0, 1),
            scalar_bar_args={"title": "Mises Stress"})
max_idx = np.argmax(stress)
print("Max stress at point: ", mesh.points[max_idx], "with stress:", stress[max_idx])

high_stress_sphere = mesh.threshold(value=stress[max_idx]*0.9, scalars="S_Mises")

clip_mesh = mesh.clip(normal="x", origin=(300, 0, 0))

pl.add_mesh(
    clip_mesh,
    cmap="plasma",
    opacity=0.8,
    label="Clipped Mesh")

warrped_mesh = mesh.warp_by_vector("U", factor=1000)

pl.add_mesh(
    warrped_mesh,
    scalars=stress,
    cmap="inferno",
    opacity=0.7,
    clim=(0, 1),
    label="Warped Mesh")

arrows = mesh.glyph(
    orient="U",
    scale="S_Mises",
    factor=50,
    tolerance=0.05,
)

pl.subplot(0,1)
pl.add_mesh(arrows, color="white", label="Displacement Vectors")
pl.link_views()


pl.show()







