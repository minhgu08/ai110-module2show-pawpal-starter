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

## ✨ Features

- **Sorting by time** — `Scheduler.sort_by_time()` orders every timed task chronologically, regardless of the order they were entered in.
- **Priority-based fallback** — `Scheduler.generate_plan()` places timed tasks first (earliest to latest), then orders any remaining untimed tasks by priority (high → medium → low).
- **Filtering** — `Scheduler.filter_tasks()` narrows the task list by pet name and/or completion status.
- **Conflict warnings** — `Scheduler.detect_conflicts()` flags when two tasks (for any pets) are scheduled at the exact same time, so double-bookings are caught before the day starts.
- **Daily/weekly recurrence** — `Task.next_occurrence()` and `Pet.mark_task_complete()` automatically schedule the next occurrence of a recurring task once the current one is marked done.
- **Plan explanations** — `Scheduler.explain_plan()` states, in plain language, why each task landed where it did (fixed time vs. priority).

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

### Main UI features

The Streamlit app (`app.py`) is organized into three sections:

- **Owner** — enter/edit the owner's name.
- **Pets** — add a pet (name, species, gender, age) via a form; added pets appear in a running list.
- **Tasks** — add a task to any existing pet (title, duration, priority, and an optional fixed time); all current tasks are shown in a table.
- **Build Schedule** — click "Generate schedule" to run the Scheduler against every pet's tasks. Any conflicts are shown as warnings first, followed by the full schedule as a table, with a collapsible "Why this order?" section explaining the ordering.

### Example workflow

1. Enter an owner name (e.g. "Jordan").
2. Add a pet, "Mochi" (dog).
3. Add a second pet, "Rex" (cat).
4. Add a task "Morning walk" for Mochi at a fixed time of 08:00.
5. Add a task "Vet check-in call" for Rex, also fixed at 08:00.
6. Click "Generate schedule."

### Key Scheduler behaviors shown

- **Conflict warning**: because both tasks above share the 08:00 slot, `detect_conflicts()` raises a warning naming both pets and tasks *before* the schedule is shown — the most useful place for an owner to catch it, since they can fix the clash before committing to the plan.
- **Sorting**: any additional timed tasks (e.g. an 08:30 feeding) appear in the table in chronological order, not the order they were entered.
- **Priority fallback**: tasks with no fixed time (e.g. medication, litter box) are still included, ordered by priority instead of time.
- **Recurrence**: completing a daily task (via the underlying `Pet.mark_task_complete()` logic) automatically schedules its next occurrence one day later.

### Sample CLI output (`python main.py`)

```
Today's Schedule (2026-07-08):
----------------------------------------
Mochi: Morning walk (30 min) - scheduled for 08:00
Rex: Vet check-in call (10 min) - scheduled for 08:00
Mochi: Feeding (10 min) - scheduled for 08:30
Rex: Evening play (15 min) - scheduled for 18:00
Mochi: Medication (5 min) - high priority, no fixed time
Rex: Litter box (5 min) - medium priority, no fixed time

Sorted by time (sort_by_time):
----------------------------------------
08:00 - Mochi: Morning walk
08:00 - Rex: Vet check-in call
08:30 - Mochi: Feeding
18:00 - Rex: Evening play

Rex's tasks only (filter_tasks by pet):
----------------------------------------
Rex: Litter box (complete=True)
Rex: Evening play (complete=False)
Rex: Vet check-in call (complete=False)

Incomplete tasks only (filter_tasks by status):
----------------------------------------
Mochi: Morning walk
Mochi: Feeding
Mochi: Medication
Rex: Evening play
Rex: Vet check-in call

Recurring task check (mark_task_complete):
----------------------------------------
Before: Mochi has 3 tasks
After:  Mochi has 4 tasks
Next occurrence created: 'Medication' due 2026-07-09 (frequency=daily)

Conflict check:
----------------------------------------
WARNING: Conflict at 08:00: Mochi's 'Morning walk', Rex's 'Vet check-in call' are scheduled at the same time.
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
