# Documentation Motion Tracking - [Oliver Straßl]

## Bewegungsbeschreibung

- Ca. zwei Sekunden in Ruhe am Anfang und Ende der Messung
- ein Vertikal gespiegeltes U
- horizontale Distanz ca. 0,4m
- vertikale Distanz ca. 0,5m
- Oszillierende während Zurücklegung Bewegung Kurvenbahn

## Entfernung der Bewegung
### Gemessene Entfernung
Ist aufgrund der Bewegung mit der Hand in der Luft und keinem passenden Messgerät nicht möglich gewesen.

### Berechnete Entfernung
Berechnet wurde eine Entfernung von **1.37 m**

## Beobachtungen (über Drift und Genauigkeit)
- Allgemein ist festzustellen, dass der Drift am Ende höher wird wenn die Messung länger dauert (>10 sek.)
- Die Genauigkeit ist in der X-& Y-Achse recht gut. Denn in der Abb.06 ist zu sehen, dass die Distanz in der XY Ebene sehr gut mit der gemessen Distanz (0,4m) zusammenpasst.
- Dem Gegenüber ist die Genauigkeit in der Z-Achse sehr schlecht. Diese Ungenauigkeit kann auf das Driften an der Z-Achse erklärt werden. Dies ist in der Abb.7 gut zu sehen, da sich der Endpunkt in Z-Achse -1.5m unter dem Anfangspunk befindet.
- Sehr interessant ist wie stark sich die Filterung (anhand Frequenz) auswirkt. Dies ist in Abb.09 sehr gut zu erkennen. Daher ist eine Filterung bis 10 Hz am besten geeignet, um die best passende Trajectorie zu bekommen.

## Herausforderungen und der Lösung
- Am Anfang bestand gleich die Herausforderung , dass das UNIX Zeitformat richtig verarbeitet werden muss.
- Zur Messung wird die Matlab Mobile App verwendet. Bei einer längeren Messung mit Hoher Abtastrate (100 Hz) werden die Messdaten als .m Dateiformat abgespeichert. Die Umwandlung in ein .csv Format war auch eine Herausforderung.