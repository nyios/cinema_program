import json
import requests
import bs4
import os
from datetime import datetime

DATE = datetime.today().strftime('%Y-%m-%d') if os.getenv('CINEMA_DATE') == None else os.getenv('CINEMA_DATE')
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

def id_groups():
    """
    returns a list of lists
    each sublist contains movie ids that map to the same movie
    """
    movies = data['movies']
    id_groups = []
    name_id_list = []
    for movie in movies.values():
        if movie['id'] != None:
            name_id_list.append((movie['name'], movie['id']))
    skippers = []
    index = 0
    for i in range(0, len(name_id_list)):
        if i in skippers:
            continue
        id_groups.append([name_id_list[i][1]])
        for j in range(i+1, len(name_id_list)):
            if (name_id_list[i][0].lower() == name_id_list[j][0].lower() 
                or name_id_list[j][0].startswith(name_id_list[i][0].lower())
                or name_id_list[i][0].startswith(name_id_list[j][0].lower())):
                id_groups[index].append(name_id_list[j][1])
                skippers.append(j)
        index += 1
    return id_groups




def get_cinema_data():
    """
    return dictionary that maps movie names to a list of tuples containing:
    - name of the cinema this movie is running in
    - a list of times this movie is showing and if it is OV/OmU/synchronized
    """
    shows = data["shows"]
    movies = data["movies"]
    print(DATE)
    shows_today = list(filter(lambda s : s["date"] == DATE, shows)) 
    map_movie = {}
    groups = id_groups()
    for movie_ids in groups:
        cinema_dictionary = {}
        for show in shows_today:
            if show['movieId'] in movie_ids:
                current_cinema = CINEMAS[show['cinemaId']]
                if show['flags']:
                    mode = show['flags'][0]['name'] if 'OV' in show['flags'][0]['name'] else 'Deutsch' 
                else:
                    mode = 'Deutsch'
                if current_cinema in cinema_dictionary.keys():
                    cinema_dictionary[current_cinema].append((show['time'],mode)) 
                else:
                    cinema_dictionary[current_cinema] = [(show['time'],mode)] 
        name = movies[movie_ids[0]]['name']
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
    for movie_ids in id_groups():
        movie = movies[movie_ids[0]]
        if movie['hasTrailer']:
            trailer = movie['trailers'][0]['url']
        else:
            trailer = ""
        name = movie['name']
        # only lowercase
        if name.isupper():
            name = name[0] + name[1::].lower()
        if not ('description' in movie.keys() and 'duration' in movie.keys() and 'lazyImage' in movie.keys()):
            continue
        map_movie[name] = (movie['duration'], movie['lazyImage'], movie['description'], trailer)

    return map_movie

data_by_movie = get_data_by_movie()
cinema_per_movie = get_cinema_data()

if __name__ == "__main__":
    print(get_cinema_data())
