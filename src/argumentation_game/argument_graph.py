from dataclasses import dataclass

from typing import Dict, List, Self
from numbers import Integral


@dataclass
class Attack:
    attacker: int
    attackee: int


@dataclass
class Argument:
    index: int
    text: str
    attackers: list[int]

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Argument):
            return self.index == __o.index
        elif isinstance(__o, Integral):
            return self.index == __o
        return NotImplemented


@dataclass
class ArgumentGraph:
    arguments: List[Argument]
    attacks: List[Attack]

    @classmethod
    def from_json(cls, js: Dict) -> Self:
        return cls(
            # Sorting the array because list order is not guaranteed in json parsing
            arguments=[Argument(int(i), str(v),None) for i, v in js["Arguments"].items()],
            attacks=[Attack(int(e), int(r)) for e, r in js["Attack Relations"]],
        )
    def calc_attackers(self):
        for argument in self.arguments:
            attacker_list = []
            for attack in self.attacks:
                if argument.index == attack.attackee:
                    attacker_list.append(attack.attacker)
            argument.attackers = attacker_list





def parse_json(json: Dict) -> ArgumentGraph:
    return ArgumentGraph.from_json(json)
