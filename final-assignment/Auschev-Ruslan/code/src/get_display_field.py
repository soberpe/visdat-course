
# Funktion für die Bestimmung des anzuzeigenden Feldes

import numpy as np

def get_display_field(self, field_name):
    field_data = self.mesh.point_data[field_name]
    if field_data.ndim > 1 and field_data.shape[1] > 1:
        magnitude = np.linalg.norm(field_data, axis=1)
        mag_field_name = f"{field_name}_magnitude"
        self.mesh[mag_field_name] = magnitude
        return mag_field_name, f"{field_name} (Magnitude)"
    else:
        return field_name, field_name