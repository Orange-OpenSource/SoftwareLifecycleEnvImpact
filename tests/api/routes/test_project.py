import pytest
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy

from api.data_model import Project

projects_root = "/api/v1/projects"


@pytest.fixture(scope="function")
def project_fixture(db: SQLAlchemy):
    """Project task fixture"""
    project = Project(name="Test project")
    db.session.add(project)
    db.session.commit()
    return project


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

    # Test no task 404
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

    # Test that task is deleted
    response = client.get(projects_root + "/" + str(project_fixture.id))
    assert response.status_code == 404

    # Test no task 404
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
    # assert response.json["models"][0]["name"] == "Model 1" # TODO
    # assert response.json["models"][1]["name"] == "Model 2" # TODO
