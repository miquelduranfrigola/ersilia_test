from .exceptions import ErsiliaError

class ClearErsiliaError(ErsiliaError):
    def __init__(self):
        self.message = "Error occured while running clear command"
        self.hints = ""
        super().__init__(self.message, self.hints)