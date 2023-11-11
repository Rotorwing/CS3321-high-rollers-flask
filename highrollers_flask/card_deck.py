
from random_api import RandomAPI

from highrollers_flask import card

"""
Luna Steed
High Rollers CardDeck Class
Stores an array of 52 cards per deck, with all suits and values.
"""


class CardDeck:
    def __init__(self):
        self.deckarr = []
        self.random_api = RandomAPI()

    def deck_gen(self, decknum: int = 1):
        """
            Creates a number of decks given how many decks are to be made.

            :param int decknum: Number of decks to generate. Default is 1.
            """
        for x in range(13):
            for y in range(4 * decknum):
                if y % 4 == 0:
                    newcard = card.Card(x + 1, "Clubs")
                    self.deckarr.append(newcard)
                elif y % 4 == 1:
                    newcard = card.Card(x + 1, "Diamonds")
                    self.deckarr.append(newcard)
                elif y % 4 == 2:
                    newcard = card.Card(x + 1, "Hearts")
                    self.deckarr.append(newcard)
                elif y % 4 == 3:
                    newcard = card.Card(x + 1, "Spades") 
                    self.deckarr.append(newcard)

    def draw_card(self, index: int) -> card.Card:
        """
        :param index: The index of the card you wish to draw
        :return: The card at the given index
        """
        if len(self.deckarr) != 0:
            return self.deckarr.pop(index)
        else:
            raise IndexError("The card deck is empty. Please regenerate the deck using deck_gen.")
    
    def add_card(self, card: card.Card):
        """
        :param card: The card you wish to add to the deck
        """
        self.deckarr.append(card)
    
    def remaining_count(self) -> int:
        """
        :return: The number of cards remaining in the deck
        """
        return len(self.deckarr)

    def shuffel_deck(self):
        """calls random api to shuffle deck-Matthew Almgren"""
        n_cards = len(self.deckarr)
        random_indices = self.random_api.random_integer(0, n_cards -1, n_cards)
        shuffled_deck = [self.deckarr[i] for i in random_indices]
        self.deckarr = shuffled_deck