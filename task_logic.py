# task_logic.py

import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

# In-memory task storage
tasks = []


def load_tasks():
    """Load tasks from the JSON file into the global tasks list."""
    global tasks

    if not os.path.exists(TASKS_FILE):
        tasks = []
        return

    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            tasks = data
        else:
            print("Warning: tasks.json is not a valid list. Starting with empty task list.")
            tasks = []

    except json.JSONDecodeError:
        print("Warning: tasks.json is corrupted. Starting with empty task list.")
        tasks = []
    except OSError as e:
        print(f"Warning: could not read {TASKS_FILE}: {e}. Starting with empty task list.")
        tasks = []


def save_tasks():
    """Save the current tasks list to the JSON file."""
    try:
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2)
    except OSError as e:
        print(f"Error: could not save tasks to {TASKS_FILE}: {e}")


def get_new_task_id():
    """Return the next task ID as an integer."""
    if not tasks:
        return 1
    max_id = max(task["id"] for task in tasks)
    return max_id + 1


def get_all_tasks():
    """Return the list of all tasks."""
    return tasks


def find_task_by_id(task_id: int):
    """Return the task dictionary with the given ID, or None if not found."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def add_task(title: str):
    """Add a new task with the given title. Return the new task dict."""
    title = title.strip()
    if not title:
        raise ValueError("Title cannot be empty.")

    new_task = {
        "id": get_new_task_id(),
        "title": title,
        "done": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    tasks.append(new_task)
    save_tasks()
    return new_task


def mark_task_done(task_id: int) -> bool:
    """
    Mark the task with the given ID as done.
    Return True if updated, False if task not found or already done.
    """
    task = find_task_by_id(task_id)
    if task is None:
        return False
    if task["done"]:
        return False

    task["done"] = True
    save_tasks()
    return True


def delete_task(task_id: int) -> bool:
    """
    Delete the task with the given ID.
    Return True if deleted, False if task not found.
    """
    task = find_task_by_id(task_id)
    if task is None:
        return False

    tasks.remove(task)
    renumber_task_ids() 
    return True

def edit_task(task_id: int, new_title: str) -> bool:
    """
    Edit a task's title.
    Returns True if edited, False if task not found or title invalid.
    """
    new_title = new_title.strip()
    if not new_title:
        return False

    task = find_task_by_id(task_id)
    if task is None:
        return False

    task["title"] = new_title
    save_tasks()
    return True

def renumber_task_ids():
    """Reset task IDs to be 1..N in order."""
    for index, task in enumerate(tasks, start=1):
        task["id"] = index
    save_tasks()

