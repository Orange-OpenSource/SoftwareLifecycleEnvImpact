import os

from api.config import db
from api.model import Project

# Data to initialize database with
PROJECT = [
    {"id": 0, "name": "Project 0"},
    {"id": 1, "name": "Project 1"},
    {"id": 2, "name": "Project 2"},
    {"id": 3, "name": "Project 3"},
]

# Delete database file if it exists currently
if os.path.exists("test.db"):
    os.remove("test.db")

# Create the database
db.create_all()

# iterate over the PEOPLE structure and populate the database
for person in PROJECT:
    p = Project(id=person.get("id"), name=person.get("name"))
    db.session.add(p)

db.session.commit()
