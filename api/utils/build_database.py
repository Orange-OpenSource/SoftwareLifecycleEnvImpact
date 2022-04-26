import os

from config import db
from data_model import Model, Project, Task, TaskInput, TaskType

projects = [
    {"id": 0, "name": "Project 0"},
    {"id": 1, "name": "Project 1"},
]

models = [
    {"id": 0, "name": "Model 0", "project_id": 0},
    {"id": 1, "name": "Model 1", "project_id": 0},
    {"id": 2, "name": "Model 2", "project_id": 1},
    {"id": 3, "name": "Model 3", "project_id": 1},
]

tasks_types = [
    {"id": 0, "name": "Type 0"},
    {"id": 1, "name": "Type 1"},
    {"id": 2, "name": "Type 2"},
]

tasks = [
    {"id": 0, "name": "Task 1", "task_type_id": 0, "model_id": 0},
    {"id": 1, "name": "Task 2", "parent_task_id": 0, "task_type_id": 1, "model_id": 0},
    {"id": 2, "name": "Task 3", "parent_task_id": 0, "task_type_id": 2, "model_id": 0},
]

task_inputs = [
    {"id": 0, "name": "Input 1", "kind": "float", "value": "0.0", "task_id": 0},
    {"id": 1, "name": "Input 2", "kind": "string", "value": "string", "task_id": 1},
    {"id": 2, "name": "Input 3", "kind": "float", "value": "0.0", "task_id": 1},
    {"id": 3, "name": "Input 4", "kind": "string", "value": "string", "task_id": 2},
]


def reset_db() -> None:
    '''
    Reset the database with standard values
    :return: None
    '''
    # Delete database file if it exists currently
    if os.path.exists("database.db"):
        os.remove("database.db")

    # Create the database
    db.create_all()

    # Populate the database
    for project in projects:
        p = Project(id=project.get("id"), name=project.get("name"))
        db.session.add(p)

    for model in models:
        p = Model(
            id=model.get("id"), name=model.get("name"), project_id=model.get("project_id")
        )
        db.session.add(p)

    for task_type in tasks_types:
        t = TaskType(id=task_type.get("id"), name=task_type.get("name"))
        db.session.add(t)

    for task in tasks:
        t = Task(
            id=task.get("id"),
            name=task.get("name"),
            parent_task_id=task.get("parent_task_id"),
            task_type_id=task.get("task_type_id"),
            model_id=task.get("model_id"),
        )
        db.session.add(t)

    for task_input in task_inputs:
        t = TaskInput(
            id=task_input.get("id"),
            name=task_input.get("name"),
            kind=task_input.get("kind"),
            value=task_input.get("value"),
            task_id=task_input.get("task_id"),
        )
        db.session.add(t)

    db.session.commit()
