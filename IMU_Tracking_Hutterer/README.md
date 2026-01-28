# Documentation motion-tracking-assignment

## What movement you performed
Für die Messung wurde eine einfache, kontrollierte lineare Bewegung durchgeführt. Das Smartphone wurde flach auf einer Tischplatte platziert und anschließend ungefähr 20 cm in positiver Y-Richtung verschoben. Die Bewegung erfolgte geradlinig, ohne bewusste Rotationen oder Neigungen. Zu Beginn und am Ende blieb das Gerät für mehrere Sekunden vollständig still, um Referenz- und Ruhephasen für Filterung und eventuelle Zero-Velocity-Techniken zu ermöglichen.

## Actual measured distance (if applicable)
Die Bewegung wurde überschlägig abgemessen und ergibt einen Weg von ca. 20cm in Y-Richtung.

## Reconstructed distance from your analysis
Ausgehend von den gefilterten Beschleunigungsdaten, der Orientierungskompensation und der zweifachen numerischen Integration wurde die Trajektorie rekonstruiert. Die rekonstruierte Strecke ergibt einen Wert von 0,247m also 24,7cm. Dies ist jedoch zu viel.
Das Ergebnis der 2D Trajektorie ergab:
   - X ist ca. 0,18m
   - Y ist ca. 0,123m

Das Ergebnis der 3D Trajektorie ergab:
   - X ist ca. 0,18m
   - Y ist ca. 0,123m
   - Z ist ca. 0,12m

Da die reale Bewegung nur in Y-Richtung stattfand, spiegeln die X- und Z-Abweichungen typische Integrationsdrift und leichte Fehler in der Orientierungsschätzung wider. Insgesamt liegt die rekonstruierte Strecke zwar im richtigen Größenbereich, zeigt jedoch klare systematische Drift in alle Richtungen.

## Key observations about drift and accuracy
Beschleunigungsdrift: Durch das zweifache Integrieren kleiner Rauschanteile entstehen deutliche Positionsfehler. Diese akkumulieren sich besonders, selbst wenn das Gerät in Wirklichkeit nur entlang einer Achse bewegt wurde.

Orientierungsrauschen: Kleine Fehler im Gyroskop führen über längere Zeit zu inkorrekten Rotationen, welche wiederum falsch transformierte Beschleunigungen erzeugen.

ZUPT zeigt deutliche Verbesserung: Das Beispiel zeigt, dass die Zero-Velocity-Korrektur die Drift extrem reduziert, jedoch stimmen dadurch die Längen der Bewegungen nicht mehr.

## Challenges encountered and how you addressed them
- Einheiten und Datenformate der Zeitwerte korrekt definieren für die korrekte funktionsweise.
- Mit Butterworth-Low-Pass-Filtern lassen sich das Rauschen und der Bias in der Beschleunigung reduzieren.
- Durch umstellen der Einheit des Gyroskops von deg/s in rad/s erhöht sich die Genauigkeit.
- Durch den ungenauen Sensor bekommt man eine künstliche Verschiebung in X- und Z-Richtung, welche im Zuge dieser Arbeit nicht verhindert werden konnte.
- Der Drift der Geschwindigkeit in Y-Richtung ergibt sich durch die Messungenauigkeiten und durch die Integration steigt dieser Drift.
- Durch diesen Effekt der numerischen Integration steigt auch der Drift beim Weg
- Die ZUPT "verschönert" das Signal, jedoch wird durch die Anwendung dieses auch der Weg, sodass dieser nicht mehr der Realität entspricht.

## Comparison between fast and slow movement
Hierbei ist klar ersichtlich, dass der Sensor im Smartphone sehr viel bessser für schnelle Bewegungen als für langsame Bewegungen geeignet ist. Hierbei ist der Drift-Effekt viel kleiner. Zudem stimmt die ZUPT sehr viel besser. Diese bewirkt, dass der Drift in Richtung X völlig verschwindet, jedoch erhält man einen Wegverlust für den Endwert der Messung in Richtung Y.

