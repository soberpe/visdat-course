# Aktualisierung der Skalarleiste nach Deformation

def update_scalar_bar(self):
    if self.mesh is None:
        return

    # Actor bewusst neu aufbauen
    self.deformed_actor = None
    self.display_mesh()