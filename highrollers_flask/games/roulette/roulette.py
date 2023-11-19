import random_api
from highrollers_flask.games.BaseGame import BaseGame
"""
Luna Steed
High Rollers Roulette Class
Contains the logic for the game of Roulette.
"""

class Roulette:
    def __init__(self):
        """Initializing Function"""
        self.numsDict = {"red": [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 36],
                         "black": [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35],
                         "green": [0, 37],
                         "row 1": [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34],
                         "row 2": [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
                         "row 3": [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
                         "twelves 1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                         "twelves 2": [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
                         "twelves 3": [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36],
                         "first half": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
                         "second half": [19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36],
                         "evens": [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36],
                         "odds": [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35]
                         }
        self.rand = random_api.RandomAPI()
        self.wincount = 0

    def handle_client_message(self, message: dict):
        if "action" not in message:
            return {"Error": "No action given!"}

        if message["action"] == "spin":
            self._spin_action()
            for category in message["categories"].split(','):
                if self._check_bet(category):
                    self.wincount += 1

            for num in message["nums"].split(','):
                if self._check_nums(num):
                    self.wincount += 1

        retstr = self.wincount.__str__()

        self.wincount = 0

        return { "data":retstr }

    def _spin_action(self) -> int:
        """Generates a random number from 0 to 37, with 37 acting as 00."""
        self.spunnum = self.rand.random_integer(self, 0, 37, 1)[0]
        return self.spunnum

    def _check_bet(self, category: str) -> bool:
        """Checks the spun number against the dictionary given the category of bet made"""
        if self.spunnum is None:
            raise ValueError("Roulette wheel has not been spun yet!")
        if self.spunnum in self.numsDict.get(category):
            return True
        else:
            return False

    def _check_nums(self, numlist: list[int]) -> bool:
        """Checks the spun number against the given list of integers bet upon."""
        if self.spunnum is None:
            raise ValueError("Roulette wheel has not been spun yet!")
        if self.spunnum in numlist:
            return True
        else:
            return False

