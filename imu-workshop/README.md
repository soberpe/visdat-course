Bewegung: Eine L-förmige Bewegung mit Anfangspunkt "links oben" zu Endpunkt "links unten" wobei die Bewegung nur in der X-Y-Ebene stattgefunden hat. 
Keine Bewegung in der Z-Richtung!
Diese L-Form wird zügig durchfahren (Zeit max. 3s).
Der durchfahrene Weg beträgt ca. 40-45cm.

Rekonstruierte Distanz: Aus Bild "08_zupt_comparison" lässt sich der zurückgelegte Weg rekonstruieren. Dabei wird das "zero velocity update" herangezogen, da diese Bewegung deutlich näher an der Realität ist als die ohne "zero velocity update" rekonstruierte Trajectorie. 
Somit lässt sich ein Weg von ca. 38cm rekonstruieren. 
Diese Rekonstruktion ist plausibel, da auch die "reale" Bewegung nicht genau abgemessen wurde (nur Schätzung des zurückgelegten Weges)

Beobachtungen bezüglich Genauigkeit und Drift:
Die Rohsensordaten sowie die gefilterten Sensordaten sind sehr sauber und mit wenig Rauschen dargestellt.

Geschwindigkeit: Zu Beginn der Messung ist das Smartphone in Ruhe. Sobald die erste Bewegung stattfindet, wird ein minimaler Drift beobachtet. Als sich das Smartphone am Ende der Messung ebenfalls wieder in Ruhelage befindet, kann ein deutlicher Drift (sehr deutlicher Unterschied zur Anfangsruhelage) beobachtet werden.

Trajectorien: 
Sowohl die 2D (ohne zupt) als auch 3D Trajectorien sind sehr ungenau und stimmen mit der real durchgeführten Bewegung nicht überein.
    2D: nur die Anfangsbewegung (vertikal nach unten) ist erkennbar, der restliche Trajectorienteil stimmt keinesfalls mit der real durchgeführten Bewegung nicht überein
    3D: hier kommt zusätzlich noch der Drift bzw. die Ungenauigkeit der Messung in Spiel. Dies Verursacht eine Trajectorie in Z-Richtung die in Wirklichkeit aber sehr viel kleiner ist (Tisch neigt sich maximal einige Millimieter nach unten; keine cm!) 
Mit zupt: diese Darstellung entspricht schon sehr der Realität!

Challenges: Achtung auf die Bezeichnungen der Spalten und Zeilen in Excel vergleich zu Python-Programmcode.
            Achtung auf die verwendeten Einheiten bzw. die automatische persönliche Annahme dieser Einheiten.
            Entscheidend ist auch die sinnvolle Filterung der Daten zu deren Weiterverarbeitung.