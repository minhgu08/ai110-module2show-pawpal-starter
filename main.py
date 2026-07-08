"""Demo/testing ground for the PawPal+ logic layer. Run with: python main.py"""

from datetime import date, time
# Import classes from pawpal_system
from pawpal_system import Owner, Pet, Scheduler, Task

# Create an owner
owner = Owner(name="Jordan", contact_phone="555-1234", email="jordan@example.com")

# Create Pet 1
mochi = Pet(name="Mochi", species="dog", gender="female", age=3)
mochi.add_task(Task("Morning walk", "Walk around the block", 30, "high", start_time=time(8, 0)))
mochi.add_task(Task("Feeding", "Breakfast", 10, "high", start_time=time(8, 30)))

# Create Pet 2
rex = Pet(name="Rex", species="cat", gender="male", age=5)
rex.add_task(Task("Litter box", "Clean litter box", 5, "medium"))
rex.add_task(Task("Evening play", "Play with feather toy", 15, "low", start_time=time(18, 0)))

owner.add_pet(mochi)
owner.add_pet(rex)

scheduler = Scheduler(schedule_date=date.today())
scheduler.generate_plan(owner)

print(f"Today's Schedule ({scheduler.schedule_date}):")
print("-" * 40)
for line in scheduler.explain_plan():
    print(line)
