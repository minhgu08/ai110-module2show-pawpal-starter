from datetime import date, time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

with st.expander("Scenario", expanded=False):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

st.divider()

# Streamlit reruns this whole script on every interaction, so the Owner must
# live in st.session_state or it would be recreated (and emptied) each time.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", contact_phone="", email="")

owner = st.session_state.owner

st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name)

st.divider()

st.subheader("Pets")
with st.form("add_pet_form", clear_on_submit=True):
    st.markdown("**Add a pet**")
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    gender = st.selectbox("Gender", ["female", "male", "unknown"])
    age = st.number_input("Age", min_value=0, max_value=40, value=1)
    if st.form_submit_button("Add pet"):
        owner.add_pet(Pet(name=pet_name, species=species, gender=gender, age=int(age)))
        st.success(f"Added pet: {pet_name}")

if not owner.pets:
    st.info("No pets yet. Add one above.")
else:
    st.write("Current pets:", ", ".join(p.name for p in owner.pets))

st.divider()

st.subheader("Tasks")

if owner.pets:
    with st.form("add_task_form", clear_on_submit=True):
        st.markdown("**Add a task**")
        target_pet_name = st.selectbox("Pet", [p.name for p in owner.pets])
        task_title = st.text_input("Task title", value="Morning walk")
        col1, col2 = st.columns(2)
        with col1:
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        with col2:
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        has_time = st.checkbox("Set a fixed time?")
        task_time = st.time_input("Time", value=time(8, 0), disabled=not has_time)
        if st.form_submit_button("Add task"):
            target_pet = next(p for p in owner.pets if p.name == target_pet_name)
            target_pet.add_task(
                Task(
                    name=task_title,
                    description=task_title,
                    duration_minutes=int(duration),
                    priority=priority,
                    start_time=task_time if has_time else None,
                )
            )
            st.success(f"Added task '{task_title}' to {target_pet_name}")

    all_tasks = owner.get_all_tasks()
    if all_tasks:
        st.write("Current tasks:")
        st.table(
            [
                {
                    "pet": pet.name,
                    "task": task.name,
                    "duration_minutes": task.duration_minutes,
                    "priority": task.priority,
                    "time": task.start_time.strftime("%H:%M") if task.start_time else "-",
                }
                for pet, task in all_tasks
            ]
        )
    else:
        st.info("No tasks yet. Add one above.")
else:
    st.info("Add a pet first before adding tasks.")

st.divider()

st.subheader("Build Schedule")

if st.button("Generate schedule"):
    if not owner.get_all_tasks():
        st.warning("Add at least one pet and task first.")
    else:
        scheduler = Scheduler(schedule_date=date.today())
        scheduler.generate_plan(owner)

        conflicts = scheduler.detect_conflicts(owner)
        if conflicts:
            for warning in conflicts:
                st.warning(warning)
        else:
            st.success("No scheduling conflicts detected.")

        st.write(f"**Today's Schedule ({scheduler.schedule_date}):**")
        st.table(
            [
                {
                    "pet": pet.name,
                    "task": task.name,
                    "time": task.start_time.strftime("%H:%M") if task.start_time else "-",
                    "duration_minutes": task.duration_minutes,
                    "priority": task.priority,
                }
                for pet, task in scheduler.plan
            ]
        )
        with st.expander("Why this order?"):
            for line in scheduler.explain_plan():
                st.write(f"- {line}")
