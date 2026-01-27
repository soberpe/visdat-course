Projektname: Visualisierungen und Rekonstruktionen von Golfballflugbahnen bzw. Golfschlägen

Hobby: Golfsport
In Trainingseinheiten werden radarunterstützte Tools ("Trackman") verwendet um den Ballflug und sehr viele unterschiedliche Parameter vom Golfball (Spin, Carry, etc.)
und vom Golfschläger (Schlagfläche, Schwungbahn) aufgezeichnet.
Diese werden zur Verbesserung der Schwungtechnik und zum generellen Training und auch um Bedingungen am Golfplatz im Training nachzustellen. 
Diese Geräte sind extrem teuer, zeigen bzw. stellen allerdings diesen Ballflug dar. Günstigere Varianten sind ebenfalls am Markt, allerdings zeichnen diese nur eine geringe Anzahl an Parameter auf 
und die Flugbahn wird nicht simuliert und dargestellt. 
Um trotzdem einen geeigneten Ballflug darstellen zu können, muss aus diesen Daten eine Flugbahn rekonstruiert werden.

Ziel dieses Projekts: Aufgrund einiger vorliegender Daten( Side Carry, Carry, max. Höhe, Abflugwinkel, etc.) vom Ballflug sollen die Daten (Auswählbar!!)
in 2D dargestellt werden und daraus entsprechend einem hinterlegten Modell ein Ballflug rekonstruiert werden. Dise werden anschließend auch in 3D visualisiert.

#####################

Features:

alle Programme können unabhängig voneinander ausgeführt werden!
Diese drei Programme laufen einzeln und stellen
die einzelnen Phasen und Schritte der Entwicklung dar. 

mainONESIMULATION.py

Im ersten Programm wird mit willkürlichen Anfangsbedingungen (an meine Erfahrungen angelehnt) eine Flugbahn berechnet.
Das mathematische Modell stammt dabei aus einem Vortrag der Uni Bremen (Seite 67).
Website: https://blogs.uni-bremen.de/blueeeye/files/2011/02/Vortrag.pdf
Daraus wird eine 3D Visualisierung erstellt. Diese Visualisierung enthält einen grünen Boden und unterschiedliche Rasterlinien,
um die Flugweite und Seitenabweichung zu erkennen. Außerdem wird der Auftreffpunt entsprechend markiert. 
Anschließend werden unterschiedliche 2D Grafiken (Flugbahnen über die Zeit, 2D Flugbahnen in X-Y und in X-Z Ebene).
Außerdem werden im Terminal folgende Werte ausgegeben:
===== Aufschlagdaten =====
Wurfweite x       : XXXX
Seitliche Drift z : XXXX
Gesamte Flugzeit  : XXXX
Maximale Flughöhe : XXXX
Seitliche Drift am Aufschlag : XXXX
und Flugbahnen in 2D dargestellt.








mainMORESIMULATIONS.py

Im zweiten Programm werden mit willkürlichen Anfangsbedingungen 8 verschiedene Flugbahn erstellt (8: im Hinblick auf 8 einzulesende Flugbahndaten)
und daraus eine 3D Visualisierung erstellt. Und ebenfalls eine 2D Darstellung (vgl. mit erstem Programm)



mainSchlagdatenEinlesen.py
Im dritten Programm werden die unten erwähnten Daten eingelesen und angezeigt. Mithilfe eines Auswahlmenues kann in der Anzeige
zwischen den 9er-Eisen und den 7er-Eisen Daten unterschieden werden.
Durch CHeckboxen können dabei einzelnen Flugbahnen eingeschalten/ausgeschalten werden.


mainSchlaegeRekonstruktion.py

Dieses Programm "verbindet" und "kombiniert" die oberen 3 Programme. Zuerst werden die Daten eingelesen. Anschließend Auswahl ob 9er-Eisen oder den 7er-Eisen. Danach werden mit Hilfe des zweiten Pragramms 
unter Verwendung der eingelesenen Daten (Anfangsbedingungen!!) Flugbhanen rekonstruiert und 3D visualisiert. Durch Checkboxen können dabei einzelnen Flugbahnen eingeschalten/ausgeschalten werden.



#####################

Technologies Used:

import numpy as np
import matplotlib.pyplot as plt    
import pyvista as pv                 
from pyvistaqt import BackgroundPlotter
from PyQt6 import QtWidgets
import sys
import pandas as pd
import seaborn as sns
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

###################

Installation & Setup

cd final-assignment/Zierler/code
pip install -r requirements.txt  # if needed


###################

Usage:
alle Programme können unabhängig voneinander ausgeführt werden!

mainONESIMULATION.py
mainMORESIMULATIONS.py
mainSchlagdatenEinlesen.py

Diese drei Programme laufen einzeln und stellen
die einzelnen Phasen und Schritte der Entwicklung dar. 
Zuerst wird im ersten Programm mit willkürlichen Anfangsbedingungen eine Flugbahn erstellt 
und daraus eine 3D Visualisierung erstellt. Anschließend werden unterschiedliche 2D Grafiken 
und Flugbahnen in 2D dargestellt.

Im zweiten Programm werden mit willkürlichen Anfangsbedingungen 8 verschiedene Flugbahn erstellt (8: im Hinblick auf 8 einzulesende Flugbahndaten)
und daraus eine 3D Visualisierung erstellt.

Im dritten Programm werden die unten erwähnten Daten eingelesen und angezeigt. Mithilfe eines Auswahlmenues kann in der Anzeige
zwischen den 9er-Eisen und den 7er-Eisen Daten unterschieden werden.


mainSchlaegeRekonstruktion.py

Dieses Programm "verbindet" und "kombiniert" die oberen 3 Programme. Zuerst werden die Daten eingelesen. Anschließende Auswhal ob 9er-Eisen oder den 7er-Eisen. Danach werden mit Hilfe des zweiten Pragramms 
unter Verwendung der eingelesenen Daten (Anfangsbedingungen!!) Flugbhanen rekonstruiert und 3D visualisiert. Durch Checkboxen können dabei einzelnen Flugbahnen eingeschalten/ausgeschalten werden.


###################

Data: 
Die Daten zur Rekonstruktion befinden sich im dafür vorgesehenen Ordner (final-assignemtn/Zierler/Code/data).
Diese Ordner enthält eine csv-Datei "Schlagdaten.csv". Diese Datei enthält Daten und Parameter von jeweils 4 durchgeführten Schlägen mit einem 9er-Eisen und 
4 durchgeführten Schlägen mit einem 7er-Eisen.
Diese Daten beinhalten einzelne Parameter (Spalten) und die einzelnen Schläge sind in Zeilen unterteilt.
Diese Schlagdaten sind im Ordner Screenshots als Bild dargestellt.
###################

Implementation Details:

für Performance: sicher nicht optimal :)
für die Rekonstruktion der einzelnen Schläge werden durchaus einige Sekunden benötigt. 
Im Hinblick auf ein Einlesen von noch mehr Daten ist dies sicher nicht optimal und es besteht sich ein Performace Nachteil/Problem!!


Interesting algorithms or approaches:
Bei der Flugbahnrekonstruktion werden zuerst 8 verschiedene und willkürliche Flugbahnen erstellt.
Danach werden die Flugbahnen so zugeteilt, dass immer jene die dem eingelesenen Anfangsbedingungen am nächsten sind auch zugeordnet werden. 
Um dies zu ermöglichen, werden außerdem Korrekturfaktoren eingeführt um einen Spielraum für die Rekonstruktion zu erzeugen.


Challenges you solved:
Das mathematische Modell ist nur eine Näherung. Zu Beginn waren die Flugweiten eindeutig zu gering (Verglichen mit meinen Erfahrungen).
Darum habe ich die Weite in x-Richtung mit 1.25 und die Werte in Y-Richtung mit 2 multipliziert. Das heißt, die Flughöhe wurde verdoppelt 
und die Flugweite wird um 1/4 gegenüber dem ursprünglichem mathematischen Modell erhöht.
Außerdem war die Erstellung des Grids (grüner Boden und Raster) etwas kompliziert, da auf die unterschiedlichen Ausrichtungen geachtet werden muss.


###################

Screenshots:
Die Screenshots befinden sich im dafür vorgesehenen Ordner (final-assignemtn/Zierler/assets/Screenshots).
Diese Screenshots sind alle mit entsprechendem Namen versehen (hoffentlich selbsterklärend). 
Diese Screenshots enthalten alle erstellten Features, Graphen, Auswahlboxen, 2D-Grafiken etc.



###################
Future Improvements: 
Ich könnte mir eine Erweiterung durch KI noch sehr gut vorstellen.
Die Flugbahnberechnung erfolgt zurzeit an einem (simplen) mathematischen (und physikalischem) Modell.
ALs Idee kann ich mir auch vorstellen, aus sehr vielen Daten (genereirt aus unzähligen Trainingseinheiten am Golfplatz) 
ein "eigenes" mathematisches Modell durch den Einsatz einer geeigneten KI zu erstellen. Würde natürlich sehr viel mehr Datenmaterial und Zeit benötigen. Außerdem würde für jeden 
einzelnen Schläger eine eigene KI bzw. eigenes mathematisches Modell benötigt werden. 
Allerdings kann ich mir diese Erweiterung sehr gut vorstellen und diese würde auch den Realitätsgrad deutlich erhöhen (vermute ich zumindest) 




