import sys
import json
import argparse
from dataclasses import dataclass

from typing import Dict, List

from argumentation_game.argument_graph import Argument, ArgumentGraph
from argumentation_game.labeling import Label
from argumentation_game.recursive_shenanigans import is_in_preferred_labeling
from argumentation_game.game import Game


@dataclass
class Args:
    json: Dict
    node: str
    game: bool


def parse_arguments(args: List[str]) -> Args:
    parser = argparse.ArgumentParser(
        prog="argumentation_game", description="playing an argumentation game"
    )
    parser.add_argument(
        "-g",
        "--game",
        action=argparse.BooleanOptionalAction,
        help="Whether to play the game or not.",
    )
    parser.add_argument(
        "json",
        help="input json file to initialize the argumentation graph",
        type=argparse.FileType("r"),
    )
    parser.add_argument(
        "node",
        help="The node to start with, or the node to credulously decide is in a preferred extension",
        type=str,
    )
    arguments = parser.parse_args(args)

    if not arguments.json:
        parser.error("Could not read the inputted file")

    return Args(json.load(arguments.json), arguments.node, arguments.game)


def run_game(argument_graph: ArgumentGraph, node: Argument):
    Game(argument_graph).play_game(node)


def run_semantics(argument_graph: ArgumentGraph, node: Argument):
    print(is_in_preferred_labeling(argument_graph, node))


# Python, I want monadic exceptions, and I want them now.
def parse_node(argument_graph: ArgumentGraph, node: str) -> Argument:
    try:
        return argument_graph.arguments[int(node)]
    except Exception:
        return [n for n in argument_graph.arguments if n.text == node].pop()


def run(args: Args):
    argument_graph = ArgumentGraph.from_json(args.json)
    try:
        node = parse_node(argument_graph, args.node)
    except Exception:
        sys.exit(f"Could not interpret input {args.node} as node.")

    if args.game:
        run_game(argument_graph, node)
    else:
        run_semantics(argument_graph, node)


def main(args: List[str]) -> None:
    run(parse_arguments(args))
