# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My UML diagram has four main classes that are now reflected in pawpal_system.py:

Class 1: Pet
Stores pet information (name, species, gender, age) and its assigned tasks. It manages its own tasks.

Class 2: Owner
Stores owner information, availability, and their pets. It manages pets and provides task information to Scheduler.

Class 3: Task
Represents a care activity with information like name, description, duration, priority, and whether it repeats.

Class 4: Scheduler
Handles scheduling logic by collecting tasks from the owner's pets, generating a plan, and explaining the schedule.

This design improved from my original brainstorm by separating data ownership from scheduling logic. My first idea placed some owner management functions inside Scheduler, but I realized it made the responsibilities less clear.

<details>
<summary>Original brainstorm (Steps 1-2)</summary>

Step 1: Core actions user should be able to perform:
1. Add, remove, or edit their new or current pet information
2. Schedule for a pet, for example: a walk
3. Review or Edit the current task corresponding to their pet 

Step 2: List the Building Blocks
Main objects: attributes and methods
1. Attributes: What information the object needs to hold
2. Methods: what actions the oject can perform

Brainstorm the main objects needed for the system. For each object, determine:
What information it needs to hold (attributes)
1. Object 1: Pet's info 
    - Pet's name, gender, species, age
2. Object 2: Owner's info
    - Owner's name, contact tel, email, availability
3. Object 3: Scheduling system / Scheduler
    - Date, Appointment time, duration in minutes, recurrent tasks yes/no, conflict allowing (overlapping appointment)
4. Object 4: Task Tracking 
    - Task name, task description

What actions it can perform (methods)
1. Object 1 - Pet's Method:
    - Enter new pet's name and info, edit pet's current info, delete info of a specific pet
2. Object 2: Owner: 
    - Add a new owner, edit a current owner info
    - Add or update owner's available time
3. Object 3: Scheduler 
    - Add a new owner, edit a current owner info
    - Add or update owner's available time
    - Set appointment
4. Object 4: Task 
    - Add a new task, update current task

</details>

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors




b. Design changes
After creating pawpal_system.py, I asked Claude to review my design and look for missing relationships or possible issues. Two changes I made:

1. Change 1: Owner.get_all_tasks()
- Originally, it returned only a list of tasks without showing which pet they belonged to. I changed it to return pet- task pairs so the schedule can show information like "Mochi's walk" instead of only "walk"

2. Change 2: Scheduler
- Scheduler did not store the generated plan, so explain_plan() had nothing to reference. I added self.plan so the Scheduler can explain the generated schedule later.

One thing I would still improve is deciding whether tasks should store preferred times or whether Scheduler should assign start times.

---

## 2. Scheduling Logic and Tradeoffs

2a. Constraints and priorities

- What constraints does your scheduler consider (for example: time, priority, preferences)? And How did you decide which constraints mattered most?
--> Ans: The scheduler considers task time and priority when creating a plan. I focused on these because they directly affect how tasks are ordered in the daily schedule. Completion status is used separately when filtering tasks, and recurring tasks are handled when creating future task occurrences.

2b. Tradeoffs
--> Ans: Scheduler.detect_conflicts() currently only checks tasks with the same start_time. It does not detect overlapping ranges, such as an 8:00–8:30 walk and an 8:15 feeding.

I decided to keep this simpler version because it handles the most obvious double-booking cases and is easier to understand and maintain. A more advanced version would compare task durations and detect all overlapping time ranges, which would be a future improvement.

I also considered an AI suggestion using groupby, but I kept the dict-based approach because groupby depends on the tasks already being sorted by start_time, which my scheduler does not guarantee.
---

## 3. AI Collaboration

a. How you used AI?

- How did you use AI tools during this project? 
--> Ans:I used AI to review code, suggest updates, add comments, polish my reflection writing, and review relationships between classes using Mermaid.js.

- What kinds of prompts or questions were most helpful?
--> Ans: The most helpful prompts were asking AI to review the design decisions, explain errors, and suggest possible improvements.

b. Judgment and verification

- Describe one moment where you did not accept an AI suggestion as-is. And How did you evaluate or verify what the AI suggested?
--> Ans: AI suggested a shorter groupby rewrite for detect_conflicts(), but I decided not to use it. I looked into how groupby works and realized it depends on tasks already being sorted by start_time, which my scheduler does not enforce.

I kept the dict-based approach because it was easier for me to understand and less likely to break if the code changes later.

c. How did separate chat sessions for different phases help you stay organized?
--> Ans: Using separate chat sessions helped me focus on one phase at a time, such as design, coding, testing, and reflection. It made it easier to track decisions and avoid mixing different problems together.
---

## 4. Testing and Verification

a. What you tested
- What behaviors did you test and why were these tests important?
--> Ans: I tested four core scheduler behaviors:
1. Sorting tasks by time
2. Filtering by pet and completion status
3. Handling recurring tasks after completion.
4. Detecting conflicts. 

These tests help verify the main scheduling logic and catch errors that could silently create incorrect daily plans.

b. Confidence

- How confident are you that your scheduler works correctly? Amd What edge cases would you test next if you had more time?
--> Answer: All 12 tests pass, confident that the core scheduler logic works correctly.

I tested both normal cases and edge cases like empty lists, untimed tasks, and non-recurring tasks. If I had more time, I would add tests for overlapping time conflicts, more recurrence scenarios, and the full generate_plan() process with different priority levels.

---

## 5. Reflection

a. What went well

- What part of this project are you most satisfied with?
--> Ans: I'm satisfied with separating responsibilities between Owner/Pet (storing data) and Scheduler (handling scheduling logic). It made adding features like detect_conflicts() easier without changing the existing data structure.

b. What you would improve

- If you had another iteration, what would you improve or redesign?
--> Ans: 
detect_conflicts() currently only checks exact matching times, not overlapping time ranges. If I had another iteration, I would improve it to compare task durations so it can detect more realistic scheduling conflicts.


c. Key takeaway

- What is one important thing you learned about designing systems or working with AI on this project?
--> Ans:
I learned that AI can quickly suggest solutions, but I still need to understand and verify them before using them. For example, I reviewed the AI's groupby suggestion and noticed it depended on sorted input. Using AI effectively means asking questions, checking assumptions, and making the final design decisions myself.

