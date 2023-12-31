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

import pytest
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy

from impacts_model.data_model import Project, ProjectSchema

projects_root = "/api/v1/projects"


@pytest.fixture(scope="function")
def project_fixture(db: SQLAlchemy):
    """Project fixture"""
    project = Project(name="Test project")
    db.session.add(project)
    db.session.commit()
    return project


def test_project_schema(project_fixture: Project):
    """Test that a ProjectSchema can dump and load correctly"""
    schema = ProjectSchema()

    dump = schema.dump(project_fixture)
    load = schema.load(dump)
    dump = schema.dump(load)


def test_get_projects(client: FlaskClient, project_fixture: Project) -> None:
    """
    Test response of GET /projects
    :param client: flask client fixture
    :param project_fixture: Project fixture
    """

    projects = Project.query.all()
    response = client.get(projects_root)
    assert response.status_code == 200
    assert len(response.json) == len(projects)


def test_post_projects(client: FlaskClient, project_fixture: Project) -> None:
    """
    Test response of POST /projects
    :param client: flask client fixture
    :param project_fixture: Project fixture
    """
    response = client.post(projects_root, json={"name": "Project test post"})
    assert response.status_code == 201
    assert response.json["name"] == "Project test post"
    assert response.json["id"] is not None

    # Test 409 project exists already
    response = client.post(projects_root, json={"name": "Project test post"})
    assert response.status_code == 409


def test_get_one_project(
    client: FlaskClient, db: SQLAlchemy, project_fixture: Project
) -> None:
    """
    Test response of GET /project/<id>
    :param client: flask client fixture
    :param db: SQLAlchemy database fixture
    :param project_fixture: Project fixture
    """

    response = client.get(projects_root + "/" + str(project_fixture.id))
    assert response.status_code == 200
    assert response.json["id"] is project_fixture.id
    assert response.json["name"] == project_fixture.name

    # Test no project 404
    db.session.delete(project_fixture)
    db.session.commit()
    response = client.get(projects_root + "/" + str(project_fixture.id))
    assert response.status_code == 404


def test_patch_project(
    client: FlaskClient, db: SQLAlchemy, project_fixture: Project
) -> None:
    """
    Test response of PATCH /project/<id>
    :param client: flask client fixture
    :param db: SQLAlchemy database fixture
    :param project_fixture: Project fixture
    """

    response = client.patch(
        projects_root + "/" + str(project_fixture.id),
        json=[{"op": "replace", "path": "/name", "value": "newer name"}],
    )
    assert response.status_code == 200
    assert response.json["name"] == "newer name"

    # Test wrong patch format
    response = client.patch(
        projects_root + "/" + str(project_fixture.id),
        json=[{"op": "replace", "path": "/nameqqsd", "value": "newer name"}],
    )
    assert response.status_code == 403

    # Test 404
    db.session.delete(project_fixture)
    db.session.commit()
    response = client.patch(
        projects_root + "/" + str(project_fixture.id),
        json=[{"op": "replace", "path": "/name", "value": "newer name"}],
    )
    assert response.status_code == 404


def test_delete_project(
    client: FlaskClient, db: SQLAlchemy, project_fixture: Project
) -> None:
    """
    Test response of DELETE /projects/<id>
    :param client: flask client fixture
    :param db: SQLAlchemy database fixture
    :param project_fixture: Project fixture
    """
    response = client.delete(projects_root + "/" + str(project_fixture.id))
    assert response.status_code == 200

    # Test that project is deleted
    response = client.get(projects_root + "/" + str(project_fixture.id))
    assert response.status_code == 404

    # Test no project 404
    response = client.delete(projects_root + "/" + str(project_fixture.id))
    assert response.status_code == 404


def test_get_project_models(
    client: FlaskClient, db: SQLAlchemy, project_fixture: Project
) -> None:
    """
    Test response of GET /project/<id>/models
    :param client: flask client fixture
    :param db: SQLAlchemy database fixture
    """
    response = client.get(projects_root + "/" + str(project_fixture.id) + "/models")
    assert response.status_code == 200
