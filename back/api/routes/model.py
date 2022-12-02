from typing import Any
from copy import copy

import jsonpatch
from flask import abort, request

from impacts_model.impacts import TaskImpact, TaskImpactSchema
from api.routes.task import get_task
from impacts_model.data_model import Model, ModelSchema, db, Project, Task, TaskSchema
from impacts_model.database import (
    insert_model_db,
)


def get_models() -> Any:
    """
    GET /models/
    :return: return all models in the. database
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
    model = db.session.query(Model).get_or_404(model_id)
    model_schema = ModelSchema()
    return model_schema.dump(model)


def get_model_impact(model_id: int) -> Any:
    """
    GET /models/<model_id>/impact
    :param model_id: the id of the model to retrieve the impact from
    :return: The impact it model exists with id, 404 else
    """
    model = db.session.query(Model).get_or_404(model_id)

    task_impact = TaskImpact(
        model.root_task.id,
        model.root_task.get_environmental_impact(),
        model.root_task.get_subtasks_impact(),
        model.root_task.get_impact_by_resource_type(),
    )
    schema = TaskImpactSchema()
    return schema.dump(task_impact)


def update_model(model_id: int) -> Any:
    """
    PATCH /models/<model_id>
    Update the model with the A JSONPatch as defined by RFC 6902 in the body
    :param model_id: the id of the model to update
    :return: The updated model if it exists with id, 403 if the JSONPatch format is incorrect, 404 else
    """
    model = db.session.query(Model).get_or_404(model_id)

    try:
        model_schema = ModelSchema()
        data = model_schema.dump(model)

        patch = jsonpatch.JsonPatch(request.json)
        data = patch.apply(data)

        if (
            Project.query.filter(Project.id == model.project_id)
            .filter(model.name == data["name"])
            .one_or_none()
            is not None
        ):
            return abort(403, "A model with this name already exists")

        model = model_schema.load(data)
        db.session.commit()

        return model_schema.dump(model)
    except jsonpatch.JsonPatchConflict:
        return abort(403, "Patch format is incorrect")


def delete_model(model_id: int) -> Any:
    """
    DELETE /models/<model_id>
    :param model_id: the id of the model to delete
    :return: 200 if the model exists and is deleted, 404 else
    """
    model = db.session.query(Model).get_or_404(model_id)
    db.session.delete(model)
    db.session.commit()
    return 200


def get_tasks(model_id: int) -> Any:
    """
    GET /models/{model_id}/tasks
    :param model_id: id of the model to get the tasks
    :return: a list of tasks corresponding to a model id
    """
    model = db.session.query(Model).get_or_404(model_id)
    return get_task(model.root_task_id)


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
        schema = ModelSchema()
        model_loaded = schema.load(model)

        if model_loaded.root_task == None:
            # Create a model only with a name imply to create the associate root_task
            root_task = Task(
                name=model_loaded.name,
            )
            model_loaded.root_task = root_task

        db.session.add(model_loaded)
        db.session.commit()

        return schema.dump(model_loaded), 201
    else:
        return abort(
            409,
            "Model {name} exists already".format(name=name),
        )


def duplicate_model(model_id: int) -> Any:
    """
    POST /models/<model_id>/copy
    :param model_id: the id of the model to copy
    :return: Model it it exists with id, 404 else
    """
    model = db.session.query(Model).get_or_404(model_id)

    model_copy = copy(model)
    model_copy.project_id = model.project_id
    model_copy = insert_model_db(model_copy)
    model_schema = ModelSchema()
    return model_schema.dump(model_copy)
