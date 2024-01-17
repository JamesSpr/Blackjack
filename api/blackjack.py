import random
import math
import json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
bp = Blueprint('play', __name__, url_prefix='/play')

class Card:
    # Constructor
    def __init__(self, value, suit):
        self.suit = suit
        self.value = value
    
    # Display   
    def __repr__(self):
        return f"{self.value} of {self.suit}"
    
    def int_value(self, index):
        units = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
        return units[index]

class Deck:
    def __init__(self, num_decks, cards=None):
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        self.values = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]

        self.cards = cards
        if cards is None:
            self.cards = [Card(value, suit) for value in self.values for suit in suits for _ in range(num_decks)]

    def __repr__(self):
        return f"Deck containing {len(self.cards)} cards"
    
    def __len__(self):
        return len(self.cards)
    
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def shuffle(self, iterations=1):
        # Shuffle a number of times
        for _ in range(iterations):
            random.shuffle(self.cards)

        # Cut the deck after the shuffle
        split = math.floor(len(self.cards)/2)
        self.cards = self.cards[split:] + self.cards[:split]
    
    def draw(self):
        card = self.cards.pop(0)
        return card
    
    def show(self, num_cards):
        return self.cards[:num_cards]

class Player:
    def __init__(self, id):
        self.id = id
        self.hand = []
        self.hand_value = 0
        # self.actions = []

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class Blackjack:
    def __init__(self, players=1, decks=1):
        self.deck = Deck(decks)
        self.dealer = Player("dealer")
        self.players = [Player(player) for player in range(players)]

        # Shuffle the deck before starting
        self.deck.shuffle(5)
        self.deal()

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def deal(self):
        for player in self.players:
            player.hand.append(self.deck.draw())
            player.hand.append(self.deck.draw())

            player.hand_value = self.calculate_player_hand(player)
                    
        self.dealer.hand.append(self.deck.draw())
        self.dealer.hand.append(self.deck.draw())
        self.dealer.hand_value = self.calculate_player_hand(self.dealer)

    def reset(self):
        while len(self.dealer.hand) > 0:
            self.deck.cards.append(self.dealer.hand.pop())

        for player in self.players:
            while len(player.hand) > 0:
                self.deck.cards.append(player.hand.pop())

        self.deck.shuffle(3)

    def get_action(self):
        print(f"  What would you like to do (H/S): ", end="")
        action = input().lower()

        while action != "h" and action != "s":
            print(f"  Please enter a valid action: ", end="")
            action = input()

        return action
    
    def draw_card(player):
        game = request.json['body']['game']
        new_card = game.deck.draw()
        game.players[player].hand.append(new_card)
        new_value = game.calculate_player_hand(player)
        game.players[player].hand_value = new_value

        return game.players[player].toJson()
        


    def player_hit(self):
        player = request.json['body']['game']
        new_card = self.deck.draw()
        self.players[player].hand.append(new_card)
        new_value = self.calculate_player_hand(player)
        self.players[player].hand_value = new_value

        return self.players[player]
        
        # print(f"  HIT: {new_card} - {new_value}")
        # if player.id == "dealer":
        #     return

        # # Give option for another turn if not over 21
        # if new_value > 21:
        #     print("  BUST")
        #     return
        

    def play_dealer(self):
        dealer_value = self.calculate_player_hand(self.dealer)

        while dealer_value < 17:
            new_card = self.deck.draw()
            self.dealer.hand.append(new_card)
            dealer_value = self.calculate_player_hand(self.dealer)

        return dealer_value

    def calculate_player_hand(self, player):
        hand_value = 0
    
        # Dealer Rule: Dealer must count their first ace as 11
        if player.id == "dealer":
            ace_rule = False
            for card in player.hand:
                card_value = card.int_value(self.deck.values.index(card.value)) 
                if card_value == 1 and not ace_rule:
                    hand_value += 11
                    ace_rule = True
                else:
                    hand_value += card_value
            return hand_value
        
        
        num_aces = 0
        for card in player.hand:
            card_value = card.int_value(self.deck.values.index(card.value)) 
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
    
    # Returns integer outcome: 0 = loss, 1 = draw, 2 = win
    def determine_outcome(self, dealer_value):
        dealer_value = self.calculate_player_hand(self.dealer)

        for player in self.players:
            player_value = self.calculate_player_hand(player)

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

    def player_round(self, player):
        action = self.get_action()
        player.actions.append(action)
        self.perform_action(player, action)

        dealer_value = self.play_dealer()
        self.determine_outcome(dealer_value)

        self.reset()