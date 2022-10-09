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
