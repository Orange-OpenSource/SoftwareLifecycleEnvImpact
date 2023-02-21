from os.path import isfile, join
from impacts_model.data_model import db, ProjectSchema
import json
from os import listdir

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

    # Fill with sampled projects
    path = "examples"
    for file in [f for f in listdir(path) if isfile(join(path, f))]:
        f = open(path + "/" + file, "r")
        data = json.load(f)
        schema = ProjectSchema()
        new_project = schema.load(data)
        db.session.add(new_project)

    # Commit to db
    db.session.commit()
