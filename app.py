import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import datetime

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs")
owner_name = st.text_input("Owner name", value="Jordan")

# Initialize owner in session state
if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name)
else:
    st.session_state.owner.name = owner_name

# --- Pet Management ---
st.markdown("### Your Pets")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add Pet"):
    new_pet = Pet(name=pet_name, breed=species, age=1)  # Default age for simplicity
    st.session_state.owner.add_pet(new_pet)
    st.success(f"Added {pet_name} to your PawPal family!")

if st.session_state.owner.pets:
    pet_choices = {pet.name: pet for pet in st.session_state.owner.pets}
    selected_pet_name = st.selectbox("Select a pet to manage", options=list(pet_choices.keys()))
    st.session_state.selected_pet = pet_choices[selected_pet_name]
    st.write(f"Current pets: {', '.join([pet.name for pet in st.session_state.owner.pets])}")
else:
    st.info("No pets added yet. Add one above to get started!")
    st.session_state.selected_pet = None

st.divider()

# --- Task Management ---
st.markdown("### Add Tasks")
st.caption("Add tasks for your selected pet.")

if st.session_state.selected_pet:
    with st.form("new_task_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            task_title = st.text_input("Task title", value="Morning walk")
            start_time_str = st.text_input("Start time (HH:MM)", value="08:00")
            priority_map = {"low": 1, "medium": 2, "high": 3}
            priority_str = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        with c2:
            duration_hours = st.number_input("Duration (hours)", min_value=0, max_value=10, value=0)
            duration_minutes = st.number_input("Duration (minutes)", min_value=0, max_value=59, value=20)
            frequency = st.selectbox("Frequency", ["daily", "weekly", "once"], index=0)

        submitted = st.form_submit_button("Add Task")
        if submitted:
            try:
                # Validate time format
                datetime.strptime(start_time_str, "%H:%M")
                duration_str = f"{int(duration_hours):02d}:{int(duration_minutes):02d}"
                priority = priority_map[priority_str]

                new_task = Task(
                    name=task_title,
                    duration=duration_str,
                    time=start_time_str,
                    priority=priority,
                    frequency=frequency,
                )
                st.session_state.selected_pet.add_task(new_task)
                st.success(f"Added task '{task_title}' for {st.session_state.selected_pet.name}.")
            except ValueError:
                st.error("Invalid time format. Please use HH:MM.")
else:
    st.warning("Please add and select a pet to manage its tasks.")


# Display tasks for the selected pet
if st.session_state.get("selected_pet") and st.session_state.selected_pet.tasks:
    st.write(f"Current tasks for {st.session_state.selected_pet.name}:")
    
    # Create a scheduler instance to use its methods
    scheduler = Scheduler(st.session_state.owner)

    # --- Filtering and Sorting ---
    st.markdown("#### View and Organize Tasks")
    sort_option = st.selectbox("Sort tasks by:", ["Priority", "Start Time", "Duration"])
    
    tasks_to_display = st.session_state.selected_pet.tasks
    
    if sort_option == "Start Time":
        tasks_to_display = sorted(tasks_to_display, key=lambda t: datetime.strptime(t.time, "%H:%M").time())
    elif sort_option == "Duration":
        tasks_to_display = sorted(tasks_to_display, key=lambda t: t.duration_in_minutes)
    else: # Default to priority
        tasks_to_display = sorted(tasks_to_display, key=lambda t: t.priority, reverse=True)

    # --- Interactive Task List ---
    if not tasks_to_display:
        st.info("No tasks to display based on current filters.")
    else:
        for i, task in enumerate(tasks_to_display):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                status = "✅" if task.is_completed else "❌"
                st.write(f"**{task.name}** ({task.duration}) - Priority: {task.priority} {status}")
                st.caption(f"Starts at {task.time} - Due: {task.due_date.strftime('%Y-%m-%d')}")
            with col2:
                # Disable button if task is already complete
                if st.button("Complete", key=f"complete_{i}_{task.name}", disabled=task.is_completed):
                    scheduler.complete_task(task)
                    st.success(f"Completed task: '{task.name}'!")
                    st.rerun() # Rerun to update the UI immediately
            st.divider()

else:
    st.info("No tasks added for the selected pet yet.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button will generate a plan based on all tasks for all your pets.")
available_time = st.slider(
    "How much time do you have today (in minutes)?", 60, 480, 120
)

if st.button("Generate schedule"):
    if st.session_state.owner.pets:
        scheduler = Scheduler(st.session_state.owner)
        
        # --- Conflict Warning ---
        conflicts = scheduler.get_conflicts()
        if conflicts:
            with st.warning("Scheduling Conflict Detected!"):
                for time_str, tasks in conflicts.items():
                    task_list = ", ".join([f"'{task}'" for task in tasks])
                    st.write(f"**At {time_str}:** The following tasks are scheduled at the same time: {task_list}")
        
        plan = scheduler.generate_plan(available_time)

        if plan:
            st.success("Here is your generated pet care plan for the day!")
            st.markdown("### Today's Plan")
            total_duration = sum(task.duration_in_minutes for task in plan)
            
            schedule_data = []
            for task in plan:
                # Find which pet this task belongs to
                pet_owner = "Unknown"
                for pet in st.session_state.owner.pets:
                    if task in pet.tasks:
                        pet_owner = pet.name
                        break
                schedule_data.append({
                    "Pet": pet_owner,
                    "Task": task.name,
                    "Start Time": task.time,
                    "Duration": task.duration,
                    "Priority": task.priority,
                })
            
            st.table(schedule_data)
            st.write(f"**Total plan duration:** {total_duration} minutes.")

        else:
            st.warning(
                "No tasks could be scheduled. Either no tasks have been added, or there isn't enough time."
            )
    else:
        st.error("Please add at least one pet before generating a schedule.")
