from collections import namedtuple
from typing import Dict, List, Self

from argumentation_game.argument import Argument

AttackRelation = namedtuple("AttackRelation", field_names=["attacker", "attackee"])


class ArgumentGraph:
    arguments: List[Argument]
    attack_relations: List[AttackRelation]  # do i actually need this?
    arguments_map: Dict[int, Argument]

    def __init__(
        self, arguments: List[Argument], attack_relations: List[AttackRelation]
    ) -> None:
        self.arguments = arguments
        self.attack_relations = attack_relations
        self.arguments_map = {argument.index: argument for argument in self.arguments}
        self.add_relations_to_arguments()

    @classmethod
    def from_json(cls, js: Dict) -> Self:
        return cls(
            [Argument(int(i), str(v)) for i, v in js["Arguments"].items()],
            [AttackRelation(int(e), int(r)) for e, r in js["Attack Relations"]],
        )

    def add_relations_to_arguments(self) -> None:
        for argument in self.arguments:
            for attacker, attackee in self.attack_relations:
                if argument == attacker:
                    argument.attacks_to.add(self.arguments_map[attackee])
                elif argument == attackee:
                    argument.is_attacked_by.add(self.arguments_map[attacker])


def parse_json(json: Dict) -> ArgumentGraph:
    return ArgumentGraph.from_json(json)
