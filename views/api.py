from flask import Blueprint, jsonify
from hanabi.game_core import GameState


api_app = Blueprint('api', __name__)


@api_app.route("/")
def dunnoyet():
    game_state = GameState()
    return jsonify(game_state.as_dict())
