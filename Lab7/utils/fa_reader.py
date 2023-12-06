from pprint import pprint


class FiniteAutomata:

    def __init__(self):
        self.__alphabet = None
        self.__states = None
        self.__initial_states = None
        self.__final_states = None
        self.__transitions = None
        self.__deterministic = True

    def read_fa(self, filepath: str) -> None:

        def extract_transitions(lines):
            transitions = {}

            for line in lines:
                if line.strip() == '':
                    continue

                key, value = [elem.strip() for elem in line.split('=')]
                state, symbol = [elem.strip() for elem in key.strip('()').split(',')]

                if (state, symbol) not in transitions:
                    transitions[(state, symbol)] = [value]
                else:
                    self.__deterministic = False
                    transitions[(state, symbol)].append(value)

            return transitions

        with open(filepath, 'r') as file:
            lines = file.readlines()

        for idx, line in enumerate(lines):
            if line.strip() == '':
                continue

            elems = [elem.strip() for elem in line.split(':')]

            if len(elems) == 1:
                key = elems[0]
            else:
                key, value = elems

            match key:
                case 'alphabet':
                    self.__alphabet = [elem.strip() for elem in value.split(',')]
                case 'states':
                    self.__states = [elem.strip() for elem in value.split(',')]
                case 'initial':
                    self.__initial_states = [value]
                case 'final':
                    self.__final_states = [elem.strip() for elem in value.split(',')]
                case 'transitions':
                    self.__transitions = extract_transitions(lines[idx + 1:])
                    break
                case _:
                    raise Exception(f'Unknown key {key} found!')

    def display_console(self) -> None:

        while True:
            print("1. Alphabet")
            print("2. States")
            print("3. Initial States")
            print("4. Final States")
            print("5. Transactions")
            print("6. Quit")

            choice = input("Enter your choice (1-6): ")

            if choice == "1":
                pprint(self.__alphabet)
            elif choice == "2":
                pprint(self.__states)
            elif choice == "3":
                pprint(self.__initial_states)
            elif choice == "4":
                print(self.__final_states)
            elif choice == "5":
                print(self.__transitions)
            elif choice == "6":
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")

            print("\n")

    def check(self, input_sequence: str) -> bool:

        if not self.__deterministic:
            print("NDFA")
            return False

        state = self.__initial_states[0]
        while input_sequence:

            symbol = input_sequence[0]
            input_sequence = input_sequence[1:]
            if (state, symbol) in self.__transitions:
                state = self.__transitions[(state, symbol)][0]
            else:
                return False

        if state not in self.__final_states:
            return False
        return True

