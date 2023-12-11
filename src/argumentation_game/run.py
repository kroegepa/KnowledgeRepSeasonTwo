import argparse
import json
import sys
from typing import Dict, List

from argumentation_game.argument_graph import ArgumentGraph, parse_json


def parse_arguments(args: List[str]) -> Dict:
    parser = argparse.ArgumentParser(
        prog="argumentation_game", description="playing an argumentation game"
    )
    parser.add_argument(
        "json",
        help="input json file to initialize the argumentation graph",
        type=argparse.FileType("r"),
    )
    parser.add_argument(
        "initial_argument", help="Argument to start the game with", type=str
    )
    arguments = parser.parse_args(args)

    if not arguments.json:
        parser.print_usage()
        return sys.exit(1)

    return json.load(arguments.json)


def run(argument_graph: ArgumentGraph):
    print(argument_graph.arguments)
    print(argument_graph.attacks)


def main(args: List[str]) -> None:
    run(parse_json(parse_arguments(args)))
