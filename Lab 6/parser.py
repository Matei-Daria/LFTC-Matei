from grammar import Grammar


class LL1:

    def __init__(self, grammar: Grammar):
        self.__grammar = grammar
        self.__first = {}
        self.__follow = {}

    def parse(self):
        self._find_first()
        self._find_follow()

    def _find_first(self) -> None:
        for nonterminal in self.__grammar.get_nonterminals:
            self.__first[nonterminal] = set()

        for terminal in self.__grammar.get_terminals:
            self.__first[terminal] = {terminal}

        changed = True
        while changed:
            changed = False

            for nonterminal in self.__grammar.get_nonterminals:
                # for each option from productions of one nonterminal
                for production_option in self.__grammar.get_productions[nonterminal]:
                    for symbol in production_option:

                        if symbol in self.__grammar.get_terminals:
                            if symbol not in self.__first[nonterminal]:
                                self.__first[nonterminal].add(symbol)
                                changed = True

                            # finished with first from current option
                            break

                        elif symbol in self.__grammar.get_nonterminals:
                            # if the first for the nonterminal 'symbol' is not calculated yet
                            if len(self.__first[symbol]) == 0:
                                break

                            if not self.__first[symbol].issubset(self.__first[nonterminal]):
                                self.__first[nonterminal].update(self.__first[symbol])
                                changed = True

                            # if epsilon is in the first of 'symbol' we go to the next production option
                            if 'epsilon' not in self.__first[symbol]:
                                break
                    else:
                        # if all can symbols can be epsilon then the current nonterminal can be epsilon
                        if 'epsilon' not in self.__first[nonterminal]:
                            self.__first[nonterminal].add('epsilon')
                            changed = True

    def _find_follow(self) -> None:
        for nonterminal in self.__grammar.get_nonterminals:
            self.__follow[nonterminal] = set()

        # adding to the follow set of the start symbol
        start_symbol = self.__grammar.get_starting_symbol
        self.__follow[start_symbol].add('$')

        changed = True
        while changed:
            changed = False

            for nonterminal in self.__grammar.get_nonterminals:
                for production_option in self.__grammar.get_productions[nonterminal]:
                    for i, symbol in enumerate(production_option):

                        if symbol in self.__grammar.get_nonterminals:
                            # for nonterminals, take the next symbol to calculate follow
                            next_symbol = production_option[i + 1] if i + 1 < len(production_option) else None

                            if next_symbol is not None:
                                # if the next symbol is a nonterminal, add its first set to the follow set
                                if next_symbol in self.__grammar.get_nonterminals:
                                    if not self.__first[next_symbol].issubset(self.__follow[symbol]):
                                        self.__follow[symbol].update(self.__first[next_symbol])
                                        changed = True

                                # if the next symbol is a terminal, add it to the follow set
                                elif next_symbol in self.__grammar.get_terminals:
                                    if next_symbol not in self.__follow[symbol]:
                                        self.__follow[symbol].add(next_symbol)
                                        changed = True

                            # if end of production, add follow of current nonterminal production to follow of the last symbol
                            else:
                                if not self.__follow[nonterminal].issubset(self.__follow[symbol]):
                                    self.__follow[symbol].update(self.__follow[nonterminal])
                                    changed = True

        # remove epsilon from sets
        for nonterminal in self.__grammar.get_nonterminals:
            if 'epsilon' in self.__follow[nonterminal]:
                self.__follow[nonterminal].remove('epsilon')


    @property
    def get_first(self):
        return self.__first

    @property
    def get_follow(self):
        return self.__follow

    def __str__(self):
        result = "First: " + str(self.__first) + "\n"
        result += "Follow: " + str(self.__follow) + "\n"
        return result


