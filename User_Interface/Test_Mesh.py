import numpy as np
import pyvista as pv
import meshio

mesh = meshio.read("dat/conrod.inp")

pv_mesh = pv.from_meshio(mesh)

stress = np.random.rand(pv_mesh.n_points) * 200
pv_mesh["Stress"] = stress

dsip = np.random.rand(pv_mesh.n_points,3)*0.1
pv_mesh["Displacment"] = dsip

warped_mesh = pv_mesh.warp_by_vector("Displacment", factor = 100.0)

pv_mesh.plot(scalars="Stress", cmap="coolwarm", show_edges=True, scalar_bar_args={"title":"Stress Distrubution"})