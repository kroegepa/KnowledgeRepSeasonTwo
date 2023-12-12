from typing import Dict, Iterable, List, NoReturn, Optional, Set

from argumentation_game.argument_graph import Argument, ArgumentGraph
from argumentation_game.labeling import Label
from argumentation_game.recursive_shenanigans import try_admissability


class InvalidArgument(Exception):
    pass


class NonExistingArgument(Exception):
    pass


EXIT_KEYS = ("q", "quit", ":q", "exit", "exit()")


class GameMessages:
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

    QUIT_GAME = "Quitting game upon user request ..."

    INVALID_ARGUMENT = "ERROR: The argument key provided is not among the possible keys"

    NON_EXISTING_ARGUMENT = "ERROR: The argument key provided doesn't exist"

    INVALID_KEY = "ERROR: The key provided cannot be interpreted as such"


class Game:
    argument_graph: ArgumentGraph
    outputed_arguments: Set[Argument]
    inputed_arguments: Set[Argument]
    labeling: Optional[List[Label]]

    def __init__(self, argument_graph: ArgumentGraph) -> None:
        self.argument_graph = argument_graph
        self.outputed_arguments = set()
        self.inputed_arguments = set()
        self.labeling = None

    @property
    def arguments(self) -> List[Argument]:
        return self.argument_graph.arguments

    @property
    def arguments_map(self) -> Dict[int, Argument]:
        return {arg.index: arg for arg in self.argument_graph.arguments}

    def print_arguments(self, arguments: Iterable[Argument]):
        print("\n".join(str(arg) for arg in arguments), "\n")

    def print_selected_argument(self, argument: Argument) -> None:
        print(f"The selected argument is {str(argument)}\n")

    def print_replied_argument(self, argument: Argument) -> None:
        print(f"The replied argument is: {argument}\n")

    def validate_argument(
        self,
        argument: Optional[Argument],
        valid_arguments: Iterable[Argument],
    ) -> Argument:
        if not argument:
            raise NonExistingArgument
        if not argument in valid_arguments:
            raise InvalidArgument
        return argument

    def get_argument_from_input(self, arguments: Iterable[Argument]) -> Argument:
        while True:
            try:
                user_input = input(GameMessages.CHOOSE_ARGUMENT)
                if user_input.lower() in EXIT_KEYS:
                    self.end_game(GameMessages.QUIT_GAME)
                argument = self.arguments_map.get(int(user_input))
                argument = self.validate_argument(argument, arguments)
                self.print_selected_argument(argument)
                return argument

            except ValueError:
                print(GameMessages.INVALID_KEY)

            except NonExistingArgument:
                print(GameMessages.NON_EXISTING_ARGUMENT)

            except InvalidArgument:
                print(GameMessages.INVALID_ARGUMENT)

    def get_arguments_available_to_opponent(self) -> Set[Argument]:
        arguments = set()
        for outputed in self.outputed_arguments:
            arguments |= {self.arguments_map[a] for a in outputed.attackers}
        arguments -= self.inputed_arguments - self.outputed_arguments
        if not arguments:
            self.end_game(GameMessages.END_GAME_NO_ARGS_OPPONENT)
        return arguments

    def choose_attacking_argument(self) -> Argument:
        print(GameMessages.CHOOSE_ATTACKING_ARGUMENT)
        self.print_arguments(self.get_arguments_available_to_opponent())
        return self.get_argument_from_input(self.get_arguments_available_to_opponent())

    def choose_replied_argument(self, argument: Argument) -> Argument:
        attackers = {self.arguments_map[a] for a in argument.attackers}
        availabe = attackers - self.inputed_arguments
        for atacker in availabe:
            if self.labeling is None or self.labeling[atacker.index] == Label.In:
                self.print_replied_argument(atacker)
                return atacker

        assert not availabe
        self.end_game(GameMessages.END_GAME_NO_ARGS_PROPONENT)

    def play_game(self, init_argument: Argument) -> NoReturn:
        if not init_argument in self.argument_graph.arguments:
            self.end_game(f"{init_argument} is not a argument from the passed graph")
        self.print_arguments(self.arguments)
        print(f"Starting game with {init_argument}\n")
        self.labeling = try_admissability(self.argument_graph, init_argument, Label.In)

        self.outputed_arguments.add(init_argument)
        while True:
            selected_argument = self.choose_attacking_argument()
            self.inputed_arguments.add(selected_argument)
            replied_argument = self.choose_replied_argument(selected_argument)
            self.outputed_arguments.add(replied_argument)
            print(GameMessages.PLAYING_NEXT_ROUND)

    def end_game(self, msg: str) -> NoReturn:
        print(msg)
        exit()
