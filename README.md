# Flask Task Manager

A small full-stack task manager built with **Flask**, **Bootstrap**, and **JSON** persistence.

Features:

- Add tasks with title and timestamp
- Mark tasks as **Done**
- Edit existing tasks
- Delete tasks with **confirmation modal**
- Task IDs are **renumbered** after deletion (1..N)
- Dark / Light mode toggle (saved in `localStorage`)
- Search bar to filter tasks by title
- Client-side pagination (5 tasks per page)
- Flash messages shown as **Bootstrap toasts**
- Deployable on PythonAnywhere or any WSGI host

---

## Tech Stack

- Python 3
- Flask
- Bootstrap 5
- Jinja2 templates
- JSON file (`tasks.json`) as a simple data store

---

## Project Structure

```text
flask-task-manager/
├─ app.py               # Flask app and routes
├─ task_logic.py        # Core task logic and JSON persistence
├─ requirements.txt     # Python dependencies
├─ README.md
├─ .gitignore
└─ templates/
   ├─ index.html        # Main task list page
   └─ edit.html         # Edit task page
