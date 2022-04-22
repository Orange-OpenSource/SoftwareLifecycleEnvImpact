import os

from config import db
from controller import Model, Project

PROJECT = [
    {"id": 0, "name": "Project 0"},
    {"id": 1, "name": "Project 1"},
]

MODEL = [
    {"id": 0, "name": "Model 0", "project_id": 0},
    {"id": 1, "name": "Model 1", "project_id": 0},
    {"id": 2, "name": "Model 2", "project_id": 1},
    {"id": 3, "name": "Model 3", "project_id": 1},
]

# Delete database file if it exists currently
if os.path.exists("../test.db"):
    os.remove("../test.db")

# Create the database
db.create_all()

# iterate over the PEOPLE structure and populate the database
for project in PROJECT:
    p = Project(id=project.get("id"), name=project.get("name"))
    db.session.add(p)

# iterate over the MODEL structure and populate the database
for model in MODEL:
    p = Model(id=model.get("id"), name=model.get("name"), project_id=model.get("project_id"))
    db.session.add(p)

db.session.commit()
