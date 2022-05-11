from api.data_model import db, Model, Project, Resource, Task

projects = [
    {"id": 0, "name": "Project 0"},
    {"id": 1, "name": "Project 1"},
]

models = [
    {"id": 0, "name": "Model 0", "project_id": 0, "root_task_id": 0},
    {"id": 1, "name": "Model 1", "project_id": 0, "root_task_id": 0},
    {"id": 2, "name": "Model 2", "project_id": 1, "root_task_id": 0},
    {"id": 3, "name": "Model 3", "project_id": 1, "root_task_id": 0},
]


tasks = [
    {"id": 0, "name": "Task 1", "task_type_id": 0, "model_id": 0},
    {"id": 1, "name": "Task 2", "parent_task_id": 0, "model_id": 0},
    {"id": 2, "name": "Task 3", "parent_task_id": 0, "model_id": 0},
]

resources = [
    {"id": 0, "name": "Resource 1", "task_id": 0, "type": "Compute", "value": 100},
    {"id": 1, "name": "Resource 2", "task_id": 1, "type": "People", "value": 100},
    {"id": 2, "name": "Resource 3", "task_id": 2, "type": "Storage", "value": 100},
]

def reset_db() -> None:
    """
    Reset the database with standard values
    :return: None
    """
    db.reflect()
    db.drop_all()

    # Create the database
    db.create_all()

    # Populate the database
    for resource in resources:
        r = Resource(
            id=resource.get("id"),
            name=resource.get("name"),
            task_id=resource.get("task_id"),
            type=resource.get("type"),
            value=resource.get("value"),
        )
        db.session.add(r)

    for project in projects:
        p = Project(id=project.get("id"), name=project.get("name"))
        db.session.add(p)

    for model in models:
        p = Model(
            id=model.get("id"),
            name=model.get("name"),
            project_id=model.get("project_id"),
            root_task_id=model.get("root_task_id"),
        )
        db.session.add(p)

    for task in tasks:
        t = Task(
            id=task.get("id"),
            name=task.get("name"),
            parent_task_id=task.get("parent_task_id"),
            model_id=task.get("model_id"),
        )
        db.session.add(t)

    db.session.commit()
