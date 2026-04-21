from dataclasses import dataclass, field
from typing import List, Dict
from datetime import date, timedelta, datetime


@dataclass
class Task:
    """Represents a single care task for a pet."""
    name: str  # Description of the task
    duration: str  # Duration in "HH:MM"
    time: str # Start time in "HH:MM"
    priority: int # e.g., 1-5 (1 is lowest)
    frequency: str # e.g., 'daily', 'weekly'
    is_completed: bool = False
    due_date: date = None

    def __post_init__(self):
        if self.due_date is None:
            self.due_date = date.today()

    def mark_as_complete(self):
        """Marks this task as complete."""
        self.is_completed = True

    def edit_name(self, name: str):
        """Updates the name of this task."""
        self.name = name

    @property
    def duration_in_minutes(self) -> int:
        """Returns the task's duration in minutes."""
        try:
            hours, minutes = map(int, self.duration.split(':'))
            return hours * 60 + minutes
        except ValueError:
            return 0

@dataclass
class Pet:
    """Represents a pet, its details, and its list of tasks."""
    name: str
    breed: str
    age: int
    general_info: str = ""
    tasks: List[Task] = field(default_factory=list)
    satisfactoryLevel: float = 0.0

    def add_task(self, task: Task):
        """Adds a new task to this pet's task list."""
        self.tasks.append(task)

        satisfaction = (len(completed_tasks) / len(self.tasks)) * 100
        self.satisfactoryLevel = satisfaction
        return self.satisfactoryLevel

class Owner:
    """Manages multiple pets and provides access to all their tasks."""
    def __init__(self, name: str):
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        """Adds a new pet to this owner's pet list."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Returns a combined list of all tasks for all of this owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

class Scheduler:
    """The 'Brain' that retrieves, organizes, and manages tasks across pets."""
    def __init__(self, owner: Owner):
        self.owner = owner

    def get_conflicts(self) -> Dict[str, List[str]]:
        """
        Checks for tasks scheduled at the same time and returns a dictionary of conflicts.
        """
        all_tasks = self.owner.get_all_tasks()
        times_seen = {}
        conflicts = {}

        for task in all_tasks:
            if not task.is_completed and task.time:
                if task.time in times_seen:
                    # If we've seen it once, it's a conflict now
                    if task.time not in conflicts:
                        conflicts[task.time] = [times_seen[task.time]]
                    conflicts[task.time].append(task.name)
                else:
                    times_seen[task.time] = task.name
        return conflicts

    def generate_plan(self, available_time: int) -> List[Task]:
        """
        Generates a schedule of tasks that fits within the owner's available time.
        """
        all_tasks = self.owner.get_all_tasks()
        
        # 1. Filter out completed tasks
        uncompleted_tasks = [t for t in all_tasks if not t.is_completed]

        # Sort by priority (desc) and then by start time (asc)
        def sort_key(task):
            # Fallback for tasks without a specific time
            start_time = datetime.strptime(task.time, "%H:%M").time() if task.time else datetime.min.time()
            return (-task.priority, start_time)

        sorted_tasks = sorted(uncompleted_tasks, key=sort_key)
        
        # 2. Build the plan within the available time
        plan = []
        time_spent = 0
        for task in sorted_tasks:
            if time_spent + task.duration_in_minutes <= available_time:
                plan.append(task)
                time_spent += task.duration_in_minutes
                
        return plan

    def complete_task(self, task_to_complete: Task):
        """
        Marks a task as complete and creates a new one if it's recurring.
        """
        task_to_complete.mark_as_complete()

        if task_to_complete.frequency in ['daily', 'weekly']:
            # Find which pet this task belongs to
            pet_owner = None
            for pet in self.owner.pets:
                if task_to_complete in pet.tasks:
                    pet_owner = pet
                    break
            
            if pet_owner:
                new_due_date = None
                if task_to_complete.frequency == 'daily':
                    # Use timedelta to get the next day
                    new_due_date = task_to_complete.due_date + timedelta(days=1)
                elif task_to_complete.frequency == 'weekly':
                    new_due_date = task_to_complete.due_date + timedelta(weeks=7)

                if new_due_date:
                    new_task = Task(
                        name=task_to_complete.name,
                        duration=task_to_complete.duration,
                        time=task_to_complete.time,
                        priority=task_to_complete.priority,
                        frequency=task_to_complete.frequency,
                        due_date=new_due_date
                    )
                    pet_owner.add_task(new_task)
    
    def filter_tasks(self, status: str = None, pet_name: str = None) -> List[Task]:
        """
        Filters tasks by completion status or pet name.
        - status: 'completed', 'incomplete', or None
        - pet_name: The name of the pet to filter by, or None
        """
        source_pets = self.owner.pets
        
        # Filter by pet name first if provided
        if pet_name:
            source_pets = [p for p in source_pets if p.name == pet_name]

        # Get all tasks from the filtered list of pets
        tasks_to_filter = []
        for pet in source_pets:
            tasks_to_filter.extend(pet.tasks)

        # Filter by completion status if provided
        if status == 'completed':
            return [t for t in tasks_to_filter if t.is_completed]
        elif status == 'incomplete':
            return [t for t in tasks_to_filter if not t.is_completed]
        
        return tasks_to_filter

    def sort_by_time(self) -> List[Task]:
        """Returns all tasks sorted by time duration (shortest first)."""
        all_tasks = self.owner.get_all_tasks()
        return sorted(all_tasks, key=lambda t: t.duration_in_minutes)

    def sort_by_start_time(self) -> List[Task]:
        """Returns all tasks sorted by start time (earliest first)."""
        all_tasks = self.owner.get_all_tasks()
        # Combine date and time for accurate sorting
        return sorted(all_tasks, key=lambda t: datetime.combine(t.due_date, datetime.strptime(t.time, "%H:%M").time()))

