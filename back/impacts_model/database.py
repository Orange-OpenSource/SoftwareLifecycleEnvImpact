from impacts_model.data_model import db, Model, Task
from typing import List


def retrieve_all_models_db() -> List[Model]:
    return Model.query.all()


def retrieve_model_db(model_id: int) -> Model:
    return Model.query.filter(Model.id == model_id).one_or_none()


def retrieve_similar_model_db(model_name: str, project_id: int) -> Model:
    return (
        Model.query.filter(Model.name == model_name)
        .filter(Model.project_id == project_id)
        .one_or_none()
    )


def insert_model_db(model: Model) -> Model:
    if model.root_task == None:
        # Create a model only with a name imply to create the associate root_task
        root_task = Task(
            name=model.name,
        )
        model.root_task = root_task

    db.session.add(model)
    db.session.commit()
    return model

# TODO  all database functions should be there ?