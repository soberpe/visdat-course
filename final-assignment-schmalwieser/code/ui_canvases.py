from __future__ import annotations

"""Matplotlib canvases embedded in a PyQt6 application."""

import matplotlib

# Use Qt backend for embedding into PyQt6.
matplotlib.use("QtAgg")

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import numpy as np


class FRFCanvas(FigureCanvas):
    """Canvas showing FRF magnitude (top) and phase (bottom)."""

    def __init__(self):
        fig = Figure(figsize=(6, 4))
        self.ax_mag = fig.add_subplot(211)
        self.ax_ph = fig.add_subplot(212, sharex=self.ax_mag)
        super().__init__(fig)


class Mode2DCanvas(FigureCanvas):
    """Canvas showing a static 2D mode shape (mean left/right per floor)."""

    def __init__(self):
        fig = Figure(figsize=(5, 4), constrained_layout=True)
        super().__init__(fig)
        self.ax = fig.add_subplot(111)

        # Floor definitions (normalized height)
        self.floor_y = np.array([0.0, 1.0/3.0, 2.0/3.0, 1.0], dtype=float)
        self.floor_labels = ["EG", "1. OG", "2. OG", "3. OG"]

        self.ax.set_xlabel("Verschiebung")
        self.ax.set_ylabel("Etage")

        # Disable default grid; we draw our own floor lines
        self.ax.grid(False)

    def plot_mode(self, z: np.ndarray, u: np.ndarray, title: str = "Mode shape (2D)") -> None:
        """Plot displacement u over height z."""
        self.ax.clear()

        # Plot mode curve
        self.ax.plot(u, z, marker="o")
        self.ax.axvline(0.0, linewidth=1, alpha=0.6)

        # --- Floor lines exactly at floor heights ---
        self.ax.grid(False)  # ensure matplotlib grid stays off
        for y in self.floor_y:
            self.ax.axhline(y, linewidth=1, alpha=0.25)

        # --- Label floors on y-axis ---
        self.ax.set_yticks(self.floor_y)
        self.ax.set_yticklabels(self.floor_labels)

        self.ax.set_xlabel("Verschiebung (normalisiert)")
        self.ax.set_ylabel("Etage")
        self.ax.set_title(title)

        # Symmetric x-limits
        umax = float(np.max(np.abs(u))) if np.size(u) else 1.0
        if umax <= 0:
            umax = 1.0
        self.ax.set_xlim(-1.1 * umax, 1.1 * umax)

        # Fixed normalized height range
        self.ax.set_ylim(-0.02, 1.02)

        self.draw()

