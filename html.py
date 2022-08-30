from crawl import data_by_cinema, CINEMAS

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

def index_builder_list (data):
    s = ""
    for show in data:
        s += "\t<li>" + data[show][1][0] + ":"
        for time in data[show][0]:
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
    f.write("</body>\n</html>")
    f.close()

def movie_sites():
    return 0

def main():
    index()

if __name__ == "__main__":
    main() 
