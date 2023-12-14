from argumentation_game.argument_graph import Argument, ArgumentGraph
from argumentation_game.labeling import DecidedLabel, Label

from typing import List, Optional


def recursive_boogaloo(
    argument_graph: ArgumentGraph, labeling: List[Label], current_node: int
) -> Optional[List[Label]]:
    if labeling[current_node] == Label.In:
        changed = False
        for attacker in argument_graph.arguments[current_node].attackers:
            if labeling[attacker] == Label.In:
                return None
            elif labeling[attacker] == Label.Undecided:
                labeling[attacker] = Label.Out
                changed = True
        if changed is False:
            return labeling
        for attacker in argument_graph.arguments[current_node].attackers:
            labeling_ = recursive_boogaloo(argument_graph, labeling, attacker)
            if labeling_ is None:
                return None
            else:
                labeling = labeling_

        return labeling

    elif labeling[current_node] == Label.Out:
        for attacker in argument_graph.arguments[current_node].attackers:
            temp_labeling = labeling
            if labeling[attacker] == Label.Out:
                temp_labeling = None
            elif labeling[attacker] == Label.Undecided:
                temp_labeling[attacker] = Label.In
                temp_labeling = recursive_boogaloo(
                    argument_graph, temp_labeling, attacker
                )
            elif labeling[attacker] == Label.In:
                return labeling

            if temp_labeling is not None:
                return temp_labeling
    return None


def try_admissability(
    argument_graph: ArgumentGraph, argument: int | Argument, label: DecidedLabel
) -> Optional[List[Label]]:
    if isinstance(argument, Argument):
        argument = argument.index

    initial_labels = [Label.Undecided for _ in argument_graph.arguments]
    initial_labels[argument] = label
    return recursive_boogaloo(argument_graph, initial_labels, argument)


def is_in_preferred_labeling(
    argument_graph: ArgumentGraph, argument: int | Argument
) -> bool:
    # If a single label being IN is in an admissable extension, it is also in a preferred extension.
    return try_admissability(argument_graph, argument, Label.In) is not None
