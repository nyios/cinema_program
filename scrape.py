import json
import requests
from datetime import datetime

DATE = datetime.today().strftime('%Y-%m-%d')
ARENA = 29
ROYAL = 1111
RIO = 748
MONOPOL = 981
MUSEUM = 995
CINEMAS = {ARENA: 'Arena', ROYAL: 'Royal Filmpalast', RIO: 'Rio', MONOPOL: 'Monopol', MUSEUM: 'Museum Lichtspiele'}

def build_URI():
    s = "https://www.kinoheld.de/ajax/getShowsForCinemas?"
    for c in CINEMAS.keys():
        s += ("cinemaIds[]=" + str(c) + "&")
    s += "lang=en"
    return s

def get_json(uri):
    return requests.get(uri).json()

data = get_json(build_URI())

def get_cinema_data():
    """
    return dictionary that maps movie names to a list of tuples containing:
    - name of the cinema this movie is running in
    - a list of times this movie is showing and if it is OV/OmU/synchronized
    """
    shows = data["shows"]
    movies = data["movies"]
    shows_today = list(filter(lambda s : s["date"] == DATE, shows)) 
    map_movie = {}
    for movie in movies.values():
        if movie['id'] == None:
            continue
        cinema_dictionary = {}
        for show in shows_today:
            if show['movieId'] == movie['id']:
                current_cinema = CINEMAS[show['cinemaId']]
                if show['flags']:
                    mode = show['flags'][0]['name']
                else:
                    mode = 'Deutsch'
                if current_cinema in cinema_dictionary.keys():
                    cinema_dictionary[current_cinema].append((show['time'],mode)) 
                else:
                    cinema_dictionary[current_cinema] = [(show['time'],mode)] 
        name = movie['name']
        # only lowercase
        if name.isupper():
            name = name[0] + name[1::].lower()
        if len(cinema_dictionary.items()) != 0:
            map_movie[name] = cinema_dictionary
    return map_movie

def get_data_by_movie():
    """
    Return dictionary that maps movie titles to 
    - duration
    - poster image url
    - description
    - trailer, if available
    """
    map_movie = {}
    movies = data["movies"]
    for movie in movies.values():
        if movie['id'] == None:
            continue
        if movie['hasTrailer']:
            trailer = movie['trailers'][0]['url']
        else:
            trailer = ""
        name = movie['name']
        # only lowercase
        if name.isupper():
            name = name[0] + name[1::].lower()
        map_movie[name] = (movie['duration'], movie['lazyImage'], movie['description'], trailer)

    return map_movie

data_by_movie = get_data_by_movie()
cinema_per_movie = get_cinema_data()
#if __name__ == "__main__":
#    print(data_by_movie)
