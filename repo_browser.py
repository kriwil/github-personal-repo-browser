# -*- coding: utf-8 -*-

from collections import namedtuple
import os
import urllib.parse

from flask import Flask, render_template, redirect, request, session, abort, url_for
from github import Github
import requests


CLIENT_ID = os.environ['GITHUB_CLIENT_ID']
CLIENT_SECRET = os.environ['GITHUB_CLIENT_SECRET']
SCOPES = ['repo']
STATE = 'supercalifragilisticexpialidocious'
BASE_URL = 'https://github-personal-repo-browser.herokuapp.com'
ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'

UserData = namedtuple('UserData', ['username', 'avatar_url'])
RepoData = namedtuple('RepoData', ['name', 'url'])

app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY']


@app.route('/')
def landing():
    return render_template('main.html')


@app.route('/authorize')
def authorize():
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
    code = request.args.get('code')
    post_data = dict(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        code=code,
        state=STATE,
    )
    url = ACCESS_TOKEN_URL
    headers = dict(
        accept='application/json',
    )
    resp = requests.post(url, post_data, headers=headers)
    data = resp.json()
    if 'error' in data:
        return redirect(url_for('authorize'))

    session['github_access_token'] = data['access_token']
    return redirect(url_for('content'))


@app.route('/content')
def content():
    if not session['github_access_token']:
        return redirect(url_for('authorize'))

    access_token = session['github_access_token']
    github = Github(access_token)
    user = github.get_user()
    user_data = UserData(username=user.login, avatar_url=user.avatar_url)
    repositories = [RepoData(name=repo.name, url=repo.html_url) for repo in user.get_repos()]

    return render_template('content.html', user=user_data, repositories=repositories)

