from dataclasses import dataclass, field
from typing import List

@dataclass
class User:
    username: str
    email: str
    suggested_categories: List[str] = field(default_factory=list)
    party_id: str

    def __post_init__(self):
        if not self.username:
            raise ValueError("Username cannot be empty")
        if not self.email:
            raise ValueError("Email cannot be empty")
        if not self.party_id:
            raise ValueError("Party ID cannot be empty")

       