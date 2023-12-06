from typing import IO

from utils.error import LexicalErr
from utils.grammar import *
from structures.program import Program
from structures.buffer import Buffer
from utils.enums import *


class Scanner:
    """
    Lexical validator for an input program.
    """
    def __init__(self, file: IO):
        self.__buffer = Buffer(file.read())
        self.__program = Program()
        self.__line = 1

    def _scan_string(self, token: str) -> str:
        """
        Checks if the token for a string is correct.
        :param token: the starting character
        :return: the valid string scanned
        :raise: LexicalErr if the string doesn't respect the grammar
        """
        if self.__buffer.empty():
            raise LexicalErr(f"Final string quote (\") not detected.",
                             self.__line, self._scan_string.__qualname__)

        char = next(self.__buffer.iter())
        while True:

            if char == STR_QUOTE:
                token += char
                self.__buffer.erase()
                return token

            elif char not in LETTER + DIGIT + SPECIAL:
                raise LexicalErr(f"'{char}' is not a valid string character.",
                                 self.__line, self._scan_string.__qualname__)

            token += char
            self.__buffer.erase()

            try:
                char = next(self.__buffer.iter())
            except StopIteration:
                break

        raise LexicalErr(f"Final string quote (\") not detected.",
                         self.__line, self._scan_string.__qualname__)

    def _scan_integer(self, token: str) -> str:
        """
        Checks if the token for an integer is correct.
        :param token: the starting integer
        :return: the valid integer scanned
        :raise: LexicalErr if the integer doesn't respect the grammar
        """

        if self.__buffer.empty():
            return token

        char = next(self.__buffer.iter())

        if token == ZERO_DIGIT and char not in WHITESPACE + SEPARATORS + OPERATORS:
            raise LexicalErr(f"0 cannot be at the beginning of an integer.",
                             self.__line, self._scan_integer.__qualname__)

        while True:

            if char in WHITESPACE + SEPARATORS + OPERATORS:
                return token

            elif char in DIGIT:
                token += char
                self.__buffer.erase()

            else:
                raise LexicalErr(f"'{char}' is not a valid integer digit.",
                                 self.__line, self._scan_integer.__qualname__)

            try:
                char = next(self.__buffer.iter())
            except StopIteration:
                break

        return token

    def _scan_operator(self, token: str) -> str:
        """
        Checks if the token for an operator is correct.
        :param token: the start of the operator
        :return: the valid operator scanned
        """

        if self.__buffer.empty():
            return token

        char = next(self.__buffer.iter())

        if token + char in OPERATORS:
            self.__buffer.erase()
            return token + char

        return token

    def _scan_word(self, token: str) -> str:
        """
        Checks if the token for a word is correct.
        :param token: the beginning character of the word
        :return: the valid word scanned
        """

        if self.__buffer.empty():
            return token

        char = next(self.__buffer.iter())
        while True:

            if char in LETTER + DIGIT + SPECIAL:
                token += char
                self.__buffer.erase()

            else:
                return token

            try:
                char = next(self.__buffer.iter())
            except StopIteration:
                break

        return token

    def scan(self) -> Program:
        """
        Scans the entire input program and checks its grammar. Creates the ProgramInternalForm,
        IdentifierSymbolTable and LiteralSymbolTable under a single entity, Program.
        :return: the complete and lexically validated program
        :raise: LexicalErr if a lexical error was found
        """
        if self.__buffer.empty():
            return self.__program

        char = next(self.__buffer.iter())
        while char:
            self.__buffer.erase()

            if char in WHITESPACE:
                if char == NEW_LINE:
                    self.__line += 1

            elif char == STR_QUOTE:
                token = self._scan_string(char)

                if not self.__program.literal_table.search(token):
                    self.__program.literal_table.insert(token)
                self.__program.pif.insert(token, Token.LITERAL)

            elif char in DIGIT:
                token = self._scan_integer(char)

                if not self.__program.literal_table.search(token):
                    self.__program.literal_table.insert(token)
                self.__program.pif.insert(token, Token.LITERAL)

            elif char in OPERATORS_START:
                token = self._scan_operator(char)

                self.__program.pif.insert(token, Token.OPERATOR)

            elif char in SEPARATORS:
                self.__program.pif.insert(char, Token.SEPARATOR)

            elif char in LETTER:
                token = self._scan_word(char)

                if token in RESERVED:
                    self.__program.pif.insert(token, Token.RESERVED)
                else:
                    if not self.__program.identifier_table.search(token):
                        self.__program.identifier_table.insert(token)
                    self.__program.pif.insert(token, Token.IDENTIFIER)

            else:
                raise LexicalErr(f"Unexpected character {char}", self.__line, self.scan.__qualname__)

            try:
                char = next(self.__buffer.iter())
            except StopIteration:
                break

        return self.__program
