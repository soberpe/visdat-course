# IMU Motion Tracking Experiment

## Kurzbeschreibung

In diesem Experiment wurde die Bewegung eines mobilen Geräts mit seinen eingebauten IMU-Sensoren (Beschleunigungsmesser und Gyroskop) aufgezeichnet. Das Gerät wurde auf einer Fläche bewegt, um kurze Bewegungen durchzuführen, darunter auch ein schnelles Fahren eines Rechtecks (data_2). Die maximale Verschiebung betrug ca. 0,5 Meter. Die Analysepipeline bestand aus dem Laden und Filtern der CSV-Daten, Umrechnung der Gyroskopeinheiten, Orientierungsschätzung mittels Madgwick-Filter, Transformation der Beschleunigungen in den globalen Rahmen, Entfernung der Schwerkraft und numerischer Integration zur Positionsrekonstruktion.

Die rekonstruierte Trajektorie zeigt jedoch das Bewegungsmuster des Geräts. Bei schnellen Richtungswechseln, wie beim Rechteckfahren, treten Drift und kleine Integrationsfehler auf, sodass die Trajektorie nicht exakt den gefahrenen Weg abbildet und die Ecken abgerundet erscheinen.

Hauptgründe hierfür sind Drift und Sensorfehler. Kleine Offsets in Beschleunigungs- und Gyroskopsignalen summieren sich über die Zeit auf, sodass integrierte Positionen von der Realität abweichen. Die Filterung und Schwerkraftkorrektur reduzieren Rauschen, können aber die Drift nicht vollständig eliminieren. Kleine Fehler bei der Orientierungsschätzung können die Umrechnung der Beschleunigungen in den globalen Raum verfälschen.

Herausforderungen in diesem Experiment waren das Sensorrauschen, kleine Abweichungen in der Gyroskopmessung sowie die genaue Bestimmung der Schwerkraft. Diese Probleme wurden durch Tiefpassfilterung, Kontrolle der Gyroskop-Einheiten und die Mittelwertbildung während stationärer Perioden adressiert. Trotz dieser Maßnahmen bleibt die absolute Positionsgenauigkeit ohne externe Referenzen begrenzt.

Zur Verbesserung der Positionsrekonstruktion wurde ein Zero Velocity Update (ZUPT) eingesetzt. Dabei werden Phasen, in denen das Gerät nahezu stillsteht, erkannt und die Geschwindigkeit während dieser Perioden korrigiert. Dies reduziert Integrationsfehler und stabilisiert die Trajektorie, insbesondere bei Bewegungen mit Richtungswechseln, ohne externe Referenzen zu benötigen.

Dieses Experiment zeigt sowohl das Potenzial als auch die Grenzen der IMU-basierten Bewegungserfassung. Die Pipeline liefert einen strukturierten Ansatz, um Rohdaten in Trajektorien zu überführen, verdeutlicht aber die Bedeutung von Drift-Korrekturen wie ZUPT oder zusätzlichen Sensoren für exakte Rekonstruktionen.