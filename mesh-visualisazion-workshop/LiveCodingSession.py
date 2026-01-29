import pyvista as pv
import numpy as np

### Introduction
'''
mesh = pv.read('data/beam_stress.vtu')
print(mesh)
print('Fields: ',mesh.array_names)
print('Points: ',mesh.points,'\nCells: ',mesh.cells)


stress = mesh['S_Mises']
# print('Stress range: ',stress.min(), 'MPa to', stress.max(), 'MPa')

displacement = mesh['U']
# print('Displacement range: ',displacement.min(), 'mm to', displacement.max(), 'mm')
# print('Displacement shape: ',displacement.shape)


# mesh.plot()

pl = pv.Plotter(shape=(1,2), window_size=(1200,600)) # optional: set window size and layout
pl.subplot(0,0) # first subplot
pl.add_text('Stress Visualization', font_size=20) # optional: add title
pl.add_mesh(mesh, 
            show_edges=False, # optional: show mesh edges
            scalars=stress, # set scalar values for coloring
            opacity=1, # optional: set mesh opacity
            cmap='coolwarm', # optional: choose colormap
            clim=[0,5], # optional: set color limits
            scalar_bar_args={'title': 'Von Mises Stress (MPa)'} # optional: customize colorbar
            ) 

## Design options

# pl.scalar_bar.SetPosition(0.8, 0.1) # optional: adjust colorbar position
# pl.add_light(pv.Light(position=(1, 1, 1), focal_point=(0, 0, 0), color='white', intensity=0.8)) # optional: add a light source
# pl.camera_position = 'xy'  # optional1: set camera position
# pl.camera_position = [(5, 5, 5), (0, 0, 0), (0, 0, 1)]  # optional2: set custom camera position

## Maximalwert ausgeben

max_idx = np.argmax(stress)
print('Max stress at point:', mesh.points[max_idx], 'with value:', stress[max_idx], 'MPa') 

## am Mesh was machen

high_stress = mesh.threshold(value = stress[max_idx]*0.8, scalars='S_Mises') # 80% des Maximalwerts der Spannung
pl.add_mesh(high_stress, 
            color='red', 
            opacity=1, 
            label='High Stress Region'
            ) # optional: highlight high-stress regions

slice_mesh = mesh.slice(normal='x', origin=(300,0,0)) # slice through the mesh at x=300
pl.add_mesh(slice_mesh,
            scalars='S_Mises', # color by stress values
            cmap='coolwarm', # colormap
            show_scalar_bar=True, # optional: show colorbar
            scalar_bar_args={'title': 'Slice Stress (MPa)'} # optional: customize colorbar
            ) # optional: add sliced mesh with different colormap

clip_mesh = mesh.clip(normal="x", origin=(300,0,0)) # clip the mesh at x=300
pl.add_mesh(clip_mesh,
            scalars=clip_mesh['S_Mises'], # color by stress values
            cmap='viridis', # colormap
            show_scalar_bar=False, # optional: show colorbar
            ) # optional: add clipped mesh with different colormap

warped_mesh = mesh.warp_by_vector('U', factor=1000) # exaggerate displacements by factor of 50
pl.add_mesh(warped_mesh,
            scalars=stress, # color by stress values
            cmap='coolwarm', # colormap
            opacity=1, # set opacity
            clim=[0,5], # optional: set color limits
            show_scalar_bar=False, # optional: show colorbar
            ) # optional: add warped mesh


pl.subplot(0,1)
arrows = mesh.glyph(orient='U', scale='S_Mises', tolerance=0.01, factor=5) # create glyphs to represent stress direction and magnitude
pl.add_mesh(arrows, color='black', label='Stress Direction') # optional: add
pl.add_text('Displacement Visualization', font_size=20) # optional: add title


pl.show()
'''
'''
### Exercise 1: The Stress Analyzer Class

class StressAnalyzer:
    """Analyze stress distribution in a mesh"""
    
    def __init__(self, mesh_file):
        self.mesh = pv.read(mesh_file)
        self.stress = self.mesh['S_Mises']
    
    def get_critical_regions(self, threshold):
        """Return regions above threshold"""
        critical_indices = []
        mask = self.stress > threshold 
        critical_indices = np.where(mask)[0] # wesentlich schneller als Schleife

#        for i in range(len(self.stress)):
#            if self.stress[i] > threshold:
#                critical_indices.append(i)
#        
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
        max_allowable = 20  # MPa
        stats['safety_factor'] = max_allowable/ self.stress.max()
        
        return stats
    
    def visualize_critical(self, threshold):
        """Visualize only critical stress regions"""
        indices = self.get_critical_regions(threshold)
        print(f'Number of critical points: {len(indices)}')
        print(f'Number of total points: {len(self.stress)}')

        # Create boolean mask
        mask = np.zeros(len(self.stress), dtype=bool)
        mask[indices] = True
        
        # Extract critical mesh
        critical = self.mesh.extract_points(mask)
        
        # Visualize
        pl = pv.Plotter()
        pl.add_mesh(critical, scalars='S_Mises', cmap='Reds', show_scalar_bar= False)
        pl.add_scalar_bar(title='Critical Stress [MPa]')
        pl.show()

# Usage
analyzer = StressAnalyzer('data/beam_stress.vtu')
stats = analyzer.calculate_statistics()
print(f"Safety factor: {stats['safety_factor']:.2f}")  # Should be > 1.0 for safe!
analyzer.visualize_critical(threshold=3.0)


### Exercise 2: The Mesh Comparison Tool

def load_and_process_mesh(filename):
    """Load mesh and prepare for analysis"""
    mesh = pv.read(filename)
    
    # Normalize stress values (scale to 0-1 range)
    stress = mesh['S_Mises']
    normalized = (stress - stress.min()) / (stress.max() - stress.min())
    mesh['normalized_stress'] = normalized
    
    return mesh

def find_differences(mesh1, mesh2, diff_mesh, field='S_Mises'):
    """Compare two meshes and find differences"""
    data1 = mesh1[field]
    data2 = mesh2[field]
    
    # Calculate difference
    diff = data1 - data2
    
    # Store in first mesh
    diff_mesh['difference'] = diff
    
    return mesh1

def visualize_comparison(original, modified):
    """Show original, modified, and difference side-by-side"""
    print(original.array_names)
    diff_mesh = original.copy()
    find_differences(original, modified, diff_mesh)
    print(original.array_names)
    print(diff_mesh.array_names)

    pl = pv.Plotter(shape=(1, 3), window_size=(1500, 500))
    
    # Original
    pl.subplot(0, 0)
    pl.add_mesh(original,
                scalars='S_Mises', 
                cmap='coolwarm', 
                clim=[0, original['S_Mises'].max()], 
                show_scalar_bar=True, 
                scalar_bar_args={'title': 'Von Mises Stress (MPa)'}
                )
    pl.add_text('Original', font_size=10)
    
    # Modified  
    pl.subplot(0, 1)
    pl.add_mesh(modified,
                scalars='S_Mises', 
                cmap='coolwarm',
                clim=[0,modified['S_Mises'].max()], 
                show_scalar_bar=True, 
                scalar_bar_args={'title': 'Von Mises Stress (MPa) mod'}
                )
    pl.add_text('Modified', font_size=10)
    
    # Difference
    pl.subplot(0, 2)
    pl.add_mesh(diff_mesh, 
                scalars='difference', 
                cmap='coolwarm',
                show_scalar_bar=True, 
                scalar_bar_args={'title': 'diffference scaled'},
                copy_mesh=True  # ensure independent colormap # needed for same meshs in multiple subplots
                )
    pl.add_text('Difference', font_size=10)
    
    pl.show()

# Load two versions
original = load_and_process_mesh('data/beam_stress.vtu')
modified = load_and_process_mesh('data/beam_stress.vtu')

# Modify one mesh (simulate design change)
modified['S_Mises'] = modified['S_Mises'] * 1.2  # 20% increase
modified['normalized_stress'] = modified['normalized_stress'] * 1.2  # 20% increase

# Compare
visualize_comparison(original, modified)
'''
### Exercise 3: The Stress Report Generator

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
