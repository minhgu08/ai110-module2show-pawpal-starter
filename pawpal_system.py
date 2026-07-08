"""Logic layer for PawPal+: Owner, Pet, Task, and Scheduler classes."""

from dataclasses import dataclass, field
from datetime import date, time, timedelta

_PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}
_FREQUENCY_DELTA = {"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}


@dataclass
class Task:
    """A single pet care activity (e.g. walk, feeding) with duration and priority."""

    name: str
    description: str
    duration_minutes: int
    priority: str  # "low" | "medium" | "high"
    start_time: time = None  # optional fixed time; unset tasks are ordered by priority
    frequency: str = None  # None | "daily" | "weekly"
    due_date: date = None  # the date this occurrence is due; required for recurring tasks
    is_complete: bool = False

    def mark_complete(self):
        """Mark this task as done."""
        self.is_complete = True

    def mark_incomplete(self):
        """Revert this task to not-done."""
        self.is_complete = False

    def next_occurrence(self):
        """Return a new Task instance for the next scheduled occurrence, or None if not recurring.

        Uses timedelta so "daily" always lands exactly 1 day later and
        "weekly" exactly 7 days later, regardless of month/year boundaries.
        """
        if self.frequency not in _FREQUENCY_DELTA:
            return None
        base_date = self.due_date if self.due_date is not None else date.today()
        next_due_date = base_date + _FREQUENCY_DELTA[self.frequency]
        return Task(
            name=self.name,
            description=self.description,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            start_time=self.start_time,
            frequency=self.frequency,
            due_date=next_due_date,
            is_complete=False,
        )


@dataclass
class Pet:
    """A pet's basic info plus the list of tasks assigned to it."""

    name: str
    species: str
    gender: str
    age: int
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's list."""
        self.tasks.append(task)

    def edit_task(self, task_name: str, **updates):
        """Update fields on the first task matching task_name."""
        task = self._find_task(task_name)
        if task is None:
            raise ValueError(f"No task named {task_name!r} for pet {self.name!r}")
        for field_name, value in updates.items():
            setattr(task, field_name, value)

    def delete_task(self, task_name: str):
        """Remove the first task matching task_name."""
        task = self._find_task(task_name)
        if task is None:
            raise ValueError(f"No task named {task_name!r} for pet {self.name!r}")
        self.tasks.remove(task)

    def mark_task_complete(self, task_name: str):
        """Mark a task complete and, if it recurs, add its next occurrence.

        Returns the newly created Task for the next occurrence, or None if
        the completed task doesn't recur.
        """
        task = self._find_task(task_name)
        if task is None:
            raise ValueError(f"No task named {task_name!r} for pet {self.name!r}")
        task.mark_complete()
        next_task = task.next_occurrence()
        if next_task is not None:
            self.add_task(next_task)
        return next_task

    def _find_task(self, task_name: str):
        """Look up a task on this pet by name, or return None."""
        return next((t for t in self.tasks if t.name == task_name), None)


@dataclass
class Owner:
    """A pet owner who manages one or more pets and their availability."""

    name: str
    contact_phone: str
    email: str
    availability: dict = field(default_factory=dict)
    pets: list = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's list."""
        self.pets.append(pet)

    def edit_pet_info(self, pet_name: str, **updates):
        """Update fields on the first pet matching pet_name."""
        pet = self._find_pet(pet_name)
        if pet is None:
            raise ValueError(f"No pet named {pet_name!r}")
        for field_name, value in updates.items():
            setattr(pet, field_name, value)

    def delete_pet(self, pet_name: str):
        """Remove the first pet matching pet_name."""
        pet = self._find_pet(pet_name)
        if pet is None:
            raise ValueError(f"No pet named {pet_name!r}")
        self.pets.remove(pet)

    def update_availability(self, availability: dict):
        """Replace/merge this owner's available time windows."""
        self.availability.update(availability)

    def get_all_tasks(self):
        """Return (pet, task) pairs across all of this owner's pets."""
        return [(pet, task) for pet in self.pets for task in pet.tasks]

    def _find_pet(self, pet_name: str):
        """Look up this owner's pet by name, or return None."""
        return next((p for p in self.pets if p.name == pet_name), None)


class Scheduler:
    """The "brain": builds and explains a daily plan from an owner's pets' tasks."""

    def __init__(self, schedule_date: date, allow_overlap: bool = False):
        """Set up an empty scheduler for a given date."""
        self.schedule_date = schedule_date
        self.allow_overlap = allow_overlap
        self.plan = []  # list of (pet, task) in scheduled order, set by generate_plan()

    def sort_by_time(self, owner: Owner):
        """Return (pet, task) pairs that have a start_time, earliest to latest.

        Tasks without a start_time are excluded since they have nothing to
        sort on; use filter_tasks() first if you need those too.
        """
        pairs = owner.get_all_tasks()
        timed = [pair for pair in pairs if pair[1].start_time is not None]
        return sorted(timed, key=lambda pair: pair[1].start_time)

    def filter_tasks(self, owner: Owner, pet_name: str = None, is_complete: bool = None):
        """Return (pet, task) pairs matching the given filters.

        Both filters are optional and combine with AND when both are given;
        pass none to get every task back.
        """
        pairs = owner.get_all_tasks()
        if pet_name is not None:
            pairs = [pair for pair in pairs if pair[0].name == pet_name]
        if is_complete is not None:
            pairs = [pair for pair in pairs if pair[1].is_complete == is_complete]
        return pairs

    def generate_plan(self, owner: Owner):
        """Build a daily plan: tasks with a start_time first (in time order),
        then remaining tasks ordered by priority (high to low)."""
        pairs = owner.get_all_tasks()
        timed = sorted(
            (pair for pair in pairs if pair[1].start_time is not None),
            key=lambda pair: pair[1].start_time,
        )
        untimed = sorted(
            (pair for pair in pairs if pair[1].start_time is None),
            key=lambda pair: _PRIORITY_RANK.get(pair[1].priority, 99),
        )
        self.plan = timed + untimed
        return self.plan

    def detect_conflicts(self, owner: Owner):
        """Find tasks scheduled at the exact same start_time (any pet).

        Lightweight check: groups timed tasks by start_time and flags any
        slot with more than one task. Returns a list of warning strings
        instead of raising, so callers can display them without crashing.
        """
        pairs = owner.get_all_tasks()
        by_time = {}
        for pet, task in pairs:
            if task.start_time is None:
                continue
            by_time.setdefault(task.start_time, []).append((pet, task))

        warnings = []
        for start_time, scheduled in by_time.items():
            if len(scheduled) < 2:
                continue
            names = ", ".join(f"{pet.name}'s '{task.name}'" for pet, task in scheduled)
            warnings.append(f"WARNING: Conflict at {start_time.strftime('%H:%M')}: {names} are scheduled at the same time.")
        return warnings

    def explain_plan(self):
        """Explain why tasks were chosen/ordered the way they were."""
        lines = []
        for pet, task in self.plan:
            if task.start_time is not None:
                reason = f"scheduled for {task.start_time.strftime('%H:%M')}"
            else:
                reason = f"{task.priority} priority, no fixed time"
            lines.append(f"{pet.name}: {task.name} ({task.duration_minutes} min) - {reason}")
        return lines
