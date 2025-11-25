
from flask import Flask, jsonify, request
import os
import json

app = Flask(__name__)

TODO_FILE = "todo.json"


def load_items():
    """Load tasks from JSON file."""
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, "r") as f:
        return json.load(f)


def save_items(items):
    """Save tasks to JSON file."""
    with open(TODO_FILE, "w") as f:
        json.dump(items, f, indent=4)


@app.get("/")
def home():
    return jsonify({"message": "To-Do List API is running!"})


@app.get("/tasks")
def get_tasks():
    """Return the full to-do list."""
    items = load_items()
    return jsonify({"tasks": items})


@app.post("/tasks")
def add_task():
    """Add a new task."""
    data = request.get_json()
    task = data.get("task")

    if not task:
        return jsonify({"error": "Task content required"}), 400

    items = load_items()
    items.append(task)
    save_items(items)

    return jsonify({"message": "Task added", "tasks": items})


@app.delete("/tasks/<int:index>")
def delete_task(index):
    """Delete task by index."""
    items = load_items()

    if 0 <= index < len(items):
        removed = items.pop(index)
        save_items(items)
        return jsonify({"message": "Task removed", "removed": removed})
    else:
        return jsonify({"error": "Invalid task index"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
