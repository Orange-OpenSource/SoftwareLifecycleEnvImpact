from typing import Any

import jsonpatch
from flask import abort, request

from api.routes.task import get_task
from impacts_model.data_model import ModelSchema, db, Project
from impacts_model.database import (
    retrieve_all_models_db,
    retrieve_model_db,
    retrieve_similar_model_db,
    insert_model_db,
)


def get_models() -> Any:
    """
    GET /models/
    :return: return all models in the. database
    """
    models = retrieve_all_models_db()

    model_schema = ModelSchema(many=True)
    return model_schema.dump(models)


def get_model(model_id: int) -> Any:
    """
    GET /models/<model_id>
    :param model_id: the id of the model to retrieve
    :return: Model it it exists with id, 404 else
    """
    model = retrieve_model_db(model_id)

    if model is not None:
        model_schema = ModelSchema()
        return model_schema.dump(model)
    else:
        return abort(
            404,
            "No model found for Id: {model_id}".format(model_id=model_id),
        )


def update_model(model_id: int) -> Any:
    """
    PATCH /models/<model_id>
    Update the model with the A JSONPatch as defined by RFC 6902 in the body
    :param model_id: the id of the model to update
    :return: The updated model if it exists with id, 403 if the JSONPatch format is incorrect, 404 else
    """
    model = retrieve_model_db(model_id)

    if model is not None:
        try:
            model_schema = ModelSchema()
            data = model_schema.dump(model)

            patch = jsonpatch.JsonPatch(request.json)
            data = patch.apply(data)
            model = model_schema.load(data)

            if (
                Project.query.filter(Project.id == model.project_id)
                .filter(model in Project.models)
                .one_or_none()
                is not None
            ):
                return abort(403, "A model with this name already exists")

            db.session.commit()

            return model_schema.dump(model)
        except jsonpatch.JsonPatchConflict:
            return abort(403, "Patch format is incorrect")

    else:
        return abort(
            404,
            "No model found for Id: {model_id}".format(model_id=model_id),
        )


def delete_model(model_id: int) -> Any:
    """
    DELETE /models/<model_id>
    :param model_id: the id of the model to delete
    :return: 200 if the model exists and is deleted, 404 else
    """
    model = retrieve_model_db(model_id)

    if model is not None:
        project = Project.query.filter(Project.id == model.project_id).one_or_none()
        if project.base_model_id == model.id:
            return abort(
                403,
                "Cannot delete model {model_id} as it is the base model of project {project}".format(
                    model_id=model.id, project=project.id
                ),
            )
        db.session.delete(model)
        db.session.commit()
        return 200
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
    model = retrieve_model_db(model_id)

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

    existing_model = retrieve_similar_model_db(name, project_id)

    if existing_model is None:
        schema = ModelSchema()
        new_model = insert_model_db(schema.load(model))
        data = schema.dump(new_model)

        return data, 201
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
    model = retrieve_model_db(model_id)

    if model is not None:
        model_copy = model.copy()
        model_copy = insert_model_db(model_copy)
        model_schema = ModelSchema()
        return model_schema.dump(model_copy)
    else:
        return abort(
            404,
            "No model found for Id: {model_id}".format(model_id=model_id),
        )
