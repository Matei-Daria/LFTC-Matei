from enum import Enum


class Token(Enum):
    """
    The defined types of token.
    """
    IDENTIFIER = 1
    LITERAL = 2
    OPERATOR = 3
    SEPARATOR = 4
    RESERVED = 5

