from crawl import data_by_cinema, CINEMAS, data_by_movie

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
    for show in data.values():
        s += "\t<li>" + show[1][0] + ":"
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
        path = "html/" + str(movieId) + ".html"
        f = open(path, "w")
        f.write(start_string)
        f.write("<p>" + info[3] + "</p>")
        f.write(end_string)
        f.close()

def main():
    movie_sites_builder()

if __name__ == "__main__":
    main() 
