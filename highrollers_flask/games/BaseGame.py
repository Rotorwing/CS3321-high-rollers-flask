class BaseGame:
    def __init__(self, manager) -> None:
        self.manager = manager

    def handle_client_message(self, message):
        raise NotImplementedError("Override me!")

    def game_init_message(self):
        raise NotImplementedError("Override me!")