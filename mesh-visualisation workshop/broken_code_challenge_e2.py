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

    diff_ = mesh1.copy()
    data1 = mesh1[field]
    data2 = mesh2[field]
    
    # Calculate difference
    #diff = data1 - data2
    
    # Store in first mesh
    diff_['difference'] = data1 - data2
    return diff_

def visualize_comparison(original, modified):
    """Show original, modified, and difference side-by-side"""
    diff_mesh = find_differences(original, modified)
    
    pl = pv.Plotter(shape=(1, 3))
    
    # Original
    pl.subplot(0, 0)
    pl.add_mesh(original, scalars='S_Mises',show_scalar_bar='S_Mises', cmap='coolwarm')
    pl.add_text('Original', font_size=10)
    
    # Modified  
    pl.subplot(0, 1)
    pl.add_mesh(modified, scalars='S_Mises',show_scalar_bar='S_Mises', cmap='coolwarm')
    pl.add_text('Modified', font_size=10)
    
    # Difference
    pl.subplot(0, 2)
    pl.add_mesh(diff_mesh, scalars='difference', cmap='coolwarm')
    pl.add_text('Difference', font_size=10)
    
    pl.show()


#Eigentliches Programm
# Load two versions
original = load_and_process_mesh('data/beam_stress.vtu')
modified = load_and_process_mesh('data/beam_stress.vtu')

# Modify one mesh (simulate design change)
modified['S_Mises'] = modified['S_Mises'] * 1.2  # 20% increase

# Compare
visualize_comparison(original, modified)

print(original.array_names)
print(modified.array_names)
