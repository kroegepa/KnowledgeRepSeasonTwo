from enum import Enum, auto

from typing import Literal


class Label(Enum):
    Undecided = auto()
    In = auto()
    Out = auto()


DecidedLabel = Literal[Label.In, Label.Out]
