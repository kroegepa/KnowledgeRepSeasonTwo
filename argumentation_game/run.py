from typing import Dict,List
import argparse
import json
from ArgumentGraph import parse_json,ArgumentGraph

def parse_arguments(args: List[str]) -> Dict:
    parser = argparse.ArgumentParser(
        prog = "argumentation_game",
        description="playing an argumentation game"
    )
    parser.add_argument(
        "json", help="input json file to initialize the argumentation graph", type=argparse.FileType("r")
    )
    arguments = parser.parse_args()
    print(arguments)
    return json.load(arguments.json)
def run(Arguments: ArgumentGraph):
    print(Arguments.argument_list)
    print(Arguments.attack_list)

def main(args: List[str]) -> None:
    run(parse_json(parse_arguments(args)))