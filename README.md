## Kino Programm München
Gibt Filme in ausgewählten Kinos aus, läuft auf einem lokalen Flaskserver

Starten durch
```
cd cinema_program
. .venv/bin/activate
python3 website.py
```
Dann entweder auf den Link klicken oder `http://127.0.0.0:5000` in einen Browser eingeben.

```
python3 website.py yyyy-mm-dd
```
Zeigt alle Filme am angegebenen Tag an. Falls kein Argument übergeben wurde, wird der heute Tag verwendet.

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
