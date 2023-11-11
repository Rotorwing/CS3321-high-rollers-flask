from card_deck import CardDeck
"""
Is the hand of the player and dealer, also allows for adding a card
to the player or dealer hand- Matthew Almgren
"""
class Hand:
    
    def __init__(self):
        self.cards = []
        self.value = 0
    
    def add_card(self, card):
        self.cards.append(card)
        self.value += card.value

    def print_hand(self):
        print("Cards in hand:")
        for card in self.cards:
            print(f" - {card}")
        print(f"Total value: {self.value}")

"""
The win conditions for blackjack, dealer will draw tell their value is >= 17. 

Main return from class is bool. If player wins it returns
true if player loses it returns false. This bool will then be send to the front end
to be used to calculate bet -Matthew Almgren
"""

class WinConditions:
    def __init__(self, player_hand, dealer_hand,card_deck):
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand
        self.card_deck = card_deck
    
    def game_logic(self):
        if self.player_hand.value > 21:
            return False
        
        if self.player_hand.value <= 21:
            while self.dealer_hand.value < 17:
                self.dealer_hand.add_card(self.card_deck.draw_card(0))

            # Run different winning scenarios
            if self.dealer_hand.value > 21:
                return True

            elif self.dealer_hand.value > self.player_hand.value:
                return False

            elif self.dealer_hand.value < self.player_hand.value:
                return True

