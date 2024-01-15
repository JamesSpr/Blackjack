import random

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

    def shuffle(self, iterations=1):
        print(f"Shuffling deck {iterations} time" + ("s" if iterations > 1 else ""))
        for _ in range(iterations):
            random.shuffle(self.cards)
    
    def draw(self):
        print(self.cards.pop(0))
    
    def show(self, num_cards):
        return self.cards[:num_cards]


if __name__ == "__main__":
    deck = Deck(2)
    print(deck)
    print(deck.show(4))
    deck.shuffle()
    print(deck.show(8))
    deck.shuffle(4)
    print(deck.show(8))
    deck.draw()
    deck.draw()
    deck.draw()
    deck.draw()
    print(deck.show(8))