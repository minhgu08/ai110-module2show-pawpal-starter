"""Demo/testing ground for the PawPal+ logic layer. Run with: python main.py"""

from datetime import date, time

# Import classes from pawpal_system
from pawpal_system import Owner, Pet, Scheduler, Task

# Create an owner
owner = Owner(name="Jordan", contact_phone="555-1234", email="jordan@example.com")

# Create Pet 1
mochi = Pet(name="Mochi", species="dog", gender="female", age=3)
# Task 1 - Mochi
mochi.add_task(Task("Morning walk", "Walk around the block", 30, "high", start_time=time(8, 0)))
# Task 2 - Mochi
mochi.add_task(Task("Feeding", "Breakfast", 10, "high", start_time=time(8, 30)))

# Create Pet 2
rex = Pet(name="Rex", species="cat", gender="male", age=5)
# Task 3 - REX
litter_box = Task("Litter box", "Clean litter box", 5, "medium")
litter_box.mark_complete()
rex.add_task(litter_box)
# Task 4 - REX
rex.add_task(Task("Evening play", "Play with feather toy", 15, "low", start_time=time(18, 0)))
# Task 5 - REX (deliberately conflicts with Mochi's 8:00 walk)
rex.add_task(Task("Vet check-in call", "Call the vet", 10, "medium", start_time=time(8, 0)))
# Task 6 - Mochi (recurring daily task, to test auto-creation of next occurrence)
mochi.add_task(
    Task("Medication", "Give heart medication", 5, "high", frequency="daily", due_date=date.today())
)

owner.add_pet(mochi)
owner.add_pet(rex)

scheduler = Scheduler(schedule_date=date.today())
scheduler.generate_plan(owner)

print(f"Today's Schedule ({scheduler.schedule_date}):")
print("-" * 40)
for line in scheduler.explain_plan():
    print(line)

print()
print("Sorted by time (sort_by_time):")
print("-" * 40)
for pet, task in scheduler.sort_by_time(owner):
    print(f"{task.start_time.strftime('%H:%M')} - {pet.name}: {task.name}")

print()
print("Rex's tasks only (filter_tasks by pet):")
print("-" * 40)
for pet, task in scheduler.filter_tasks(owner, pet_name="Rex"):
    print(f"{pet.name}: {task.name} (complete={task.is_complete})")

print()
print("Incomplete tasks only (filter_tasks by status):")
print("-" * 40)
for pet, task in scheduler.filter_tasks(owner, is_complete=False):
    print(f"{pet.name}: {task.name}")

print()
print("Recurring task check (mark_task_complete):")
print("-" * 40)
print(f"Before: Mochi has {len(mochi.tasks)} tasks")
next_task = mochi.mark_task_complete("Medication")
print(f"After:  Mochi has {len(mochi.tasks)} tasks")
if next_task:
    print(f"Next occurrence created: '{next_task.name}' due {next_task.due_date} (frequency={next_task.frequency})")

print()
print("Conflict check:")
print("-" * 40)
conflicts = scheduler.detect_conflicts(owner)
if conflicts:
    for warning in conflicts:
        print(warning)
else:
    print("No conflicts found.")
