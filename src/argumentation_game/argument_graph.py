from __future__ import annotations

from dataclasses import dataclass

from typing import Dict, List
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
    def from_json(cls, js: Dict) -> ArgumentGraph:
        attacks = [Attack(int(r), int(e)) for r, e in js["Attack Relations"]]
        arguments = [
            Argument(int(i), str(v), [a.attacker for a in attacks if i == a.attackee])
            for i, v in js["Arguments"].items()
        ]
        return cls(sorted(arguments, key=lambda x: x.index), attacks)


def parse_json(json: Dict) -> ArgumentGraph:
    return ArgumentGraph.from_json(json)
