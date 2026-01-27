from __future__ import annotations
import numpy as np

def mag_phase(H: np.ndarray):
    mag = np.abs(H)
    phase = np.unwrap(np.angle(H))
    return mag, phase
