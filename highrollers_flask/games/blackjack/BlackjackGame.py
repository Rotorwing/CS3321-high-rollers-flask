from ..BaseGame import BaseGame

from highrollers_flask.card_deck import CardDeck
from highrollers_flask.random_api import RandomAPI
from highrollers_flask.games.BaseGame import BaseGame

class BlackjackGame(BaseGame):
    def __init__(self, manager) -> None:
        super().__init__(manager)
        self.rand = RandomAPI()

        self.deck = CardDeck()
        self.discard = CardDeck()
        self.player = CardDeck()
        self.dealer = CardDeck()
        self.deck.deck_gen(1)

        self.DECK_SHUFFLE_CUTOFF = 10
    
    def shuffle(self):
        """Shuffles the deck and resets the discard pile -JS"""
        self.deck.deck_gen(1)
        self.discard.empty()
        self.deck.shuffle_deck()

    def deck_value(self, deck: CardDeck):
        """Calculates the value of a deck or hand -JS"""
        total = 0
        aces = 0
        for card in deck.get_deck():
            if card.value > 10:
                total += 10
            else:
                total += card.value
            if card.value == 1:
                aces += 1
        
        while aces > 0:
            if total + 10 <= 21:
                total += 10
            aces -= 1
        return total
    
    def check_bust(self, deck):
       """Checks if a deck is over 21 -JS"""
       return self.deck_value(deck) > 21
    
    def player_hit(self):
        """Deals a card to the player -JS"""
        if self.deck.remaining_count() == 0:
            self.shuffle()

        card = self.deck.deal()
        self.player.add_card(card)
        # Convert the card to a string or a dictionary format
        return {"card": str(card)}
    
    def dealer_hit(self):
        """Deals a card to the dealer -JS"""
        if self.deck.remaining_count() == 0:
            self.shuffle()

        card = self.deck.deal()
        self.dealer.add_card(card)
        return {"card": str(card)}
    
    def dealer_turn(self):
        """If dealers hand is <= to 17 dealer hits-MJ"""
        if self.deck_value(self.dealer) <= 17:
            self.dealer_hit()

    
    def round_setup(self):
        """Sets up a new round by drawing the starting cards -JS"""
        self.player.empty()
        self.dealer.empty()
        self.player_hit()
        self.player_hit()
        self.dealer_hit()
        self.dealer_hit()
    
    def pack_deck_data(self, deck: CardDeck, hide_first: bool = False):
        """ Packs a deck into an array of strings to be sent to the front-end -JS
        :param deck: The deck to pack
        :param hide_first: Set true to make the first card face-down
        :return: An array of strings representing the deck
        """

        arr = (str(card) for card in deck.get_deck())
        if hide_first:
            arr[0] = "B"
        return arr
    
    def send_game_state(self, hide_dealer_card: bool = False):
        """Sends the current game state to the front-end -JS"""
        return {
            "player":self.pack_deck_data(self.player),
            "dealer":self.pack_deck_data(self.dealer, hide_dealer_card),
            "player_value":self.deck_value(self.player),
            "dealer_value":self.deck_value(self.dealer),
            "remaining":self.deck.remaining_count()
            }
    
    def calculate_winner(self):
        player_value = self.deck_value(self.player)
        dealer_value = self.deck_value(self.dealer)

        if player_value > dealer_value:
            return "player"
        elif dealer_value > player_value:
            return "dealer"
        return "tie"
    
    def continue_round(self):
        """Finishes the rest of the round after the player stands, after player stands dealer has a chance to hit, if dealer does
        it checks dealers hand to see if they busted. If they busted it returns player indicating player win.
        If not it checks to see if the player wins-MJ"""
        self.dealer_turn()

        self.send_game_state(False)

        if self.check_bust(self.dealer):
            return "player"
        else:
            results = self.calculate_winner()
            return results
    
    

    def game_init_message(self):
        """Starts a new game of blackjack -JS"""
        self.round_setup()
        return {
            "id": self.id,  # Assuming each game has a unique ID
            "player_cards": [str(card) for card in self.player.get_deck()],
            "dealer_cards": ["B"] + [str(card) for card in self.dealer.get_deck()[1:]],  # Hide first dealer card
            "player_value": self.deck_value(self.player),
            "dealer_value": self.deck_value(self.dealer, hide_first=True),
            "remaining": self.deck.remaining_count()
        }
    
    def handle_client_message(self, message):
        if "action" not in message:
            return {"Error": "No action given!"}
        
        if message["action"] == "hit":
            return self.player_hit()
        elif message["action"] == "stand":
            return self.continue_round()