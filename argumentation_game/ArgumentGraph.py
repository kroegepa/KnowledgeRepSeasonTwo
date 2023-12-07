from typing import Dict,List,Tuple
from dataclasses import dataclass
import marshmallow_dataclass

@dataclass
class ArgumentGraph():
    #Class has two main attributes
    #List of arguments ["sth","sth else"], their index corresponds to their number
    #List of tuples of attacks [(0,1)...]

    argument_list : List[str]
    attack_relation_list : List[Tuple]

parser = marshmallow_dataclass.class_schema(ArgumentGraph)()

def parse_json(json: Dict) -> ArgumentGraph:
    print(json)
    return parser.load(json)








