import meshio
import pyvista as pv
import numpy as np

# 1. Load Abaqus mesh
mesh = pv.read('mesh-visualisation-workshop/data/beam_stress.vtu')
print(mesh)
print("Fields", mesh.array_names)
print("Points", mesh.points)
print("Cells", mesh.cells)

stress = mesh["S_Mises"]

print("Stress range", stress.min(), "to", stress.max())
displacement = mesh["U"]
print("Displacement range:", displacement.min(), "to", displacement.max())
print("Displacement shape:", displacement.shape)

#mesh.plot()

pl = pv.Plotter()
pl.add_mesh(mesh, show_edges=True, scalars=stress, cmap="coolwarm", scalar_bar_args={"title": "Mises S (MPa)"})
pl.background_color = "white"
light = pv.Light(position=(5, 5, 5), focal_point=(0, 0, 0), color='white', intensity=1.0)
pl.add_light(light)

#pl.camera_position = 'xy'
#pl.camera_position = [(-1, -1, 1), (0, 0, 0), (0, 0, 0)]

#pl.show()


pl = pv.Plotter()
pl.add_mesh(mesh, scalars=stress, 
            cmap="viridis", 
            opacity=0.3, 
            show_scalar_bar = True, 
            scalar_bar_args = {"title": "Mises Stress"})

max_idx = np.argmax(stress)
print("Max stress at point:", mesh.points[max_idx], "with value:", stress[max_idx])
high_stress_sphere = mesh.threshold(value=stress[max_idx]*0.5, scalars="S_Mises")
pl.add_mesh(high_stress_sphere, color='red', opacity=1, label='High Stress Regions') 

#slice_mesh = mesh.slice(normal='x', origin=(300, 0, 0))

clip_mesh = mesh.clip(normal='x', origin=(300, 0, 0))

pl.add_mesh(clip_mesh, 
            cmap="plasma", 
            opacity=1, 
            label='Clipped Mesh')

warped_mesh = mesh.warp_by_vector("U", factor=1000)
pl.add_mesh(warped_mesh, 
            scalars=stress, 
            cmap="inferno", 
            opacity=1,
            clim = (0,1), 
            label='Warped Mesh')


arrows = mesh.glyph(scale="S_Mises", orient="U",factor = 50, tolerance=0.05)


pl.add_mesh(arrows, color='black')

#pl.subplot(0,1)
#pl.link_views()

pl.show()









