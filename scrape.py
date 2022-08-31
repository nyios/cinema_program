import json
import requests
from datetime import datetime

DATE = datetime.today().strftime('%Y-%m-%d')
ARENA = 29
ROYAL = 1111
RIO = 748
MONOPOL = 981
MAXIM = 952
MUSEUM = 995
CINEMAS = [ARENA, ROYAL, RIO, MONOPOL, MAXIM, MUSEUM]

def build_URI():
    s = "https://www.kinoheld.de/ajax/getShowsForCinemas?"
    for c in CINEMAS:
        s += ("cinemaIds[]=" + str(c) + "&")
    s += "lang=en"
    return s

def get_json(uri):
    return requests.get(uri).json()

complete_json = get_json(build_URI())

def extract_data(data, cinemaId):
    shows = data["shows"]
    movies = data["movies"]
    shows_today = list(filter(lambda s : s["date"] == DATE and s["cinemaId"] == cinemaId, shows)) 
    # dictionary that maps movieIds to 
    # - list of pairs : (time slots, OmU/OV/etc)
    # - title
    # - duration
    # - trailer
    # - description
    map_movie = {}
    for s in shows_today:
        if s["movieId"] in map_movie.keys():
            map_movie[s["movieId"]][0].append(s["time"])
        else:
            map_movie[s["movieId"]] = [[s["time"]]]

    movies_today = list(filter(lambda m : m in map_movie.keys(), movies))
    for m in movies_today:
        if "title_orig" in movies[m]:
            map_movie[m].append([movies[m]["title_orig"]])
        else:
            map_movie[m].append([movies[m]["title"]])
        map_movie[m].append([movies[m]["duration"]])
        map_movie[m].append([movies[m]["trailers"][0]["url"]])
        map_movie[m].append([movies[m]["description"]])
    return map_movie

def get_data_by_cinema():
    map_cinema = {}
    for cinema in CINEMAS:
        map_cinema[cinema] = extract_data(complete_json, cinema)
    return map_cinema

data_by_cinema = get_data_by_cinema()

def get_data_by_movie():
    movieIds = []
    movieTitles = []
    movieDict = {} 
    for movies in data_by_cinema.values():
        for movieId, value in movies.items():
            if not movieId in movieIds and not value[1] in movieTitles:
                movieIds.append(movieId)
                movieTitles.append(value[1])
                movieDict[movieId] = value
    return movieDict

data_by_movie = get_data_by_movie()
