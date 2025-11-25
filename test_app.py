import os
import json
from app import app, TODO_FILE

def setup_function():
    """Delete todo.json before each test."""
    if os.path.exists(TODO_FILE):
        os.remove(TODO_FILE)


def test_home():
    client = app.test_client()
    res = client.get("/")
    assert res.status_code == 200
    assert res.json["message"] == "To-Do List API is running!"


def test_get_tasks_empty():
    client = app.test_client()
    res = client.get("/tasks")
    assert res.status_code == 200
    assert res.json["tasks"] == []


def test_add_task():
    client = app.test_client()
    res = client.post("/tasks", json={"task": "Buy milk"})
    assert res.status_code == 200
    assert res.json["message"] == "Task added"
    assert res.json["tasks"] == ["Buy milk"]


def test_delete_task():
    client = app.test_client()

    # Add item first
    client.post("/tasks", json={"task": "Task 1"})
    
    # Delete it
    res = client.delete("/tasks/0")
    assert res.status_code == 200
    assert res.json["message"] == "Task removed"
    assert res.json["removed"] == "Task 1"

    # Confirm list becomes empty
    res2 = client.get("/tasks")
    assert res2.json["tasks"] == []