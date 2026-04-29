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