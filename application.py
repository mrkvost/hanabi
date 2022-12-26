#!/usr/bin/env python3

from flask import (
    Flask,
    session,
    redirect,
    url_for,
    request,
    abort,
)
from flask_session import Session
from flask_login import LoginManager


from http import HTTPStatus

import sys
import os
from os.path import abspath, dirname

# To be able to import when using running: './application.py'
sys.path.insert(0, dirname(dirname(abspath(__file__))))

from hanabi.views.api import api_app
from hanabi.views.base import base_app
from hanabi.views.auth import auth_app, csrf

from hanabi.models import User


app = Flask(__name__)

# app.config.from_prefixed_env(prefix='HANABI')
app.config.from_object('hanabi.settings')

app.register_blueprint(base_app, url_prefix='')
app.register_blueprint(api_app, url_prefix='/api')
app.register_blueprint(auth_app, url_prefix='/auth')

session_ = Session()
session_.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

csrf.init_app(app)
csrf.exempt('auth.login')
csrf.exempt('auth')
csrf.exempt('app.auth')
csrf.exempt(auth_app)


@login_manager.user_loader
def load_user(user_id):
    if int(user_id) == 1:
        return User()
    return None


@login_manager.unauthorized_handler
def unauthorized():
    if request.blueprint == 'api':
        abort(HTTPStatus.UNAUTHORIZED)
    return redirect(url_for('auth.login'))


# @login_manager.request_loader
# def load_user_from_request(req):
#     return None


def run():
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    run()
