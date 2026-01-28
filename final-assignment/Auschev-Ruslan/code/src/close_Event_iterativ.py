
#schließen von zwei plottern beim schließen des fensters

def closeEvent(self, event):
    """Clean up VTK resources before closing"""
    if self.plotters:
        for plotter in self.plotters:
            if plotter is not None:
                try:
                    plotter.close()   # PyVista QtInteractor Cleanup
                except Exception:
                    pass
    event.accept()