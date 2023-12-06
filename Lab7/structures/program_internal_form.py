from utils.enums import Token


class ProgramInternalForm:

    def __init__(self):
        self.__tokens = []

    @property
    def tokens(self) -> list[tuple[str, Token]]:
        """
        Returns a list of the tokens in the PIF.
        """
        return self.__tokens

    def __getitem__(self, index: int) -> str:
        return self.__tokens[index]

    def __add__(self, other):
        self.__tokens.extend(other)
        return self

    def insert(self, token: str, type_t: Token) -> None:
        """
        Adds a token in the PIF.
        :param token: the name of the token
        :param type_t: the type of the token as defined by Token
        """
        self.__tokens.append((token, type_t))

    def __str__(self):
        return '\n'.join(
            f"({e_token}, {e_type_t})" for e_token, e_type_t in self.__tokens
        )