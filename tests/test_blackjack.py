from highrollers_flask.games.blackjack.BlackjackGame import BlackjackGame
from unittest.mock import Mock
from highrollers_flask.card_deck import CardDeck
from highrollers_flask.card import Card

import pytest
import mock

@pytest.fixture
def blackjack_game_instance():
    """Checks if the BlackjackGame initializes with the necessary attributes -MJ"""
    return BlackjackGame(manager=Mock())

def test_initialization_creation(blackjack_game_instance):
    """Verifies if the shuffle method calls the deck's shuffle_deck method -MJ"""
    assert isinstance(blackjack_game_instance.player, CardDeck)
    assert isinstance(blackjack_game_instance.deck, CardDeck)
    assert isinstance(blackjack_game_instance.dealer, CardDeck)
    assert isinstance(blackjack_game_instance.discard,CardDeck)

def test_shuffle(blackjack_game_instance):
    """Tests the calculation of hand value without aces present -MJ"""
    blackjack_game_instance.deck.shuffle_deck=Mock()
    blackjack_game_instance.shuffle()
    blackjack_game_instance.deck.shuffle_deck.assert_called_once()

def test_deck_value_no_aces(blackjack_game_instance):
    """Tests the calculation of hand value without aces present -MJ"""
    deck = CardDeck()
    deck.add_card(Card(10,'s'))
    deck.add_card(Card(7,'s'))
    value = blackjack_game_instance.deck_value(deck)
    assert value == 17

def test_deck_value_with_aces(blackjack_game_instance):
    """Tests the calculation of hand value with aces present -MJ"""
    deck = CardDeck()
    deck.add_card(Card(1, 'Hearts'))  
    deck.add_card(Card(9, 'Diamonds'))  
    value = blackjack_game_instance.deck_value(deck)
    assert value == 20  

def test_check_bust(blackjack_game_instance):
    """Verifies the bust condition for a given deck -MJ"""
    deck = CardDeck()
    deck.add_card(Card(10,'s'))
    deck.add_card(Card(7,'s'))
    deck.add_card(Card(10,'s'))
    deck.add_card(Card(7,'s'))
    blackjack_game_instance.check_bust(deck) == True

def test_player_hit(blackjack_game_instance):
    """Checks if the player successfully receives a card upon hitting -MJ"""
    assert blackjack_game_instance.player.remaining_count() == 0
    blackjack_game_instance.player_hit()
    assert blackjack_game_instance.player.remaining_count()==1

def  test_dealer_turn(blackjack_game_instance):
    """Ensures the dealer successfully receives a card during its turn -MJ"""

    assert blackjack_game_instance.dealer.remaining_count() == 0
    blackjack_game_instance.dealer_hit()
    assert blackjack_game_instance.dealer.remaining_count()==1

def test_round_setup(blackjack_game_instance):
    """Verifies the setup of the round by checking initial card distribution -MJ"""

    blackjack_game_instance.round_setup()
    assert blackjack_game_instance.player.remaining_count() == 2
    assert blackjack_game_instance.player.remaining_count() == 2

def test_pack_data(blackjack_game_instance):
    """Tests the packing of the deck data for front-end display -MJ"""
    blackjack_game_instance.round_setup()
    dealer_deck = blackjack_game_instance.dealer
    dealer_packed = blackjack_game_instance.pack_deck_data(dealer_deck, hide_first = True)
    assert dealer_packed[0] == "B"
    
def test_send_game_state(blackjack_game_instance):
    """Checks the formatting of the game state data sent to the front-end -MJ"""
    blackjack_game_instance.round_setup()
    game_state = blackjack_game_instance.send_game_state()
    assert "player" in game_state
    assert "dealer" in game_state
    assert "player_value" in game_state
    assert "dealer_value" in game_state
    assert "remaining" in game_state

    assert isinstance(game_state["player"], list)  
    assert isinstance(game_state["dealer"], list)  
    assert isinstance(game_state["player_value"], int)  
    assert isinstance(game_state["dealer_value"], int)  
    assert isinstance(game_state["remaining"], int)

def test_calculate_winner_player(blackjack_game_instance):
    """Ensures correct determination of winner when player wins -MJ"""
    blackjack_game_instance.player.add_card(Card(10,'s'))

    blackjack_game_instance.dealer.add_card(Card(5,'s'))

    assert blackjack_game_instance.calculate_winner() == "player"

def test_calculate_winner_dealer(blackjack_game_instance):
    """Ensures correct determination of winner when dealer wins -MJ"""
    blackjack_game_instance.dealer.add_card(Card(10,'s'))

    blackjack_game_instance.player.add_card(Card(5,'s'))

    assert blackjack_game_instance.calculate_winner() == "dealer"

def test_game_init_message(blackjack_game_instance):
    """Tests the initialization message returned when starting a game -MJ"""
    game_state = blackjack_game_instance.game_init_message()

    assert "player" in game_state
    assert "dealer" in game_state
    assert "player_value" in game_state
    assert "dealer_value" in game_state
    assert "remaining" in game_state

    assert isinstance(game_state["player"], list)  
    assert isinstance(game_state["dealer"], list)  
    assert isinstance(game_state["player_value"], int)  
    assert isinstance(game_state["dealer_value"], int)  
    assert isinstance(game_state["remaining"], int)  

    assert game_state["dealer"][0] == "B" 

def test_handle_client_message_no_action(blackjack_game_instance):
    """Verifies error message handling when no action is given in a message -MJ"""

    message = {"key": "value"}
    result = blackjack_game_instance.handle_client_message(message)
    assert result == {"Error": "No action given!"}

def test_handle_client_message_hit_given(blackjack_game_instance):
    """Checks if the player successfully receives a card when hit action is given -MJ"""
    message = {"action": "hit"}
    assert blackjack_game_instance.player.remaining_count() == 0
    result = blackjack_game_instance.handle_client_message(message)
    assert blackjack_game_instance.player.remaining_count() == 1

def test_handle_client_message_stand(blackjack_game_instance):
    """Ensures the dealer receives a card when the stand action is given -MJ"""
    message = {"action": "stand"}
    assert blackjack_game_instance.dealer.remaining_count() == 0
    result = blackjack_game_instance.handle_client_message(message)
    assert blackjack_game_instance.dealer.remaining_count() == 1