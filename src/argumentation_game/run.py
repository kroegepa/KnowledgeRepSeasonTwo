import sys
import json
import argparse

from typing import Dict, List

from argumentation_game.argument_graph import parse_json, ArgumentGraph
from argumentation_game.recursive_shenanigans import recursive_boogaloo

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
    print()
    Arguments.calc_attackers()
    label = [2,0,0,0,0,0,0]
    print(Arguments.arguments[0].attackers)
    label = recursive_boogaloo(Arguments,label,0)
    print(label)



def main(args: List[str]) -> None:
    run(parse_json(parse_arguments(args)))
