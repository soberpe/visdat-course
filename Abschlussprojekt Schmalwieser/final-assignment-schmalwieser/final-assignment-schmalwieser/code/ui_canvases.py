from __future__ import annotations

"""Matplotlib canvases embedded in a PyQt6 application."""

import matplotlib

# Use Qt backend for embedding into PyQt6.
matplotlib.use("QtAgg")

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class FRFCanvas(FigureCanvas):
    """Canvas showing FRF magnitude (top) and phase (bottom)."""

    def __init__(self):
        fig = Figure(figsize=(6, 4))
        self.ax_mag = fig.add_subplot(211)
        self.ax_ph = fig.add_subplot(212, sharex=self.ax_mag)
        super().__init__(fig)
