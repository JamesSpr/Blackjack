from flask import Flask, request
from blackjack import Blackjack, Deck, Player, Card
import json

# from flask_cors import CORS, cross_origin

def create_app():
    app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
    # cors = CORS(app=app, origins="https://blackjack-demo-dev.vercel.app/")

    @app.route("/")
    def index():
        return app.send_static_file('index.html')
    
    @app.route("/blackjack", methods=['GET', 'OPTIONS'])
    @app.route("/blackjack/<int:players>", methods=['GET', 'OPTIONS'])
    def initialise_game(players):
        blackjack = Blackjack(num_players=players)

        # Shuffle the deck before starting
        blackjack.deck.shuffle(5)
        blackjack.deal()

        return blackjack.toJson()

    @app.route("/blackjack/draw/<int:player>", methods=('POST', 'OPTIONS'))
    def draw_card(player):
        if request.method == 'POST':            
            blackjack = parse_game_from_json(request.json['game'])
            blackjack.player_draw(player)

            return blackjack.toJson()
                
        return None
    
    @app.route("/blackjack/draw/dealer", methods=('POST',))
    def dealers_turn():
        if request.method == 'POST':
            blackjack = parse_game_from_json(request.json['game'])
            blackjack.dealer_draw()
            blackjack.set_player_outcomes()

            return blackjack.toJson()
        
        return None
    
    @app.route("/blackjack/reset", methods=('POST',))
    def reset_game():
        if request.method == 'POST':
            blackjack = parse_game_from_json(request.json['game'])
            blackjack.reset()
            return blackjack.toJson()

    def parse_game_from_json(json_str):
        game_str = json.dumps({'blackjack': json_str})
        return json.loads(game_str, object_hook=game_loader)['blackjack']

    def game_loader(game):
        if 'blackjack' in game:
            game['blackjack'] = Blackjack(**game['blackjack'])
            return game
        elif 'deck' in game:
            for idx, _ in enumerate(game['deck']['cards']):
                game['deck']['cards'][idx] = Card(**game['deck']['cards'][idx])

            game['deck'] = Deck(**game['deck'])

            if 'players' in game:
                for idx, player in enumerate(game['players']):
                    for card_idx, _ in enumerate(player['hand']):
                        game['players'][idx]['hand'][card_idx] = Card(**game['players'][idx]['hand'][card_idx])

                    game['players'][idx] = Player(**game['players'][idx])

                if 'dealer' in game:
                    for idx, _ in enumerate(game['dealer']['hand']):
                        game['dealer']['hand'][idx] = Card(**game['dealer']['hand'][idx])

                    game['dealer'] = Player(**game['dealer'])
                    return game
                
            return game
        else:
            return game

    return app
