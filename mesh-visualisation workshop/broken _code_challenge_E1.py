import pyvista as pv
import numpy as np

class StressAnalyzer:
    """Analyze stress distribution in a mesh"""
    
    def __init__(self, mesh_file):
        self.mesh = pv.read(mesh_file)
        self.stress = self.mesh['S_Mises']
    
    def get_critical_regions(self, threshold):
        """Return regions above threshold"""
        mask=self.stress > threshold
        critical_indices = np.where(mask)[0]

        #for i in range(len(self.stress)):           #For-Schleife über alle elemente dinglichst vermeiden!
            #if self.stress[i] > threshold:          #Falsches Zeichen
                #critical_indices.append(i)
        
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
        stats['safety_factor'] = max_allowable /self.stress.max()              #Zähler und nenner vertauschen
        
        return stats
    
    def visualize_critical(self, threshold):
        """Visualize only critical stress regions"""
        indices = self.get_critical_regions(threshold)
        
        # Create boolean mask
        mask = np.zeros(len(self.stress), dtype=bool)
        mask[indices] = True
        
        # Extract critical mesh
        critical = self.mesh.extract_points(mask,include_cells=True)
        
        # Visualize
        pl = pv.Plotter()
        pl.add_mesh(critical, scalars="S_Mises", cmap="Reds",scalar_bar_args={'title':"Critical Stress [MPa]"})
       
        pl.add_mesh(self.mesh, scalars="S_Mises",opacity=0.3, cmap="Reds",show_scalar_bar=False)
        pl.show()

# Usage
analyzer = StressAnalyzer('data/beam_stress.vtu')
stats = analyzer.calculate_statistics()
print(f"Safety factor: {stats['safety_factor']:.2f}")  # Should be > 1.0 for safe!
analyzer.visualize_critical(threshold=2.0)