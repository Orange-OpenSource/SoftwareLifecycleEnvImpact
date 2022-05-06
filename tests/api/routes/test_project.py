from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy

from api.data_model import Model, Project

projects_root = "/api/v1/projects"


def test_get_projects(client: FlaskClient, db: SQLAlchemy) -> None:
    """
    Test response of GET /projects
    :param client: flask client fixture
    :param db: SQLAlchemy database fixture
    """
    db.session.add(Project(name="Project 1"))
    db.session.add(Project(name="Project 2"))

    response = client.get(projects_root)
    assert response.status_code == 200
    assert response.json[0]["name"] == "Project 1"
    assert response.json[1]["name"] == "Project 2"
    assert len(response.json) == 2

    assert response.json[0]["id"] is not None
    assert response.json[0]["created_at"] is not None
    assert (
        response.json[0]["updated_at"] is None
    )  # TODO maybe these three should go elsewhere ?


def test_post_projects(client: FlaskClient, db: SQLAlchemy) -> None:
    """
    Test response of POST /projects
    :param client: flask client fixture
    :param db: SQLAlchemy database fixture
    """
    response = client.post(projects_root, json={"name": "Project 1"})
    assert response.status_code == 201
    assert response.json["name"] == "Project 1"
    assert response.json["id"] is not None

    # Test 409 project exists already
    response = client.post(projects_root, json={"name": "Project 1"})
    assert response.status_code == 409


def test_get_one_project(client: FlaskClient, db: SQLAlchemy) -> None:
    """
    Test response of GET /project/<id>
    :param client: flask client fixture
    :param db: SQLAlchemy database fixture
    """
    # Test no project 404
    response = client.get(projects_root + "/" + str(0))
    assert response.status_code == 404

    # Test with one project
    project = Project(name="Project 1")
    db.session.add(project)
    db.session.commit()
    response = client.get(projects_root + "/" + str(project.id))
    assert response.status_code == 200
    assert response.json["id"] is project.id
    assert response.json["name"] == "Project 1"


def test_patch_project(client: FlaskClient, db: SQLAlchemy) -> None:
    """
    Test response of PATCH /project/<id>
    :param client: flask client fixture
    :param db: SQLAlchemy database fixture
    """
    # Test no project 404
    response = client.patch(
        projects_root + "/" + str(0),
        json=[{"op": "replace", "path": "/name", "value": "newer name"}],
    )
    assert response.status_code == 404

    # Test on real project
    project = Project(name="Project 1")
    db.session.add(project)
    db.session.commit()
    response = client.patch(
        projects_root + "/" + str(project.id),
        json=[{"op": "replace", "path": "/name", "value": "newer name"}],
    )
    assert response.status_code == 200
    assert response.json["name"] == "newer name"

    # Test wrong patch format
    response = client.patch(
        projects_root + "/" + str(project.id),
        json=[{"op": "replace", "path": "/nameqqsd", "value": "newer name"}],
    )
    assert response.status_code == 403


def test_delete_project(client: FlaskClient, db: SQLAlchemy) -> None:
    # Test no project 404
    response = client.delete(projects_root + "/" + str(0))
    assert response.status_code == 404

    # Test with one project
    project = Project(name="Project 1")
    db.session.add(project)
    db.session.commit()
    response = client.delete(projects_root + "/" + str(project.id))
    assert response.status_code == 200

    # Test that project is deleted
    response = client.get(projects_root)
    assert len(response.json) == 0


def test_get_project_models(client: FlaskClient, db: SQLAlchemy) -> None:
    """
    Test response of GET /project/<id>/models
    :param client: flask client fixture
    :param db: SQLAlchemy database fixture
    """
    model1 = Model(name="Model 1")
    model2 = Model(name="Model 2")
    project = Project(name="Project 1")
    project.models = [model1, model2]
    db.session.add_all([model1, model2, project])
    db.session.commit()

    response = client.get(projects_root + "/" + str(project.id))
    assert response.status_code == 200
    assert response.json["models"][0]["name"] == "Model 1"
    assert response.json["models"][1]["name"] == "Model 2"
