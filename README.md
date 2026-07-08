# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output (Phase 2- Step 2:Create and Run a Demo Script)

Output from running `python main.py`:

```
Today's Schedule (2026-07-07):
----------------------------------------
Mochi: Morning walk (30 min) - scheduled for 08:00
Mochi: Feeding (10 min) - scheduled for 08:30
Rex: Evening play (15 min) - scheduled for 18:00
Rex: Litter box (5 min) - medium priority, no fixed time
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Returns `(pet, task)` pairs with a `start_time`, sorted earliest to latest via `sorted()` with a lambda key on `task.start_time`. Untimed tasks are excluded — use `filter_tasks()` for those. |
| Filtering | `Scheduler.filter_tasks(owner, pet_name=None, is_complete=None)` | Filters `(pet, task)` pairs by pet name and/or completion status; both filters are optional and combine with AND. |
| Conflict handling | `Scheduler.detect_conflicts(owner)` | Lightweight check: groups all timed tasks by exact `start_time` (across every pet, not just one) and returns a warning string for any time slot with 2+ tasks, instead of raising an exception. Only catches exact-time matches, not overlapping durations — see `reflection.md` § 2b for that tradeoff. |
| Recurring tasks | `Task.next_occurrence()`, `Pet.mark_task_complete(task_name)` | `Task.frequency` (`"daily"`/`"weekly"`) plus `Task.due_date` drive recurrence. Calling `Pet.mark_task_complete()` marks the task done and, if it recurs, automatically creates and appends the next occurrence using `timedelta` (`+1 day` or `+7 days`) so month/year boundaries are handled correctly. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
