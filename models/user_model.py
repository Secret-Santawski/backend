from dataclasses import dataclass, field
from typing import List

@dataclass
class User:
    username: str
    email: str
    party_id: str = None
    suggested_categories: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.username:
            raise ValueError("Username cannot be empty")
        if not self.email:
            raise ValueError("Email cannot be empty")
