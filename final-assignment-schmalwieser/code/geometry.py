from __future__ import annotations
import numpy as np

def building_points_16(width: float = 0.5, depth: float | None = None, height: float = 1.0) -> np.ndarray:
    """Create the 16-node 'high-rise' used in this assignment.

    The model consists of TWO identical vertical frames (front & back) to create a 3D impression.
    Only the FRONT frame represents measurement locations. The BACK frame is for visualization only.

    Node numbering (1-based in the assignment) is:

        FRONT frame (y = 0):
            Level 3 (top):      1 (left),  2 (right)
            Level 2:            3 (left),  4 (right)
            Level 1:            5 (left),  6 (right)
            Level 0 (ground):   7 (left),  8 (right)   <-- fixed / EG

        BACK frame (y = depth):
            Level 3 (top):      9 (left), 10 (right)
            Level 2:           11 (left), 12 (right)
            Level 1:           13 (left), 14 (right)
            Level 0 (ground):  15 (left), 16 (right)  <-- fixed / EG

    Internally we use 0-based indices. Therefore:
        1 -> 0, 2 -> 1, ..., 16 -> 15.

    Parameters
    ----------
    width:
        Building width (x-direction). The building is rendered *square* in plan view by default.
    depth:
        Distance between front and back frame (y-direction). If None, depth == width.
    height:
        Total height (z-direction).
    """
    width = float(width)
    depth = float(width if depth is None else depth)
    height = float(height)

    xL, xR = -0.5 * width, 0.5 * width
    yF, yB = 0.0, depth

    # 4 levels: ground + 3 upper levels
    z_levels = np.linspace(0.0, height, 4)  # [0, h/3, 2h/3, h]
    # Assignment lists from TOP to BOTTOM (1-2, 3-4, 5-6, 7-8)
    z_top_to_bottom = z_levels[::-1]

    pts = []

    # Front frame (8 nodes)
    for z in z_top_to_bottom:
        pts.append([xL, yF, z])  # left
        pts.append([xR, yF, z])  # right

    # Back frame (8 nodes)
    for z in z_top_to_bottom:
        pts.append([xL, yB, z])  # left
        pts.append([xR, yB, z])  # right

    return np.asarray(pts, dtype=float)

def building_edges_16() -> list[tuple[int, int]]:
    """Edges for the 16-node model.

    - Horizontal beams (left-right) on each level for front and back frame.
    - Vertical columns connecting levels for front and back frame.
    - Connectors between front and back frame (left-left and right-right) on each level.
    """
    edges: list[tuple[int, int]] = []

    # Helper to add beams/columns in an 8-node frame (indices start at base)
    def add_frame_edges(base: int) -> None:
        # Horizontal beams: (0-1), (2-3), (4-5), (6-7)
        edges.extend([(base+0, base+1), (base+2, base+3), (base+4, base+5), (base+6, base+7)])
        # Vertical columns left: 0-2-4-6 ; right: 1-3-5-7
        edges.extend([(base+0, base+2), (base+2, base+4), (base+4, base+6)])
        edges.extend([(base+1, base+3), (base+3, base+5), (base+5, base+7)])

    # Front frame: 0..7 ; Back frame: 8..15
    add_frame_edges(0)
    add_frame_edges(8)

    # Connectors between frames on each level (left-left and right-right)
    for lvl in range(4):  # 0..3 top-to-bottom
        oF = 2 * lvl
        oB = 8 + 2 * lvl
        edges.extend([(oF+0, oB+0), (oF+1, oB+1)])

    return edges

def fixed_ground_indices() -> np.ndarray:
    """Fixed ground nodes (EG): 7,8,15,16 in 1-based numbering."""
    return np.asarray([6, 7, 14, 15], dtype=int)
