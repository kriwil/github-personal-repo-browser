# -*- coding: utf-8 -*-

import os
import urllib.parse

from flask import Flask, render_template, redirect, request, session
from github import Github
import requests


CLIENT_ID = os.environ['GITHUB_CLIENT_ID']
CLIENT_SECRET = os.environ['GITHUB_CLIENT_SECRET']
SCOPES = ['repo']
STATE = 'supercalifragilisticexpialidocious'
BASE_URL = 'https://github-personal-repo-browser.herokuapp.com'
ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'


app = Flask(__name__)


@app.route('/')
def landing():
    return render_template('main.html')


@app.route('/authorize')
def authorize():
    if request.method == 'POST':
        code = request.args.get('code')
        post_data = dict(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            code=code,
            state=STATE,
        )
        resp = requests.post(post_data)
        print(resp.headers)
        return 'ok'

    params = dict(
        client_id=CLIENT_ID,
        state=STATE,
        scope=' '.join(SCOPES),
    )
    encoded_params = urllib.parse.urlencode(params)
    url = 'https://github.com/login/oauth/authorize?' + encoded_params
    return redirect(url)


@app.route('/callback')
def callback():
    return render_template('main.html')
