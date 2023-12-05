import pytest
import mock
from highrollers_flask.card import Card

def test_init(mocker) -> None:
    """Unit test for the Card class to check if it initializes correctly - LS"""
    mocked_cardval = mocker.patch.object(Card, "_is_valid_value", return_value=1)
    mocked_cardsuit = mocker.patch.object(Card, "_is_valid_suit", return_value="C")
    card = Card(mocked_cardval, mocked_cardsuit)
    assert card.value == 1
    assert card.suit == "C"
def test_is_valid_value() -> None:
    """Unit test for the Is Valid Value function to check if it returns valid inputs - LS"""
    for i in range(1, 14):
        val = Card._is_valid_value(i)
        assert val == i

def test_is_valid_value_exception() -> None:
    """Unit test for the Is Valid Value function to check if it catches invalid input - LS"""
    with pytest.raises(ValueError):
        Card._is_valid_value(0)
    with pytest.raises(ValueError):
        Card._is_valid_value(14)

def test_is_valid_suit() -> None:
    """Unit test for the Is Valid Suit function to check if it returns valid inputs - LS"""
    suits = ["C", "D", "H", "S"]
    for suit in suits:
        val = Card._is_valid_suit(suit)
        assert val == suit

def test_is_valid_suit_exception() -> None:
    """Unit test for the Is Valid Suit function to check if it catches invalid input - LS"""
    with pytest.raises(ValueError):
        Card._is_valid_suit("X")

def test_str() -> None:
    """Unit test for the __str__ override to check if it returns the correct strings.
     Checks each suit and each face card and ace - LS"""
    card = Card(1, "C")
    assert str(card) == "AC"
    card = Card(2, "D")
    assert str(card) == "2D"
    card = Card(10, "H")
    assert str(card) == "10H"
    card = Card(11, "S")
    assert str(card) == "JS"
    card = Card(12, "C")
    assert str(card) == "QC"
    card = Card(13, "D")
    assert str(card) == "KD"