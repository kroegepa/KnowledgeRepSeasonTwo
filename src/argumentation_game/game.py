from enum import Enum
from typing import Dict, Iterable, List, Optional, Set

from argumentation_game.argument import Argument
from argumentation_game.argument_graph import ArgumentGraph


class InvalidArgument(Exception):
    pass


class NonExistingArgument(Exception):
    pass


EXIT_KEYS = ("q", "quit", "exit")


class GameMessages(Enum):
    CHOOSE_INITIAL_ARGUMENT = (
        "\nChoose one argument among the following to START the game\n"
    )

    CHOOSE_ATTACKING_ARGUMENT = "Choose one argument among the following to ATTACK previously outputed arguments\n"

    CHOOSE_ARGUMENT = "Choose one of the provided arguments using its identifier or press `q` to quit: "

    PLAYING_NEXT_ROUND = f"\n{'NEXT ROUND':-^80}\n"

    END_GAME_NO_ARGS_OPPONENT = (
        "Game ends because opponent is left with no arguments to use\nPROPONENT WINS"
    )

    END_GAME_NO_ARGS_PROPONENT = (
        "Game ends because proponent is left with no arguments to use\nOPPONENT WINS"
    )

    INVALID_ARGUMENT = "ERROR: The argument key provided is not among the possible keys"

    NON_EXISTING_ARGUMENT = "ERROR: The argument key provided doesn't exist"

    INVALID_KEY = "ERROR: The key provided cannot be interpreted as such"


class Game:
    argument_graph: ArgumentGraph
    outputed_arguments: Set[Optional[Argument]]
    inputed_arguments: Set[Optional[Argument]]

    def __init__(self, argument_graph: ArgumentGraph) -> None:
        self.argument_graph = argument_graph
        self.outputed_arguments = set()
        self.inputed_arguments = set()

    @property
    def arguments(self) -> List[Argument]:
        return self.argument_graph.arguments

    @property
    def arguments_map(self) -> Dict[int, Argument]:
        return self.argument_graph.arguments_map

    def print_arguments(self, arguments: Iterable[Argument]):
        for argument in arguments:
            print(argument)
        print("\n")

    def print_selected_argument(self, argument: Argument) -> None:
        print(f"The selected argument is {str(argument)}\n")

    def print_replied_argument(self, argument: Argument) -> None:
        print(f"The replied argument is: {argument}\n")

    def validate_argument(
        self,
        argument: Argument,
        valid_arguments: Iterable[Argument],
    ) -> None:
        if not argument:
            raise NonExistingArgument
        if not argument in valid_arguments:
            raise InvalidArgument

    def get_argument_from_input(
        self, valid_arguments: Optional[Iterable[Argument]] = None
    ) -> Argument:
        valid_arguments = valid_arguments if valid_arguments else self.arguments
        while True:
            try:
                user_input = input(GameMessages.CHOOSE_ARGUMENT.value)
                if user_input.lower() in EXIT_KEYS:
                    print("Quitting the game ...")
                    exit()
                argument = self.arguments_map.get(int(user_input))
                self.validate_argument(argument, valid_arguments)
                self.print_selected_argument(argument)
                return argument

            except ValueError:
                print(GameMessages.INVALID_KEY.value)

            except NonExistingArgument:
                print(GameMessages.NON_EXISTING_ARGUMENT.value)

            except InvalidArgument:
                print(GameMessages.INVALID_ARGUMENT.value)

    def get_arguments_available_to_opponent(self) -> Set[Optional[Argument]]:
        arguments = set()
        for outputed in self.outputed_arguments:
            arguments |= outputed.is_attacked_by
        arguments -= self.inputed_arguments - self.outputed_arguments
        if not arguments:
            self.end_game(GameMessages.END_GAME_NO_ARGS_OPPONENT.value)
        return arguments

    def choose_initial_argument(self) -> Argument:
        print(GameMessages.CHOOSE_INITIAL_ARGUMENT.value)
        self.print_arguments(self.arguments)
        return self.get_argument_from_input()

    def choose_attacking_argument(self) -> Argument:
        print(GameMessages.CHOOSE_ATTACKING_ARGUMENT.value)
        self.print_arguments(self.get_arguments_available_to_opponent())
        return self.get_argument_from_input(
            valid_arguments=self.get_arguments_available_to_opponent()
        )

    def choose_replied_argument(self, argument: Argument) -> Optional[Argument]:
        availabe = argument.is_attacked_by - self.inputed_arguments
        if not availabe:
            self.end_game(GameMessages.END_GAME_NO_ARGS_PROPONENT.value)
        for atacker in availabe:
            self.print_replied_argument(atacker)
            return atacker

    def play_game(self) -> None:
        initial_argument = self.choose_initial_argument()
        self.outputed_arguments.add(initial_argument)
        while True:
            selected_argument = self.choose_attacking_argument()
            self.inputed_arguments.add(selected_argument)
            replied_argument = self.choose_replied_argument(selected_argument)
            self.outputed_arguments.add(replied_argument)
            print(GameMessages.PLAYING_NEXT_ROUND.value)

    def end_game(self, msg: str) -> None:
        print(msg)
        exit()
