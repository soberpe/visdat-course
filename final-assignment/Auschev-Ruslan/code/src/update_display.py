
# hier wurde die Funktion erweitert, um die Anzeigeoptionen zu aktualisieren

def update_display_options(self):
    if not self.deformed_actors or not self.plotters:
        return

    for actor in self.deformed_actors:
        if actor is None:
            continue
        prop = actor.GetProperty()
        if self.edges_checkbox.isChecked():
            prop.EdgeVisibilityOn()
        else:
            prop.EdgeVisibilityOff()

    # Render für alle Plotter
    for plotter in self.plotters:
        plotter.render()