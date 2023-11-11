from highrollers_flask.card_deck import CardDeck
from highrollers_flask.random_api import RandomAPI
from highrollers_flask.games.BaseGame import BaseGame

class TestGame(BaseGame):
    def __init__(self, manager) -> None:
        super().__init__(manager)
        self.rand = RandomAPI()
        self.deck = CardDeck()
        self.discard = CardDeck()
        self.hand = CardDeck()
        self.deck.deck_gen(1)

    def handle_client_message(self, message):
        if "action" not in message:
            return {"Error": "No action given!"}
        
        if message["action"] == "draw":
            return self._draw_card_action(message)
        elif message["action"] == "discard":
            return self._discard_card_action(message)


    def _draw_card_action(self, message):
        if self.deck.remaining_count() == 0:
            self.discard.for_card(lambda card: self.deck.add_card(card))
            self.discard.empty()

        remaining_count = self.deck.remaining_count()
        card = self.deck.draw_card(self.rand.random_integer(0, remaining_count, 1)[0])

        self.hand.add_card(card)

        value = str(card)
        output = {"card":value}
        output.update(self._standard_response())
        return {"data":output}
    
    def _discard_card_action(self, message):
        if "card" not in message:
            return {"Error": "No card given!"}
        
        if message["card"] < 0 or message["card"] >= self.hand.remaining_count():
            return {"Error": "Invalid card given!"}
         
        card = self.hand.draw_card(message["card"])
        self.discard.add_card(card)
        output = {"card":str(card)}
        output.update(self._standard_response())
        return {"data":output}
    
    def _standard_response(self):
        return {"remaining":self.deck.remaining_count(), "discard":self.discard.remaining_count(), "hand":self.hand.remaining_count()}
