#!/bin/python3
from scrape import get_movie_data, get_cinema_data
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import time
import requests
import bs4
from datetime import datetime

CINEMA_URLS = {'Arena': 'https://www.arena-kino.de/de/unser-gesamtes-filmprogramm',
        'Royal Filmpalast': 'https://www.royal-muenchen.de/de/programm-tickets',
        'Rio': 'https://riopalast.de/de/programm-tickets',
        'Monopol': 'https://www.monopol-kino.de/de/programm-tickets',
        'Museum Lichtspiele': 'https://www.museum-lichtspiele.de/programm'}


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

app = Flask(__name__)

@app.route('/<movie>')
def movie_sites(movie):
    data_by_movie = get_movie_data()
    res = requests.get(f"https://letterboxd.com/s/search/{movie}/", headers=headers, allow_redirects=True)
    if res.status_code != 200:
        print("letterboxd went wrong")
    bs_object = bs4.BeautifulSoup(res.text, 'html.parser')
    url = bs_object.select('.results > li:nth-child(1) > div:nth-child(2) > h2:nth-child(1) > span:nth-child(1) > a:nth-child(1)')
    print(url)
    if len(url) == 0:
        rating = 'No rating available'
    else:
        url = url[0].get('href')
        res = requests.get("https://letterboxd.com"+str(url))
        if res.status_code != 200:
            print("letterboxd went wrong")
        bs_object = bs4.BeautifulSoup(res.text, 'html.parser')
        rating = bs_object.select('head > meta:nth-child(21)')
        if len(rating) == 0 or not str(rating[0].get('content'))[0].isdigit():
            rating = 'No rating available'
        else:
            rating = str(rating[0].get('content'))[0:4]
        if not rating:
            rating = 'No rating available'
    return render_template('movie_site.html', name=movie, entry=data_by_movie[movie], rating=rating, url="https://letterboxd.com"+str(url))

@app.route('/')
def home():
    date = request.args['date'] if 'date' in request.args else datetime.today().strftime('%Y-%m-%d')
    cinema_per_movie = get_cinema_data(date)
    return render_template('home.html', movies=cinema_per_movie.keys(), data=cinema_per_movie, date=date, urls=CINEMA_URLS)

if __name__ == "__main__":
    app.run(host='127.0.0.0', port=5000)

