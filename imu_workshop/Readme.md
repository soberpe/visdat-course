---
marp: true
paginate: true
footer: " Motion Tracking Assignment – Documentation [Elias Gradinger]"
---

Für die Datenerfassung am Anfang habe ich mich mit meinem Sitznachbarn zusammen getan da ich mein MathWorks Passwort nicht mehr wusste. Er hat eine eine kurze und kontrollierte Bewegung ausgeführt, indem er sein Smartphone etwa round about 60cm von links nach rechts über den Tisch, liegend auf der Tischplatte, bewegte und dabei möglichst gleichmäßig die Bewegung ausgeführt hat und am Ende klar erkennbar angehalten hat. Diese Strecke wurde dann auf 60cm geschätzt, um später einen direkten Vergleich zwischen realer und rekonstruierter Distanz zu ermöglichen.

Nach dem Einlesen der IMU-Rohdaten (Beschleunigung und Gyroskop) habe ich die Signale zunächst gefiltert und anschließend die Orientierung des Smartphones mithilfe des Madgwick-Algorithmus geschätzt. Mit diesen Orientierungsdaten konnte ich die Beschleunigungen vom Gerätekoordinatensystem in das globale Koordinatensystem transformieren. Anschließend wurde die global transformierte Beschleunigung zweimal integriert zuerst zur Geschwindigkeit, danach zur Position.

Während die tatsächliche Bewegung 60cm betragen hat, ergab die rekonstruierten Positionsdaten eine geschätzte Strecke von 0,702m. Die Rekonstruktion überschätzte die reale Bewegung also etwas. Diese Abweichung ist typisch für IMU-basierte Positionsbestimmung und wird durch Integration von Rauschen, Bias-Drift und Orientierungsfehler verursacht. Laut Aussage des Professors fällt besonders bei so kurzen Strecken jeder kleine Messfehler stark ins Gewicht, was die Positionsergebnisse schnell verfälscht.

Zu beobachten war unter anderem ein Geschwindigkeitsdrift. Selbst in Phasen, in denen das Gerät eindeutig stillstand, wuchs die integrierte Geschwindigkeit geringfügig weiter an. Dies weist auf kleine konstante Beschleunigungsfehler hin, die durch die doppelte Integration zu deutlichen Positionsfehlern führen. Zudem bewirkt schon eine minimale falsche Orientierung, dass ein Teil der Schwerkraft als horizontale Beschleunigung interpretiert wird.

Zu den zentralen Herausforderungen gehörten:
- Bias-Korrektur in Ruhephasen  
- Auswahl geeigneter Filterparameter
- Stabilität der Orientierungsbestimmung, da schon kleine Fehler die gesamte Rekonstruktion verfälschen  

Insgesamt zeigt die Analyse trotz einer einfachen, klar definierten Bewegung sehr deutlich, wie schwierig eine präzise Positionsrekonstruktion allein aus IMU-Daten ist – insbesondere bei kurzen Strecken wie den hier untersuchten 60 cm.

~290 Wörter