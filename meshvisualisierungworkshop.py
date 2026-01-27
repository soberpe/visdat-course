import pyvista as pv
import numpy as np

mesh=pv.read("data/beam_stress.vtu")
print (mesh)
print ("Fields:", mesh.array_names)
print ("Points:", mesh.points)
print ("Cells:", mesh.cells)

stress = mesh["S_Mises"]
# print("Stress range:", stress.min(), "to", stress.max(),"MPa")

displacement=mesh["U"]
# print("Displacement range:", displacement.min(), "to", displacement.max(),"mm")
# print("Displacement shape:", displacement.scells_dict)

# mesh.plot(show_edges=True)

pl=pv.Plotter(shape=(1,2), window_size=[1200,600])
pl.subplot(0,0)
pl.add_mesh(mesh,show_edges=True,opacity=0.3,scalars=stress, clim=[0,100],cmap="viridis", scalar_bar_args={"title": "Von Mises Stress [MPa]"},show_scalar_bar="true")

max_idx=np.argmax(stress)
print("maximum stress at point:", mesh.points[max_idx], "with value", stress[max_idx])


# high_stress = mesh.threshold(value=stress[max_idx]*0.5, scalars="S_Mises")
# slice_mesh=mesh.slice(normal="X", origin=(300,0,0))
# pl.add_mesh(slice_mesh, scalars=slice_mesh["S_Mises"] ,color="red", opacity=1,label="high stress regions")

# clip_mesh=mesh.clip(normal="X", origin=(300,0,0))
# pl.add_mesh(clip_mesh, scalars=clip_mesh["S_Mises"] ,color="red", opacity=1.0)


warped_mesh=mesh.warp_by_vector("U", factor=1000.0)
pl.add_mesh(warped_mesh, cmap="coolwarm", opacity=1.0,clim=[0,100],show_scalar_bar="false")

pl.subplot(0,1)
arrows=mesh.glyph(scale="S_Mises", orient="U", tolerance=0.05)
pl.add_mesh(arrows, color="black")


pl.add_text("Vectoren", position="upper_edge")

pl.show()




# #pl.screenshot("beam_stress.png")

# pl.background_color="white"
# light=pv.Light(position=(-1,-1,1), focal_point=(0,0,0), color="white")
# pl.add_light
# pl.camera_position="xy"
# pl.camera_position=[(100,100,100),(0,0,0),(0,0,1)]
# pl.show()


