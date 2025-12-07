Good. Let’s turn this into a clean, ready-to-push GitHub repo.

Below is a complete project structure with **all files** and a **README**.
You can literally copy this into a folder, run it, then `git init` and push.

---

## 1. Repository structure

```text
flask-task-manager/
├─ app.py
├─ task_logic.py
├─ requirements.txt
├─ README.md
├─ .gitignore
└─ templates/
   ├─ index.html
   └─ edit.html
```

Create a folder (e.g. `flask-task-manager`) and put these files in it.

---

## 2. `.gitignore`

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd

# Environments
.env
.venv
venv/
ENV/
env/

# IDE/editor
.vscode/
.idea/
*.swp

# Local data
tasks.json
```

---

## 3. `requirements.txt`

```text
Flask==3.0.3
```

(If version mismatch later, just run `pip install Flask` and regenerate requirements if needed.)

---

## 4. `task_logic.py`

```python
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
    if task is None or task["done"]:
        return False

    task["done"] = True
    save_tasks()
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


def delete_task(task_id: int) -> bool:
    """
    Delete the task with the given ID.
    Return True if deleted, False if task not found.
    After deletion, renumber IDs to be continuous from 1..N.
    """
    task = find_task_by_id(task_id)
    if task is None:
        return False

    tasks.remove(task)
    renumber_task_ids()
    return True
```

---

## 5. `app.py`

```python
from flask import Flask, render_template, request, redirect, url_for, flash
from task_logic import (
    load_tasks,
    get_all_tasks,
    add_task,
    mark_task_done,
    delete_task,
    edit_task,
)

app = Flask(__name__)

# CHANGE THIS in a real deployment
app.secret_key = "CHANGE_THIS_TO_A_RANDOM_SECRET_KEY"

# Load existing tasks on startup
load_tasks()


@app.route("/")
def home():
    tasks = get_all_tasks()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def route_add_task():
    title = request.form.get("title", "")
    try:
        add_task(title)
        flash("Task added successfully.", "success")
    except ValueError:
        flash("Title cannot be empty.", "danger")
    return redirect(url_for("home"))


@app.route("/done/<int:task_id>")
def route_mark_done(task_id):
    if mark_task_done(task_id):
        flash(f"Task {task_id} marked as done.", "success")
    else:
        flash(f"Task {task_id} not found or already done.", "warning")
    return redirect(url_for("home"))


@app.route("/delete/<int:task_id>")
def route_delete_task(task_id):
    if delete_task(task_id):
        flash(f"Task {task_id} deleted and IDs renumbered.", "success")
    else:
        flash(f"Task {task_id} not found.", "warning")
    return redirect(url_for("home"))


@app.route("/edit/<int:task_id>")
def route_edit_task(task_id):
    tasks = get_all_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return "Task not found", 404
    return render_template("edit.html", task=task)


@app.route("/update/<int:task_id>", methods=["POST"])
def route_update_task(task_id):
    new_title = request.form.get("title", "")
    if edit_task(task_id, new_title):
        flash(f"Task {task_id} updated.", "success")
        return redirect(url_for("home"))
    else:
        flash("Invalid title or task not found.", "danger")
        return redirect(url_for("route_edit_task", task_id=task_id))


if __name__ == "__main__":
    app.run(debug=True)
```

---

## 6. `templates/index.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Task Manager</title>

    <!-- Bootstrap CSS -->
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
      rel="stylesheet"
    >

    <style>
        body.dark-mode {
            background-color: #121212;
            color: #f8f9fa;
        }

        body.dark-mode .card {
            background-color: #1e1e1e;
            color: #f8f9fa;
            border-color: #333;
        }

        body.dark-mode .table {
            color: #f8f9fa;
        }

        body.dark-mode .table thead {
            background-color: #343a40;
            color: #f8f9fa;
        }

        body.dark-mode .form-control {
            background-color: #2b2b2b;
            color: #f8f9fa;
            border-color: #444;
        }

        body.dark-mode .form-control::placeholder {
            color: #aaaaaa;
        }

        body.dark-mode .btn-outline-secondary {
            color: #f8f9fa;
            border-color: #777;
        }

        body.dark-mode .btn-outline-secondary:hover {
            background-color: #444;
        }

        body.dark-mode .btn-outline-danger {
            color: #ff6b6b;
            border-color: #ff6b6b;
        }

        body.dark-mode .btn-outline-danger:hover {
            background-color: #ff6b6b;
            color: #121212;
        }

        body.dark-mode .btn-outline-success {
            color: #66d9a3;
            border-color: #66d9a3;
        }

        body.dark-mode .btn-outline-success:hover {
            background-color: #66d9a3;
            color: #121212;
        }

        body.dark-mode .table-striped > tbody > tr:nth-of-type(odd) > * {
            --bs-table-accent-bg: #1a1a1a;
            color: #f8f9fa;
        }

        body.dark-mode .table-striped > tbody > tr:nth-of-type(even) > * {
            --bs-table-accent-bg: #181818;
            color: #f8f9fa;
        }
    </style>
</head>

<body class="bg-light">

<div class="container mt-4">

    <!-- Header / Toolbar -->
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="mb-0">Task Manager</h1>
        <div class="d-flex gap-2">
            <input type="text" id="searchInput" class="form-control form-control-sm" placeholder="Search tasks...">
            <button id="themeToggle" class="btn btn-sm btn-outline-secondary">Dark mode</button>
        </div>
    </div>

    <!-- Add Task Form -->
    <div class="card shadow-sm mb-4">
        <div class="card-body">
            <form action="/add" method="POST" class="row g-3">
                <div class="col-md-10">
                    <input type="text" name="title" class="form-control" placeholder="Enter new task..." required>
                </div>
                <div class="col-md-2 d-grid">
                    <button class="btn btn-primary">Add Task</button>
                </div>
            </form>
        </div>
    </div>

    <!-- Tasks Table -->
    <div class="card shadow-sm">
        <div class="card-body">
            <table class="table table-striped align-middle" id="tasksTable">
                <thead class="table-dark">
                    <tr>
                        <th>ID</th>
                        <th>Title</th>
                        <th>Status</th>
                        <th>Created At</th>
                        <th style="width: 220px;">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for task in tasks %}
                    <tr>
                        <td class="task-id">{{ task.id }}</td>
                        <td class="task-title">{{ task.title }}</td>
                        <td>
                            {% if task.done %}
                                <span class="badge bg-success">Done</span>
                            {% else %}
                                <span class="badge bg-warning text-dark">Pending</span>
                            {% endif %}
                        </td>
                        <td>{{ task.created_at }}</td>
                        <td>
                            <div class="btn-group btn-group-sm" role="group">
                                <a href="/edit/{{ task.id }}" class="btn btn-outline-secondary">Edit</a>

                                {% if not task.done %}
                                <a href="/done/{{ task.id }}" class="btn btn-outline-success">Done</a>
                                {% endif %}

                                <!-- Delete via modal -->
                                <a href="#" class="btn btn-outline-danger btn-delete"
                                   data-task-id="{{ task.id }}"
                                   data-task-title="{{ task.title }}">
                                    Delete
                                </a>
                            </div>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>

            <!-- Pagination -->
            <nav>
                <ul class="pagination justify-content-center mt-3" id="pagination"></ul>
            </nav>
            <small class="text-muted">Note: Pagination is disabled while searching.</small>
        </div>
    </div>
</div>

<!-- Toast container (bottom-right) -->
<div class="position-fixed bottom-0 end-0 p-3" style="z-index: 1055">
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        {% for category, message in messages %}
        <div class="toast align-items-center text-bg-{{ 'success' if category=='success' else ('danger' if category=='danger' else 'secondary') }} border-0 mb-2"
             role="alert" aria-live="assertive" aria-atomic="true" data-bs-delay="3000">
          <div class="d-flex">
            <div class="toast-body">
              {{ message }}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"
                    aria-label="Close"></button>
          </div>
        </div>
        {% endfor %}
      {% endif %}
    {% endwith %}
</div>

<!-- Delete confirmation modal -->
<div class="modal fade" id="deleteModal" tabindex="-1" aria-labelledby="deleteModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="deleteModalLabel">Delete Task</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        Are you sure you want to delete this task?
        <br>
        <strong id="deleteTaskTitle"></strong>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
        <a href="#" class="btn btn-danger" id="confirmDeleteBtn">Delete</a>
      </div>
    </div>
  </div>
</div>

<!-- Bootstrap JS -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>

<script>
    // ----- Dark mode toggle -----
    const body = document.body;
    const themeToggleBtn = document.getElementById('themeToggle');

    function applyTheme(theme) {
        if (theme === 'dark') {
            body.classList.add('dark-mode');
            themeToggleBtn.textContent = 'Light mode';
        } else {
            body.classList.remove('dark-mode');
            themeToggleBtn.textContent = 'Dark mode';
        }
    }

    const savedTheme = localStorage.getItem('theme') || 'light';
    applyTheme(savedTheme);

    themeToggleBtn.addEventListener('click', function () {
        const newTheme = body.classList.contains('dark-mode') ? 'light' : 'dark';
        localStorage.setItem('theme', newTheme);
        applyTheme(newTheme);
    });

    // ----- Bootstrap toasts (for flash messages) -----
    const toastElList = [].slice.call(document.querySelectorAll('.toast'));
    toastElList.forEach(function (toastEl) {
        const toast = new bootstrap.Toast(toastEl);
        toast.show();
    });

    // ----- Delete modal -----
    const deleteButtons = document.querySelectorAll('.btn-delete');
    const deleteModalEl = document.getElementById('deleteModal');
    const deleteTaskTitleEl = document.getElementById('deleteTaskTitle');
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');

    deleteButtons.forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const taskId = this.dataset.taskId;
            const taskTitle = this.dataset.taskTitle;

            deleteTaskTitleEl.textContent = taskTitle;
            confirmDeleteBtn.href = '/delete/' + taskId;

            const modal = new bootstrap.Modal(deleteModalEl);
            modal.show();
        });
    });

    // ----- Search filter + Pagination -----
    const searchInput = document.getElementById('searchInput');
    const tableBody = document.querySelector('#tasksTable tbody');
    let allRows = Array.from(tableBody.querySelectorAll('tr'));

    const rowsPerPage = 5;
    let currentPage = 1;

    const paginationEl = document.getElementById('pagination');

    function renderPagination(totalPages) {
        paginationEl.innerHTML = '';

        if (totalPages <= 1) {
            return;
        }

        for (let i = 1; i <= totalPages; i++) {
            const li = document.createElement('li');
            li.className = 'page-item' + (i === currentPage ? ' active' : '');
            const a = document.createElement('a');
            a.className = 'page-link';
            a.href = '#';
            a.textContent = i;
            a.addEventListener('click', function (e) {
                e.preventDefault();
                currentPage = i;
                renderTablePage();
            });
            li.appendChild(a);
            paginationEl.appendChild(li);
        }
    }

    function renderTablePage() {
        const visibleRows = allRows.filter(row => row.style.display !== 'none'); // rows not filtered by search

        const totalPages = Math.ceil(visibleRows.length / rowsPerPage) || 1;
        if (currentPage > totalPages) currentPage = totalPages;

        visibleRows.forEach(row => row.style.display = 'none');

        const start = (currentPage - 1) * rowsPerPage;
        const end = start + rowsPerPage;

        visibleRows.slice(start, end).forEach(row => {
            row.style.display = '';
        });

        renderPagination(totalPages);
    }

    // Initial pagination render
    renderTablePage();

    // Search filter
    searchInput.addEventListener('input', function () {
        const filter = this.value.toLowerCase();

        allRows.forEach(row => {
            const titleCell = row.querySelector('.task-title');
            const titleText = titleCell ? titleCell.textContent.toLowerCase() : '';
            if (titleText.includes(filter)) {
                row.style.display = '';   // visible
            } else {
                row.style.display = 'none'; // hidden
            }
        });

        if (filter.trim() !== '') {
            paginationEl.innerHTML = '';
        } else {
            allRows.forEach(row => row.style.display = '');
            currentPage = 1;
            renderTablePage();
        }
    });
</script>

</body>
</html>
```

---

## 7. `templates/edit.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Edit Task</title>

    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
      rel="stylesheet"
    >
</head>

<body class="bg-light">

<div class="container mt-5" style="max-width: 500px;">

    <div class="card shadow-sm">
        <div class="card-header bg-dark text-white">
            Edit Task #{{ task.id }}
        </div>

        <div class="card-body">
            <form action="/update/{{ task.id }}" method="POST">
                <div class="mb-3">
                    <label class="form-label">New Title</label>
                    <input type="text" name="title" class="form-control" value="{{ task.title }}" required>
                </div>

                <button class="btn btn-primary w-100">Save Changes</button>
            </form>

            <a href="/" class="btn btn-outline-secondary w-100 mt-3">Back to Tasks</a>
        </div>
    </div>

</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>

</body>
</html>
```

---

## 8. `README.md`

````markdown
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
````

---

## Getting Started (Local)

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/flask-task-manager.git
cd flask-task-manager
```

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python app.py
```

Open your browser at:

```text
http://127.0.0.1:5000
```

---

## Data Storage

Tasks are stored in a local JSON file:

```text
tasks.json
```

This file is automatically created on first write.
It is **ignored by Git** via `.gitignore` so your local tasks do not get committed.

---

## Deploying (Example: PythonAnywhere)

1. Create a PythonAnywhere account.
2. Upload this project folder to `/home/<your-username>/flask-task-manager/`.
3. Create a virtualenv and install `Flask`.
4. Configure the WSGI file to:

```python
import sys
import os

project_home = '/home/<your-username>/flask-task-manager'
if project_home not in sys.path:
    sys.path.append(project_home)

from app import app as application
```

5. Reload your web app from the PythonAnywhere **Web** tab.

---

## Possible Improvements

* Switch from JSON to SQLite or PostgreSQL
* Add user accounts and authentication
* Expose REST API endpoints (`/api/tasks`)
* Add React/Vue frontend consuming the API
* Better error handling and input validation

---

## License

MIT License.

````

---

## 9. Push to GitHub

From inside `flask-task-manager`:

```bash
git init
git add .
git commit -m "Initial commit - Flask Task Manager"
git branch -M main
git remote add origin https://github.com/kaungsithu19/flask-task-manager.git
git push -u origin main
````
