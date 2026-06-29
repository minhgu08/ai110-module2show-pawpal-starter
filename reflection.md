# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

#- Briefly describe your initial UML design.
#- What classes did you include, and what responsibilities did you assign to each?
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

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors




**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
