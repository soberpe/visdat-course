import pyvista as pv
import meshio
import numpy as np

mesh = meshio.read("data/conrod.inp")

pv_mesh = pv.from_meshio(mesh)

stress=np.random.rand(pv_mesh.n_points) * 200
pv_mesh["Stress"] = stress

disp = np.random.rand(pv_mesh.n_points,3) * 0.1
pv_mesh["Displacement"] = disp
        
warped_mesh = pv_mesh.warp_by_vector("Displacement", factor=100.0)

#warped_mesh.plot(scalars="Stress", cmap="coolwarm", show_edges=True, scalar_bar_args=("title":"Stress Distribution"))