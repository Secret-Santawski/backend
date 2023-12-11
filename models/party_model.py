from dataclasses import dataclass, field
from typing import List

@dataclass
class PartyRequest:
    name: str
    budget: int
    categories: List[str]

    def __post_init__(self):
        if self.budget < 0:
            raise ValueError("Budget cannot be negative")
        if not self.name:
            raise ValueError("Name cannot be empty")

@dataclass
class Party:
    name: str
    budget: int
    categories: List[str]
    ownerId: str = ''
    closed: bool = False

    def __post_init__(self):
        if self.budget < 0:
            raise ValueError("Budget cannot be negative")
        if not self.name:
            raise ValueError("Name cannot be empty")