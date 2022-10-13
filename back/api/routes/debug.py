from impacts_model.data_model import db, Model, Project, Resource, Task, ProjectSchema
import json

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


def reset_db() -> None:
    """
    Reset the database with standard values
    :return: None
    """
    db.reflect()
    db.drop_all()

    # Create the database
    db.create_all()

    f = open("api/mockdata/data.json", "r")
    data = json.load(f)
    schema = ProjectSchema()
    new_project = schema.load(data)

    db.session.add(new_project)
    db.session.commit()
