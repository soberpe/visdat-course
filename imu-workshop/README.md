# Aufzeichnung und Analyse der Smartphone-Bewegung

## Versuchsbeschreibung
Mithilfe der MATLAB Mobile App wurden die Bewegungen (Beschleunigungen in die drei Raumrichtungen und Winkelgeschwindigkeiten um die drei Raumachsen) aufgezeichnet. Ausgeführt wurde eine lineare Hin- und Herbewegung auf einem Tisch. Der Weg betrug dabei ca. 80 cm hin und 80 cm her. Die Verschiebungsrichtung stellt die x-Richtung dar.

## Rekonstruktion der Bewegung
Die Exprotierten Daten wurde in diesem Workshop eingelesenen, gefiltert (Tiefpassfilter) und geplottet. Von den Beschleunigungen wurden die Geschwinigkeiten und die Position mithilfe einer (zweifachen) Integration berechnet. Diese wurden im 2D und 3D Plot dargetellt. Es wurden Verschiebungen von ~ 0,4 Meter bestimmt. Die Verschiebungen der einzelnen Richtungen sollten am Ende der Aufzeichnung 0 betragen da der Ausgangspunkt wieder erreicht wurde. In X-Richtung beträgt sie -0,045, in  Y-Rcihtung 0,393 und in Z-Richtung -0,105. 

## Filterung
Die Filterung hat gut funktioniert. Hohe Frequenzen wurden deutlich sichtbar herausgenommen. Die Kurve ist glätter.

## Beobachtungen zu Drift und Genauigkeit
Betrachtet man die Plots erkennt man, dass die scheinbar positive geringe Abweichung in X-Richtung, schlicht weg einfach an den so kleinen Werten liegt. Die Verschiebung um 80 cm hin und 80 cm weg wurden gar nicht detektiert. Die Verschiebungen während der Messung in den anderen Raumrichtungen ist hingegen bei weitem Größer. Das lässt zu, diese Messung als ziemlich ungenau zu deklarieren. 

Die Werte für die y und z richtung Driften ab, obwohl gar keine Beschleunigung in diese Richtung stattgefunden hat.
Zu beginn der Messung, und auch am Ende ändern dich die Werte jedoch nicht wirklich. in der Ruhe sollte das System demnach nur wenig Drift haben.

## Fazit
Mir ist der Nutzen des Madgwick filters noch nicht ganz klar. Außerdem hab ich nicht vertanden für was die Winkelgeschwindigkeiten einen Mehrwert bilden. Kann ich nicht rein aus den Beschleunigungen die Geschwindigkeiten und Demnach auch die Position bestimmen.

## Anmerkung
Hab in der Vorleung (25.11) aufgrund einer wichtigen Veranstaltung meiner alten Hochschule gefehlt.