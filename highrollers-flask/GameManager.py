from random import randrange
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .games.test.TestGame import TestGame
from .games.blackjack.BlackjackGame import BlackjackGame
from .games.BaseGame import BaseGame

from django.core.handlers.wsgi import WSGIRequest

class GameManager:
    def __init__(self) -> None:
        self.games:dict[str, BaseGame] = {}
        self.ID_LENGTH = 10
    
    def new_game(self, game: str):
        """ Register a new game with a unique id"""
        id = ""
        while True:
            id = self._generate_id()
            if id not in self.games.keys():
                break
        
        self.games[id] = self._create_game_by_name(game)
        return id
    
    def delete_game(self, id:str) -> BaseGame:
        return self.games.pop(id)
    
    @csrf_exempt
    def handle_client_message(self, request:WSGIRequest, game:str):
        """Send the client's message to the appropriate game"""

        if (request.body == b''):
            return JsonResponse({"Error": "No body given!"})

        print(request.body)
        message = json.loads(request.body)
        print(message)

        response_message = ""
        if "data" in message and message["data"]:
            if "id" in message and message["id"] in self.games.keys():
                id =  message["id"]
                response_message = self.games[id].handle_client_message(message["data"])
            elif message["data"] == "newgame":
                id = self.new_game(game)
                response_message = {"id":id}
            else:
                response_message = {"Error": "No game with given ID found!"}
        else:
            response_message = {"Error": "No data given!"}
        
        return JsonResponse(response_message)
    
    def _create_game_by_name(self, name: str) -> BaseGame:
        if name == "test":
            return TestGame(self)
        elif name == "blackjack":
            return BlackjackGame(self)
        
    def _generate_id(self) -> str:
        """Generates a random ID for a game"""
        out = ""
        for i in range(self.ID_LENGTH):
            out+=self._generate_id_char()
        return out
    
    def _generate_id_char(self) -> str:
        r = randrange(10+26) # 10 numbers, 26*2 letters
        if (r < 10): return chr(r+48)
        else: return chr(r-10+97)