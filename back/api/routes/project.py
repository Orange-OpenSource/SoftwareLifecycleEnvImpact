from typing import Any

import jsonpatch
from flask import abort, request

from impacts_model.data_model import (
    db,
    Model,
    ModelSchema,
    Project,
    ProjectSchema,
    Task,
)


def get_projects() -> Any:
    """
    GET /projects/
    :return: all Project in the database
    """
    # Create the list from data
    projects = Project.query.all()

    # Serialize
    project_schema = ProjectSchema(many=True)
    return project_schema.dump(projects)


def get_project(project_id: int) -> Any:
    """
    GET /project/<project_id>
    :param project_id: id of the project to get
    :return: Project if it exists with id, 404 else
    """
    project = Project.query.filter(Project.id == project_id).one_or_none()

    if project is not None:
        project_schema = ProjectSchema()
        return project_schema.dump(project)
    else:
        return abort(
            404,
            "No project found for Id: {project_id}".format(project_id=project_id),
        )


def export_project(project_id: int) -> Any:
    project = Project.query.filter(Project.id == project_id).one_or_none()
    project_copy = project.copy()
    if project is not None:
        project_schema = ProjectSchema()
        return project_schema.dump(project_copy)
    else:
        return abort(
            404,
            "No project found for Id: {project_id}".format(project_id=project_id),
        )


def update_project(project_id: int) -> Any:
    """
    PATCH /projects/<project_id>
    Update the project with the A JSONPatch as defined by RFC 6902 in the body
    :param project_id: the id of the project to update
    :return: The updated project if it exists with id, 403 if the JSONPatch format is incorrect, 404 else
    """
    project = Project.query.filter(Project.id == project_id).one_or_none()

    if project is not None:
        try:
            project_schema = ProjectSchema()
            data = project_schema.dump(project)

            patch = jsonpatch.JsonPatch(request.json)
            data = patch.apply(data)

            model = project_schema.load(data)
            db.session.commit()

            return project_schema.dump(model)
        except jsonpatch.JsonPatchConflict:
            return abort(403, "Patch format is incorrect")
    else:
        return abort(
            404,
            "No project found for Id: {project_id}".format(project_id=project_id),
        )


def delete_project(project_id: int) -> Any:
    """
    DELETE /projects/<project_id>
    :param project_id: the id of the project to delete
    :return: 200 if the project exists and is deleted, 404 else
    """
    project = Project.query.filter(Project.id == project_id).one_or_none()

    if project is not None:
        db.session.delete(project)
        db.session.commit()
        return 200
    else:
        return abort(
            404,
            "No project found for Id: {project_id}".format(project_id=project_id),
        )


def create_project(project: dict[str, Any]) -> Any:
    """
    POST /projects/

    :param project: project to merge_aggregated_impact
    :return: the project inserted with its id
    """
    name = project.get("name")

    existing_project = Project.query.filter(Project.name == name).one_or_none()

    if existing_project is None:
        schema = ProjectSchema()
        new_project = schema.load(project)

        root_task = Task(
            name=name,
        )

        model = Model(
            name=name,
        )

        model.root_task = root_task
        model.tasks = [root_task]
        new_project.base_model = model
        new_project.models = [model]

        db.session.add_all([new_project, model, root_task])

        db.session.commit()

        data = schema.dump(new_project)

        return data, 201
    else:
        return abort(
            409,
            "Project {name} exists already".format(name=name),
        )


def import_project(project: dict[str, Any]) -> Any:
    """
    POST /projects/import

    :param project: project to import
    :return: the project inserted with its id
    """
    name = project.get("name")

    existing_project = Project.query.filter(Project.name == name).one_or_none()

    if existing_project is None:
        schema = ProjectSchema()
        new_project = schema.load(project)

        db.session.add(new_project)
        db.session.commit()
        data = schema.dump(new_project)
        return data, 201
    else:
        return abort(
            409,
            "Project {name} exists already".format(name=name),
        )


def get_models(project_id: int) -> Any:
    """
    /projects/{project_id}/models
    :param project_id: id of the project to get the models
    :return: All the models for the project id
    """
    project = Project.query.filter(Project.id == project_id).one_or_none()

    if project is not None:
        model_schema = ModelSchema(many=True)
        return model_schema.dump(project.models)
    else:
        return abort(
            404,
            "No project found for Id: {project_id}".format(project_id=project_id),
        )
