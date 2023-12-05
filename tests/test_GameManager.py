from flask import Flask
from highrollers_flask import GameManager

import pytest
import mock
import json

@pytest.mark.parametrize("type", ["test", "blackjack"])
def test_new_game(type):
    """Tests that a new game is created -JS"""
    game_manager = GameManager.GameManager()
    id = game_manager.new_game(type)
    assert len(game_manager.games) == 1
    assert list(game_manager.games.values())[0].__class__.__name__ == type.capitalize() + "Game"
    assert id in game_manager.games.keys()

def test_delete_game():
    """Tests that a game is deleted -JS"""
    game_manager = GameManager.GameManager()
    id = game_manager.new_game("test")
    game_manager.delete_game(id)
    assert len(game_manager.games) == 0

@pytest.mark.parametrize("game", ["test", "blackjack"])
def test_handle_client_message_new_game(game):
    """Tests that a new game is created when the client sends a newgame message -JS"""
    app = Flask(__name__)
    with app.app_context():
        game_manager = GameManager.GameManager()
        mock_request = type('', (), dict(json={"data": "newgame"}))()
        keys = {}
        for i in range(100):
            response = game_manager.handle_client_message(mock_request, game)
            assert "id" in response.json
            assert len(response.json["id"]) == game_manager.ID_LENGTH
            assert response.json["id"] not in keys
            assert len(game_manager.games) == i + 1
            keys = list(game_manager.games.keys())[:]

@pytest.mark.parametrize("action", ["draw", "discard", "shuffle"])
def test_handle_client_message_action(mocker, action):
    app = Flask(__name__)
    with app.app_context():
        game = "test"
        game_handle_client_message_mock = mocker.patch.object(GameManager.GameManager, "handle_client_message")
        game_manager = GameManager.GameManager()
        id = game_manager.new_game(game)
        mock_request = type('', (), dict(json={"data": {"id": "123456", "action": action}}))()
        game_manager.handle_client_message(mock_request, game)
        game_handle_client_message_mock.assert_called_once()

def test_generate_id():
    """Tests that the id is generated correctly -JS"""
    game_manager = GameManager.GameManager()
    id = game_manager._generate_id()
    assert len(id) == game_manager.ID_LENGTH