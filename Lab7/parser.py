from tabulate import tabulate

from grammer import Grammar
from structures.program_internal_form import ProgramInternalForm
from utils.enums import Token
from utils.error import SyntacticalError, CompatibilityError


class LL1:

    def __init__(self, grammar: Grammar):
        self.__grammar = grammar
        self.__first = {}
        self.__follow = {}
        self.__parsing_table = {}

    @property
    def parsing_table(self):
        return self.__parsing_table

    def initialize(self) -> None:
        self._find_first()
        self._find_follow()
        self._construct_parsing_table()

    def pretty_print_parsing_table(self) -> None:
        """
        Print the parsing table as a visual table.
        """
        row_names = set(row for row, _ in self.__parsing_table)
        col_names = set(col for _, col in self.__parsing_table)
        headers = [''] + sorted(col_names)
        table_data = [[row] + [" ".join(self.__parsing_table.get((row, col), '')) for col in sorted(col_names)] for row
                      in sorted(row_names)]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

    @staticmethod
    def pretty_print_parsing_tree(data: list[dict]) -> None:
        """
        Print the parsing tree table after the father-sibling relation as a visual table.
        """
        # data = self.parse_input(["id", "+", "id", "*", "id"])
        headers = list(data[0].keys())[:-1]
        table_data = [tuple(d.values())[:-1] for i, d in enumerate(data)]

        print(tabulate(table_data, headers=headers, tablefmt="grid"))

    def _find_first(self) -> None:
        """
        Find the first sets of the grammar.
        """
        for nonterminal in self.__grammar.nonterminals:
            self.__first[nonterminal] = set()

        for terminal in self.__grammar.terminals:
            self.__first[terminal] = {terminal}

        changed = True
        while changed:
            changed = False

            for nonterminal in self.__grammar.nonterminals:
                # for each option from productions of one nonterminal
                for production_option in self.__grammar.productions[nonterminal]:
                    for symbol in production_option:

                        if symbol in self.__grammar.terminals:
                            if symbol not in self.__first[nonterminal]:
                                self.__first[nonterminal].add(symbol)
                                changed = True

                            # finished with first from current option
                            break

                        elif symbol in self.__grammar.nonterminals:
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
        """
        Find the follow sets of the grammar.
        """
        for nonterminal in self.__grammar.nonterminals:
            self.__follow[nonterminal] = set()

        # adding to the follow set of the start symbol
        start_symbol = self.__grammar.starting_symbol
        self.__follow[start_symbol].add('$')

        changed = True
        while changed:
            changed = False

            for nonterminal in self.__grammar.nonterminals:
                for production_option in self.__grammar.productions[nonterminal]:
                    for i, symbol in enumerate(production_option):

                        if symbol in self.__grammar.nonterminals:
                            # for nonterminals, take the next symbol to calculate follow
                            next_symbol = production_option[i + 1] if i + 1 < len(production_option) else None

                            if next_symbol is not None:

                                if next_symbol in self.__grammar.nonterminals:
                                    # if the next symbol is a nonterminal, add its first set to the follow set
                                    if not self.__first[next_symbol].issubset(self.__follow[symbol]):
                                        self.__follow[symbol].update(self.__first[next_symbol])
                                        changed = True

                                    # if next symbol can be epsilon, we give the current nonterminal the follow set of it
                                    if 'epsilon' in self.__first[next_symbol]:
                                        self.__follow[symbol].update(self.__follow[next_symbol])

                                # if the next symbol is a terminal, add it to the follow set
                                elif next_symbol in self.__grammar.terminals:
                                    if next_symbol not in self.__follow[symbol]:
                                        self.__follow[symbol].add(next_symbol)
                                        changed = True

                            # if end of production, add follow of current nonterminal production to follow of the last symbol
                            else:
                                if not self.__follow[nonterminal].issubset(self.__follow[symbol]) and nonterminal:
                                    self.__follow[symbol].update(self.__follow[nonterminal])
                                    changed = True

        # remove epsilon from sets
        for nonterminal in self.__grammar.nonterminals:
            if 'epsilon' in self.__follow[nonterminal]:
                self.__follow[nonterminal].remove('epsilon')

    def _construct_parsing_table(self) -> None:
        """
        Construct the LL(1) parsing table.
        """
        for nonterminal in self.__grammar.nonterminals:
            for production_option in self.__grammar.productions[nonterminal]:

                if production_option != ['epsilon']:

                    # construct the first set of a particular production from a nonterminal;
                    # see what terminals you can construct from the first set of the nonterminal
                    first_set = self._calculate_first_set(production_option)

                    for terminal in first_set:
                        if terminal != 'epsilon':

                            if (nonterminal, terminal) in self.__parsing_table.keys():

                                print([f"{i[1]} p{self.__parsing_table[i]}" for i in self.__parsing_table.keys() if
                                       i[0] == nonterminal and nonterminal == "simplstmt"])
                                print(production_option, (nonterminal, terminal))

                                raise CompatibilityError("The grammar provided is not LL1")

                            # add in table in the corresponding position
                            self.__parsing_table[(nonterminal, terminal)] = production_option

                # if production is in epsilon, we put the epsilon production in all the places where terminals follow this nonterminal
                else:
                    for terminal in self.__follow[nonterminal]:

                        if (nonterminal, terminal) in self.__parsing_table.keys():

                            print(self.__follow[nonterminal])
                            print(production_option, nonterminal)
                            print([f"{i[1]} p{self.__parsing_table[i]}" for i in self.__parsing_table.keys() if
                                   i[0] == nonterminal and nonterminal == "simplestmt"])
                            print(self.__parsing_table[(nonterminal, terminal)], (nonterminal, terminal))

                            raise CompatibilityError(f"The grammar provided is not LL1.")

                        self.__parsing_table[(nonterminal, terminal)] = production_option

    def _calculate_first_set(self, symbols: list) -> set:
        """
        Calculate the first set for a list of symbols.
        """
        first_set = set()
        for symbol in symbols:

            # we stop at the first terminal
            if symbol in self.__grammar.terminals:
                first_set.add(symbol)
                break

            # add the first of the nonterminal and continue with iteration if epsilon present
            elif symbol in self.__grammar.nonterminals:
                first_set.update(self.__first[symbol])
                if 'epsilon' not in self.__first[symbol]:
                    break

        return first_set

    def parse_input(self, input: ProgramInternalForm) -> list[dict]:
        """
        Find the parsing tree given by the representation father-sibling relation table.
        :param input: a list of tokens in a specific order
        :return: a dictionary where each node in the tree is a key in dictionary and its value are the parent
                and right sibling; or None if the grammar is not ll1 parsable
        """

        # mark the end
        stack = ['$']
        input += [('$', Token.SEPARATOR)]

        # start from the starting symbol
        current_node = self.__grammar.starting_symbol
        stack.append(self.__grammar.starting_symbol)

        # 'parent-sibling' parsing tree table
        index_tree = 0
        parsing_tree_table = [{}]
        parsing_tree_table[index_tree]["index"] = index_tree + 1
        parsing_tree_table[index_tree]["value"] = current_node
        parsing_tree_table[index_tree]["parent"] = 0
        parsing_tree_table[index_tree]["right_sibling"] = 0
        parsing_tree_table[index_tree]["derived_epsilon"] = False
        index_tree += 1

        index_input = 0
        while stack:
            top = stack[-1]
            stack.pop()
            symbol, type_symbol = input[index_input]

            # treat literals and identifiers as terminals and go to next input
            if top == "identifier" and type_symbol == Token.IDENTIFIER or \
                    (top == "intconst" or top == "stringconst" or top == "assignchoice") and type_symbol == Token.LITERAL:

                parent = [
                    node["index"] for node in parsing_tree_table
                    if node["value"] == top and
                       node["index"] not in [node["parent"] for node in parsing_tree_table] and
                       node["derived_epsilon"] is False
                ].pop(0)

                parsing_tree_table.append({})
                parsing_tree_table[index_tree]["index"] = index_tree + 1
                parsing_tree_table[index_tree]["value"] = symbol
                parsing_tree_table[index_tree]["parent"] = parent
                parsing_tree_table[index_tree]["right_sibling"] = 0
                parsing_tree_table[index_tree]["derived_epsilon"] = False
                index_tree += 1

                index_input += 1
                continue

            # else continue till you find the nonterminal identifier or constant
            elif type_symbol == Token.IDENTIFIER or type_symbol == Token.LITERAL:
                # take the first symbol for navigation in the parsing table
                symbol = symbol[0]

            if top in self.__grammar.terminals or top == "$":

                # terminal on top of the stack
                if top == symbol:
                    # is a match -> move to the next input symbol
                    index_input += 1
                else:
                    # error handling, mismatch
                    raise SyntacticalError(f"Mismatch in input for symbol {symbol} expected {top}",
                                           self.parse_input.__qualname__)  # TODO print line error or smth

            elif (top, symbol) in self.__parsing_table:

                # nonterminal on top of the stack -> build the tree
                production = self.__parsing_table[(top, symbol)]

                # take as parent the index of the first node that has the value equal to the top nonterminal
                # and it isn't yet a parent or has derived epsilon
                parent = [
                    node["index"] for node in parsing_tree_table
                    if node["value"] == top and
                       node["index"] not in [node["parent"] for node in parsing_tree_table] and
                       node["derived_epsilon"] is False
                ].pop(0)

                if production != ["epsilon"]:

                    # index used later to identify from which index we should add in the stack elements
                    index_continuation_parse_tree_table = len(parsing_tree_table)

                    # create children nodes in the parse tree
                    for symbol_production in production:

                        # if we have a right node
                        if symbol_production != production[-1]:
                            right_sibling = index_tree + 2
                        else:
                            right_sibling = 0

                        parsing_tree_table.append({})
                        parsing_tree_table[index_tree]["index"] = index_tree + 1
                        parsing_tree_table[index_tree]["value"] = symbol_production
                        parsing_tree_table[index_tree]["parent"] = parent
                        parsing_tree_table[index_tree]["right_sibling"] = right_sibling
                        parsing_tree_table[index_tree]["derived_epsilon"] = False
                        index_tree += 1

                    # add in reverse order in stack the nodes created
                    for node in reversed(parsing_tree_table[index_continuation_parse_tree_table:]):
                        stack.append(node["value"])

                else:
                    parsing_tree_table[parent - 1]["derived_epsilon"] = True

            else:
                # error handling, no entry in the parsing table
                raise SyntacticalError(f"No production in the parsing table for input {(top, symbol)}",
                                       self.parse_input.__qualname__)  # TODO print line error or smth

        return parsing_tree_table

    def __str__(self):
        result = "First: " + str(self.__first) + "\n"
        result += "Follow: " + str(self.__follow) + "\n"
        result += "Parsing Table: " + str(self.__parsing_table) + "\n"
        return result
