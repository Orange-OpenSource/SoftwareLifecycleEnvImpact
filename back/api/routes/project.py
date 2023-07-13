# BSD-3-Clause License
#
# Copyright 2017 Orange
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from typing import Any
from copy import copy
import jsonpatch
from flask import abort, request

from impacts_model.data_model import (
    db,
    Model,
    ModelSchema,
    Project,
    ProjectSchema,
    Activity,
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
    project = db.session.query(Project).get_or_404(project_id)
    project_schema = ProjectSchema()
    return project_schema.dump(project)


def export_project(project_id: int) -> Any:
    project = db.session.query(Project).get_or_404(project_id)
    project_copy = copy(project)
    project_schema = ProjectSchema()
    return project_schema.dump(project_copy)


def update_project(project_id: int) -> Any:
    """
    PATCH /projects/<project_id>
    Update the project with the A JSONPatch as defined by RFC 6902 in the body
    :param project_id: the id of the project to update
    :return: The updated project if it exists with id, 403 if the JSONPatch format is incorrect, 404 else
    """
    project = db.session.query(Project).get_or_404(project_id)

    try:
        project_schema = ProjectSchema()
        data = project_schema.dump(project)

        patch = jsonpatch.JsonPatch(request.json)
        data = patch.apply(data)

        if Project.query.filter(Project.name == data["name"]).one_or_none() is not None:
            return abort(403, "A model with this name already exists")

        model = project_schema.load(data)
        db.session.commit()

        return project_schema.dump(model)
    except jsonpatch.JsonPatchConflict:
        return abort(403, "Patch format is incorrect")


def delete_project(project_id: int) -> Any:
    """
    DELETE /projects/<project_id>
    :param project_id: the id of the project to delete
    :return: 200 if the project exists and is deleted, 404 else
    """
    project = db.session.query(Project).get_or_404(project_id)

    db.session.delete(project)
    db.session.commit()
    return 200


def create_project(project: dict[str, Any]) -> Any:
    """
    POST /projects/

    :param project: project to create
    :return: the project inserted with its id
    """
    name = project.get("name")

    existing_project = Project.query.filter(Project.name == name).one_or_none()

    if existing_project is None:
        schema = ProjectSchema()
        new_project = schema.load(project)

        root_activity = Activity(
            name=name,
        )

        model = Model(
            name=name,
        )

        model.root_activity = root_activity
        new_project.models = [model]

        db.session.add_all([new_project, model, root_activity])

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
    project = db.session.query(Project).get_or_404(project_id)

    model_schema = ModelSchema(many=True)
    return model_schema.dump(project.models)
