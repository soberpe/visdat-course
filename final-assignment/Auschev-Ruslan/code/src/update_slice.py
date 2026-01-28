
# Slicer wird aktualisiert
# Diese Funktion zeigt einen Schnitt des Meshs entlang der ausgewählten Achse an.
# Wenn kein Schnitt ausgewählt ist, wird das gesamte Mesh angezeigt.
# Der Plotter wird mit dem neuen Schnitt-Mesh aktualisiert.

def update_slice(self):
    """Display a slice of the mesh along the selected axis"""
    if self.mesh is None or not self.slice_checkbox.isChecked():
        self.display_mesh()
        return

    axis = self.slice_axis_combo.currentText().upper()
    pos_percent = self.slice_slider.value() / 100.0
    bounds = self.mesh.bounds

    if axis == "X":
        pos = bounds[0] + pos_percent * (bounds[1] - bounds[0])
        slice_mesh = self.mesh.slice(normal=[1, 0, 0], origin=[pos, 0, 0])
    elif axis == "Y":
        pos = bounds[2] + pos_percent * (bounds[3] - bounds[2])
        slice_mesh = self.mesh.slice(normal=[0, 1, 0], origin=[0, pos, 0])
    else:  # Z
        pos = bounds[4] + pos_percent * (bounds[5] - bounds[4])
        slice_mesh = self.mesh.slice(normal=[0, 0, 1], origin=[0, 0, pos])

    # **Check for empty mesh**
    if slice_mesh.n_points == 0:
        # Warnung ausgeben und Original-Mesh anzeigen
        self.statusBar().showMessage("Slice erzeugt leeres Mesh – verschiebe den Slider.", 3000)
        self.display_mesh()
        return

    # Plotter aktualisieren
    for plotter in self.plotters:
        plotter.clear()
        plotter.add_mesh(
            slice_mesh,
            scalars=self.field_combo.currentText() if self.field_combo.currentText() != "(No Field)" else None,
            cmap='coolwarm',
            show_edges=self.edges_checkbox.isChecked(),
            show_scalar_bar=self.scalar_bar_checkbox.isChecked()
        )

        if self.show_undeformed_checkbox.isChecked() and self.original_mesh is not None:
            plotter.add_mesh(
                self.original_mesh,
                color='black',
                style='wireframe',
                line_width=1
            )
        plotter.reset_camera()