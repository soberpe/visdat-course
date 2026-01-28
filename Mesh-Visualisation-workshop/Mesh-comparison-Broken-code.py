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
    diff_mesh = mesh1.copy()  # Kopie, damit mesh1 nicht verändert wird
    data1 = mesh1[field]
    data2 = mesh2[field]
    
    # Calculate difference
    diff = data1 - data2
    
    # Store in first mesh
    diff_mesh['difference'] = diff
    
    return diff_mesh

def visualize_comparison(original, modified):
    """Show original, modified, and difference side-by-side"""
    diff_mesh = find_differences(original, modified, field='S_Mises')
    
    pl = pv.Plotter(shape=(1, 3))
    
    # Original
    pl.subplot(0, 0)
    pl.add_mesh(original, 
                scalars='S_Mises', 
                cmap='coolwarm', 
                show_scalar_bar=True, 
                scalar_bar_args={"title": "Mieses Spg Mesh1"},)
    pl.add_text('Original', font_size=10)
    
    # Modified  
    pl.subplot(0, 1)
    pl.add_mesh(modified, 
                scalars='S_Mises', 
                cmap='coolwarm',
                show_scalar_bar=True, 
                scalar_bar_args={"title": "Mieses Spg Mesh2"},)
    pl.add_text('Modified (20% increase)', font_size=10)
    
    # Difference
    pl.subplot(0, 2)
    pl.add_mesh(diff_mesh, 
                scalars='difference', 
                cmap='coolwarm',
                show_scalar_bar=True, 
                scalar_bar_args={"title": "Mieses Spg Difference"},)
    pl.add_text('Difference', font_size=10)
    
    pl.show()

# Load two versions
original = load_and_process_mesh('data/beam_stress.vtu')
#modified = pv.read('data/beam_stress.vtu')
modified = load_and_process_mesh('data/beam_stress.vtu')

# Modify one mesh (simulate design change)
modified['S_Mises'] = modified['S_Mises'] * 1.2  # 20% increase

print(original['S_Mises'].max())
print(modified['S_Mises'].max())
# → modified max sollte ~ 1.2 * original max sein

#Überprüfen der Array namen
print("Original arrays:", original.array_names)
print("Modified arrays:", modified.array_names)

diff_mesh = find_differences(original, modified)
print("Diff-mesh arrays:", diff_mesh.array_names)

print("original is diff_mesh:", original is diff_mesh)  # sollte True sein


# Compare
visualize_comparison(original, modified)