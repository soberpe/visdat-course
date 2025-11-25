# Aufzeichnung und Analyse der Smartphone-Bewegung

## Versuchsbeschreibung
In diesem Experiment wurde die Bewegung eines Smartphones mithilfe der MATLAB Mobile App aufgezeichnet. Das Gerät wurde in der Hand gehalten und auf einer ebenen Oberfläche eine U-förmige Bewegung ausgeführt. Der Bewegungsablauf bestand aus einem vertikalen Abwärtspfad von etwa 40 cm, einer horizontalen Verschiebung von circa 30 cm und einem anschließenden vertikalen Aufwärtspfad über weitere 40 cm.

## Rekonstruktion der Bewegung
Durch die Analyse der vom Beschleunigungssensor erfassten Daten konnte die Bewegung rekonstruiert werden. Nach Integration der Beschleunigungswerte über die Zeit ergaben sich rekonstruierte Distanzen von ungefähr 35 cm für den vertikalen Abwärtspfad, 30 cm für die horizontale Verschiebung und 50 cm für den vertikalen Aufwärtspfad.Aufgund von Vibrationen sowie auch des Drücken des Start sowie auch des End-Buttons am Smartphone wurde eine Beschleunigugn in Z-Richtung auch aufgenommen. Deswegen wurde eine Distanz auch abweichend zur Realität eine Distanz in Z-Richtung rekonstruiert.
## Beobachtungen zu Drift und Genauigkeit
Die Ergebnisse zeigen, dass die Rekonstruktion nicht exakt den gemessenen Distanzen entspricht. Dies ist hauptsächlich auf Drift und Rauschen der Sensordaten zurückzuführen. Kleine Fehler im Beschleunigungssignal summieren sich bei der Integration schnell auf, was insbesondere bei der letzten vertikalen Bewegung deutlich wird. Trotz dieser Abweichungen konnte die grobe U-Form der Bewegung klar erkannt werden.

## Herausforderungen und Lösungsansätze
Eine der größten Herausforderungen war die Minimierung von Rauschen und Drift. Um die Genauigkeit zu verbessern, wurden die Daten vor der Integration geglättet. Weiters wurde auch der Sensor kalibriert. Außerdem war es schwierig, das Smartphone exakt auf einer geraden Linie zu bewegen, wodurch kleine Schwankungen in den Messwerten entstanden. Weiters wurde noch eine Zero-Velocity-Update implementiert.


## Fazit
Insgesamt zeigt das Experiment, dass eine grobe Rekonstruktion der Smartphone-Bewegung möglich ist, während exakte Distanzen durch Sensorrauschen und Drift eingeschränkt werden. Die Analyse liefert wertvolle Einblicke in die Dynamik der Bewegung und die Grenzen der Messgenauigkeit mobiler Beschleunigungssensoren.
