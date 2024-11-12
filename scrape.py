import json
import requests
import bs4
from datetime import datetime

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

def get_json_city():
    res = requests.get("https://city-kinos.de/en/films")
    if res.status_code != 200:
        print("city-kinos went wrong")
    bs_object = bs4.BeautifulSoup(res.text, 'html.parser')
    # get movie data as dictionary from city kino website inside a script tag with id "NEXT_DATA"
    movie_data = json.loads(bs_object.css.select('#__NEXT_DATA__')[0].string)
    return movie_data['props']['pageProps']['films']

data = get_json(build_URI())
data_city = get_json_city()

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




def get_cinema_data(date):
    """
    return dictionary that maps movie titles to a list of tuples containing:
    - name of the cinema this movie is running in
    - a list of times this movie is showing and if it is OV/OmU/synchronized
    """
    shows = data['shows']
    movies = data['movies']
    shows_today = list(filter(lambda s : s['date'] == date, shows)) 
    map_movie = {}
    groups = id_groups()
    for movie_ids in groups:
        cinema_dictionary = {}
        for show in shows_today:
            if show['movieId'] in movie_ids:
                current_cinema = CINEMAS[show['cinemaId']]
                if show['flags']:
                    mode_string = show['flags'][0]['name']
                    mode = mode_string if 'OV' in mode_string or 'OmU' in mode_string  else 'Deutsch' 
                else:
                    mode = 'Deutsch'
                if current_cinema in cinema_dictionary.keys():
                    cinema_dictionary[current_cinema].append((show['time'],mode)) 
                else:
                    cinema_dictionary[current_cinema] = [(show['time'],mode)] 
        name = movies[movie_ids[0]]['name']
        if len(cinema_dictionary.items()) != 0:
            map_movie[name] = cinema_dictionary
    
    # incorporate city films
    map_movie_city = get_city_data(date)
    for (titleCity, showingsCity) in map_movie_city.items():
        was_found = False
        for (title, showings) in map_movie.items():
            # this test is sometimes not enough but is good enough for now
            if titleCity.lower() ==  title.lower():
                showings['City'] = showingsCity
                was_found = True
                break
        if not was_found:
            map_movie[titleCity] = {'City': showingsCity}
    return map_movie

def get_movie_data():
    """
    Return dictionary that maps movie titles to 
    - duration
    - poster image url
    - description
    - trailer, if available
    """
    map_movie = {}
    movies = data['movies']
    for movie_ids in id_groups():
        movie = movies[movie_ids[0]]
        if movie['hasTrailer']:
            trailer = movie['trailers'][0]['url']
        else:
            trailer = ""
        name = movie['name']
        if not ('description' in movie.keys() and 'duration' in movie.keys() and 'lazyImage' in movie.keys()):
            continue
        map_movie[name] = (movie['duration'], movie['lazyImage'], movie['description'], trailer)

    # incorporate city films
    map_movie_city = get_movie_data_city()
    for (titleCity, infoCity) in map_movie_city.items():
        was_found = False
        for title in map_movie.keys():
            if titleCity.lower() == title.lower():
                was_found = True
                break
        if not was_found:
            map_movie[titleCity] = infoCity
    return map_movie

def get_city_data(date):
    """
    return dictionary that maps movie titles to a list containing tuples containing
    times this movie is showing at date in city kino and if it is OV/OmU/synchronized
    """
    movie_map = {}
    for movie in data_city:
        if movie['fields']['title'] == 'Sneak Preview':
            continue
        sessions = movie['fields']['sessions']
        shows_today = list(filter(lambda s : s['fields']['startTime'].startswith(date), sessions))
        if not shows_today:
            continue
        shows = []
        for show in shows_today:
            time = str(datetime.fromisoformat(show['fields']['startTime']).time())
            if ('formats' in show['fields']):
                shows.append((time[:5], show['fields']['formats'][0]))
            else:
                shows.append((time[:5], 'x'))
        movie_map[movie['fields']['title']] = shows
    return movie_map

def get_movie_data_city():
    """
    Return dictionary that maps movie titles to 
    - duration
    - poster image url
    - description
    - trailer, if available
    """
    map_movie = {}
    for movie in data_city:
        if movie['fields']['title'] == 'Sneak Preview':
            continue
        map_movie[movie['fields']['title']] = (movie['fields']['runtime'], 
                movie['fields']['heroImage']['fields']['image']['fields']['file']['url'],
                movie['fields']['tagline'], "")

    return map_movie

