from os.path import isfile, join
from impacts_model.data_model import db, ProjectSchema
import json
from os import listdir


def reset_db() -> None:
    """
    Reset the database with standard values
    :return: None
    """
    db.reflect()
    db.drop_all()

    # Create the database
    db.create_all()

    path = "examples"
    # Fill with sampled projects
    try:
        for file in [f for f in listdir(path) if isfile(join(path, f))]:
            f = open(path + "/" + file, "r")
            data = json.load(f)
            schema = ProjectSchema()
            new_project = schema.load(data)
            db.session.add(new_project)
    except:
        print("An error occurred while reading files")
        print(listdir("."))

    # Commit to db
    db.session.commit()
