import pyvista as pv
import numpy as np

#print(pv.Report())
mesh=pv.read("data/beam_stress.vtu")



stress=mesh["S_Mises"]
displacement=mesh["U"]

pl=pv.Plotter(shape=(1,2),window_size=[1200,600])

pl.add_mesh(mesh,scalars=stress,cmap="coolwarm",opacity=0.3, clim=[0,100], show_scalar_bar=True, scalar_bar_args={"title":"Von Mises Stress"})

#max_idx=np.argmax(stress)
#print("maximum stress at point:",mesh.points[max_idx],"with value:",stress[max_idx])

#high_stress=mesh.threshold(value=stress[max_idx]*0.5,scalars="S_Mises")
#pl.add_mesh(high_stress, color="red", opacity=0.5, label="High Stress Regions")

#clip_mesh=mesh.clip(normal="X", origin=(300,0,0))
#pl.add_mesh(clip_mesh,show_edges=True,scalars="S_Mises",cmap="coolwarm", scalar_bar_args={"title":"Von Mises Stress"})

pl.subplot(0,0)
warped_mesh=mesh.warp_by_vector("U",factor=1000.0)
pl.add_mesh(warped_mesh,scalars="S_Mises",cmap="coolwarm", clim=[0,100], scalar_bar_args={"title":"Von Mises Stress (Deformed)"})

pl.subplot(0,1)
arrows=mesh.glyph(orient="U",scale="S_Mises",factor=50.0, tolerance=0.1)
pl.add_mesh(arrows,color="black",label="Displacement Vectors")

pl.show()