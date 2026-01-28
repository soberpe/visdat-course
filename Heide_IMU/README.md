IMU Motion Tracking

#1 Bewegung
Ich habe das Handy rechts an meinen Laptop, Kante an Kante gelegt. Die obere Kante vom Handy war auf einer Linie mit der oberen Kante vom Laptop. 
Nach ca. 5 Sekunden habe ich angefangen, das Handy im Uhrzeigersinn um den Laptop zu bewegen, während die Kante des Handys immer in Berührung mit der Kante des Laptops war.
Sobald das Handy an der linken Kante oben angekommen ist, wurde das Handy wieder den selben Weg zurück bewegt bist zum Startpunkt der Messung.

#2 Gemessene Distanz
Durch einen Messfehler wurde dauerhaft eine Beschleunigung in X- und Y-Richtung aufgenommen. Bei Intergration resultiert dies in einen Drift in der Geschwindigkeit.
Man könnte einen Offset festlegen, was ich auch gemacht habe, jedoch variiert der Offset über den Verlauf der Messung. Daher reicht es nicht aus den Mittelwert am Ende und Anfang zu berechnen. Den Mittelwert in der Mitte zu berechnen würde nicht helfen, da dort ja tatsächlich Beschleunigungen aufgebracht wurden.

#3 Rekonstruierte Distanz
s. #2

#4 Beobachtungen zu Drift und Genauigkeit
Die Geschwindigkeit in X-Richtung steigt mit der Zeit bist auf 0.25 m/s, aufgrund der Beschreibung in #2.
Die Geschwindigkeit in Y-Richtung steigt mit der Zeit bist auf -0.5 m/s, aufgrund der Beschreibung in #2.
Die Geschwindigkeit in Z-Richtung steigt mit der Zeit bist auf 0.025 m/s, aufgrund der Beschreibung in #2.
Die Trajektorien sind aufgrund dieser Beobachtungen ebenfalls stark abgedriftet
Die Orientierung in Yaw, also in der X-Y-Ebene wurde gut aufgezeichnet und man die Winkelveränderungen des Handys gut erkennen.

#5 Schwierigkeiten und deren Lösung
Ich habe einen Offset für X- und Y-Richtung anhand berechnet, indem ich den Ruhestand in den ersten und letzten 3 Sekunden der Messung gemittelt habe. Diesen habe ich dann von der gefilterten Beschleunigung abgezogen. In den Graphen konnte ich beobachten, dass die Beschleunigung bei ruhendem Sensor auf der x-Achse lag, bzw. 0 war. Allerdings sind die Geschwindigkeiten und Trajektorien trotzdem abgedriftet. Es liegt nahe, dass die Problematik mit dem Mittelwert aus #2 der Grund dafür ist.

Offset in X-Richtung: +0,155054781
Offset in Y-Richtung: -0,310827177 

Durch die berechneten Offsets konnte ich in den Graphen beobachten, dass die Beschleunigung bei ruhendem Sensor auf der x-Achse lag, bzw. 0 war. Allerdings sind die Geschwindigkeiten und Trajektorien trotzdem abgedriftet. Es liegt nahe, dass die Problematik mit dem Mittelwert aus #2 der Grund dafür ist.
