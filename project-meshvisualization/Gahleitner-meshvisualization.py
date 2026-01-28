import pyvista as pv
import numpy as np

mesh=pv.read("data/beam_stress.vtu")
print(mesh)
print("Fields:", mesh.array_names)
print("Points:", mesh.points)
print("Cells:", mesh.cells)

stress=mesh["S_Mises"]
displacement=mesh["U"]

pl=pv.Plotter()
pl.add_mesh(
    mesh,
    scalars=stress,
    cmap="coolwarm",
    opacity=0.7,
    show_scalar_bar=True,
    scalar_bar_args={"title": "Von Mises Stress [MPa]"},
)

max_idx=np.argmax(stress)
print("Max Stress:", stress[max_idx], "at point", mesh.points[max_idx])

mesh_highstress=mesh.threshold(value=stress[max_idx]*0.75, scalars="S_Mises")
pl.add_mesh(
    mesh_highstress,
    color="red",
    opacity=1,
    label="High Stress Regions",
)

mesh_sliced=mesh.slice(normal="x", origin=(300, 0, 0 ))
pl.add_mesh(
    mesh_sliced,
    scalars = mesh_sliced["S_Mises"],
    cmap="coolwarm",
    opacity=1,
)

mesh_clipped=mesh.clip(normal="x", origin=(300, 0, 0))
pl.add_mesh(
    mesh_clipped,
    scalars=mesh_clipped["S_Mises"],
    cmap="coolwarm",
    opacity=1,
)

mesh_warped=mesh.warp_by_vector("U", factor=1200)
pl.add_mesh(
    mesh_warped,
    scalars=mesh_warped["S_Mises"],
    cmap="viridis",
    opacity=0.5,
)

pl.show()