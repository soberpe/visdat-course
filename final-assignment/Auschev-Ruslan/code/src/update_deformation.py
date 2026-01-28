
# wurde verändert um Deformationen von zwei plotter zu aktualisieren

import numpy as np

def update_deformation(self):
    """Apply deformation to mesh for all plotters"""
    if self.mesh is None or not self.deform_checkbox.isChecked():
        # Restore original if not deforming
        if self.original_mesh is not None:
            self.mesh = self.original_mesh.copy()
        self.display_mesh()
        return

    # Find displacement field (common names)
    displacement_field = None
    for field_name in ['U', 'Displacement', 'displacement', 'DISPL']:
        if field_name in self.mesh.point_data:
            displacement_field = field_name
            break

    if displacement_field is None:
        self.statusBar().showMessage("No displacement field found", 3000)
        self.deform_checkbox.setChecked(False)
        return

    # Scale factor from slider
    scale = self.deform_slider.value() / 10.0
    self.deform_label.setText(f"{scale:.1f}x")

    # Store original if not already stored
    if self.original_mesh is None:
        self.original_mesh = self.mesh.copy()

    # Apply deformation
    displacement = self.mesh.point_data[displacement_field]

    # Ensure 3D displacement
    if displacement.shape[1] == 2:
        displacement = np.hstack([displacement, np.zeros((displacement.shape[0], 1))])

    deformed_points = self.original_mesh.points + scale * displacement
    self.mesh.points = deformed_points

    # Update all plotters
    if self.deformed_actors:
        for deformed_actor, plotter in zip(self.deformed_actors, self.plotters):
            deformed_actor.GetMapper().SetInputData(self.mesh)
            plotter.render()
    else:
        # Fallback beim ersten Mal
        self.display_mesh()