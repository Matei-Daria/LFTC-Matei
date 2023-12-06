
class HashTable:

    def __init__(self, size):
        self.size = size
        self.__table = [
            [] for _ in range(self.size)
        ]

    @property
    def table(self):
        return self.__table

    def hash(self, key):
        return sum([ord(letter) for letter in key]) % self.size

    def get(self, key):
        position = self.hash(key)

        for e_key, e_value in self.__table[position]:
            if key == e_key:
                return e_value
        return None

    def set(self, key, value):
        position = self.hash(key)
        pair = (key, value)
        position_list = self.__table[position]

        if pair in position_list:
            position_list.remove(pair)
        position_list.append(pair)

    def delete(self, key):
        position = self.hash(key)
        position_list = self.__table[position]

        for idx, tuple in enumerate(position_list):
            if key == tuple[0]:
                position_list.pop(idx)
                break

    def search(self, key):
        position = self.hash(key)

        for e_key, _ in self.__table[position]:
            if e_key == key:
                return True
        return False
