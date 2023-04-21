import datetime
import json
from flask import Flask, render_template, request, jsonify
import os

template_dir = os.path.abspath("templates")
static_dir = os.path.abspath("static")
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)


tasks = []
task_id = 0


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_tasks")
def get_tasks():
    return jsonify(tasks)


@app.route("/add_task", methods=["POST"])
def add_task():
    global task_id
    task = request.form["task"]
    priority = request.form["priority"]
    due_date = request.form["due_date"]
    due_time = request.form["due_time"]

    task_data = {"id": task_id, "task": task, "priority": priority,
                 "due_date": due_date, "due_time": due_time}
    tasks.append(task_data)
    task_id += 1

    return jsonify(task_data)

@app.route("/clear_tasks", methods=["POST"])
def clear_tasks():
    global tasks, task_id
    tasks.clear()
    task_id = 0
    return "All tasks cleared", 200

if __name__ == "__main__":
    app.run(debug=True)
