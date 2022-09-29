#!/usr/bin/env python3

from flask import Flask
from views.api import api_app


app = Flask(__name__)
app.register_blueprint(api_app, url_prefix='/api')


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
            '<br/>- dockerfile and uwsgi'
        '</p>'
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
