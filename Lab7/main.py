from pprint import pprint

from grammer import Grammar
from parser import LL1
from utils.enums import Token
from utils.error import LexicalErr, SyntacticalError
from scanner import Scanner
from utils.fa_reader import FiniteAutomata


def main():

    # fa_path = "definitions/Fa.in"
    #
    # fa = FiniteAutomata()
    # fa.read_fa(fa_path)
    # # fa.display_console()
    # print(fa.check("1234556"))
    #
    # gr_path = "definitions/g1.txt"
    # grammer = Grammar()
    # grammer.readFromFile(gr_path)
    # parser = LL1(grammer)
    # parser.initialize()
    # parser.pretty_print_parsing_table()
    # parser.pretty_print_parsing_tree(parser.parse_input([("id", Token.SEPARATOR), ("+", Token.SEPARATOR), ("id", Token.SEPARATOR), ("*", Token.SEPARATOR), ("id", Token.SEPARATOR)]))

    try:
        program_path = "programs/program_1.in"
        st_path = "out/ST.out"
        pif_path = "out/PIF.out"
        file = open(program_path, 'r')
        scanner = Scanner(file)
        program = scanner.scan()

        print("Lexically correct.")

        gr_path = "definitions/g2.txt"
        tree_path = "out/TREE.out"

        grammer = Grammar()
        grammer.readFromFile(gr_path)

        parser = LL1(grammer)
        parser.initialize()
        parser.pretty_print_parsing_table()
        tree = parser.parse_input(program.pif)
        parser.pretty_print_parsing_tree(tree)

        print("Syntactically correct.")

        with open(st_path, 'w') as file:
            file.write(str(program.identifier_table.table) + "\n")
            file.write(str(program.literal_table.table))

        with open(pif_path, 'w') as file:
            file.write(str(program.pif))

        with open(tree_path, 'w') as file:
            file.write('\n'.join(map(str, tree)))

    except LexicalErr as e:
        print(e)
    except SyntacticalError as e:
        print(e)


if __name__ == '__main__':
    main()
