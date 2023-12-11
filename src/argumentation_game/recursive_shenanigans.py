from argumentation_game.argument_graph import ArgumentGraph
from typing import List, Optional


# Labeling is list of integers
# 1 is in 2 is out 0 undecided
def recursive_boogaloo(
    argument_graph: ArgumentGraph, labeling: List[int], current_node: int
) -> Optional[List[int]]:
    if labeling[current_node] == 1:
        changed_flag = 0
        for attacker in argument_graph.arguments[current_node].attackers:
            if labeling[attacker] == 1:
                return None
            elif labeling[attacker] == 0:
                labeling[attacker] = 2
                changed_flag = 1
        if changed_flag == 0:
            return labeling
        for attacker in argument_graph.arguments[current_node].attackers:
            labeling = recursive_boogaloo(argument_graph, labeling, attacker)
            if labeling is None:
                return None
        return labeling

    # If current_node is out
    elif labeling[current_node] == 2:
        for attacker in argument_graph.arguments[current_node].attackers:
            temp_labeling = labeling
            if labeling[attacker] == 2:
                temp_labeling = None
            elif labeling[attacker] == 0:
                temp_labeling[attacker] = 1
                temp_labeling = recursive_boogaloo(
                    argument_graph, temp_labeling, attacker
                )
            elif labeling[attacker] == 1:
                return labeling

            if temp_labeling is not None:
                return temp_labeling
    return None
