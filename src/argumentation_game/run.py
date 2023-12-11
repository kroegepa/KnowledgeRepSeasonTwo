import sys
import json
import argparse

from typing import Dict, List

from argumentation_game.argument_graph import parse_json, ArgumentGraph
from argumentation_game.recursive_shenanigans import recursive_boogaloo
from argumentation_game.labeling import Label


def parse_arguments(args: List[str]) -> Dict:
    parser = argparse.ArgumentParser(
        prog="argumentation_game", description="playing an argumentation game"
    )
    parser.add_argument(
        "json",
        help="input json file to initialize the argumentation graph",
        type=argparse.FileType("r"),
    )
    arguments = parser.parse_args(args)

    if not arguments.json:
        parser.print_usage()
        return sys.exit(1)

    return json.load(arguments.json)


def run(Arguments: ArgumentGraph):
    print(Arguments.arguments)
    print(Arguments.attacks)
    labeling = [
        Label.Out,
        Label.Undecided,
        Label.Undecided,
        Label.Undecided,
        Label.Undecided,
        Label.Undecided,
        Label.Undecided,
    ]
    labeling = recursive_boogaloo(Arguments, labeling, 0)
    print(labeling)


def main(args: List[str]) -> None:
    run(parse_json(parse_arguments(args)))
