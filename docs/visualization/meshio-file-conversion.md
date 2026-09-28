---
title: File Conversion with meshio
sidebar_position: 4
---

# File Conversion with meshio

## Overview

meshio is a Python library for reading and writing mesh files in various formats. It serves as a universal translator between different mesh file formats, making it particularly valuable when working with data from different simulation software packages.

In scientific computing and engineering, different tools use different file formats for historical, technical, or proprietary reasons. meshio bridges these gaps, allowing you to convert meshes from one format to another and integrate them into visualization workflows with VTK and PyVista.

:::info Engineering Workflow Integration
A typical finite element workflow involves multiple software packages: CAD modeling (STEP, IGES), mesh generation (Gmsh, ANSYS), simulation (CalculiX, Abaqus), and post-processing (ParaView, PyVista). meshio enables seamless data exchange between these stages.
:::

:::tip Best Practice
When working with FEM results, export to standardized formats (VTK, XDMF) rather than proprietary formats. This ensures long-term accessibility and interoperability with various analysis tools.
:::

## What is meshio?

meshio is:
- **Format-agnostic** - reads and writes 30+ mesh file formats
- **Lightweight** - simple Python interface with minimal dependencies
- **Well-maintained** - actively developed open-source project
- **Command-line ready** - includes CLI tools for quick conversions
- **PyVista-compatible** - seamless integration with visualization tools

## Why Use meshio?

Common scenarios where meshio is essential:

- **FEM software integration** - Convert Abaqus, ANSYS, or Gmsh meshes for visualization
- **Format standardization** - Convert proprietary formats to open standards (VTK, XDMF)
- **Workflow bridges** - Move data between preprocessing, simulation, and postprocessing tools
- **Data accessibility** - Extract mesh data for custom analysis or visualization

## Installation

```bash
# Basic installation
pip install meshio

# With all optional dependencies
pip install meshio[all]
```

Optional dependencies enable support for specific formats:
- `netcdf4` - for NetCDF files
- `h5py` - for HDF5-based formats (XDMF, H5M)

## Supported File Formats

meshio supports a wide range of formats commonly used in engineering and scientific computing:

### Finite Element Analysis
- **Abaqus** (`.inp`) - Abaqus input files with mesh and element definitions
- **ANSYS** (`.msh`) - ANSYS mesh format
- **Gmsh** (`.msh`) - Open-source mesh generator format
- **Exodus II** (`.e`, `.exo`) - Sandia National Labs format, widely used in multiphysics
- **FLAC3D** (`.f3grid`) - Itasca FLAC3D grids for geomechanical analysis
- **COMSOL** - COMSOL Multiphysics meshes
- **CalculiX** - Limited support for CalculiX input format

:::note Format Compatibility
While meshio can read mesh geometry from most FEM formats, result fields (stress, strain, displacement) are often format-specific. For results post-processing, prefer formats explicitly designed for results exchange like Exodus II or XDMF.
:::

### Visualization Formats
- **VTK Legacy** (`.vtk`) - ParaView/VTK legacy format
- **VTK XML** (`.vtu`, `.vtp`, `.vts`, `.vtr`) - Modern VTK formats
- **XDMF** (`.xdmf`) - eXtensible Data Model and Format
- **STL** (`.stl`) - Stereolithography format

### General Mesh Formats
- **PLY** (`.ply`) - Polygon File Format
- **OBJ** (`.obj`) - Wavefront OBJ
- **OFF** (`.off`) - Object File Format
- **CGNS** (`.cgns`) - CFD General Notation System

For a complete list, see the [meshio documentation](https://github.com/nschloe/meshio).

## Basic Usage

### Reading Mesh Files

meshio automatically detects the file format from the extension:

```python
import meshio

# Read any supported format
mesh = meshio.read("model.inp")  # Abaqus
mesh = meshio.read("data.msh")   # ANSYS or Gmsh
mesh = meshio.read("grid.exo")   # Exodus II

# Access mesh data
print(f"Points: {len(mesh.points)}")
print(f"Cells: {len(mesh.cells)}")

# Inspect cell types
for cell_block in mesh.cells:
    print(f"  {cell_block.type}: {len(cell_block.data)} elements")
```

### Mesh Data Structure

A meshio mesh object contains:

```python
# Geometry
mesh.points          # NumPy array of point coordinates (n_points, 3)

# Topology
mesh.cells           # List of cell blocks
mesh.cells[0].type   # Cell type (e.g., "tetra", "hexahedron")
mesh.cells[0].data   # Cell connectivity array

# Data arrays
mesh.point_data      # Dictionary of data defined at points
mesh.cell_data       # Dictionary of data defined at cells
mesh.field_data      # Dictionary of field/material data
```

### Writing Mesh Files

Convert to any supported format by specifying the output filename:

```python
# Read Abaqus mesh
mesh = meshio.read("model.inp")

# Write as VTK for ParaView
meshio.write("output.vtu", mesh)

# Write as XDMF for time series
meshio.write("output.xdmf", mesh)

# Write as STL for CAD
meshio.write("output.stl", mesh)
```

## Command-Line Tools

meshio provides command-line utilities for quick operations without writing Python code.

### Format Conversion

```bash
# Convert Abaqus to VTK
meshio convert input.inp output.vtu

# Convert ANSYS to Exodus
meshio convert mesh.msh output.exo

# Convert Gmsh to STL
meshio convert geometry.msh surface.stl
```

### Mesh Information

```bash
# Display mesh statistics
meshio info model.inp

# Output shows:
#   - Number of points
#   - Number of cells by type
#   - Available data arrays
#   - File format details
```

### File Compression

```bash
# Compress VTK XML files
meshio compress large_mesh.vtu

# Decompress
meshio decompress large_mesh.vtu
```

### Format Conversion

```bash
# Convert to binary format
meshio binary mesh.vtu

# Convert to ASCII format
meshio ascii mesh.vtu
```

## Integration with PyVista

meshio meshes can be directly converted to PyVista for visualization.

### Simple Conversion

```python
import meshio
import pyvista as pv

# Read mesh with meshio
mesh = meshio.read("model.inp")

# Convert to PyVista
pv_mesh = pv.from_meshio(mesh)

# Visualize
pv_mesh.plot(show_edges=True)
```

### Preserving Data Arrays

Data arrays (scalars, vectors) are automatically transferred:

```python
# Read mesh with solution data
mesh = meshio.read("results.inp")

# Check available data
print("Point data:", mesh.point_data.keys())
print("Cell data:", mesh.cell_data.keys())

# Convert to PyVista (data preserved)
pv_mesh = pv.from_meshio(mesh)

# Visualize with scalar coloring
if "Temperature" in pv_mesh.point_data:
    pv_mesh.plot(scalars="Temperature", cmap="coolwarm")
```

## Practical Examples

### Example 1: Abaqus to VTK Conversion

Convert Abaqus finite element mesh for visualization in ParaView:

```python
import meshio

# Read Abaqus input file
mesh = meshio.read("structure.inp")

# Display mesh information
print(f"Nodes: {len(mesh.points)}")
for cell_block in mesh.cells:
    print(f"{cell_block.type}: {len(cell_block.data)}")

# Write as VTK XML format
meshio.write("structure.vtu", mesh)

print("Conversion complete: structure.vtu")
```

### Example 2: Batch Conversion

Convert multiple files in a directory:

```python
import meshio
from pathlib import Path

# Find all Abaqus files
input_dir = Path("simulation_results")
inp_files = input_dir.glob("*.inp")

# Convert each to VTK
for inp_file in inp_files:
    mesh = meshio.read(inp_file)
    output_file = inp_file.with_suffix(".vtu")
    meshio.write(output_file, mesh)
    print(f"Converted: {inp_file.name} → {output_file.name}")
```

### Example 3: Mesh with Scalar Data

Create a mesh with solution data and export:

```python
import meshio
import numpy as np

# Read mesh
mesh = meshio.read("mesh.inp")

# Add scalar field (e.g., from analysis results)
temperature = np.random.rand(len(mesh.points)) * 100
mesh.point_data["Temperature"] = temperature

# Add vector field
displacement = np.random.rand(len(mesh.points), 3) * 0.1
mesh.point_data["Displacement"] = displacement

# Write with data
meshio.write("results.vtu", mesh)
```

### Example 4: Extracting Specific Cell Types

Extract only surface elements from a 3D mesh:

```python
import meshio

# Read full 3D mesh
mesh = meshio.read("volume.inp")

# Extract only triangular surface elements
triangles = []
triangle_data = {}

for i, cell_block in enumerate(mesh.cells):
    if cell_block.type == "triangle":
        triangles.append(cell_block)
        # Also extract corresponding cell data
        for key in mesh.cell_data:
            if key not in triangle_data:
                triangle_data[key] = []
            triangle_data[key].append(mesh.cell_data[key][i])

# Create new mesh with only triangles
surface_mesh = meshio.Mesh(
    points=mesh.points,
    cells=triangles,
    cell_data=triangle_data
)

# Write surface mesh
meshio.write("surface.stl", surface_mesh)
```

## Time Series Data

For transient simulations, meshio supports time series in XDMF format.

### Writing Time Series

```python
import meshio
import numpy as np

# Create or read base mesh
mesh = meshio.read("mesh.vtu")

# Write time series
with meshio.xdmf.TimeSeriesWriter("transient.xdmf") as writer:
    # Write mesh once
    writer.write_points_cells(mesh.points, mesh.cells)
    
    # Write data at each time step
    for t in np.linspace(0, 1, 11):  # 11 time steps
        # Compute or load solution at time t
        temperature = np.sin(2 * np.pi * t) * mesh.points[:, 0]
        
        # Write time and data
        writer.write_data(
            t,
            point_data={"Temperature": temperature}
        )

print("Time series written to transient.xdmf")
```

### Reading Time Series

```python
import meshio

# Read time series
with meshio.xdmf.TimeSeriesReader("transient.xdmf") as reader:
    # Read mesh
    points, cells = reader.read_points_cells()
    
    print(f"Number of time steps: {reader.num_steps}")
    
    # Read each time step
    for k in range(reader.num_steps):
        t, point_data, cell_data = reader.read_data(k)
        print(f"Time {t}: Temperature range [{point_data['Temperature'].min():.2f}, {point_data['Temperature'].max():.2f}]")
```

## Cell Type Mapping

meshio uses standardized cell type names that differ from VTK or Abaqus conventions:

| meshio | VTK | Abaqus | Description |
|--------|-----|--------|-------------|
| `vertex` | VERTEX | - | Single point |
| `line` | LINE | B31, T2D2 | Two-node line |
| `triangle` | TRIANGLE | S3, CPS3 | Three-node triangle |
| `quad` | QUAD | S4, CPS4 | Four-node quadrilateral |
| `tetra` | TETRA | C3D4 | Four-node tetrahedron |
| `pyramid` | PYRAMID | C3D5 | Five-node pyramid |
| `wedge` | WEDGE | C3D6 | Six-node wedge |
| `hexahedron` | HEXAHEDRON | C3D8 | Eight-node hexahedron |
| `tetra10` | QUADRATIC_TETRA | C3D10 | Ten-node quadratic tetrahedron |
| `hexahedron20` | QUADRATIC_HEXAHEDRON | C3D20 | Twenty-node quadratic hexahedron |

## Best Practices

:::tip File Format Selection
Choose the output format based on your needs:
- **VTK XML** (`.vtu`, `.vtp`) - best for ParaView visualization, preserves all data
- **XDMF** (`.xdmf`) - ideal for large datasets and time series
- **STL** (`.stl`) - for CAD compatibility, surface meshes only
- **Exodus II** (`.exo`) - standard for FEM, widely supported
:::

:::tip Data Preservation
When converting formats, be aware that:
- Not all formats support all cell types
- Some formats may lose metadata or field data
- Cell ordering may change between formats
- Always verify the converted mesh before use
:::

:::tip Performance
For large meshes:
- Use binary formats when available (faster I/O)
- Consider XDMF for datasets larger than 1GB
- Compress VTK XML files with `meshio compress`
- Use appropriate data types (float32 vs float64)
:::

## Resources

- **GitHub Repository:** https://github.com/nschloe/meshio
- **PyPI Package:** https://pypi.org/project/meshio/
 **Issue Tracker:** Report bugs or request features on GitHub

## Conclusion

:::tip Engineering Workflow Integration
meshio fills a critical gap in the FEM post-processing pipeline. By enabling seamless conversion between proprietary and open formats, it allows you to use best-in-class tools at each workflow stage while maintaining data accessibility and reproducibility.
:::

For complete workflows combining meshio with PyVista visualization, refer to [PyVista documentation](./3d-visualization-pyvista.md) and explore the example scripts provided in the course materials.

## Next Steps

Now that you understand mesh file conversion with meshio, you can:

1. **Work with any mesh format** - Convert between FEM, CAD, and visualization formats
2. **Integrate with PyVista** - Use converted meshes for advanced visualization
3. **Process simulation results** - Extract and visualize data from various solvers
4. **Automate workflows** - Build pipelines for mesh conversion and analysis

For visualization of converted meshes, see:
- [VTK Documentation](./3d-visualization-vtk.md) - Low-level VTK interface
- [PyVista Documentation](./3d-visualization-pyvista.md) - High-level Python visualization
