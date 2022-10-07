from flask import Blueprint
from flask_login import login_required


base_app = Blueprint('base', __name__)


@base_app.route("/")
@login_required
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
