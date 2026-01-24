from __future__ import annotations
import numpy as np

def default_points_xyz() -> np.ndarray:
    """6 points: top-left(1), top-right(2), mid-left(3), mid-right(4), bot-left(5), bot-right(6)"""
    xL, xR = -0.5, 0.5
    y = 0.0
    z_top, z_mid, z_bot = 1.0, 0.5, 0.0
    pts = np.array([
        [xL, y, z_top],  # 1
        [xR, y, z_top],  # 2
        [xL, y, z_mid],  # 3
        [xR, y, z_mid],  # 4
        [xL, y, z_bot],  # 5
        [xR, y, z_bot],  # 6
    ], dtype=float)
    return pts

def stick_lines() -> list[tuple[int,int]]:
    """Connectivity for a simple frame."""
    return [
        (0,2),(2,4),  # left column 1-3-5
        (1,3),(3,5),  # right column 2-4-6
        (0,1),        # top beam
        (2,3),        # mid beam
        (4,5),        # bottom beam
    ]
