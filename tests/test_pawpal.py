"""Quick tests for the PawPal+ logic layer."""

from datetime import date, time, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_changes_status():
    task = Task("Morning walk", "Walk around the block", 30, "high")
    assert task.is_complete is False

    task.mark_complete()

    assert task.is_complete is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog", gender="female", age=3)
    assert len(pet.tasks) == 0

    pet.add_task(Task("Feeding", "Breakfast", 10, "high"))

    assert len(pet.tasks) == 1


def _owner_with_mochi_and_rex():
    """Build a small owner/pet/task fixture reused across several tests."""
    owner = Owner(name="Jordan", contact_phone="555-1234", email="jordan@example.com")
    mochi = Pet(name="Mochi", species="dog", gender="female", age=3)
    rex = Pet(name="Rex", species="cat", gender="male", age=5)
    owner.add_pet(mochi)
    owner.add_pet(rex)
    return owner, mochi, rex


# --- Sorting correctness -----------------------------------------------


def test_sort_by_time_returns_chronological_order():
    owner, mochi, rex = _owner_with_mochi_and_rex()
    # Added out of order on purpose: 18:00, then 08:00, then 08:30.
    rex.add_task(Task("Evening play", "Play", 15, "low", start_time=time(18, 0)))
    mochi.add_task(Task("Morning walk", "Walk", 30, "high", start_time=time(8, 0)))
    mochi.add_task(Task("Feeding", "Breakfast", 10, "high", start_time=time(8, 30)))

    scheduler = Scheduler(schedule_date=date.today())
    sorted_pairs = scheduler.sort_by_time(owner)

    sorted_times = [task.start_time for _, task in sorted_pairs]
    assert sorted_times == sorted(sorted_times)
    assert [task.name for _, task in sorted_pairs] == ["Morning walk", "Feeding", "Evening play"]


def test_sort_by_time_excludes_untimed_tasks():
    owner, mochi, _ = _owner_with_mochi_and_rex()
    mochi.add_task(Task("Morning walk", "Walk", 30, "high", start_time=time(8, 0)))
    mochi.add_task(Task("Play", "No fixed time", 15, "low"))  # start_time=None

    scheduler = Scheduler(schedule_date=date.today())
    sorted_pairs = scheduler.sort_by_time(owner)

    assert len(sorted_pairs) == 1
    assert sorted_pairs[0][1].name == "Morning walk"


# --- Filtering ------------------------------------------------------------


def test_filter_tasks_by_pet_name():
    owner, mochi, rex = _owner_with_mochi_and_rex()
    mochi.add_task(Task("Morning walk", "Walk", 30, "high"))
    rex.add_task(Task("Litter box", "Clean", 5, "medium"))

    scheduler = Scheduler(schedule_date=date.today())
    rex_only = scheduler.filter_tasks(owner, pet_name="Rex")

    assert len(rex_only) == 1
    assert rex_only[0][1].name == "Litter box"


def test_filter_tasks_by_completion_status():
    owner, mochi, _ = _owner_with_mochi_and_rex()
    done = Task("Feeding", "Breakfast", 10, "high")
    done.mark_complete()
    pending = Task("Walk", "Walk", 30, "high")
    mochi.add_task(done)
    mochi.add_task(pending)

    scheduler = Scheduler(schedule_date=date.today())
    incomplete = scheduler.filter_tasks(owner, is_complete=False)

    assert len(incomplete) == 1
    assert incomplete[0][1].name == "Walk"


def test_filter_tasks_on_pet_with_no_tasks_returns_empty():
    owner, mochi, rex = _owner_with_mochi_and_rex()
    mochi.add_task(Task("Morning walk", "Walk", 30, "high"))
    # Rex has zero tasks.

    scheduler = Scheduler(schedule_date=date.today())
    rex_only = scheduler.filter_tasks(owner, pet_name="Rex")

    assert rex_only == []


# --- Recurrence logic -------------------------------------------------


def test_mark_task_complete_creates_next_daily_occurrence():
    pet = Pet(name="Mochi", species="dog", gender="female", age=3)
    today = date.today()
    pet.add_task(Task("Medication", "Give meds", 5, "high", frequency="daily", due_date=today))

    next_task = pet.mark_task_complete("Medication")

    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.is_complete is False
    assert len(pet.tasks) == 2
    assert pet.tasks[0].is_complete is True  # the original is marked done, not replaced


def test_mark_task_complete_on_non_recurring_task_does_not_duplicate():
    pet = Pet(name="Mochi", species="dog", gender="female", age=3)
    pet.add_task(Task("One-off vet visit", "Checkup", 30, "high"))

    next_task = pet.mark_task_complete("One-off vet visit")

    assert next_task is None
    assert len(pet.tasks) == 1
    assert pet.tasks[0].is_complete is True


# --- Conflict detection -------------------------------------------------


def test_detect_conflicts_flags_same_time_different_pets():
    owner, mochi, rex = _owner_with_mochi_and_rex()
    mochi.add_task(Task("Morning walk", "Walk", 30, "high", start_time=time(8, 0)))
    rex.add_task(Task("Vet call", "Call vet", 10, "medium", start_time=time(8, 0)))

    scheduler = Scheduler(schedule_date=date.today())
    conflicts = scheduler.detect_conflicts(owner)

    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]


def test_detect_conflicts_returns_empty_when_no_overlap():
    owner, mochi, rex = _owner_with_mochi_and_rex()
    mochi.add_task(Task("Morning walk", "Walk", 30, "high", start_time=time(8, 0)))
    rex.add_task(Task("Evening play", "Play", 15, "low", start_time=time(18, 0)))

    scheduler = Scheduler(schedule_date=date.today())
    assert scheduler.detect_conflicts(owner) == []


def test_detect_conflicts_with_no_tasks_returns_empty():
    owner, _, _ = _owner_with_mochi_and_rex()

    scheduler = Scheduler(schedule_date=date.today())
    assert scheduler.detect_conflicts(owner) == []
