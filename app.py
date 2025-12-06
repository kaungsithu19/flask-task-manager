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
app.secret_key = "CHANGE_THIS_TO_SOMETHING_RANDOM"  # required for flash messages

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
        flash(f"Task {task_id} deleted.", "success")
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
