from flask import Blueprint, render_template
from flask_login import login_required


base_app = Blueprint('base', __name__)


@base_app.route("/")
@login_required
def index():
    return render_template('index.html')


@base_app.route("/game")
@login_required
def game():
    return render_template('game.html')


@base_app.route("/new_game")
@login_required
def new_game():
    return render_template('new_game.html')


@base_app.route("/join_game")
@login_required
def join_game():
    return render_template('join_game.html')
