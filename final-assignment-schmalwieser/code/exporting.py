from __future__ import annotations
from pathlib import Path
import numpy as np
import imageio.v2 as imageio

def _ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def save_figure_png(fig, path: str | Path, dpi: int = 200):
    path = Path(path)
    _ensure_dir(path.parent)
    fig.savefig(path, dpi=dpi, bbox_inches="tight")

def save_gif(frames_rgb: list[np.ndarray], path: str | Path, fps: int = 30):
    path = Path(path)
    _ensure_dir(path.parent)
    imageio.mimsave(path, frames_rgb, fps=fps)
