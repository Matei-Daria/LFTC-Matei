

class LexicalErr(Exception):

    def __init__(self, message: str, line: int, name: str):
        self.message = message
        self.line = line
        self.name = name

    def __str__(self):
        return f"{self.name} raised {self.__class__.__name__}: line {self.line} : {self.message}"


class SyntacticalError(Exception):

    def __init__(self, message: str, name: str):
        self.message = message
        self.name = name

    def __str__(self):
        return f"{self.name} raised {self.__class__.__name__}: {self.message}"


class CompatibilityError(Exception):

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return f"{self.message}"
