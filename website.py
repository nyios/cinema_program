#!/bin/python3
from scrape import cinema_per_movie, data_by_movie, letterboxd, DATE
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import os
import time
import fcntl


app = Flask(__name__)

@app.route('/<movie>')
def movie_sites(movie):
    if movie in letterboxd.keys():
        rating = letterboxd[movie]
    else:
        rating = 'No rating available'
    return render_template('movie_site.html', name=movie, entry=data_by_movie[movie], rating=rating)

@app.route('/')
def home():
    return render_template('home.html', movies=cinema_per_movie.keys(), data=cinema_per_movie, date=DATE)

if __name__ == "__main__":
    app.run(host='127.0.0.0', port=5000)

