
# IMU Workshop – Documentation

## Durchgeführte Bewegung  
Das Smartphone wurde in einer U-förmigen Bahn um einen Laptop bewegt, dabei wurden zwei Drehungen um die Z‑Achse vorgenommen. Das Gerät zeigte währenddessen konstant in X‑Richtung. Ziel war die Aufzeichnung der Bewegung durch Beschleunigungs‑ und Gyroskopsensoren und die anschließende Rekonstruktion der Trajektorie.

## Gemessene Distanz  
Die von Hand gemessene Distanz beträgt etwa **0,9 m**.  
Der Drehwinkel um die Z‑Achse liegt bei ungefähr **180°**.

## Rekonstruierte Distanz  
Durch Analyse der Beschleunigungs- und Winkelgeschwindigkeitsdaten sowie numerische Integration der globalen Beschleunigungen wurde eine rekonstruierte Trajektoriedistanz von **ca. 1 m** bestimmt. Diese wurde sowohl in 2D als auch in 3D visualisiert.

## Beobachtungen zu Drift und Genauigkeit  
- In den 3D-Plots der Trajektorie zeigt sich ein deutliches „Driften“, besonders in Z-Richtung. Sensorisch scheint das Gerät auch horizontal zu wandern, obwohl dies physisch nicht passiert ist.  
- In der X‑Y‑Ebene folgt die rekonstruierte Bewegung weitgehend der erwarteten U-Form. Kleine Abweichungen stammen vermutlich aus Integrationsfehlern und Sensordrift.  
- Der Drehwinkel um die Z-Achse wird im Plot *Device Orientation Over Time* sehr gut abgebildet.

## Herausforderungen und Lösungsansätze  
- **Sensor‑Drift**: Vor der Messung wurde eine Kalibrierung der Sensoren durchgeführt, um systematische Fehler zu reduzieren.  
- **Ungewollte Z‑Bewegung**: In den 3D-Darstellungen zeigte sich eine vertikale Bewegung, obwohl keine vorhanden ist. Mehrfache Messungen bestätigten den Effekt, der Fehler ließ sich nicht vollständig eliminieren.  
- **Randbereiche**: Die ersten 1,5 s und letzten 2 s wurden abgeschnitten, um Artefakte am Messanfang bzw. -ende zu vermeiden.  
- **Filterung & Integration**: Ein Butterworth-Tiefpassfilter bei 5 Hz wurde auf Beschleunigungs- und Gyroskopdaten angewendet, bevor sie in den Madgwick‑Filter und die numerische Integration einflossen.  
- **ZUPT**: Mit der Zero-Velocity-Update-Methode wurden stationäre Phasen genutzt, um die Geschwindigkeit zurückzusetzen und Drift zu verringern.

## Fazit  
Die Kombination aus Filterung, Madgwick-Orientierungsschätzung und ZUPT führt zu einer annehmbaren Näherung der realen Trajektorie. Die erzeugte Bewegung entspricht qualitativ der erwarteten U-Kurve, allerdings treten typische Drifteffekte auf — insbesondere bei längeren Messungen und vertikalen Bewegungen.
