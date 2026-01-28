import pyvista as pv
import numpy as np
mesh = pv.read("mesh-visualization-workshop/data/beam_stress.vtu")
print(mesh)
print("Fields", mesh.array_names)
print("Points", mesh.points)
print("Cells", mesh.cells)

stress = mesh ["S_Mises"]
print("Stress range" , stress.min(), "to" , stress.max() , "MPa")
displacement = mesh ["U"]
print("Displacement range", displacement.min(), "to", displacement.max(), "mm")
print("Displacemnt shape", displacement.shape)

mesh.plot()

pl = pv.Plotter()
pl.add_mesh(mesh, show_edges=True, scalars=stress, cmap="coolwarm", scalar_bar_args={"title": "Von Mises Stress (MPa)"})
light = pv.Light(position=(1, 1, 1), focal_point=(0, 0, 0), color="white", intensity=0.8)
pl.add_light(light)

pl.camera_position = 'xy'
pl.camera.position = [(10,10,10) , (0,0,0) , (0,0,1)]

pl.show()
print("Hallo Welt")

pl = pv.Plotter()
pl.add_mesh(mesh,scalars=stress,cmap="viridis",show_scalar_bar=True, scalar_by_args=["title":"Von Mises Stress"])

max_idx = np.argmax(stress)
print("Max stress at point index:", mesh.point[max.idx], "with value", stress[max_idx])

high_stress = mesh.threshold(value=stress[max_idx]*0.9,scalars="S_Mises")
pl.add_mesh(high_stress,color="red",opacity=0.5, label="High Stress Regions")

clip_mesh = mesh.clip(normal="x", origin=(300,0,0))
pl.add_mesh(clip_mesh, scalars=clip_mesh ["S_Mises"], cmap="coolwarm", show_scalar_bar=True)

warped_mesh = mesh.warp_by_vector ("u" , factor=100)
pl.add_mesh(warped_mesh, scalars=stress, cmap=coolwarm, capacity=1,0 , show_scalar_bar=false)
