import json
import os

DATA_FILE = "data.json"

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)
    print("Saved.")
def show_menu():
    print("\n" + "="*35)
    print("       TASK MANAGER")
    print("="*35)
    print("1. Add task")
    print("2. View tasks")
    print("3. Mark task done")
    print("4. Delete task")
    print("5. Exit")
    print("="*35)

def add_task(tasks):
    title = input("Task title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    deadline = input("Deadline (e.g. 2026-07-01): ").strip()
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "deadline": deadline,
        "done": False
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task '{title}' added.")


def handleViewTasks(tasks):
    for records in tasks:
        print("-"*35)
        print(f"ID: {records['id']}")
        print(f"Title: {records['title']}")
        print(f"Deadline: {records['deadline']}")
        print(f"Done: {records['done']}")

def handleTaskDone():
    tasks = load_tasks()
    handleViewTasks(tasks)
    selectedId= int(input("Choose Id: ").strip())
    print("Press 1 for Done")
    print("Press 2 for InProgress")
    updated=False
    selectedStatus= input("Status: ").strip()
    for record in tasks:
        if record.get('id') == selectedId:
            if selectedStatus== "1":
                status=True
                updated=True
            elif selectedStatus =="2":
                status=False
                updated=True
            else:
                status=record["done"]
                updated=False
            record['done'] = status
            print("-"*35)
            print(f"ID: {record['id']}")
            print(f"Title: {record['title']}")
            print(f"Deadline: {record['deadline']}")
            print(f"Done: {record['done']}")
            break
    if(updated):
        with open(DATA_FILE, "w") as file:
            # indent=4 makes the JSON file neat and easy to read
            json.dump(tasks, file, indent=4) 
        print("Changes saved to file successfully.")
    
# to delete a task from the file, we will use the pythonic way, of creating the file with excluding the data we want to delete.
def deleteTask():
    tasks = load_tasks()
    handleViewTasks(tasks)
    secretCode= int(input("For confirmation enter Secret Code: ").strip())
    if(secretCode==99):
        print("User Verified...")
        try:
            id_to_delete = int(input("Enter the ID of the task to delete: ").strip())
        except ValueError:
            print("Please enter a valid number.")
            id_to_delete = None

        if id_to_delete is not None:
    # Track the original number of tasks
            original_count = len(tasks)
    
    # 3. Filter out the task with the matching ID
    # This keeps every task EXCEPT the one with id_to_delete
            tasks = [record for record in tasks if record.get('id') != id_to_delete]
    
    # 4. Check if a task was actually removed
            if len(tasks) < original_count:
        # 5. Save the updated list back to the JSON file
                with open(DATA_FILE, "w") as file:
                    json.dump(tasks, file, indent=4)
                print(f"Task {id_to_delete} deleted and file updated successfully.")
            else:
                print(f"No task found with ID {id_to_delete}.")
    else:
        print("You cannot Oversmart Me!")


def main():
    tasks = load_tasks()

    while True:
        show_menu()
        choice = input("Choose (1-5): ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            tasks = load_tasks()
            print(f"Loaded {len(tasks)} tasks.")
            handleViewTasks(tasks)
        elif choice == "3":
            handleTaskDone()
        elif choice =="4":
            deleteTask()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Coming soon...")

if __name__ == "__main__":
    main()