from __future__ import annotations

from dataclasses import dataclass, field
from numbers import Integral
from typing import Optional, Set


@dataclass
class Argument:
    index: int
    text: str
    attacks_to: Set[Optional[Argument]] = field(default_factory=set)
    is_attacked_by: Set[Optional[Argument]] = field(default_factory=set)

    def __hash__(self) -> int:
        return hash(self.index)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Argument):
            return self.index == __o.index
        elif isinstance(__o, Integral):
            return self.index == __o
        return NotImplemented

    def __str__(self) -> str:
        return f"{self.index}: {self.text}"
