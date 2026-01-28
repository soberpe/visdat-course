---
title: 3D Visualization with PyVista
sidebar_position: 4
---

# 3D Visualization with PyVista

## Overview

PyVista is a high-level, Pythonic interface to VTK (Visualization Toolkit) that makes 3D visualization more accessible and intuitive. While VTK is powerful, it can be complex and verbose for rapid prototyping and exploratory analysis. PyVista simplifies common visualization tasks while maintaining access to VTK's full capabilities, making it ideal for engineering workflows that require quick iteration and visualization of simulation results.

:::info Building on VTK
PyVista wraps VTK, providing a more intuitive API while leveraging VTK's robust rendering engine. Understanding [VTK fundamentals](./3d-visualization-vtk.md) is valuable for advanced usage, but PyVista allows you to start visualizing complex 3D data immediately.
:::

:::note Design Philosophy
PyVista follows the principle of "make simple things simple, and complex things possible." Common tasks require minimal code, while VTK's full power remains accessible when needed.
:::

## Why PyVista?

**Advantages over pure VTK:**
- **Pythonic API** - intuitive, object-oriented interface
- **Less boilerplate** - simpler code for common tasks
- **NumPy integration** - seamless array handling
- **Interactive** - built-in plotting and interaction
- **Jupyter support** - renders in notebooks
- **Easy mesh manipulation** - simplified geometry operations
- **Better documentation** - extensive examples and guides

**When to use PyVista:**
- Rapid prototyping and exploration
- Scientific data visualization
- Engineering analysis results
- Interactive 3D plotting
- Teaching and learning

**When to use VTK directly:**
- Maximum performance optimization
- Complex custom pipelines
- Low-level control needed
- Integration with existing VTK code

## Installation

```bash
# Basic installation
pip install pyvista

# With all optional dependencies
pip install pyvista[all]

# For Jupyter notebook support
pip install pyvista[jupyter]
```

**Optional dependencies:**
- `trame` - for interactive web-based visualization
- `imageio` - for animations and screenshots
- `matplotlib` - for enhanced colormaps
- `colorcet` - additional color palettes

## Quick Start

A minimal PyVista example:

```python
import pyvista as pv

# Create a sphere
sphere = pv.Sphere()

# Plot it
sphere.plot()
```

That's it! Compare this to the equivalent VTK code (30+ lines).

## Core Concepts

### Mesh Objects

PyVista provides mesh classes that wrap VTK data objects:

- `pv.PolyData` - surface meshes (triangles, quads, polygons)
- `pv.UnstructuredGrid` - 3D elements (tetrahedra, hexahedra, etc.)
- `pv.StructuredGrid` - structured 3D grids
- `pv.ImageData` - regular grids (voxels)
- `pv.RectilinearGrid` - rectilinear grids

All meshes have consistent, intuitive interfaces.

### The Plotter

The `pv.Plotter` class manages visualization:

```python
# Create plotter
plotter = pv.Plotter()

# Add meshes
plotter.add_mesh(sphere)

# Configure and show
plotter.show()
```

The plotter handles camera, lighting, interaction, and rendering automatically.

## Creating Geometric Primitives

PyVista provides simple constructors for common shapes:

```python
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
```

## Loading and Saving Data

### Reading Files

PyVista can read many file formats:

```python
# Automatic format detection
mesh = pv.read("model.stl")
mesh = pv.read("data.vtp")
mesh = pv.read("grid.vtu")

# Specific readers
mesh = pv.get_reader("model.obj").read()
```

Supported formats:
- STL (`.stl`)
- VTK Legacy (`.vtk`)
- VTK XML (`.vtp`, `.vtu`, `.vti`, `.vts`, `.vtr`)
- PLY (`.ply`)
- OBJ (`.obj`)
- Exodus (`.e`, `.exo`)
- And many more

### Writing Files

```python
# Save mesh (format from extension)
mesh.save("output.stl")
mesh.save("output.vtp")
mesh.save("output.ply")

# Specific options
mesh.save("output.stl", binary=True)
```

## Basic Plotting

### Simple Plot

```python
mesh = pv.Sphere()

# Basic plot
mesh.plot()

# With options
mesh.plot(
    color="red",
    show_edges=True,
    line_width=2,
    opacity=0.8,
    window_size=[800, 600]
)
```

### Common Plotting Options

```python
mesh.plot(
    # Appearance
    color="blue",              # Color name or RGB tuple
    opacity=0.5,               # Transparency (0-1)
    show_edges=True,           # Show mesh edges
    edge_color="black",        # Edge color
    line_width=2,              # Edge line width
    
    # Style
    style="surface",           # "surface", "wireframe", "points"
    pbr=True,                  # Physically-based rendering
    metallic=0.5,              # Metallic appearance (with pbr)
    roughness=0.5,             # Surface roughness (with pbr)
    
    # Camera
    cpos="xy",                 # Camera position preset
    camera_position=[(5,5,5), (0,0,0), (0,0,1)],  # [position, focal_point, viewup]
    zoom=1.2,                  # Zoom factor
    
    # Window
    window_size=[1024, 768],   # Window dimensions
    full_screen=False,         # Full screen mode
    screenshot="image.png",    # Save screenshot
    
    # Interaction
    interactive=True,          # Enable interaction
    notebook=False,            # Jupyter notebook mode
    
    # Rendering
    anti_aliasing=True,        # Anti-aliasing
    smooth_shading=True        # Smooth shading
)
```

## Working with Data Arrays

PyVista's tight NumPy integration enables efficient manipulation of large FEM datasets. All mesh data is stored as NumPy arrays, allowing direct application of numerical operations without data conversion overhead.

:::tip Engineering Workflow
In post-processing workflows, you can directly compute derived quantities (von Mises stress, principal stresses, strain energy density) using NumPy operations on PyVista mesh arrays. This eliminates the need for intermediate file exports and keeps all analysis in Python.
:::

### Adding Scalar Data

```python
import numpy as np

# Create mesh
mesh = pv.Sphere()

# Add scalar data to points
mesh["Temperature"] = np.random.rand(mesh.n_points)

# Add scalar data to cells
mesh["Pressure"] = np.random.rand(mesh.n_cells)

# Plot with scalar coloring
mesh.plot(scalars="Temperature", cmap="coolwarm")
```

### Adding Vector Data

```python
# Create vector field
vectors = np.random.rand(mesh.n_points, 3)
mesh["Velocity"] = vectors

# Plot vectors with arrows
arrows = mesh.glyph(orient="Velocity", scale="Velocity", factor=0.1)
arrows.plot()
```

### Accessing Data

```python
# Get point coordinates
points = mesh.points  # NumPy array

# Get cell connectivity
cells = mesh.cells

# Get scalar arrays
temp = mesh["Temperature"]

# Get bounds
bounds = mesh.bounds  # [xmin, xmax, ymin, ymax, zmin, zmax]

# Mesh statistics
print(f"Points: {mesh.n_points}")
print(f"Cells: {mesh.n_cells}")
print(f"Bounds: {mesh.bounds}")
print(f"Center: {mesh.center}")
print(f"Volume: {mesh.volume}")
```

:::info Data Access Performance
Direct array access is efficient because PyVista stores data as contiguous NumPy arrays. For large meshes (>1M elements), prefer vectorized NumPy operations over Python loops when computing derived quantities.
:::

## The Plotter Class

For advanced visualization, use the `Plotter` class:

```python
# Create plotter
plotter = pv.Plotter(
    window_size=[1024, 768],
    notebook=False,
    shape=(1, 2)  # Subplot grid
)

# Add meshes
plotter.add_mesh(
    mesh,
    color="blue",
    show_edges=True,
    opacity=0.8,
    name="my_mesh"  # For later reference
)

# Add more visual elements
plotter.add_text("Title", position="upper_edge", font_size=20)
plotter.add_axes()
plotter.add_scalar_bar("Temperature", vertical=True)

# Camera control
plotter.camera_position = "xy"
plotter.camera.zoom(1.5)

# Show
plotter.show()
```

### Multiple Subplots

```python
# Create 2x2 subplot grid
plotter = pv.Plotter(shape=(2, 2))

# Plot in different subplots
plotter.subplot(0, 0)
plotter.add_mesh(sphere, color="red")
plotter.add_text("Sphere", font_size=20)

plotter.subplot(0, 1)
plotter.add_mesh(cube, color="blue")
plotter.add_text("Cube", font_size=20)

plotter.subplot(1, 0)
plotter.add_mesh(cylinder, color="green")
plotter.add_text("Cylinder", font_size=20)

plotter.subplot(1, 1)
plotter.add_mesh(cone, color="yellow")
plotter.add_text("Cone", font_size=20)

# Link cameras (optional)
plotter.link_views()

plotter.show()
```

## Mesh Operations

### Filtering and Manipulation

```python
# Clip mesh with plane
clipped = mesh.clip(normal="z", origin=(0, 0, 0))

# Slice mesh
slices = mesh.slice_along_axis(n=10, axis="z")

# Extract surface
surface = mesh.extract_surface()

# Threshold by scalar
filtered = mesh.threshold(value=0.5, scalars="Temperature")

# Compute normals
mesh.compute_normals(inplace=True)

# Smooth mesh
smoothed = mesh.smooth(n_iter=100)

# Decimate (reduce triangles)
decimated = mesh.decimate(0.5)  # Keep 50% of triangles

# Triangulate
triangulated = mesh.triangulate()

# Subdivide
subdivided = mesh.subdivide(nsub=2)
```

### Boolean Operations

```python
# Union
result = sphere.boolean_union(cube)

# Difference
result = sphere.boolean_difference(cube)

# Intersection
result = sphere.boolean_intersection(cube)
```

### Transformations

```python
# Translate
mesh.translate([1, 2, 3], inplace=True)

# Rotate (degrees)
mesh.rotate_x(45, inplace=True)
mesh.rotate_y(30, inplace=True)
mesh.rotate_z(60, inplace=True)

# Scale
mesh.scale([2, 2, 2], inplace=True)

# Transform with 4x4 matrix
import numpy as np
matrix = np.eye(4)
mesh.transform(matrix, inplace=True)
```

## Visualization Techniques

### Contouring

```python
# Load or create mesh with scalar data
mesh = pv.read("data.vtu")

# Extract isosurfaces
contours = mesh.contour(isosurfaces=10, scalars="Temperature")

# Or specify values
contours = mesh.contour(isosurfaces=[0.1, 0.5, 0.9], scalars="Temperature")

# Plot
contours.plot(scalars="Temperature", cmap="coolwarm")
```

### Streamlines

Visualize vector fields with streamlines:

```python
# Create mesh with vector field
mesh["Velocity"] = vectors

# Generate streamlines
streamlines = mesh.streamlines(
    vectors="Velocity",
    source_center=(0, 0, 0),
    source_radius=1.0,
    n_points=100,
    max_time=10.0
)

# Plot
streamlines.plot(scalars="Velocity", cmap="jet")
```

### Glyphs

```python
# Create glyphs (arrows for vectors)
arrows = mesh.glyph(
    orient="Velocity",
    scale="Velocity",
    factor=0.1,
    geom=pv.Arrow()
)

# Plot
arrows.plot()

# Or use different glyph shapes
spheres = mesh.glyph(scale="Temperature", geom=pv.Sphere())
cones = mesh.glyph(orient="Velocity", geom=pv.Cone())
```

### Volume Rendering

```python
# For volumetric data (ImageData)
volume = pv.read("volume.vti")

# Volume rendering
volume.plot(
    volume=True,
    opacity="sigmoid",
    cmap="bone",
    scalar_bar_args={"title": "Density"}
)

# Or with plotter
plotter = pv.Plotter()
plotter.add_volume(
    volume,
    opacity="sigmoid",
    cmap="bone"
)
plotter.show()
```

## Color Maps and Styling

### Color Maps

```python
# Built-in matplotlib colormaps
mesh.plot(scalars="Temperature", cmap="viridis")
mesh.plot(scalars="Temperature", cmap="plasma")
mesh.plot(scalars="Temperature", cmap="coolwarm")

# Custom colormap
import matplotlib.cm as cm
mesh.plot(scalars="Temperature", cmap=cm.jet)

# Reverse colormap
mesh.plot(scalars="Temperature", cmap="viridis_r")

# Discrete colormap
mesh.plot(
    scalars="Temperature",
    cmap="viridis",
    n_colors=10  # Discrete levels
)
```

### Scalar Bar Customization

```python
plotter = pv.Plotter()
plotter.add_mesh(mesh, scalars="Temperature", cmap="coolwarm")

plotter.add_scalar_bar(
    title="Temperature [K]",
    n_labels=5,
    italic=False,
    bold=True,
    title_font_size=20,
    label_font_size=16,
    position_x=0.85,
    position_y=0.05,
    width=0.1,
    height=0.9,
    vertical=True
)

plotter.show()
```

## Lighting and Materials

### Lighting

```python
plotter = pv.Plotter()
plotter.add_mesh(mesh, color="white")

# Add custom lights
light = pv.Light(
    position=(5, 5, 5),
    focal_point=(0, 0, 0),
    color="white",
    intensity=1.0
)
plotter.add_light(light)

# Multiple lights
light2 = pv.Light(position=(-5, 5, 5), color="cyan")
plotter.add_light(light2)

plotter.show()
```

### Physically-Based Rendering (PBR)

```python
# Enable PBR for realistic materials
mesh.plot(
    pbr=True,
    metallic=0.8,     # 0=dielectric, 1=metal
    roughness=0.2,    # 0=smooth, 1=rough
    color="gold"
)

# With plotter
plotter = pv.Plotter()
plotter.add_mesh(
    mesh,
    pbr=True,
    metallic=0.9,
    roughness=0.1,
    color="silver"
)
plotter.enable_shadows()  # Add shadows
plotter.show()
```

## Interactive Features

### Widgets

PyVista provides interactive widgets:

```python
# Plane widget for clipping
plotter = pv.Plotter()
plotter.add_mesh(mesh, opacity=0.5)

def callback(normal, origin):
    clipped = mesh.clip(normal=normal, origin=origin)
    plotter.add_mesh(clipped, name="clipped")

plotter.add_plane_widget(callback)
plotter.show()

# Other widgets
plotter.add_sphere_widget(callback)
plotter.add_box_widget(callback)
plotter.add_line_widget(callback)
plotter.add_slider_widget(callback, [0, 1], value=0.5)
```

### Picking

```python
def pick_callback(picked_mesh):
    print(f"Picked point: {picked_mesh}")

plotter = pv.Plotter()
plotter.add_mesh(mesh, pickable=True)
plotter.enable_surface_picking(callback=pick_callback)
plotter.show()
```

## Animations

### Camera Animation

```python
plotter = pv.Plotter()
plotter.add_mesh(mesh)

# Open movie file
plotter.open_movie("rotation.mp4")

# Animate camera rotation
for angle in range(0, 360, 2):
    plotter.camera.azimuth = angle
    plotter.write_frame()

plotter.close()
```

### Property Animation

```python
plotter = pv.Plotter()
actor = plotter.add_mesh(mesh, color="blue")

plotter.open_movie("fade.mp4")

# Animate opacity
for opacity in np.linspace(1, 0, 50):
    actor.GetProperty().SetOpacity(opacity)
    plotter.write_frame()

plotter.close()
```

## Integration with NumPy

PyVista works seamlessly with NumPy:

```python
import numpy as np

# Create mesh from NumPy arrays
points = np.random.rand(100, 3)
cloud = pv.PolyData(points)

# Create structured grid
x = np.arange(-10, 10, 0.5)
y = np.arange(-10, 10, 0.5)
z = np.arange(-10, 10, 0.5)
x, y, z = np.meshgrid(x, y, z)
grid = pv.StructuredGrid(x, y, z)

# Add computed scalar field
values = np.sin(np.sqrt(x**2 + y**2 + z**2))
grid["Values"] = values.flatten()

# Plot
grid.plot(scalars="Values", cmap="coolwarm")
```

## Examples

### Example 1: Visualize Finite Element Results

```python
import pyvista as pv
import numpy as np

# Load FEM mesh
mesh = pv.read("fem_results.vtu")

# Add stress data
mesh["Stress"] = np.random.rand(mesh.n_points) * 100

# Create plotter
plotter = pv.Plotter()

# Add mesh with stress coloring
plotter.add_mesh(
    mesh,
    scalars="Stress",
    cmap="jet",
    show_edges=True,
    edge_color="black",
    scalar_bar_args={
        "title": "von Mises Stress [MPa]",
        "vertical": True
    }
)

# Add axes
plotter.add_axes()

# Add title
plotter.add_text("FEM Stress Analysis", position="upper_edge", font_size=16)

plotter.show()
```

### Example 2: Interactive Slice Viewer

```python
import pyvista as pv

# Load volume data
volume = pv.read("ct_scan.vti")

# Create orthogonal slices
slices = volume.slice_orthogonal()

# Plot with multiple views
plotter = pv.Plotter(shape=(2, 2))

# XY slice
plotter.subplot(0, 0)
plotter.add_mesh(slices[0], cmap="bone")
plotter.add_text("XY Plane", font_size=12)

# XZ slice
plotter.subplot(0, 1)
plotter.add_mesh(slices[1], cmap="bone")
plotter.add_text("XZ Plane", font_size=12)

# YZ slice
plotter.subplot(1, 0)
plotter.add_mesh(slices[2], cmap="bone")
plotter.add_text("YZ Plane", font_size=12)

# 3D view
plotter.subplot(1, 1)
plotter.add_mesh(volume.outline(), color="black")
plotter.add_mesh(slices, cmap="bone", opacity=0.5)

plotter.show()
```

### Example 3: Vector Field Visualization

```python
import pyvista as pv
import numpy as np

# Create grid
x = np.arange(-5, 5, 0.5)
y = np.arange(-5, 5, 0.5)
z = np.arange(-5, 5, 0.5)
x, y, z = np.meshgrid(x, y, z)
grid = pv.StructuredGrid(x, y, z)

# Compute velocity field (circular flow)
vectors = np.empty((grid.n_points, 3))
vectors[:, 0] = -grid.points[:, 1]
vectors[:, 1] = grid.points[:, 0]
vectors[:, 2] = 0
grid["Velocity"] = vectors

# Compute magnitude
grid["Speed"] = np.linalg.norm(vectors, axis=1)

# Create streamlines
seed = pv.Disc(inner=0, outer=4, r_res=2, c_res=12)
streamlines = grid.streamlines_from_source(
    seed,
    vectors="Velocity",
    max_time=10.0
)

# Plot
plotter = pv.Plotter()
plotter.add_mesh(streamlines, scalars="Speed", cmap="plasma", line_width=2)
plotter.add_mesh(seed, color="white", opacity=0.3)
plotter.add_axes()
plotter.add_text("Velocity Field", position="upper_edge", font_size=16)
plotter.show()
```

## Best Practices

### Performance Tips

:::tip In-Place Operations
Use in-place operations when possible to reduce memory usage and improve performance. Many PyVista methods, such as `compute_normals` and `translate`, support the `inplace=True` argument to modify the mesh directly:

```python
mesh.compute_normals(inplace=True)
mesh.translate([1, 0, 0], inplace=True)
```
:::

:::tip Mesh Decimation
For meshes with very high cell counts, decimation can significantly improve interactive performance. This reduces the number of triangles while preserving the overall shape:

```python
# Decimate large meshes for smoother interaction
if mesh.n_cells > 1000000:
    mesh = mesh.decimate(0.9)  # Keep 10% of triangles
```
:::

:::tip Data Types
Use appropriate data types to reduce memory consumption. Single-precision floats (`float32`) are usually sufficient for visualization and use half the memory of double-precision (`float64`):

```python
# Use float32 instead of float64 for large datasets
mesh["Data"] = data.astype(np.float32)
```
:::

### Memory Management

```python
# Clean up large meshes
del mesh
import gc
gc.collect()

# Or use context managers for plotters
with pv.Plotter() as plotter:
    plotter.add_mesh(mesh)
    plotter.show()
# Automatically cleaned up
```

## Comparison: VTK vs PyVista

The same visualization in VTK and PyVista:

**VTK (30+ lines):**
```python
import vtk

cone = vtk.vtkConeSource()
cone.SetResolution(50)

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(cone.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(1.0, 0.0, 0.0)

renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)

interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(renderWindow)

renderWindow.Render()
interactor.Start()
```

**PyVista (3 lines):**
```python
import pyvista as pv
cone = pv.Cone(resolution=50)
cone.plot(color="red", background="lightblue")
```

## Resources

- **Official Documentation:** https://docs.pyvista.org
- **Examples Gallery:** https://docs.pyvista.org/examples/
- **Tutorial:** https://tutorial.pyvista.org
- **GitHub:** https://github.com/pyvista/pyvista
- **Discussions:** https://github.com/pyvista/pyvista/discussions

## Next Steps

1. **Explore Examples:** Browse the PyVista examples gallery
2. **Practice:** Try visualizing your own data
3. **Learn VTK:** Understand [VTK concepts](./3d-visualization-vtk.md) for advanced usage
4. **File Conversion:** Use [meshio](./meshio-file-conversion.md) to load FEM results
5. **Join Community:** Ask questions on GitHub Discussions

:::tip Engineering Application
PyVista excels at FEM post-processing visualization. Combined with meshio for file I/O and NumPy for analysis, you have a complete Python-based post-processing environment that rivals commercial visualization software.
:::

PyVista makes 3D visualization in Python accessible, intuitive, and powerful for mechanical engineering applications. Start with simple examples and gradually explore more advanced features as your visualization needs grow.
