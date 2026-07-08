"""Logic layer for PawPal+: Owner, Pet, Task, and Scheduler classes."""

from dataclasses import dataclass, field
from datetime import date


@dataclass
class Task:
    """A single pet care activity (e.g. walk, feeding) with duration and priority."""

    name: str
    description: str
    duration_minutes: int
    priority: str  # "low" | "medium" | "high"
    is_recurring: bool = False
    is_complete: bool = False

    def mark_complete(self):
        pass

    def mark_incomplete(self):
        pass


@dataclass
class Pet:
    """A pet's basic info plus the list of tasks assigned to it."""

    name: str
    species: str
    gender: str
    age: int
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        pass

    def edit_task(self, task_name: str, **updates):
        pass

    def delete_task(self, task_name: str):
        pass


@dataclass
class Owner:
    """A pet owner who manages one or more pets and their availability."""

    name: str
    contact_phone: str
    email: str
    availability: dict = field(default_factory=dict)
    pets: list = field(default_factory=list)

    def add_pet(self, pet: Pet):
        pass

    def edit_pet_info(self, pet_name: str, **updates):
        pass

    def delete_pet(self, pet_name: str):
        pass

    def update_availability(self, availability: dict):
        pass

    def get_all_tasks(self):
        """Collect tasks across all of this owner's pets."""
        pass


class Scheduler:
    """The "brain": builds and explains a daily plan from an owner's pets' tasks."""

    def __init__(self, schedule_date: date, allow_overlap: bool = False):
        self.schedule_date = schedule_date
        self.allow_overlap = allow_overlap

    def generate_plan(self, owner: Owner):
        """Build a daily plan from the owner's pets' tasks."""
        pass

    def explain_plan(self):
        """Explain why tasks were chosen/ordered the way they were."""
        pass
