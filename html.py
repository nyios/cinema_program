from scrape import data_by_cinema, CINEMAS, data_by_movie
from pathlib import Path

cinemas_string = ["Arena", "Royal", "Rio", "Monopol", "Neues Maxim", "Museum Lichtspiele"]

start_string = """<!DOCTYPE html>
        <html>

        <head>
        <title>home</title>
        <meta charset="UTF-8">
        <style>
            body {
            background-color: #FFFFFF;
            }
        </style>
        </head>
        <body>"""

end_string = "</body>\n</html>"

def index_builder_list (data):
    s = ""
    for movieid, show in data.items():
        if type(show[1]) == list:
            show[1] = show[1][0]
        s += "\t<li><a href=\"" + "movie_sites/" + str(movieid) + ".html\">" + str(show[1]) + "</a>" + ":"
        for time in show[0]:
           s += " " + time 
           s += "\n"
    s += "</ul>"
    return s

def index_builder ():
    s = ""
    for i in range(len(CINEMAS)):
        s += "<h2>Vorstellungen im " + cinemas_string[i] + "</h2>\n<ul>\n"
        data = data_by_cinema[CINEMAS[i]] 
        s += index_builder_list(data)
    return s

def index():
    f = open("html/index.html", "w")
    f.write(start_string)
    f.write(index_builder())
    f.write(end_string)
    f.close()

def movie_sites_builder():
    for movieId, info in data_by_movie.items():
        path = "html/movie_sites/" + str(movieId) + ".html"
        f = open(path, "w")
        f.write(start_string)
        s = "<h2>" + str(info[1]) + "</h2>"
        s += "<h3>Beschreibung:</h3>"
        s += "<p>" + info[4] + "</p>"
        s += "<h3>Dauer:</h3>"
        s += "<p>" + str(info[2]) + " Minuten</p>"
        s += "<h3>Trailer:</h3>"
        s += "<a href=\"" + info[3] + "\" target=\"_blank\">Link</a>"
        f.write(s)
        f.write(end_string)
        f.close()

def main():
    Path("html/movie_sites/").mkdir(parents=True, exist_ok=True)
    index()
    movie_sites_builder()

if __name__ == "__main__":
    main() 
