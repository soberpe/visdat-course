# Roadmap

Was am Kursmaterial als Nächstes geplant ist. Die Liste ist bewusst öffentlich:
Der Kurs wird jedes Semester weiterentwickelt, und wer wissen will, wohin er
sich entwickelt, soll das nachlesen können.

Anregungen und Fehlermeldungen gerne als Issue in diesem Repository.

## Vor dem Semesterstart

- [ ] **Abgabetermine eintragen.** IMU-Workshop und Final Assignment stehen
      derzeit auf "announced in class" und bekommen die konkreten Daten.
- [ ] **Zugänge zum Abgabe-Repository.** Einladungen gehen in der ersten Woche
      raus, sobald die GitHub-Benutzernamen vorliegen.
- [ ] **Labels und Milestones** je Assignment im Abgabe-Repository anlegen,
      damit die Abgaben von Anfang an sortiert sind.

## Inhaltliche Erweiterungen

- [ ] **Verifikation und Tests.** Der Kurs fragt bisher, ob der Code läuft. Die
      wichtigere Frage im Ingenieursalltag ist, ob das Ergebnis stimmt. Geplant
      ist ein Baustein zur Verifikation gegen eine analytische Referenzlösung,
      am Beispiel des Kragbalkens aus der FEM-Challenge, mit `pytest`. Dazu ein
      entsprechendes Kriterium im Final Assignment.
- [ ] **Debuggen.** Der Python-Debugger steht in der Extension-Liste, wird aber
      nirgends erklärt. Geplant ist eine Einheit zu Breakpoint, Step, Watch und
      Call Stack, direkt am Broken-Code-Block des Mesh-Workshops.
- [ ] **Urteil über Diagramme.** Diagrammwahl, Farbskalen, Achsenskalierung.
      Bisher eine knappe Seite. Geplant ist eine Übung, in der ein schwacher
      Plot verbessert und die Entscheidung begründet wird.
- [ ] **AI im Kurs.** Eine eigene Seite zur Haltung, zu den Erwartungen und zur
      Deklaration des Werkzeugeinsatzes in der Abgabe. Der Abschnitt im
      Pull-Request-Template ist der erste Schritt dazu.
- [ ] **Übungen in den Referenzkapiteln.** Die Kapitel zu Python, C++ und den
      Paradigmen sind derzeit reines Nachschlagewerk. Geplant sind zwei bis drei
      kurze Selbstkontrollaufgaben pro Kapitel, mit aufklappbarer Lösung.

## Struktur des Kurses

- [ ] **C++ anwendbar machen.** C++ steht in diesem Kurs stellvertretend für die
      kompilierten Sprachen, und dieser Unterschied zu Python zieht sich durch
      den ganzen Stoff: er erklärt, warum NumPy schnell ist, warum `pip install`
      manchmal kompiliert, wozu CMake da ist und warum Python-Threads nichts
      beschleunigen. Bisher bleibt der Strang aber theoretisch. Geplant ist ein
      kleines pybind11-Beispiel, das eine heiße Schleife aus einer Python-Übung
      nach C++ verlagert, mit CMake gebaut und gegen die Python-Variante
      gemessen wird. Damit schließen sich C++, Build-Systeme und der
      Performance-Teil zu einer Geschichte.
- [ ] **IMU- und Qt-Workshop umbauen.** Beide geben die vollständige Lösung zum
      Mitschreiben vor. Der Mesh-Workshop macht es mit Live Coding, kaputtem
      Code und leerer Seite besser, und dieses Muster sollen die beiden anderen
      übernehmen.

## Technisches

- [ ] **Schriften bündeln.** Seite und Foliendesign laden IBM Plex zur Laufzeit
      von Google Fonts. Für Vorträge ohne Netzzugang sollen die woff2-Dateien im
      Repository liegen, etwa 350 KB.
- [ ] **GitHub Actions aktualisieren.** `actions/checkout@v4` und
      `actions/setup-node@v4` zielen auf Node 20, das GitHub abgekündigt hat.
      Sie laufen weiter, sollen aber bei Gelegenheit angehoben werden.
- [ ] **Prosa statt Stichwortlisten.** In einigen Überblicksseiten stehen
      Aufzählungen aus Schlagworten ohne Erklärung. Der Stilleitfaden dieses
      Repositories unter `.github/copilot-instructions.md` verlangt ganze Sätze,
      und daran sollen sich die Seiten auch halten.
