# -*- coding: utf-8 -*-

from flask import Flask, render_template
from github import Github


app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('main.html')
