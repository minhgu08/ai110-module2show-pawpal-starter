"""Quick tests for the PawPal+ logic layer."""

from pawpal_system import Pet, Task


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
