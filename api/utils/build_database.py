from impacts_model.data_model import db, Model, Project, Resource, Task

projects = [
    {"id": 2, "name": "Real project", "base_model_id": 4},
]

models = [
    {"id": 4, "name": "Real project model 1", "project_id": 2, "root_task_id": 3},
]

tasks = [
    {"id": 0, "name": "Task 1", "task_type_id": 0, "model_id": 0},
    {"id": 1, "name": "Task 2", "parent_task_id": 0, "model_id": 0},
    {"id": 2, "name": "Task 3", "parent_task_id": 0, "model_id": 0},
    {"id": 3, "name": "Real project", "model_id": 4},
    {"id": 4, "name": "Build", "parent_task_id": 3, "model_id": 4},
    {"id": 5, "name": "Implementation", "parent_task_id": 4, "model_id": 4},
    {"id": 6, "name": "Development", "parent_task_id": 5, "model_id": 4},
    {"id": 7, "name": "Design", "parent_task_id": 5, "model_id": 4},
    {"id": 8, "name": "Specifications", "parent_task_id": 4, "model_id": 4},
    {"id": 9, "name": "Management", "parent_task_id": 4, "model_id": 4},
    {"id": 10, "name": "Run", "parent_task_id": 3, "model_id": 4},
    {"id": 11, "name": "Maintenance", "parent_task_id": 10, "model_id": 4},
    {"id": 12, "name": "Hosting", "parent_task_id": 10, "model_id": 4},
    {"id": 13, "name": "Compute", "parent_task_id": 11, "model_id": 4},
    {"id": 14, "name": "Storage", "parent_task_id": 11, "model_id": 4},
    {"id": 15, "name": "Network", "parent_task_id": 11, "model_id": 4},
    {"id": 16, "name": "Usage", "parent_task_id": 10, "model_id": 4},
]

"""
Real project
    Build
        Implementation
            Development
            Design
        Specifications
        Management
    Run
        Maintenance
        Hosting
        Usage
"""

resources = [
    {"id": 0, "name": "Resource 1", "task_id": 0, "type": "Compute", "value": 100},
    {"id": 1, "name": "Resource 2", "task_id": 1, "type": "People", "value": 100},
    {"id": 2, "name": "Resource 3", "task_id": 2, "type": "Storage", "value": 100},
    {
        "id": 3,
        "name": "Development man days",
        "task_id": 6,
        "type": "People",
        "value": 100,
    },
    {"id": 4, "name": "Design man days", "task_id": 7, "type": "People", "value": 100},
    {
        "id": 5,
        "name": "Specifications man days",
        "task_id": 8,
        "type": "People",
        "value": 100,
    },
    {
        "id": 6,
        "name": "Management man days",
        "task_id": 9,
        "type": "People",
        "value": 100,
    },
    {"id": 7, "name": "Servers amount", "task_id": 13, "type": "Compute", "value": 100},
    {
        "id": 8,
        "name": "Storage terabytes",
        "task_id": 11,
        "type": "Storage",
        "value": 100,
    },
    {
        "id": 9,
        "name": "Data transferred",
        "task_id": 15,
        "type": "Network",
        "value": 100,
    },
    {"id": 10, "name": "Users", "task_id": 16, "type": "UserDevice", "value": 100},
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
        p = Project(
            id=project.get("id"),
            name=project.get("name"),
            base_model_id=project.get("base_model_id"),
        )
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
