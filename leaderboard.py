#!/bin/python3
from results import get_results
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import os
import sqlite3
import threading
import time
import requests
import fcntl
import gitlab

app = Flask(__name__)

die_elite = ["2604", "1030", "2545", "2546", "1723"]

@app.route('/external_sort')
def external_sort():
    db = get_db()
    cur = db.execute("select gitlabid, boardname, time from externalsort order by time asc")
    entries = cur.fetchall()
    return render_template('leaderboard.html', entries=entries, die_elite=die_elite, task='External Sort')

@app.route('/buffer_manager')
def buffer_manager():
    db = get_db()
    cur = db.execute("select gitlabid, boardname, time from buffermanager order by time asc")
    entries = cur.fetchall()
    return render_template('leaderboard.html', entries=entries, die_elite=die_elite, task='Buffer Manager')

@app.route('/slotted_pages')
def slotted_pages():
    db = get_db()
    cur = db.execute("select gitlabid, boardname, time from slottedpages order by time asc")
    entries = cur.fetchall()
    return render_template('leaderboard.html', entries=entries, die_elite=die_elite, task='Slotted Pages')

@app.route('/btree')
def btree():
    db = get_db()
    cur = db.execute("select gitlabid, boardname, time from btree order by time asc")
    entries = cur.fetchall()
    return render_template('leaderboard.html', entries=entries, die_elite=die_elite, task='B+ Tree')

@app.route('/operators')
def operators():
    db = get_db()
    cur = db.execute("select gitlabid, boardname, time from operators order by time asc")
    entries = cur.fetchall()
    return render_template('leaderboard.html', entries=entries, die_elite=die_elite, task='Algebraic Operators')

@app.route('/')
def home():
    return render_template('home.html')

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'submissions.db'),
))

class UpdateDB(threading.Thread):
    def run (self, *args, **kawrgs):
        projects = [(8045, "ExternalSort_Random", "externalsort"), 
                (8270, "BufferManager_Multi", "buffermanager"),
                (8448, "SlottedPages", "slottedpages"),
                (8615, "Btree_Multi", "btree"),
                (8712, "Iterator", "operators")]
        while True:
            for (project_id, bench_name, table_name) in projects:
                while True:
                    try:
                        results = get_results(project_id, bench_name)
                        break
                    except requests.exceptions.ConnectionError:
                        print("ConnectionError, try again in 5 seconds")
                        time.sleep(5)
                    except gitlab.exceptions.GitlabError:
                        print("GitlabError, try again in a minute")
                        time.sleep(60)
                with app.app_context():
                    db = get_db()
                    for r in results:
                        db.execute('replace into '+table_name+' (gitlabid, boardname, time) values (?,?,?)', [r.gitlabid, r.boardname, r.time])
                        db.commit()
            # update db every 5 minutes
            time.sleep(5*60)


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    from os.path import isfile
    if(isfile(app.config['DATABASE'])):
       print('Database exists. No action taken.')
       return
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        db.cursor().executescript(f.read())
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    db.commit()
    print('Initialized the database.')


with app.app_context():
    init_db()
t = UpdateDB()
t.start()

if __name__ == "__main__":
    app.run(host='127.0.0.0', port=5000)

