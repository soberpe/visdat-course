
# Animation um automatisch den slider zu bewegen

from PyQt6.QtCore import Qt, QTimer

def run_animation(self):
    """Animate deformation by moving the slider automatically"""
    if not self.animation_checkbox.isChecked():
        return  # Animation wurde deaktiviert

    # Maximalwert des Sliders
    max_value = self.deform_slider.maximum()
    min_value = self.deform_slider.minimum()
    
    # Einfacher Slider von min → max → min
    step = 500  # Geschwindigkeit (höher = schneller)
    
    def animate():
        if not self.animation_checkbox.isChecked():
            return  # Stoppt, wenn Checkbox deaktiviert wird

        current = self.deform_slider.value()
        # Richtung umdrehen, wenn wir an den Grenzen sind
        if current >= max_value:
            self._animation_direction = -1
        elif current <= min_value:
            self._animation_direction = 1

        # Sliderwert aktualisieren
        self.deform_slider.setValue(current + self._animation_direction * step)

        # Wiederhole die Funktion nach kurzer Verzögerung
        QTimer.singleShot(5, animate)  

    # Startrichtung initialisieren
    self._animation_direction = 1
    animate()