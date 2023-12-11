from __future__ import annotations

from dataclasses import dataclass

from typing import Dict, List
from numbers import Integral

from argumentation_game.labeling import Label


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
            Argument(int(i), v, [a.attacker for a in attacks if int(i) == a.attackee])
            for i, v in js["Arguments"].items()
        ]
        return cls(sorted(arguments, key=lambda x: x.index), attacks)

    def is_admissable(self, labeling: List[Label]) -> bool:
        def _is_admissable(label: Label, arg: Argument) -> bool:
            match label:
                case Label.In:
                    return all(labeling[l] == Label.Out for l in arg.attackers)
                case Label.Out:
                    return any(labeling[l] == Label.In for l in arg.attackers)
                case Label.Undecided:
                    return True

        return all(
            _is_admissable(label, arg)
            for label, arg in zip(labeling, self.arguments, strict=True)
        )


def parse_json(json: Dict) -> ArgumentGraph:
    return ArgumentGraph.from_json(json)
