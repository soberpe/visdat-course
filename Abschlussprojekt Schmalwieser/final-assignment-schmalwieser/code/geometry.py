from __future__ import annotations
import numpy as np

def building_points_16(width: float = 1.0, depth: float = 0.6, height: float = 1.0) -> np.ndarray:
    """Return a simple 4-floor, 4-corner 'high-rise' stick model (16 nodes).

    Node order is *floor-wise* from bottom to top to make 'the lowest 4 nodes' easy to address:

        Floor 0 (ground, z=0):  indices 0..3  (fixed in the visualization)
        Floor 1 (z=h/3):        indices 4..7
        Floor 2 (z=2h/3):       indices 8..11
        Floor 3 (roof, z=h):    indices 12..15

    On each floor the 4 corner nodes are ordered:
        0: front-left   (-x, yF)
        1: front-right  (+x, yF)
        2: back-right   (+x, yB)
        3: back-left    (-x, yB)

    Parameters
    ----------
    width:
        Building width in x-direction.
    depth:
        Building depth in y-direction.
    height:
        Total height in z-direction.
    """
    xL, xR = -0.5 * float(width), 0.5 * float(width)
    yF, yB = 0.0, float(depth)

    z0 = 0.0
    z1 = float(height) / 3.0
    z2 = 2.0 * float(height) / 3.0
    z3 = float(height)

    floors = []
    for z in (z0, z1, z2, z3):
        floors.append(np.array([
            [xL, yF, z],  # front-left
            [xR, yF, z],  # front-right
            [xR, yB, z],  # back-right
            [xL, yB, z],  # back-left
        ], dtype=float))

    return np.vstack(floors)

def building_edges_16() -> list[tuple[int, int]]:
    """Edges for the 16-node frame: perimeter on each floor + vertical columns."""
    edges: list[tuple[int, int]] = []

    # Perimeter edges on each floor
    for floor in range(4):
        o = 4 * floor
        edges += [
            (o+0, o+1),
            (o+1, o+2),
            (o+2, o+3),
            (o+3, o+0),
        ]

    # Vertical edges (columns) connecting floors
    for corner in range(4):
        edges += [
            (0*4 + corner, 1*4 + corner),
            (1*4 + corner, 2*4 + corner),
            (2*4 + corner, 3*4 + corner),
        ]

    return edges

def fixed_ground_indices() -> np.ndarray:
    """Indices of the fixed ground-floor nodes (0..3)."""
    return np.array([0, 1, 2, 3], dtype=int)
