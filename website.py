#!/bin/python3
from scrape import cinema_per_movie, CINEMAS, data_by_movie
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import os
import time
import fcntl


app = Flask(__name__)

@app.route('/<movie>')
def movie_sites(movie):
    return render_template('movie_site.html', name=movie, entry=data_by_movie[movie])

@app.route('/')
def home():
    return render_template('home.html', movies=cinema_per_movie.keys(), data=cinema_per_movie)

if __name__ == "__main__":
    app.run(host='127.0.0.0', port=5000)

