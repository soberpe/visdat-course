---
title: Mesh Visualization Workshop
sidebar_position: 6
---

# Mesh Visualization Workshop

**Duration:** 3 blocks (3 × 45 minutes)  
**Goal:** Learn to visualize and manipulate 3D meshes using PyVista through active coding

## Prerequisites

Install required packages:
```bash
pip install pyvista numpy meshio
```

:::info Real FEM Data
The mesh file `beam_stress.vtu` contains actual finite element analysis results from CalculiX. Available fields include:
- `U`: Displacement vector (3 components, in mm)
- `S_Mises`: von Mises stress (scalar, in MPa)  
- `S`: Full stress tensor (6 components)
- `E`: Strain tensor (6 components)
- `S_Principal`: Principal stresses (3 components)
- `E_Principal`: Principal strains (3 components)
- `RF`: Reaction forces (3 components)

Use `mesh.array_names` to see all available fields.
:::

---

## Block 1: Live Coding Session (45 min)

**Format**: Instructor codes live, students type along (NO copy-paste!)

### Part 1: Setup & Mesh Fundamentals

**Goal**: Working environment + understanding mesh data structures

**Tasks:**
1. Quick installation check: `pip install pyvista numpy meshio`
2. Import and verify: `pv.Report()`
3. Load mesh: `data/beam_stress.vtu`
4. Explore structure:
   - Print mesh info
   - Check `.array_names` for available fields
   - Examine `.points` shape and `.n_cells`
   - Access data: `mesh['S_Mises']`

**Discussion points:**
- Points = 3D coordinates (vertices)
- Cells = connectivity (how points connect)
- Arrays = data at points or cells
- **Key insight:** Mesh = geometry + data!

---

### Part 2: Interactive Visualization

**Goal**: Understand PyVista's interactive window

**Tasks:**
1. Quick plot: `mesh.plot()` - opens interactive window
2. Learn mouse controls:
   - Left drag = rotate
   - Right drag = zoom
   - Middle drag = pan
3. Keyboard shortcuts: `r` (reset), `w` (wireframe), `q` (quit)

**Important distinction - two ways to plot:**
4. Quick method: `mesh.plot()` - simple, one-liner
5. Manual method: Build a `Plotter` object, then call `.show()`

**Critical concept - blocking behavior:**
6. Both `.plot()` and `.show()` block execution!
   ```
   mesh.plot()
   print("After plot")  # This waits for window to close
   
   pl = pv.Plotter()
   pl.add_mesh(mesh)
   pl.show()
   print("After show")  # This also waits for window to close
   ```

**Explore camera control:**
7. Try preset camera positions: `camera_position='iso'`, `'xy'`, `'xz'`, `'yz'`
8. Change background: `pl.set_background('white')` or other colors
9. Optional: Experiment with lighting and shadows

**Note on non-blocking mode:**
- For animations or continuous updates, PyVista offers non-blocking alternatives
- These require additional packages (`pyvistaqt` with Qt, or `trame` for web-based)
- Not covered in this workshop - blocking mode is sufficient for most tasks!

**Key insight:** Blocking mode is standard. You build your visualization, then display it at the end.

---

### Part 3: Custom Visualization Workflow

**Goal**: Build publication-quality plots step-by-step

**Progressive construction:**
1. Basic: `Plotter()` → `add_mesh()` → `show()`
2. Add coloring: Use `scalars='S_Mises'` and `cmap='coolwarm'`
3. Add context: `add_scalar_bar(title='Stress [MPa]')`
4. Set view: `camera_position='iso'`

**Data analysis:**
5. Extract stress array and compute min/max/mean
6. Find maximum stress location with NumPy
7. Use `.threshold(value=threshold_val, scalars='S_Mises')` to filter high stress

**Layering:**
8. Add base mesh with `opacity=0.3`
9. Add thresholded regions (opaque) on top
10. Understand rendering order

**Advanced (time permitting):**
11. Try mesh operations: `.slice()`, `.clip()`
12. Experiment with different rendering styles (edges, wireframe)

**Key concept:** Test each step before adding complexity

---

### Part 4: Multi-Panel Layouts

**Goal**: Compare different views side-by-side

**Tasks:**
1. Create `shape=(1, 2)` for two columns
2. Left: `.subplot(0, 0)` → full mesh with stress
3. Right: `.subplot(0, 1)` → high stress only
4. Add text labels to each panel

**Experimentation:**
5. Try different colormaps: `'plasma'`, `'viridis'`, `'jet'`
6. Show edges: `show_edges=True, edge_color='black'`
7. Save output: `.screenshot('my_viz.png')`
8. Optional: Link cameras across subplots with `.link_views()`

**Challenge:** Create a clear visualization showing failure location!

---

## Block 2: Broken Code Challenge (45 min)

**Objective**: Debug code with logic errors in both Python fundamentals AND visualization. These are syntactically correct but logically flawed - you must understand the code to fix it!

---

### Exercise 1: The Stress Analyzer Class

```python
import pyvista as pv
import numpy as np

class StressAnalyzer:
    """Analyze stress distribution in a mesh"""
    
    def __init__(self, mesh_file):
        self.mesh = pv.read(mesh_file)
        self.stress = self.mesh['S_Mises']
    
    def get_critical_regions(self, threshold):
        """Return regions above threshold"""
        critical_indices = []
        for i in range(len(self.stress)):
            if self.stress[i] < threshold:
                critical_indices.append(i)
        
        return critical_indices
    
    def calculate_statistics(self):
        """Calculate stress statistics"""
        stats = {
            'min': self.stress.min(),
            'max': self.stress.max(),
            'mean': self.stress.mean(),
            'std': self.stress.std()
        }
        
        # Calculate safety factor (max allowable / actual)
        max_allowable = 200.0  # MPa
        stats['safety_factor'] = self.stress.max() / max_allowable
        
        return stats
    
    def visualize_critical(self, threshold):
        """Visualize only critical stress regions"""
        indices = self.get_critical_regions(threshold)
        
        # Create boolean mask
        mask = np.zeros(len(self.stress), dtype=bool)
        mask[indices] = True
        
        # Extract critical mesh
        critical = self.mesh.extract_points(mask)
        
        # Visualize
        pl = pv.Plotter()
        pl.add_mesh(critical, scalars='S_Mises', cmap='Reds')
        pl.add_scalar_bar(title='Critical Stress [MPa]')
        pl.show()

# Usage
analyzer = StressAnalyzer('data/beam_stress.vtu')
stats = analyzer.calculate_statistics()
print(f"Safety factor: {stats['safety_factor']:.2f}")  # Should be > 1.0 for safe!
analyzer.visualize_critical(threshold=100.0)
```

**Your task**: Run this code and analyze the results. Something is wrong!

**Questions to investigate:**
1. Run the code and look at the visualization. Does it show what you expect?
2. Print the safety factor value. Does it make engineering sense?
3. Add print statements to understand what the code actually does.
4. What should "critical regions" mean in a stress analysis?

**Learning Goals**: 
- Class methods and state management
- Loop logic and conditionals
- Mathematical formulas in code
- Boolean array indexing

---

### Exercise 2: The Mesh Comparison Tool

```python
import pyvista as pv
import numpy as np

def load_and_process_mesh(filename):
    """Load mesh and prepare for analysis"""
    mesh = pv.read(filename)
    
    # Normalize stress values (scale to 0-1 range)
    stress = mesh['S_Mises']
    normalized = (stress - stress.min()) / (stress.max() - stress.min())
    mesh['normalized_stress'] = normalized
    
    return mesh

def find_differences(mesh1, mesh2, field='S_Mises'):
    """Compare two meshes and find differences"""
    data1 = mesh1[field]
    data2 = mesh2[field]
    
    # Calculate difference
    diff = data1 - data2
    
    # Store in first mesh
    mesh1['difference'] = diff
    
    return mesh1

def visualize_comparison(original, modified):
    """Show original, modified, and difference side-by-side"""
    diff_mesh = find_differences(original, modified)
    
    pl = pv.Plotter(shape=(1, 3))
    
    # Original
    pl.subplot(0, 0)
    pl.add_mesh(original, scalars='S_Mises', cmap='viridis')
    pl.add_text('Original', font_size=10)
    
    # Modified  
    pl.subplot(0, 1)
    pl.add_mesh(modified, scalars='S_Mises', cmap='viridis')
    pl.add_text('Modified', font_size=10)
    
    # Difference
    pl.subplot(0, 2)
    pl.add_mesh(original, scalars='difference', cmap='coolwarm')
    pl.add_text('Difference', font_size=10)
    
    pl.show()

# Load two versions
original = load_and_process_mesh('data/beam_stress.vtu')
modified = pv.read('data/beam_stress.vtu')

# Modify one mesh (simulate design change)
modified['S_Mises'] = modified['S_Mises'] * 1.2  # 20% increase

# Compare
visualize_comparison(original, modified)
```

**Your task**: This code is supposed to show differences between two meshes. Debug it!

**Questions to investigate:**
1. Run the code. Does the "Difference" panel make sense?
2. Check which meshes have which fields. Print their `array_names`.
3. Trace the data flow: what gets passed to `find_differences()`?
4. Compare the preprocessing steps for both meshes.

**Learning Goals**:
- Function return values and data flow
- Variable scope and object references
- Data preprocessing consistency
- Debugging visualization pipelines

---

### Exercise 3: The Stress Report Generator

```python
import pyvista as pv
import numpy as np

class MeshReport:
    """Generate analysis report for mesh"""
    
    def __init__(self, mesh_file):
        self.mesh = pv.read(mesh_file)
        self.results = {}
    
    def analyze_zones(self, num_zones=5):
        """Divide stress range into zones and count elements"""
        stress = self.mesh['S_Mises']
        
        # Create zone boundaries
        min_stress = stress.min()
        max_stress = stress.max()
        zone_width = (max_stress - min_stress) / num_zones
        
        zones = {}
        for i in range(num_zones):
            lower = min_stress + i * zone_width
            upper = min_stress + (i + 1) * zone_width
            
            # Count points in this zone
            count = 0
            for s in stress:
                if s >= lower and s < upper:
                    count += 1
            
            # Store zone info
            zones[f'Zone_{i+1}'] = {
                'range': (lower, upper),
                'count': count,
                'percentage': count / len(stress) * 100
            }
        
        self.results['zones'] = zones
        return zones
    
    def find_peak_location(self):
        """Find location of maximum stress"""
        stress = self.mesh['S_Mises']
        max_idx = np.argmax(stress)
        
        # Get 3D coordinates
        peak_location = self.mesh.points[max_idx]
        peak_stress = stress[max_idx]
        
        # Check if it's on the boundary
        bounds = self.mesh.bounds
        x, y, z = peak_location
        
        is_boundary = (
            x == bounds[0] or x == bounds[1] or
            y == bounds[2] or y == bounds[3] or
            z == bounds[4] and z == bounds[5]
        )
        
        self.results['peak'] = {
            'location': peak_location,
            'stress': peak_stress,
            'on_boundary': is_boundary
        }
        
        return self.results['peak']
    
    def visualize_zones(self):
        """Color mesh by stress zones"""
        if 'zones' not in self.results:
            self.analyze_zones()
        
        stress = self.mesh['S_Mises']
        zone_labels = np.zeros(len(stress))
        
        # Assign zone labels
        zones = self.results['zones']
        for i, (zone_name, zone_info) in enumerate(zones.items()):
            lower, upper = zone_info['range']
            mask = (stress >= lower) & (stress < upper)
            zone_labels[mask] = i + 1
        
        # Add to mesh
        self.mesh['zone'] = zone_labels
        
        # Visualize
        pl = pv.Plotter()
        pl.add_mesh(self.mesh, scalars='zone', cmap='Set3', show_edges=True)
        pl.add_scalar_bar(title='Stress Zone', n_labels=len(zones))
        pl.show()

# Generate report
report = MeshReport('data/beam_stress.vtu')
zones = report.analyze_zones(num_zones=5)

# Print summary
for zone_name, info in zones.items():
    print(f"{zone_name}: {info['count']} points ({info['percentage']:.1f}%)")

peak = report.find_peak_location()
print(f"\nPeak stress: {peak['stress']:.2f} MPa at {peak['location']}")
print(f"On boundary: {peak['on_boundary']}")

report.visualize_zones()
```

**Your task**: This analysis report has subtle bugs. Find and fix them!

**Questions to investigate:**
1. Do all the zone percentages add up to 100%? If not, why?
2. Test the boundary detection with a mesh where you know the peak location.
3. What happens if you increase `num_zones` to a large number?
4. Read the boolean logic carefully. Can both conditions be true simultaneously?

**Learning Goals**:
- Class-based program structure
- Loop logic and boundary conditions
- Boolean logic operators (and/or)
- NumPy array indexing
- Edge case handling

---

**Debugging Strategy:**
1. Read the code completely before running
2. Identify what the code SHOULD do
3. Trace variable values mentally or with print statements
4. Test edge cases (min/max values, empty arrays, boundaries)
5. Fix ONE bug at a time and verify

**Time allocation:**
- Exercise 1: 15 minutes
- Exercise 2: 12 minutes  
- Exercise 3: 18 minutes

## Block 3: Blank Canvas Challenges (45 min)

### Instructions

You will receive:
- ✅ A mesh file
- ✅ A target screenshot showing the desired result
- ❌ **NO CODE TEMPLATE**

You must write everything from scratch!

### Challenge 1: Basic Visualization

**Given:**
- File: `data/beam_stress.vtu`
- Target:

<div align="center">

<img src={require('../../static/img/mesh-visualization-workshop/challenge1.png').default} alt="Target challenge 1" style={{width: "60%"}} />

*Figure: Target of challenge 1*

</div>

**Requirements:**
- Load the mesh
- Visualize the 'S_Mises' stress field
- Use 'coolwarm' colormap
- Add colorbar with title
- Show mesh edges in black

**No hints - figure it out!**

---

### Challenge 2: Advanced Techniques

**Given:**
- Same mesh: `data/beam_stress.vtu`
- Target:

<div align="center">

<img src={require('../../static/img/mesh-visualization-workshop/challenge2.png').default} alt="Target challenge 2" style={{width: "60%"}} />

*Figure: Target of challenge 2*

</div>

**Requirements:**
- Create a **slice** through the middle of the mesh
- Show only regions where S_Mises > 0.5 (or use appropriate threshold)
- Use two different colormaps for comparison
- Side-by-side view (hint: subplots?)

---

### Challenge 3: Create Your Own

**Freedom round!**

Pick ONE of these to implement:

**Option A: Warp Visualization**
- Load a mesh with displacement vectors
- Use `.warp_by_vector()` to show deformation
- Show original and deformed side-by-side
- Scale deformation for visibility

<div align="center">

<img src={require('../../static/img/mesh-visualization-workshop/challenge3a_warp.png').default} alt="Target challenge 3a" style={{width: "60%"}} />

*Figure: Target of challenge 3a*

</div>

**Option B: Clipping Exploration**
- Load a mesh
- Use `.clip()` to cut it in half
- Show interior structure
- Add different colors to inside vs outside

<div align="center">

<img src={require('../../static/img/mesh-visualization-workshop/challenge3b_clip.png').default} alt="Target challenge 3b" style={{width: "60%"}} />

*Figure: Target of challenge 3b*

</div>

**Option C: Multiple Meshes**
- Load 2-3 different meshes
- Combine them in one scene
- Use different colors for each
- Animate rotation (bonus!)

<div align="center">

<img src={require('../../static/img/mesh-visualization-workshop/challenge3c_multiple.png').default} alt="Target challenge 3c" style={{width: "60%"}} />

*Figure: Target of challenge 3*

</div>

**Deliverable:**
- Working code
- Screenshot or saved animation
- 2 sentences explaining what you learned

---

## Tips for Success

### When Stuck:
1. Check PyVista docs: https://docs.pyvista.org/
2. Use `print(mesh)` to see what data is available
3. Try `mesh.array_names` to see field names
4. Ask your neighbor (after trying yourself!)

### Common Mistakes:
- Forgetting `()` on methods: `show()` not `show`
- Wrong array names: check `mesh.array_names` first
- Typos in method names: `add_mesh` not `add_mseh`

### Keyboard Shortcuts in PyVista Window:
- `q`: Quit
- `r`: Reset camera
- `s`: Surface mode
- `w`: Wireframe mode
- `v`: Vertex mode

---

## Bonus Challenges (If You Finish Early)

### Bonus 1: Streamlines
Load a mesh with vector field and create streamlines

### Bonus 2: Animation
Create a rotating animation and save as GIF

### Bonus 3: Custom Colormap
Define your own colormap using matplotlib

### Bonus 4: Glyph Visualization
Show vectors as arrows using glyphs

---

## Assessment Checklist

By the end of Block 3, you should be able to:

- ☐ Load mesh files with PyVista
- ☐ Visualize scalar fields with colormaps
- ☐ Debug common PyVista errors
- ☐ Use basic mesh operations (threshold, slice, clip)
- ☐ Create publication-quality visualizations
- ☐ Write PyVista code from scratch (no templates!)

**Most importantly: You should be comfortable writing mesh visualization code without constantly copying examples!**
