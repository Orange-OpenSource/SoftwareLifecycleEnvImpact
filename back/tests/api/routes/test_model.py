import pytest
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy

from impacts_model.data_model import Model, Project, Resource, Task

models_root = "/api/v1/models"

@pytest.fixture(scope="function")
def model_fixture(db: SQLAlchemy) -> Model:
    """Fixture Model object"""
    model = Model(name="Test Model")
    project = Project(name="Project test_model")
    project.models = [model]

    task = Task(name="Test task")

    resource = Resource(
        name="Resource 1 test task",
        type="TestResource",
        value=1,
    )
    task.resources = [resource]
    model.tasks = [task]
    model.root_task = task
    db.session.add_all([model, project, task, resource])
    db.session.commit()
    return model


def test_get_models(client: FlaskClient, model_fixture: Model) -> None:
    """
    Test response of GET /models
    :param client: flask client fixture
    :param model_fixture: Model fixture
    """
    all_models = Model.query.all()
    response = client.get(models_root)
    assert response.status_code == 200
    assert len(response.json) == len(all_models)


def test_post_model(client: FlaskClient, model_fixture: Model) -> None:
    """
    Test response of POST /models
    :param client: flask client fixture
    :param model_fixture: Model fixture
    """
    response = client.post(
        models_root, json={"name": "Model 1", "project_id": model_fixture.project_id}
    )
    assert response.status_code == 201
    assert response.json["name"] == "Model 1"
    assert response.json["id"] is not None

    # Test 409 project exists already
    response = client.post(
        models_root, json={"name": "Model 1", "project_id": model_fixture.project_id}
    )
    assert response.status_code == 409


def test_get_one_model(
    client: FlaskClient, db: SQLAlchemy, model_fixture: Model
) -> None:
    """
    Test response of GET /models/<id>
    :param client: flask client fixture
    :param db: SQLAlchemy database fixture
    :param model_fixture: Model fixture
    """
    response = client.get(models_root + "/" + str(model_fixture.id))
    assert response.status_code == 200
    assert response.json["id"] is model_fixture.id
    assert response.json["name"] == model_fixture.name

    # Test no task 404
    db.session.delete(model_fixture)
    db.session.commit()
    response = client.get(models_root + "/" + str(model_fixture.id))
    assert response.status_code == 404


def test_patch_model(client: FlaskClient, db: SQLAlchemy, model_fixture: Model) -> None:
    """
    Test response of PATCH /models/<id>
    :param client: flask client fixture
    :param db: SQLAlchemy database fixture
    :param model_fixture: Model fixture
    """

    response = client.patch(
        models_root + "/" + str(model_fixture.id),
        json=[{"op": "replace", "path": "/name", "value": "newer name"}],
    )
    assert response.status_code == 200
    assert response.json["name"] == "newer name"

    # Test wrong patch format
    response = client.patch(
        models_root + "/" + str(model_fixture.id),
        json=[{"op": "replace", "path": "/nameqqsd", "value": "newer name"}],
    )
    assert response.status_code == 403

    # Test no model 404
    db.session.delete(model_fixture)
    db.session.commit()
    response = client.patch(
        models_root + "/" + str(model_fixture.id),
        json=[{"op": "replace", "path": "/name", "value": "newer name"}],
    )
    assert response.status_code == 404


def test_delete_model(
    client: FlaskClient, db: SQLAlchemy, model_fixture: Model
) -> None:
    """
    Test response of DELETE /models/<id>
    :param client: flask client fixture
    :param db: SQLAlchemy database fixture
    :param model_fixture: Model fixture
    """
    # Test to delete root model
    project = Project.query.filter(Project.id == model_fixture.project_id).one_or_none()
    project.base_model = model_fixture
    db.session.commit()
    response = client.delete(models_root + "/" + str(model_fixture.id))
    assert response.status_code == 403
    project.base_model = None
    db.session.commit()

    # Test nominal
    response = client.delete(models_root + "/" + str(model_fixture.id))
    assert response.status_code == 200

    # Test that model is deleted
    response = client.get(models_root + "/" + str(model_fixture.id))
    assert response.status_code == 404

    # Test no model 404
    response = client.delete(models_root + "/" + str(model_fixture.id))
    assert response.status_code == 404


def test_get_model_tasks(client: FlaskClient, db: SQLAlchemy) -> None:
    """
    Test response of GET /models/<id>/tasks
    :param client: flask client fixture
    :param db: SQLAlchemy database fixture
    """
    task1 = Task(name="Task 1")
    task2 = Task(name="Task 2")
    model = Model(name="Model 1")
    project = Project(name="Project 1")
    project.models = [model]
    project.base_model_id = model.id
    model.tasks = [task1, task2]
    model.root_task = task1
    db.session.add_all([task1, task2, model, project])
    db.session.commit()

    response = client.get(models_root + "/" + str(model.id) + "/tasks")
    assert response.status_code == 200