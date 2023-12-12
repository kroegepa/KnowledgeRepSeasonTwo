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

    CHOOSE_OPPONENT_ARGUMENT = "Choose one argument among the following to ATTACK previously outputed arguments\n"

    CHOOSE_ARGUMENT = "Choose one of the provided arguments using its identifier or press `q` to quit: "

    PLAYING_NEXT_ROUND = f"\n{'NEXT ROUND':-^80}\n"

    END_GAME_NO_ARGS_OPPONENT = (
        "Game ends because opponent is left with no arguments to use\nPROPONENT WINS"
    )

    END_GAME_NO_ARGS_PROPONENT = (
        "Game ends because proponent is left with no arguments to use\nOPPONENT WINS"
    )

    QUIT_GAME = "Quitting game upon user request ..."

    INVALID_ARGUMENT = "ERROR: The argument key provided is not among the possible keys"

    NON_EXISTING_ARGUMENT = "ERROR: The argument key provided doesn't exist"

    INVALID_KEY = "ERROR: The key provided cannot be interpreted as such"


class Game:
    argument_graph: ArgumentGraph
    outputted_arguments: Set[Optional[Argument]]
    inputted_arguments: Set[Optional[Argument]]

    def __init__(self, argument_graph: ArgumentGraph) -> None:
        self.argument_graph = argument_graph
        self.outputted_arguments = set()
        self.inputted_arguments = set()

    @property
    def arguments(self) -> List[Argument]:
        return self.argument_graph.arguments

    @property
    def arguments_map(self) -> Dict[int, Argument]:
        return self.argument_graph.arguments_map

    def print_arguments(self, arguments: Iterable[Argument]) -> None:
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
                    self.end_game(GameMessages.QUIT_GAME.value)
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

    def get_arguments_available_to_opponent(self) -> Set[Argument]:
        """
        1.  The opponent can only choose arguments that attack another
            argument previously outputted by the proponent. The attacked
            arguments can be from the previous round, but also from an
            earlier round.
        2.  If the opponent uses an argument previously used by the proponent, then the proponent wins.
        3.  The opponent is not allowed to use the same argument twice.
        4.  If the opponent has no choices left, then the proponent wins.
        """
        arguments = set()
        for outputed in self.outputted_arguments:
            arguments |= outputed.is_attacked_by  # 1
        arguments -= self.inputted_arguments - self.outputted_arguments  # 2, 3
        if not arguments:
            self.end_game(GameMessages.END_GAME_NO_ARGS_OPPONENT.value)  # 4
        return arguments

    def choose_initial_argument(self) -> Argument:
        print(GameMessages.CHOOSE_INITIAL_ARGUMENT.value)
        self.print_arguments(self.arguments)
        return self.get_argument_from_input()

    def choose_opponent_argument(self) -> Argument:
        print(GameMessages.CHOOSE_OPPONENT_ARGUMENT.value)
        opponent_available = self.get_arguments_available_to_opponent()
        self.print_arguments(opponent_available)
        return self.get_argument_from_input(valid_arguments=opponent_available)

    def choose_proponent_argument(self, argument: Argument) -> Argument:
        """
        1.  The proponent always has to answer with an argument that attacks
            the argument that the opponent selected in the directly preceding round.
        2.  If the proponent uses an argument previously used by the opponent,
            then the opponent wins.
        3.  If the proponent is unable to make a move, then the opponent wins.
        """
        proponent_availabe = argument.is_attacked_by - self.inputted_arguments  # 1, 2
        if not proponent_availabe:
            self.end_game(GameMessages.END_GAME_NO_ARGS_PROPONENT.value)  # 3
        for atacker in proponent_availabe:
            self.print_replied_argument(atacker)
            return atacker

    def play_game(self) -> None:
        initial_argument = self.choose_initial_argument()
        self.outputted_arguments.add(initial_argument)
        while True:
            selected_argument = self.choose_opponent_argument()
            self.inputted_arguments.add(selected_argument)
            replied_argument = self.choose_proponent_argument(selected_argument)
            self.outputted_arguments.add(replied_argument)
            print(GameMessages.PLAYING_NEXT_ROUND.value)

    def end_game(self, msg: str) -> None:
        print(msg)
        exit()
