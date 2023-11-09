class BaseGame:
    def __init__(self, manager) -> None:
        self.manager = manager

    def handle_client_message(self, message):
        raise NotImplementedError("Override me!")