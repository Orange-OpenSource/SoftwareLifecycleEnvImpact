from typing import Any

import jsonpatch
from flask import abort, request

from api.routes.task import get_task
from impacts_model.data_model import db, Model, ModelSchema, Project, Task
from impacts_model.impacts import EnvironmentalImpactTreeSchema


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


def update_model(model_id: int) -> Any:
    """
    PATCH /models/<model_id>
    Update the model with the A JSONPatch as defined by RFC 6902 in the body
    :param model_id: the id of the model to update
    :return: The updated model if it exists with id, 403 if the JSONPatch format is incorrect, 404 else
    """
    model = Model.query.filter(Model.id == model_id).one_or_none()

    if model is not None:
        try:
            model_schema = ModelSchema()
            data = model_schema.dump(model)

            patch = jsonpatch.JsonPatch(request.json)
            data = patch.apply(data)

            model = model_schema.load(data)
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
    model = Model.query.filter(Model.id == model_id).one_or_none()

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
    model = Model.query.filter(Model.id == model_id).one_or_none()

    if model is not None:
        return get_task(model.root_task_id)
    else:
        return abort(
            404,
            "No model found for Id: {model_id}".format(model_id=model_id),
        )


def get_impacts(model_id: int) -> Any:
    """
    GET /models/{model_id}/impact
    :param model_id: id of the model to get the impact
    :return: All impact_sources computed for a model
    """
    model = Model.query.filter(Model.id == model_id).one_or_none()

    if model is not None:
        impact_tree = get_task_environmental_impact_tree(model.root_task)
        schema = EnvironmentalImpactTreeSchema()
        return schema.dump(impact_tree)
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
