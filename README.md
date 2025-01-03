## Kino Programm München
Das Program startet einen lokalen Flaskserver und zeigt Filmvorstellungen in bestimmten Kinos in München für einen Tag an.

Starten durch
```
cd cinema_program
. .venv/bin/activate
python3 website.py
```
Um alle Filme an einem bestimmten Tag zu sehen, gibt man das Datum als Commandline Parameter mit:
```
python3 website.py yyyy-mm-dd
```
Wird nichts übergeben, wird der heutige Tag genommen.

### Features
* Vorstellungen per Film mit Angabe von Kino und Uhrzeit
* Subpage pro Film mit:
    * Kurzbeschreibung und Poster
    * Film Trailer
    * Letterboxd Bewertung

### TODOs
* Bereich an Tagen als Parameter
* Uhrzeit als Parameter
* eigenens CSS statt Bootstrap
