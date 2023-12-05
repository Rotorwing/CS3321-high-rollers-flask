import pytest
import mock
from highrollers_flask.random_api import RandomAPI
from highrollers_flask.games.roulette.roulette import Roulette
from highrollers_flask.games.BaseGame import BaseGame
from highrollers_flask.GameManager import GameManager


def test_handle_client_message(mocker) -> None:
    """Unit test for the Handle Client Message function - LS"""
    mock_manage = mocker.patch.object(GameManager, "__init__", return_value=None)
    game = Roulette(mock_manage)
    message_1 = {"action": "spin", "categories": "row 1, row 2, row 3", "nums": []}
    message_2 = {"action": "spin", "categories": "red, black, green ", "nums": [1, 5, 10, 37]}
    message_3 = {"action": "spin"}

    mocked_spin = mocker.patch.object(Roulette, "_spin_action", return_value=14)
    game.spunnum = 14

    assert game.handle_client_message(message_1) == {"data": "1"}
    assert game.handle_client_message(message_2) == {"data": "1"}
    with pytest.raises(KeyError):
        game.handle_client_message(message_3)


def test_spin_action(mocker) -> None:
    """Unit test for the Spin Action function - LS"""
    mock_manage = mocker.patch.object(GameManager, "__init__", return_value=None)
    game = Roulette(mock_manage)
    mock_rand = mocker.patch.object(RandomAPI, "random_integer", return_value=[1])
    assert game._spin_action() == 1
    assert game.spunnum == 1


def test_check_bet(mocker) -> None:
    """Unit test for the Check Bet function - LS"""
    mock_manage = mocker.patch.object(GameManager, "__init__", return_value=None)
    game = Roulette(mock_manage)
    mock_category = "row 1"
    game.spunnum = 0
    assert game._check_bet(mock_category) is False

    game.spunnum = 1
    assert game._check_bet(mock_category) is True

    game.spunnum = None
    with pytest.raises(ValueError):
        game._check_bet(mock_category)

def test_check_nums(mocker) -> None:
    """Unit test for the Check Nums function - LS"""
    mock_manage = mocker.patch.object(GameManager, "__init__", return_value=None)
    game = Roulette(mock_manage)
    mocked_nums_empty = []
    mocked_nums = [1, 5, 9]
    game.spunnum = 0
    assert game._check_nums(mocked_nums_empty) is False

    game.spunnum = 1
    assert game._check_nums(mocked_nums) is True

    game.spunnum = None
    with pytest.raises(ValueError):
        game._check_nums(mocked_nums)
