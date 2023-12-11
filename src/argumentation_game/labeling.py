from enum import IntEnum, unique

from typing import Literal


@unique
class Label(IntEnum):
    Undecided = 0
    In = 1
    Out = 2


DecidedLabel = Literal[Label.In, Label.Out]
