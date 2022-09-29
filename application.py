#!/usr/bin/env python3

from flask import Flask, session
from flask_session import Session

import sys
from os.path import abspath, dirname

# To be able to import when using running: './application.py'
sys.path.insert(0, dirname(dirname(abspath(__file__))))

from hanabi.views.api import api_app


app = Flask(__name__)

app.register_blueprint(api_app, url_prefix='/api')
app.config.from_object('hanabi.settings')

session_ = Session()
session_.init_app(app)


@app.route("/")
def root():
    return (
        '<p>'
            'TODOs:'
            '<br/>- main view'
            '<br/>- login / auth of some kind'
            '<br/>- game start'
            '<br/>- join game'
            '<br/>- game save'
            '<br/>- session'
            '<br/>- dockerfile and uwsgi'
        '</p>'
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
