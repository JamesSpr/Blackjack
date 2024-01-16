import random
import math

class Card:
    # Constructor
    def __init__(self, value, suit):
        self.suit = suit
        self.value = value
    
    # Display
    def __repr__(self):
        return f"{self.value} of {self.suit}"

class Deck:
    def __init__(self, num_decks):
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        values = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]

        self.cards = [Card(value, suit) for value in values for suit in suits for _ in range(num_decks)]

    def __repr__(self):
        return f"Deck containing {len(self.cards)} cards"
    
    def __len__(self):
        return len(self.cards)

    def shuffle(self, iterations=1):
        print(f"Shuffling deck {iterations} time" + ("s" if iterations > 1 else ""))
        for _ in range(iterations):
            random.shuffle(self.cards)
    
    def cut(self):
        split = math.floor(len(self.cards)/2)
        self.cards = self.cards[split:] + self.cards[:split]
    
    def draw(self):
        print(self.cards.pop(0))
    
    def show(self, num_cards):
        return self.cards[:num_cards]

class Player:
    def __init__(self, id):
        self.id = id
        self.hand = []
        self.actions = []

class Blackjack:
    def __init__(self, rounds, players=1, decks=1):
        self.deck = Deck(decks)
        self.rounds = rounds
        self.players = [Player(player) for player in range(players)]

        # Thoroughly shuffle and cut the deck before starting
        self.deck.shuffle(5)
        self.deck.cut()


if __name__ == "__main__":
    blackjack = Blackjack(5, 1, 1)