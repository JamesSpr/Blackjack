from flask import Flask, request, jsonify
from blackjack import Blackjack, Deck, Player, Card
import json

def create_app():
    app = Flask(__name__)

    @app.route("/blackjack")
    @app.route("/blackjack/<int:players>")
    def initialise_game(players):
        blackjack = Blackjack(num_players=players)

        # Shuffle the deck before starting
        blackjack.deck.shuffle(5)
        blackjack.deal()

        return blackjack.toJson()

    @app.route("/draw/<int:player>", methods=('POST',))
    def draw_card(player):
        if request.method == 'POST':            
            blackjack = parse_game_from_json(request.json['game'])
            blackjack.player_draw(player)

            return blackjack.toJson()
                
        return None
    
    @app.route("/draw/dealer", methods=('POST',))
    def dealers_turn():
        if request.method == 'POST':
            blackjack = parse_game_from_json(request.json['game'])
            blackjack.dealer_draw()
            blackjack.set_player_outcomes()

            return blackjack.toJson()
        
        return None
    
    @app.route("/reset", methods=('POST',))
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