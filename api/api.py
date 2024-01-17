from flask import Flask
from blackjack import Blackjack

def create_app():
    app = Flask(__name__)
    blackjack = None

    @app.route("/play")
    def initialise_game():
        blackjack = Blackjack(players=1)
        return blackjack.toJson()


    return app