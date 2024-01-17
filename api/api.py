from flask import Flask, request, jsonify
from blackjack import Blackjack, Deck
import json

def create_app():
    app = Flask(__name__)
    blackjack = None

    @app.route("/blackjack")
    @app.route("/blackjack/<int:players>")
    def initialise_game(players):
        blackjack = Blackjack(players=players)
        return blackjack.toJson()

    @app.route("/draw/<int:player>", methods=('POST',))
    def draw_card(player):
        if request.method == 'POST':
            game = request.json['game']
            player = game['players'][player]
            new_card = game['deck']['cards'].pop()
            player['hand'].append(new_card)
            player['hand_value'] = calculate_player_hand(game, player)

            return jsonify({'player': player, 'deck': game['deck']})
        
        return None
    
    
    @app.route("/draw/dealer", methods=('POST',))
    def dealers_turn():
        if request.method == 'POST':
            game = request.json['game']
            dealer = game['dealer']
            while dealer['hand_value'] < 17:
                new_card = game['deck']['cards'].pop()
                dealer['hand'].append(new_card)
                dealer['hand_value'] = calculate_player_hand(game, dealer)

            outcome = []
            for player in game['players']:
                outcome.append(determine_outcome(game, player, dealer['hand_value']))

            return jsonify({'dealer': dealer, 'outcome': outcome})
        return None
    
    # @app.route("/reset", methods=('POST',))
    # def reset_game():
    #     if request.method == 'POST':
            # game = request.json['game']
            # deck = Deck(0, game['deck']['cards'])

            # while len(game['dealer']['hand']) > 0:
            #     deck.cards.append(game['dealer']['hand'].pop())

            # for player in game['players']:
            #     while len(player['hand']) > 0:
                    # deck.cards.append(player['hand'].pop())

            # deck.shuffle(3)
            # game['deck'] = json.loads(deck.toJson())
            # return jsonify(game)


    def calculate_player_hand(game, player):
        hand_value = 0
        card_ints = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    
        # Dealer Rule: Dealer must count their first ace as 11
        if player['id'] == "dealer":
            ace_rule = False
            for card in player['hand']:
                card_value = card_ints[game['deck']['values'].index(card['value'])]
                if card_value == 1 and not ace_rule:
                    hand_value += 11
                    ace_rule = True
                else:
                    hand_value += card_value

            return hand_value
        
        num_aces = 0
        for card in player['hand']:
            card_value = card_ints[game['deck']['values'].index(card['value'])]
            if card_value == 1:
                hand_value += 11
                num_aces += 1
            else: 
                hand_value += card_value

        # Count aces as 11, unless that makes the value exceed 21
        if hand_value > 21 and num_aces > 0:
            while num_aces > 0 and hand_value > 21:
                hand_value -= 10
                num_aces -= 1

        return hand_value
    
    def determine_outcome(game, player, dealer_value):
        player_value = calculate_player_hand(game, player)

        if player_value > 21: # Player Bust
            return 0
        
        if dealer_value > 21: # Dealer Bust
            return 2
        
        if player_value > dealer_value: # Player Higher
            return 2
        
        if player_value < dealer_value: # Dealer Higher
            return 0
        
        if player_value == dealer_value: # Same
            return 1
        
        return 1

    return app