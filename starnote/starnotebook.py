#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, url_for, redirect
from jinja2 import *
from starnote import Starnote
import requests, json

env = Environment(loader=PackageLoader('starnote', 'templates'))
starred_tmpl = env.get_template('starred.html')
tagged_tmpl = env.get_template('tagged.html')

app = Flask(__name__)

def init_user(username, starred_file, tagged_file):

    global user
    user = {
        "settings": 'settings.json',
        "username": username,
        "user_url": 'https://github.com/' + username,
        "starred_file": starred_file,
        "starred_url": 'https://api.github.com/users/{}/starred'.format(username),
        "tagged_file": tagged_file
    }

    try:
        with open(user['starred_file'], 'r') as filehandle:
            global starlist
            starlist = json.loads(filehandle.read())

        with open(user['settings'], 'r') as filehandle:
            global settings
            settings = json.loads(filehandle.read())
    except Exception, e:
        raise e

    global pagination, total_pages, current_page, bottom, top
    pagination = settings['pagination']
    total_pages = len(starlist) / pagination + 1
    current_page = 1
    bottom, top = 0, pagination

@app.route('/')
@app.route('/starred')
@app.route('/starred/<action>')
def send_starred(action=None):

    favicon = url_for('static', filename='favicon.ico')
    bootstrap = url_for('static', filename='lib/bootstrap.min.css')
    theme = url_for('static', filename='lib/jumbotron-narrow.css')
    custom = url_for('static', filename='src/custom.css')
    viewport_hack = url_for('static', filename='lib/ie10-viewport-bug-workaround.js')

    global pagination, total_pages, current_page, bottom, top

    if action == 'next':
        if current_page < total_pages:
            current_page += 1
            bottom, top = bottom + pagination, top + pagination
    elif action == 'previous':
        if current_page > 1:
            current_page -= 1
            bottom, top = bottom - pagination, top - pagination
    else:
        current_page = 1
        bottom, top = 0, pagination

    return starred_tmpl.render(
        favicon=favicon,
        bootstrap_css=bootstrap,
        theme_css=theme,
        custom_css=custom,
        username=user['username'],
        user_url=user['user_url'],
        starlist=starlist[bottom:top],
        current_page=current_page,
        total_pages=total_pages,
        viewport_hack_js=viewport_hack
        )

@app.route('/tagged')
def send_tagged():

    favicon = url_for('static', filename='favicon.ico')
    bootstrap = url_for('static', filename='lib/bootstrap.min.css')
    theme = url_for('static', filename='lib/jumbotron-narrow.css')
    custom = url_for('static', filename='src/custom.css')
    viewport_hack = url_for('static', filename='lib/ie10-viewport-bug-workaround.js')

    return tagged_tmpl.render(
        favicon=favicon,
        bootstrap_css=bootstrap,
        theme_css=theme,
        custom_css=custom,
        username=user['username'],
        user_url=user['user_url'],
        viewport_hack_js=viewport_hack
        )

@app.route('/update')
def update_starred_repositories():

    try:
        r = requests.get(user['starred_url'])

        if r.status_code == 200:
            return 'Success'
        elif r.status_code == 404:
            return 'Failed'
    except:
        return redirect('/')

def run_starnotebook():

    app.debug = True
    app.run()