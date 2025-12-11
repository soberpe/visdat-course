import pyvista as pv
import numpy as np

def load_and_process_mesh(filename):
    mesh = pv.read(filename)
    stress = mesh['S_Mises']
    normalized = (stress - stress.min()) / (stress.max() - stress.min())
    mesh['normalized_stress'] = normalized
    return mesh

def find_differences(mesh1, mesh2, field='S_Mises'):
    result = mesh1.copy()
    diff = mesh1[field] - mesh2[field]
    result['difference'] = diff
    return result

def visualize_comparison(original, modified):
    diff_mesh = find_differences(original, modified)
    
    pl = pv.Plotter(shape=(1, 3))

    pl.subplot(0, 0)
    pl.add_mesh(original, scalars='S_Mises', cmap='viridis')
    pl.add_text('Original')

    pl.subplot(0, 1)
    pl.add_mesh(modified, scalars='S_Mises', cmap='viridis')
    pl.add_text('Modified')

    pl.subplot(0, 2)
    pl.add_mesh(diff_mesh, scalars='difference', cmap='coolwarm')
    pl.add_text('Difference')

    pl.show()

original = load_and_process_mesh('data/beam_stress.vtu')
modified = pv.read('data/beam_stress.vtu')
modified['S_Mises'] = modified['S_Mises'] * 5

visualize_comparison(original, modified)
