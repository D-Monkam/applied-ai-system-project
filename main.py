from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date

def main():
    """
    A script to demonstrate the core functionality of the PawPal system.
    """
    today = date.today()

    # 1. Create an Owner
    owner = Owner(name="Alex")

    # 2. Create two Pets
    pet1 = Pet(name="Buddy", breed="Golden Retriever", age=5)
    pet2 = Pet(name="Lucy", breed="Siamese Cat", age=3)

    # 3. Add tasks to the pets, with start times to test conflict warning
    # Tasks for Buddy
    task1 = Task(name="Morning Walk", duration="00:30", time="08:00", priority=5, frequency='daily', due_date=today)
    task2 = Task(name="Evening Feed", duration="00:15", time="18:00", priority=4, frequency='daily', due_date=today)
    task3 = Task(name="Play fetch", duration="00:20", time="16:00", priority=3, frequency='daily', due_date=today)
    
    pet1.add_task(task1)
    pet1.add_task(task2)
    pet1.add_task(task3)

    # Tasks for Lucy - create a conflict at 08:00
    task4 = Task(name="Administer Medication", duration="00:05", time="08:00", priority=5, frequency='daily', due_date=today)
    task5 = Task(name="Grooming", duration="00:25", time="19:00", priority=2, frequency='daily', due_date=today)
    task6 = Task(name="Clean litter box", duration="00:10", time="12:00", priority=4, frequency='daily', due_date=today)
    task9 = Task(name="Check water bowl", duration="00:02", time="12:00", priority=3, frequency='daily', due_date=today) # Another conflict

    pet2.add_task(task4)
    pet2.add_task(task5)
    pet2.add_task(task6)
    pet2.add_task(task9)

    # 4. Add pets to the owner
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    # 5. Create a Scheduler and generate a plan
    scheduler = Scheduler(owner)
    available_time = 120  # Owner has 2 hours available today
    todays_plan = scheduler.generate_plan(available_time)

    # 6. Print the schedule to the terminal
    print("--- Today's Schedule ---")
    if not todays_plan:
        print("No tasks scheduled for today.")
    else:
        total_time = 0
        for task in todays_plan:
            print(f"- {task.name} ({task.time}) - Priority: {task.priority}")
            total_time += task.duration_in_minutes
        print("------------------------")
        print(f"Total estimated time: {total_time} minutes")

    # 7. Demonstrate sorting and filtering
    print("\n--- Sorting and Filtering ---")
    
    # Add tasks out of order
    task7 = Task(name="Brush teeth", duration="00:05", time="20:00", priority=1, frequency='daily', due_date=today)
    task8 = Task(name="Midday nap", duration="01:00", time="13:00", priority=1, frequency='daily', due_date=today)
    pet1.add_task(task8)
    pet2.add_task(task7)

    print("\nAll tasks for Buddy, sorted by start time:")
    sorted_buddy_tasks = scheduler.sort_by_start_time()
    for task in sorted_buddy_tasks:
        if task in pet1.tasks:
            print(f"- {task.name} (Starts: {task.time}, Duration: {task.duration})")

    print("\nAll incomplete tasks:")
    incomplete_tasks = scheduler.filter_tasks(status='incomplete')
    for task in incomplete_tasks:
        # Find which pet this task belongs to
        pet_owner = "Unknown"
        for pet in owner.pets:
            if task in pet.tasks:
                pet_owner = pet.name
                break
        print(f"- {task.name} (Pet: {pet_owner})")
    
    # Mark a task as complete to test filtering
    scheduler.complete_task(task1)
    print("\nAll completed tasks:")
    completed_tasks = scheduler.filter_tasks(status='completed')
    for task in completed_tasks:
        pet_owner = "Unknown"
        for pet in owner.pets:
            if task in pet.tasks:
                pet_owner = pet.name
                break
        print(f"- {task.name} (Pet: {pet_owner})")

    print("\n--- Recurring Task Demo ---")
    print(f"\nTotal tasks for Buddy before completing a daily task: {len([t for t in owner.pets if t.name == 'Buddy'][0].tasks)}")
    # Complete a daily task for Buddy
    scheduler.complete_task(task2)
    print(f"Completed '{task2.name}'.")
    print(f"Total tasks for Buddy after completing a daily task: {len([t for t in owner.pets if t.name == 'Buddy'][0].tasks)}")

    print("\nBuddy's tasks now include a new occurrence:")
    buddys_tasks = scheduler.filter_tasks(pet_name="Buddy")
    for task in buddys_tasks:
        status = "Completed" if task.is_completed else "Incomplete"
        print(f"- {task.name} (Due: {task.due_date}) - Status: {status}")

if __name__ == "__main__":
    main()
