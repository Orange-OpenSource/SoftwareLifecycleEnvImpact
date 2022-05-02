from typing import Any

import jsonpatch
from flask import abort, request

from api.data_model import db, Model, ModelSchema, Task
from api.routes.task import get_task


def get_models() -> Any:
    """
    GET /models/
    :return: return all models in the database
    """
    models = Model.query.all()

    model_schema = ModelSchema(many=True)
    return model_schema.dump(models)


def get_model(model_id: int) -> Any:
    """
    GET /models/<model_id>
    :param model_id: the id of the model to retrieve
    :return: Model it it exists with id, 404 else
    """
    model = Model.query.filter(Model.id == model_id).one_or_none()

    if model is not None:
        model_schema = ModelSchema()
        return model_schema.dump(model)
    else:
        return abort(
            404,
            "No model found for Id: {model_id}".format(model_id=model_id),
        )


def update_model(model_id: int):
    model = Model.query.filter(Model.id == model_id).one_or_none()

    if model is not None:
        model_schema = ModelSchema()

        patch = jsonpatch.JsonPatch(request.json)
        data = model_schema.dump(model)
        data = patch.apply(data)

        model = model_schema.load(data)
        db.session.commit()

        return model_schema.dump(model)
    else:
        return abort(
            404,
            "No model found for Id: {model_id}".format(model_id=model_id),
        )


def get_tasks(model_id: int) -> Any:
    """
    GET /models/{model_id}/tasks
    :param model_id: id of the model to get the tasks
    :return: a list of tasks corresponding to a model id
    """
    model = Model.query.filter(Model.id == model_id).one_or_none()

    if model is not None:
        return get_task(model.root_task_id)
    else:
        return abort(
            404,
            "No model found for Id: {model_id}".format(model_id=model_id),
        )


def create_model(model: dict[str, Any]) -> Any:
    """
    POST /models/
    :param model: model to create
    :return: inserted model populated with its id
    """
    name = model.get("name")
    project_id = model.get("project_id")

    existing_model = (
        Model.query.filter(Model.name == name)
            .filter(Model.project_id == project_id)
            .one_or_none()
    )

    if existing_model is None:
        root_task = Task(
            name=name,
            task_type_id=0,  # Root task type, # TODO replace by new api architecture
        )
        schema = ModelSchema()
        new_model = schema.load(model)
        new_model.root_task = root_task
        new_model.tasks = [root_task]

        db.session.add(new_model)
        db.session.commit()

        data = schema.dump(new_model)

        return data, 201
    else:
        return abort(
            409,
            "Model {name} exists already".format(name=name),
        )
