from flask import Flask, render_template, request, redirect, url_for
import json
import os
import uuid
from datetime import datetime

app = Flask(__name__)

FILE_NAME = "tasks.json"


# -------- Load Tasks --------
def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as file:
        return json.load(file)


# -------- Save Tasks --------
def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)


# -------- Home --------
@app.route("/")
def home():
    return render_template("index.html")


# -------- Add Task --------
@app.route("/add", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        title = request.form["title"]
        priority = request.form["priority"]

        tasks = load_tasks()

        new_task = {
            "id": str(uuid.uuid4()),
            "title": title,
            "priority": priority,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        tasks.append(new_task)
        save_tasks(tasks)

        return redirect(url_for("view_tasks"))

    return render_template("add_task.html")


# -------- View Tasks --------
@app.route("/view")
def view_tasks():
    tasks = load_tasks()
    return render_template("view_tasks.html", tasks=tasks)


# -------- Complete Task --------
@app.route("/complete/<task_id>")
def complete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            break
    save_tasks(tasks)
    return redirect(url_for("view_tasks"))


# -------- Delete Task --------
@app.route("/delete/<task_id>")
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
    return redirect(url_for("view_tasks"))


# -------- Search --------
@app.route("/search", methods=["GET", "POST"])
def search_task():
    results = []
    if request.method == "POST":
        keyword = request.form["keyword"]
        tasks = load_tasks()
        results = [
            task for task in tasks
            if keyword.lower() in task["title"].lower()
        ]
    return render_template("search.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)
