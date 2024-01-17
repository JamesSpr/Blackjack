from flask import Flask
from blackjack import Blackjack, bp as blackjack_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(blackjack_bp)

    @app.route("/blackjack")
    @app.route("/blackjack/<int:players>")
    def initialise_game(players=1):
        blackjack = Blackjack(players)
        return blackjack.toJson()

    return app