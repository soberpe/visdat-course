import pyvista as pv

# Basic shapes
sphere = pv.Sphere(radius=1.0, center=(0, 0, 0))
cube = pv.Cube(center=(0, 0, 0), x_length=1.0, y_length=1.0, z_length=1.0)
cylinder = pv.Cylinder(radius=1.0, height=2.0, center=(0, 0, 0))
cone = pv.Cone(radius=1.0, height=2.0, center=(0, 0, 0))
arrow = pv.Arrow(start=(0, 0, 0), direction=(1, 0, 0))
plane = pv.Plane(center=(0, 0, 0), direction=(0, 0, 1), i_size=1.0, j_size=1.0)

# Parametric surfaces
torus = pv.ParametricTorus()
mobius = pv.ParametricMobius()
klein = pv.ParametricKlein()

# Text in 3D
text = pv.Text3D("Hello PyVista!", depth=0.5)

# Plot multiple objects
pv.plot([sphere, cube, cylinder])