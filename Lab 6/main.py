from grammar import Grammar
from parser import LL1

def printMenu():
    print("Enter an option to see the following information")
    print("1. Set of nonterminals")
    print("2. Set of terminals")
    print("3. Set of productions")
    print("4. Productions for a given nonterminal")
    print("5. CFG check")


if __name__ == '__main__':
    grammar = Grammar()
    file = "g1.txt"
    grammar.readFromFile(file)
    print("The grammar was read from file " + file)
    while True:
        printMenu()
        option = int(input("Enter an option: "))
        if option == 1:
            print(str(grammar.get_nonterminals))
        elif option == 2:
            print(str(grammar.get_terminals))
        elif option == 3:
            print(str(grammar.get_productions))
        elif option == 4:
            nonterminal = input("Enter a nonterminal: ")
            if grammar.get_productions.keys().__contains__(nonterminal):
                print(str(grammar.get_productions[nonterminal]))
            else:
                print("No such nonterminal in the grammar.")
        elif option == 5:
            if grammar.checkCFG():
                print("It is CFG.")
            else:
                print("It is not CFG.")
        else:
            print("Enter a valid option.")
