from highrollers_flask import card
from highrollers_flask import random_api

"""
Luna Steed
High Rollers CardDeck Class
Stores an array of 52 cards per deck, with all suits and values.
"""


class CardDeck:
    def __init__(self):
        self.deckarr = []
        self.rand = random_api.RandomAPI

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

    def deal(self):
        """pops a card off the top of the stack to be dealed to player-MJ"""
        return self.draw_card(0)

    def shuffle_deck(self):
        """calls random api to shuffle deck-MJ"""
        n_cards = len(self.deckarr)
        random_indices = self.rand.random_integer(0, n_cards - 1, n_cards)
        shuffled_deck = [self.deckarr[i] for i in random_indices]
        self.deckarr = shuffled_deck

    def peek(self, index: int = 0) -> card:
        """
        Peeks either the top card or a card at a given index LS
        :param index: optional index
        :return: card at index
        """
        peekcard = self.deckarr[index]
        return peekcard

    def get_deck(self) -> list:
        """
        Simple method for grabbing the list LS
        :return: a list of cards
        """
        return self.deckarr

    def __str__(self):
        """
        Defines how to display deck as a string LS
        :return: Display string
        """
        ret_str = ""
        for i in range(self.remaining_count() - 1):
            ret_str += self.deckarr[i]
            ret_str += ", "
        ret_str += self.deckarr[-1]
        return ret_str
