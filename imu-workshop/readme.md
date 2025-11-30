What movement you performed
Das Telefon wurde L-Färmig bewegt. 50cm nach rechts (X-Richtung), 40cm (Unterkante Handy, bis Oberkante Handy) cm nach oben (Y-Richtung). Die Eigentlich BEwegung des Beschleunigsungssensors im Telefon entsprich unter BErücksichtung der Abmessungen des Teelfons also ca. 45 cm nach rechts und 25 cm nach oben.

Actual measured distance (if applicable)
Die Bewegung wurde manuell am Tisch durchgeführt und 50 cm in X-Richtung und 40 cm in Y-Richtung
Die Gesamtdistanz des L-Pfades liegt also real bei ungefähr 90 cm.

Reconstructed distance from your analysis
Die Rekonstruktion erfolgte durch Low-Pass-Filterung der Beschleunigung, Orientierungskorrektur via Madgwick-Filter, Umrechnung in globale Koordinaten, Doppelte numerische Integration und abschliessend mit Zero-Velocity-Update (ZUPT)

Ohne ZUPT:

Die reine doppelte Integration (2D-Plot „Trajectory Without ZUPT“):
Grundsätzlihc ist auch Ohne ZUpt die L-Förmige bewegung erkennbar, allerdings zeicht nach Stillstand des HAndys eine Diagonale Bewegung nach X und -Y. 
Durch das wegschneiden der Stillstände (ZUPT) ist in der Trajekttorie sehr gut die reine L-Förmige bewegung zu erkennen.

Sowohlt Mit als auch Ohen Zupt sind allerdings deutliche drifts zu erkennen. In X Richtung Driftet der Weg 4cm nach unten, in Y.Richtung 2-3 nach Rechts. 
die Berechneten Distanzen stimmen allerdings gut mit der Tatsächlcihen BEwegung über ein.
in X-Richtung ergab sich en Wert von 47cm in Y Richtung ein Wert von 20 cm.


Key observations about drift and accuracy
Bereits durch eine KLeinen BIas im Gyroskop entstehen durch die Zweifache Integration starke Drifts am Weg. 
Die Geschwindigkeit der BEwegung hat starken einfluss, bei Langsamer BEwegung steigt der Fehler Quadratisch mit der Zeit. 


Challenges encountered and how you addressed them
Phython Module wie ahrs und glob wurden anfangs nciht gefunden.
Arbeiten im Falschen Dateipfad.
Namensgebung in den CSV Files anders. 