from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Task:
    """Represents a single care task for a pet."""
    name: str  # Description of the task
    time: int  # Duration in minutes
    frequency: str # e.g., 'daily', 'weekly'
    is_completed: bool = False

    def mark_as_complete(self):
        """Marks the task as completed."""
        self.is_completed = True

    def edit_name(self, name: str):
        """Edits the name of the task."""
        self.name = name

@dataclass
class Pet:
    """Represents a pet, its details, and its list of tasks."""
    name: str
    breed: str
    age: int
    tasks: List[Task] = field(default_factory=list)
    diet: List[str] = field(default_factory=list)
    medication: List[str] = field(default_factory=list)
    satisfactoryLevel: float = 0.0

    def add_task(self, task: Task):
        """Adds a task to the pet's list of tasks."""
        self.tasks.append(task)

    def add_to_diet(self, item: str):
        """Adds a food item to the pet's diet."""
        self.diet.append(item)

    def add_to_medication(self, item: str):
        """Adds a medication to the pet's medication list."""
        self.medication.append(item)

    def calculate_satisfaction(self) -> float:
        """Calculates the pet's satisfaction level based on various factors."""
        # This logic will depend on completed tasks, etc.
        pass

class Owner:
    """Manages multiple pets and provides access to all their tasks."""
    def __init__(self, name: str):
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        """Adds a pet to the owner's list of pets."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Returns a single list of all tasks for all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

class Scheduler:
    """The 'Brain' that retrieves, organizes, and manages tasks across pets."""
    def __init__(self, owner: Owner):
        self.owner = owner

    def generate_plan(self, available_time: int) -> List[Task]:
        """
        Retrieves all tasks from the owner's pets, and creates an 
        optimized schedule based on priority, time, and other constraints.
        """
        all_tasks = self.owner.get_all_tasks()
        # Core scheduling logic will go here
        pass
