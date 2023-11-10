"""
Luna Steed
High Rollers Card Class
This class facilitates cards for all card games.
Very simply, it is a container to keep both an integer and a character.
"""


class Card:
    def __init__(self, val: int, suit: str):
        self.value = self._is_valid_value(val)
        self.suit = self._is_valid_suit(suit)

# ls f23
# Validates card value
    @staticmethod
    def _is_valid_value(val: int):
        if val < 1 or val > 13:
            raise ValueError("Card value must be within 1 and 13, including 1 and 13.")
        return val

# ls f23
# Validates card suit based on first letter
    @staticmethod
    def _is_valid_suit(suit: str):
        if suit[0].capitalize() == "C":
            return "C"
        if suit[0].capitalize() == "D":
            return "D"
        if suit[0].capitalize() == "H":
            return "H"
        if suit[0].capitalize() == "S":
            return "S"
        else:
            raise ValueError("Please input a valid choice: (C)lubs, (D)iamonds, (H)earts, (S)pades.")

# ls f23
# Returns the value and suit
    def __str__(self):
        if 10 >= self.value > 1:
            return f'{self.value}{self.suit}'
        elif self.value == 1:
            return f'A{self.suit}'
        elif self.value == 11:
            return f'J{self.suit}'
        elif self.value == 12:
            return f'Q{self.suit}'
        elif self.value == 13:
            return f'K{self.suit}'
