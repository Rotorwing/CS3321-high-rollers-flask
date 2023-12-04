import pytest
import mock
from highrollers_flask.card import Card
from highrollers_flask.card_deck import CardDeck
from highrollers_flask.random_api import RandomAPI

def test_deck_gen() -> None:
    """Unit test for the Deck Gen function to ensure it is generating the right
    amount of cards and also generating different values and suits.- LS"""
    deck = CardDeck()
    deck.deck_gen(1)
    assert len(deck.deckarr) == 52
    assert deck.deckarr[0].value == 1
    assert deck.deckarr[0].suit == "C"
    assert deck.deckarr[51].value == 13
    assert deck.deckarr[51].suit == "S"
    deck.deck_gen(2)
    assert len(deck.deckarr) == 104
    assert deck.deckarr[52].value == 1
    assert deck.deckarr[52].suit == "C"
    assert deck.deckarr[103].value == 13
    assert deck.deckarr[103].suit == "S"

def test_deck_gen_exception() -> None:
    """Unit test for the Deck Gen function to ensure it catches invalid input - LS"""
    deck = CardDeck()
    with pytest.raises(ValueError):
        deck.deck_gen(0)
    with pytest.raises(ValueError):
        deck.deck_gen(-1)

def test_draw_card(mocker) -> None:
    """Unit test for the Draw Card function - LS"""
    deck = CardDeck()
    mock_card = mocker.patch.object(Card, "__init__", return_value=None)
    deck.deckarr.append(mock_card)
    card = deck.draw_card(0)
    assert card == mock_card

def test_draw_card_exception() -> None:
    """Unit test for the Draw Card function to ensure it catches invalid input - LS"""
    deck = CardDeck()
    with pytest.raises(IndexError):
        deck.draw_card(0)
    with pytest.raises(IndexError):
        deck.draw_card(-1)
    with pytest.raises(IndexError):
        deck.draw_card(1)

def test_add_card(mocker) -> None:
    """Unit test for the Add Card function - LS"""
    deck = CardDeck()
    mock_card = mocker.patch.object(Card, "__init__", return_value=None)
    deck.add_card(mock_card)
    assert deck.deckarr[0] == mock_card

def test_remaining_count(mocker) -> None:
    """Unit test for the Remaining Count function - LS"""
    deck = CardDeck()
    mock_card = mocker.patch.object(Card, "__init__", return_value=None)
    deck.deckarr.append(mock_card)
    assert deck.remaining_count() == 1
    deck.deckarr.append(mock_card)
    assert deck.remaining_count() == 2
    deck.deckarr.pop(0)
    assert deck.remaining_count() == 1
    deck.deckarr.pop(0)
    assert deck.remaining_count() == 0

def test_deal(mocker) -> None:
    """Unit test for the Deal function to ensure it is returning the correct card - LS"""
    deck = CardDeck()
    mock_card = mocker.patch.object(Card, "__init__", return_value=None)
    deck.deckarr.append(mock_card)
    card = deck.deal()
    assert card == mock_card

def test_shuffle_deck() -> None:
    """Unit test for the Shuffle Deck function - LS"""
    deck = CardDeck()
    deck.deck_gen(1)
    first_card = deck.deckarr[0]
    deck.shuffle_deck()
    assert first_card != deck.deckarr[0]

def test_peek(mocker) -> None:
    """Unit test for the Peek function to ensure it is returning the correct card - LS"""
    deck = CardDeck()
    mock_card = mocker.patch.object(Card, "__init__", return_value=None)
    deck.deckarr.append(mock_card)
    card = deck.peek()
    assert card == mock_card
    assert len(deck.deckarr) == 1

def test_get_deck() -> None:
    """Unit test for the Get Deck function to ensure it is returning the deck - LS"""
    deck = CardDeck()
    deck.deck_gen(1)
    assert deck.get_deck() == deck.deckarr