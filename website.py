#!/bin/python3
from scrape import cinema_per_movie, data_by_movie, DATE
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import os
import time
import fcntl
import requests
import bs4


app = Flask(__name__)

@app.route('/<movie>')
def movie_sites(movie):
    res = requests.get("https://letterboxd.com/search/" +movie+"/")
    if res.status_code != 200:
        print("letterboxd went wrong")
    bs_object = bs4.BeautifulSoup(res.text, 'html.parser')
    url = bs_object.select('.results > li:nth-child(1) > div:nth-child(2) > h2:nth-child(1) > span:nth-child(1) > a:nth-child(1)')
    if len(url) == 0:
        rating = 'No rating available'
    else:
        url = url[0].get('href')
        res = requests.get("https://letterboxd.com"+str(url))
        if res.status_code != 200:
            print("letterboxd went wrong")
        bs_object = bs4.BeautifulSoup(res.text, 'html.parser')
        rating = bs_object.select('head > meta:nth-child(20)')
        if len(rating) == 0 or not str(rating[0].get('content'))[0].isdigit():
            rating = 'No rating available'
        else:
            rating = str(rating[0].get('content'))[0:4]
    return render_template('movie_site.html', name=movie, entry=data_by_movie[movie], rating=rating)

@app.route('/')
def home():
    return render_template('home.html', movies=cinema_per_movie.keys(), data=cinema_per_movie, date=DATE)

if __name__ == "__main__":
    app.run(host='127.0.0.0', port=5000)

