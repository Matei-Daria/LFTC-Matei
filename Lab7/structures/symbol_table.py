from itertools import chain
from structures.hash_table import HashTable


class SymbolTable:

    def __init__(self, size):
        self.__table = HashTable(size)

    @property
    def table(self) -> list[tuple[str, any]]:
        """
        Returns a list with the tokens from the table.
        """
        return list(chain.from_iterable(self.__table.table))

    def get(self, token: str) -> any:
        """
        Get the value of a token.
        :param token: the name of the token
        :return: the value of the token
        """
        if not self.__table.search(token):
            raise ValueError(f"{self.get.__qualname__}:Token {token} is not declared.")
        return self.__table.get(token)

    def insert(self, token: str) -> None:
        """
        Insert a token into the table with the initial value "None".
        :param token: the name of the token
        """
        if self.__table.search(token):
            raise ValueError(f"{self.insert.__qualname__}:Token {token} is already declared.")
        self.__table.set(token, None)

    def delete(self, token: str) -> None:
        """
        Deletes a token from the table.
        :param token: the name of the token
        """
        if not self.__table.search(token):
            raise KeyError(f"{self.delete.__qualname__}:Token {token} is not declared.")
        self.__table.delete(token)

    def search(self, token: str) -> bool:
        """
        Searches for a token in the table.
        :param token: the name of the token
        :return: True -> if the token is in the table; False -> otherwise
        """
        return self.__table.search(token)

    def __str__(self):
        return str(self.__table)
