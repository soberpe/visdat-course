
#erweitert um zwei Screenshots zu exportieren

import os
from PyQt6.QtWidgets import QFileDialog

def export_screenshot(self):
    """Save current view(s) as image(s)"""
    if not self.plotters or self.mesh is None:
        self.statusBar().showMessage("No mesh to export", 2000)
        return

    # Dialog zum Speichern
    filename, _ = QFileDialog.getSaveFileName(
        self,
        "Save Screenshot",
        "screenshot.png",
        "PNG Images (*.png);;JPEG Images (*.jpg);;All Files (*.*)"
    )

    if not filename:
        return

    # Prüfen, ob Extension angegeben ist
    base, ext = os.path.splitext(filename)
    if not ext:
        ext = ".png"

    try:
        # Alle Plotter speichern
        for i, plotter in enumerate(self.plotters, start=1):
            file_i = f"{base}_{i}{ext}" if len(self.plotters) > 1 else f"{base}{ext}"
            plotter.set_background("white")
            plotter.screenshot(file_i, transparent_background=False)

        self.statusBar().showMessage(f"Saved screenshots: {base}_1...{base}_{len(self.plotters)}", 3000)
    except Exception as e:
        self.statusBar().showMessage(f"Error saving screenshots: {str(e)}", 5000)