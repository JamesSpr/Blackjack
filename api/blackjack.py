import random
import math
import json

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
    def __init__(self, num_decks=1, cards=None, values=None):
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        self.values = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]

        self.cards = [Card(value, suit) for value in self.values for suit in suits for _ in range(num_decks)] if cards is None else cards

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
        card = self.cards.pop()
        return card
    
    def show(self, num_cards):
        return self.cards[:num_cards]

class Player:
    def __init__(self, id, hand=None, hand_value=0, outcome=""):
        self.id = id
        self.hand = [] if hand is None else hand
        self.hand_value = hand_value
        self.outcome = ""
        # self.actions = []

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class Blackjack:
    def __init__(self, num_players=1, num_decks=1, deck=None, dealer=None, players=None):
        self.deck = Deck(num_decks) if deck is None else deck
        self.dealer = Player("dealer") if dealer is None else dealer
        self.players = [Player(player) for player in range(num_players)] if players is None else players

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
        self.deal()
    
    def player_draw(self, playerId):
        player = self.players[playerId]
        new_card = self.deck.draw()
        player.hand.append(new_card)
        new_value = self.calculate_player_hand(player)
        player.hand_value = new_value
        

    def dealer_draw(self):
        while self.dealer.hand_value < 17:
            print(self.deck)
            new_card = self.deck.draw()
            self.dealer.hand.append(new_card)
            self.dealer.hand_value = self.calculate_player_hand(self.dealer)

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
    def set_player_outcomes(self):
        for player in self.players:
            if player.hand_value > 21: # Player Bust
                player.outcome = "Loss"
            
            if self.dealer.hand_value > 21: # Dealer Bust
                player.outcome = "Win"
            
            if player.hand_value > self.dealer.hand_value: # Player Higher
                player.outcome = "Win"
            
            if player.hand_value < self.dealer.hand_value: # Dealer Higher
                player.outcome = "Loss"
            
            if player.hand_value == self.dealer.hand_value: # Same
                player.outcome = "Draw"