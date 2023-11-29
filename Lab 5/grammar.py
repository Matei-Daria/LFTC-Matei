class Grammar:

    def __init__(self):
        self.__nonterminals = []
        self.__terminals = []
        self.__productions = {}
        self.__starting_symbol = ""

    def readFromFile(self, file_name) -> None:
        with open(file_name) as file:
            self.__nonterminals = file.readline().strip().split(' ')[1:]
            self.__terminals = file.readline().strip().split(' ')[1:]
            self.__starting_symbol = file.readline().strip().split(' ')[1:][0]

            file.readline()
            self.__productions = {}
            for line in file:
                split = line.strip().split('->')
                lhs = split[0].strip()
                rhs = split[1].split("||")
                for option in rhs:
                    rhs_list = []
                    for symbol in option.strip().split(" "):
                        rhs_list.append(symbol)

                    if lhs in self.__productions.keys():
                        self.__productions[lhs].append(rhs_list)
                    else:
                        self.__productions[lhs] = [rhs_list]

    def checkCFG(self) -> bool:
        has_s = False
        for key in self.__productions.keys():
            if key == self.__starting_symbol:
                has_s = True
            if key not in self.__nonterminals:
                return False

        if not has_s:
            return False

        for rhs_list in self.__productions.values():
            for rhs in rhs_list:
                for value in rhs:
                    if value not in self.__nonterminals and value not in self.__terminals and value != "epsilon":
                        print(value, rhs, rhs_list)
                        return False
        return True

    @property
    def get_nonterminals(self):
        return self.__nonterminals

    @property
    def get_terminals(self):
        return self.__terminals

    @property
    def get_productions(self):
        return self.__productions

    @property
    def get_starting_symbol(self):
        return self.__starting_symbol

    def __str__(self):
        result = "N: " + str(self.__nonterminals) + "\n"
        result += "E: " + str(self.__terminals) + "\n"
        result += "S: " + str(self.__starting_symbol) + "\n"
        result += "P: " + str(self.__productions) + "\n"
        return result
