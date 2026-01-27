from __future__ import annotations
import numpy as np
import pyvista as pv

def build_frame(points_xyz: np.ndarray, edges: list[tuple[int,int]]) -> pv.PolyData:
    poly = pv.PolyData(points_xyz)
    lines = []
    for a,b in edges:
        lines += [2, a, b]
    poly.lines = np.array(lines, dtype=np.int64)
    return poly

def deform(points_xyz: np.ndarray, v_complex: np.ndarray, direction: np.ndarray, t: float, omega: float, scale: float) -> np.ndarray:
    """Animate points along 'direction' with complex amplitudes v_complex."""
    direction = direction / (np.linalg.norm(direction) + 1e-12)
    disp = scale * np.real(v_complex * np.exp(1j * omega * t))  # (N,)
    return points_xyz + disp[:,None] * direction[None,:]
