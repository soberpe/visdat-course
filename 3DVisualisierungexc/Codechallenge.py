import pyvista as pv
import numpy as np

# Stress Analyzer 

# class StressAnalyzer:
#     """Analyze stress distribution in a mesh"""
    
#     def __init__(self, mesh_file):
#         self.mesh = pv.read(mesh_file)
#         self.stress = self.mesh["S_Mises"]
    
#     def get_critical_regions(self, threshold):
#         """Return regions above threshold"""
# #         critical_indices = []
# #         for i in range(len(self.stress)):
# #             if self.stress[i] > threshold:
# #                 #größer > !!!!
# #                 critical_indices.append(i)
        


# for Schleife nicht ideal
# mask=self.stress > threshold
# critical_indices= np.where(mask)[0]





#         return critical_indices
    
#     def calculate_statistics(self):
#         """Calculate stress statistics"""
#         stats = {
#             'min': self.stress.min(),
#             'max': self.stress.max(),
#             'mean': self.stress.mean(),
#             'std': self.stress.std()
#         }
        
#         # Calculate safety factor (max allowable / actual)
#         max_allowable = 200.0  # MPa
#        # stats['safety_factor'] = self.stress.max() / max_allowable FALSCHE DEFINITION
#         stats["safety_factor"] = max_allowable / self.stress.max() 

#         return stats
    
#     def visualize_critical(self, threshold):
#         """Visualize only critical stress regions"""
#         indices = self.get_critical_regions(threshold)
        
#         # Create boolean mask
#         mask = np.zeros(len(self.stress), dtype=bool)
#         mask[indices] = True
        
#         # Extract critical mesh
#         critical = self.mesh.extract_points(mask)
        
#         # Visualize
#         pl = pv.Plotter()
#         pl.add_mesh(critical, scalars="S_Mises", cmap="Reds", scalar_bar_args={"title:"csdsf})
#         pl.add_scalar_bar(title="Critical Stress [MPa]")
#         pl.show()

# # Usage
# analyzer = StressAnalyzer("data/beam_stress.vtu")
# stats = analyzer.calculate_statistics()
# print(f"Safety factor: {stats["safety_factor"]:.2f}")  # Should be > 1.0 for safe!
# analyzer.visualize_critical(threshold=5.0)


#Mesh Comparison TOOL

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
    diff_mesh=mesh1.copy

    # Store in first mesh
    diff_mesh['difference'] = diff
    
    return diff_mesh

def visualize_comparison(original, modified):
    """Show original, modified, and difference side-by-side"""
    diff_mesh = find_differences(original, modified)
    
    pl = pv.Plotter(shape=(1, 3))
    
    # Original
    pl.subplot(0, 0)
    pl.add_mesh(original, scalars='S_Mises', cmap='coolwarm')
    pl.add_text('Original', font_size=10)
    
    # Modified  
    pl.subplot(0, 1)
    pl.add_mesh(modified, scalars='S_Mises', cmap='coolwarm')
    pl.add_text('Modified (20%)', font_size=10)
    
    # Difference
    pl.subplot(0, 2)
    pl.add_mesh(diff_mesh, scalars='difference', cmap='coolwarm')
    pl.add_text('Difference', font_size=10)
    
    pl.show()

# Load two versions
# original = load_and_process_mesh('data/beam_stress.vtu')
# modified = pv.read('data/beam_stress.vtu')

original = load_and_process_mesh('data/beam_stress.vtu')
modified = load_and_process_mesh('data/beam_stress.vtu')
modified['S_Mises'] *= 1.2



# Modify one mesh (simulate design change)
modified['S_Mises'] = modified['S_Mises'] * 1.2  # 20% increase

# Compare
visualize_comparison(original, modified)




#Stress Report Generator

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
                if s >= lower and s <= upper:
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
            z == bounds[4] or z == bounds[5]
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
            mask = (stress >= lower) & (stress <= upper)
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