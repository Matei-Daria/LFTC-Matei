from typing import Iterator


class Buffer:
    """
    A data structure only for reading. The data is given only at the beginning and then it's read with an iterator.
    """
    def __init__(self, data: str):
        self.__data = list(data)

    def iter(self) -> Iterator[str]:
        """
        Gets the next character in the buffer.
        :return: the first character in the stored data
        """
        while self.__data:
            yield self.__data[0]

    def erase(self) -> None:
        """
        Erases the characters that have been read.
        """
        self.__data.pop(0)

    def empty(self) -> bool:
        """
        Checks if the list of data is empty.
        :return: True -> if the list is empty; False -> otherwise
        """
        return True if not self.__data else False
