from __future__ import annotations
import numpy as np

def building_points_12(depth: float = 0.6) -> np.ndarray:
    """12 points: 6 front + 6 back (same pattern), on 3 levels."""
    xL, xR = -0.5, 0.5
    yF, yB = 0.0, float(depth)
    zT, zM, zB = 1.0, 0.5, 0.0

    front = np.array([
        [xL, yF, zT], [xR, yF, zT],
        [xL, yF, zM], [xR, yF, zM],
        [xL, yF, zB], [xR, yF, zB],
    ], dtype=float)

    back = np.array([
        [xL, yB, zT], [xR, yB, zT],
        [xL, yB, zM], [xR, yB, zM],
        [xL, yB, zB], [xR, yB, zB],
    ], dtype=float)

    return np.vstack([front, back])

def building_edges_12() -> list[tuple[int, int]]:
    edges: list[tuple[int,int]] = []

    def face(o: int) -> list[tuple[int,int]]:
        return [
            (o+0, o+2), (o+2, o+4),
            (o+1, o+3), (o+3, o+5),
            (o+0, o+1),
            (o+2, o+3),
            (o+4, o+5),
        ]

    edges += face(0)
    edges += face(6)

    for i in range(6):
        edges.append((i, i+6))

    return edges
