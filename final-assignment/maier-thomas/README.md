Project Title
    Schwingungsanalyse

Description
    Mit dem Code ist es möglich Übertragungsfunktion grafisch darzustellen, die Eigenfrequenzen zu ermitteln und anschließend die Moden qualitativ darstellen.
     
     Das Skript übernimmt dadurch große teile der Aufgabenstellung der Dokumentation von messungen aus der Prüfstandstechnik zur ermittlung von Eigenfrequenzen und der qualitativen Darstellung von Moden.
     Weiters können säömtliche Plots als Grafiken gespeichert werden.

Main features/capabilities
    Die Hauptfunktion ist definitiv das ermitteln der Eigenfrequenzen und das Darstellen der Moden.
    Auch bei unsortierten Messwerten können diese mittels Featuremap sortiert werden.

Python libraries:
    NumPy
    PyQt6
    MatPlotlib
    h5py  zum Lesen eines h5 files
    scipy

Special techniques 
    Eigenes allgemeines File zur auffinden der Eignefrequenzen aufbauen und Plotten der Moden für allgemeine verwendung


requirements.txt  # if needed

Usage
   Es muss schwingungsanalyse_main.py ausgeführt werden; Anschließend müssen je nach Bedarf die entsprechenden files geladen werden. Eine Info zum Laden fehlender Files wird beim Drücken der entsprechenden Button angezeigt.

   Hinweis: Die in schwingungsanalyse_main.py inkludierte Feature map ost speziell für die Testdaten abgestimmt.


Data
    Testdaten zum Testen des Codes liegen unter cd final-assignment/maier-thomas/testdata
    Hinweis: Die in schwingungsanalyse_main.py inkludierte Feature map ost speziell für die Testdaten abgestimmt. 

    Für die Analyse der Eigenfrequenzen und zum Plotten der Übertrtagungsfunktion bedarf es ein tsv File mit allen Beträgen sämtlicher gemessener Übertragungsfunktionen.

    Zum qualitativen Plotten der Moden Bedarf es einem tsv File mit allen Imaginärteilen sämtlicher gemessener Übertragungsfunktionensowie einem geometriefile des undeformierten Systems im Dateiformat h5.
    

Interesting algorithms or approaches
    Das Ploten der Moden war eine sehr aufwendige prozedur. Nachdme über 12 Stockwerke nur 3 Messpunkte gemacht wurden müssen alle weiteren inter und extrapoliert werden.
    Weiters wurden 3 Seitenkanten gemessen. Werden alle 3 Kanten im code verwendet kommt es zu unplausibeln moden. Es sollte immer nur eineKante gewählt werden, dann von paraleller verschiebung auszugehen ist. 

Future Improvements, Ideas for extending the project

    Herauslösen der Featuremap aus dem skript, diese soll eigenständig geladen werden

    Füttern des Skripts mit Kräfte und Beschleunigungen direkt aus der Messung darus beträge und imaginärteile ableiten, anstatt 2 Files zu laden.

    Funktion für filecompressing, damit alle Messungen in ein File gespeichert werden

    Darstellen und ermitteln von Torsionsmoden

    Probleme bei Kanälen im skript beheben.

    Einfügen einer Eingabezeile für die Einstellparameter der Eigenfrequenzanalyse