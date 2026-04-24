from dataclasses import dataclass, field
from typing import List


@dataclass
class Pet:
    """Represents a pet and its details."""
    name: str
    breed: str
    age: int
    general_info: str = ""

class Owner:
    """Manages multiple pets."""
    def __init__(self, name: str):
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        """Adds a new pet to this owner's pet list."""
        self.pets.append(pet)

