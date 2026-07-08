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

**Core behaviors verified:**
1. Sorting correctness — timed tasks are returned in chronological order.
2. Filtering — tasks can be filtered by pet name and/or completion status.
3. Recurrence logic — completing a daily/weekly task automatically schedules the next occurrence.
4. Conflict detection — two tasks at the exact same time are flagged as a scheduling conflict.
5. Task/pet state changes — marking a task complete and adding tasks to a pet update state correctly.

```bash
# Run the full test suite:
python -m pytest

# Run with coverage:
pytest --cov
```

The suite (`tests/test_pawpal.py`) covers:
- **Sorting correctness** — `sort_by_time()` returns tasks in chronological order regardless of insertion order, and excludes untimed tasks.
- **Filtering** — `filter_tasks()` by pet name, by completion status, and confirms a pet with zero tasks returns an empty result rather than an error.
- **Recurrence logic** — `mark_task_complete()` on a daily task creates a new task due exactly one day later (via `timedelta`) and leaves the original marked complete; a non-recurring task does not spawn a duplicate.
- **Conflict detection** — `detect_conflicts()` flags two tasks (different pets) at the exact same time, and returns an empty list when there's no overlap or no tasks at all.

Sample test output:

```
============================= test session starts =============================
platform win32 -- Python 3.13.0, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\SN\CP\W4\ai110-module2show-pawpal-starter
plugins: anyio-4.14.1
collected 12 items

tests/test_pawpal.py::test_mark_complete_changes_status PASSED           [  8%]
tests/test_pawpal.py::test_add_task_increases_pet_task_count PASSED      [ 16%]
tests/test_pawpal.py::test_sort_by_time_returns_chronological_order PASSED [ 25%]
tests/test_pawpal.py::test_sort_by_time_excludes_untimed_tasks PASSED    [ 33%]
tests/test_pawpal.py::test_filter_tasks_by_pet_name PASSED               [ 41%]
tests/test_pawpal.py::test_filter_tasks_by_completion_status PASSED      [ 50%]
tests/test_pawpal.py::test_filter_tasks_on_pet_with_no_tasks_returns_empty PASSED [ 58%]
tests/test_pawpal.py::test_mark_task_complete_creates_next_daily_occurrence PASSED [ 66%]
tests/test_pawpal.py::test_mark_task_complete_on_non_recurring_task_does_not_duplicate PASSED [ 75%]
tests/test_pawpal.py::test_detect_conflicts_flags_same_time_different_pets PASSED [ 83%]
tests/test_pawpal.py::test_detect_conflicts_returns_empty_when_no_overlap PASSED [ 91%]
tests/test_pawpal.py::test_detect_conflicts_with_no_tasks_returns_empty PASSED [100%]

============================= 12 passed in 0.04s ==============================
```

**Confidence Level:** ⭐⭐⭐⭐☆ (4/5) — all core scheduling algorithms (sorting, filtering, recurrence, conflict detection) are covered with both happy-path and edge-case tests. Not yet tested: the `Scheduler.generate_plan()`/`explain_plan()` priority-ordering path for untimed tasks, and the Streamlit UI layer in `app.py`, which is why this isn't a 5/5.

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
