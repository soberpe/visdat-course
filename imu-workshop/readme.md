What movement you performed
Alle Bewegungen wurden einmal durchprobiert. Die Dateinamen sind als Kommentar im .py File hinterlegt
Das Handy wurde dabei bei jeder Bewegung bis auf Index Gravity flach am Tisch positioniert und verschoben. Bei Index Gravity wurde das Mobiltelefon auf Tischhöhe gehalten und ca 1-2 Sekunden nach Messbeginn rasch Richtung Boden bewegt. 
Zur Dokumentation wurde einfach die gerade Linie -> Index Linie verwendet.

Actual measured distance (if applicable)
Laut Maßband App (Iphone) ca 69cm pro Strecke. Also hin und zurück ca. 1,28m.

Reconstructed distance from your analysis
Aus den Plots lässt sich eine Distanz von ca. 65-69 cm ablesen. Die Berechnung der Trajektorienlänge ergibt 1,596m. Das ist vermutlich darauf zurückzuführen, da die Trajektorie keine Pfeilgerade Linie sonder etwas verzittert ist.

Key observations about drift and accuracy
Je schneller die Messung voran geht umso besser ist das Ergebnis. Anfangs habe ich ganz langsam ein L gezeichnet. Dabei ist allerdings eine fast gerade Linie enstanden. Das kommt daher da die Zeit quadratisch eingeht. Somit entsteht ein quadratischer Fehler. Dieser wird im anschluss noch 2 mal integriert und steigt somit weiter.

Challenges encountered and how you addressed them
Zuerst war die Challenge die richtige virtuelle Umgebung (myproject) aufzurufen da dort die notwendigen Pakete installiert sind. Anschließend ist ein die musste um die CSV Datei einlesen zu können die Bezeichnung Time auf timestamp umgeschrieben werden. Danach war noch ein Merge Fehler zu beheben weil die Zeitspalte ein Integer war und Toleranz als float definiert. Um den verzerrten 3D Plot zu bereinigen wurden noch automatische Achsenskalierungen hinzugefügt.