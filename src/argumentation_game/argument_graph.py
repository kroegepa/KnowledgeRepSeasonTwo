from __future__ import annotations

from dataclasses import dataclass, field
from numbers import Integral
from typing import Dict, List, Optional, Self, Set


@dataclass
class Attack:
    attackee: int
    attacker: int


@dataclass
class Argument:
    index: int
    text: str
    attacks_to: Set[Optional[Argument]] = field(default_factory=set)
    is_attacked_by: Set[Optional[Argument]] = field(default_factory=set)

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
        # Sorting the array because list order is not guaranteed in json parsing
        arguments = [Argument(int(i), str(v)) for i, v in js["Arguments"].items()]
        attacks = [Attack(int(e), int(r)) for e, r in js["Attack Relations"]]
        ArgumentGraph.add_attackers_to_arguments(arguments)

        return cls(arguments=arguments, attacks=attacks)

    @staticmethod
    def add_attackers_to_arguments(
        arguments: List[Argument], attacks: List[Attack]
    ) -> None:
        arguments_map = ArgumentGraph.create_arguments_mapping(arguments)

    @staticmethod
    def create_arguments_mapping(
        arguments: List[Argument],
    ) -> Dict[int, Argument]:
        return {argument.index: argument for argument in arguments}

    @staticmethod
    def find_attackees(argument: Argument, attack_relations: List[Attack]) -> None:
        for attacker, attackee in attack_relations:
            if attacker == argument.index:
                argument.attacks_to.add(attackee)


def parse_json(json: Dict) -> ArgumentGraph:
    return ArgumentGraph.from_json(json)
