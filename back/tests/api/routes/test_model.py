import pytest
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from unittest import mock
from unittest.mock import MagicMock
from impacts_model.data_model import Model, ModelSchema, Project, Resource, Task
from impacts_model.impact_sources import ImpactSource
from impacts_model.quantities.quantities import (
    KG_CO2E,
    DAY,
    SERVER,
)

models_root = "/api/v1/models"


@pytest.fixture(scope="function")
def model_fixture(db: SQLAlchemy) -> Model:
    """Fixture Model object"""
    model = Model(name="Test Model")
    project = Project(name="Project test_model")
    project.models = [model]

    task = Task(name="Test task")

    resource = Resource(
        impact_source_id="TestResource",
        input=1 * SERVER,
        duration=3 * DAY,
    )
    task.resources = [resource]
    model.root_task = task
    db.session.add_all([model, project, task, resource])
    db.session.commit()
    return model


@mock.patch(
    "impacts_model.data_model.impact_source_factory",
    MagicMock(
        return_value=ImpactSource(
            id="testid", name="test", unit=SERVER, climate_change=1776 * KG_CO2E
        ),
    ),
)
def test_model_schema(model_fixture: Model) -> None:
    """Test that a ModelSchema can dump and load correctly"""
    schema = ModelSchema()

    dump = schema.dump(model_fixture)
    load = schema.load(dump)
    dump = schema.dump(load)


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
    assert response.json["name"] == "Model 1"  # type: ignore
    assert response.json["id"] is not None  # type: ignore

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


@mock.patch(
    "impacts_model.data_model.impact_source_factory",
    MagicMock(
        return_value=ImpactSource(
            id="testid", name="test", unit=SERVER, climate_change=1776 * KG_CO2E
        ),
    ),
)
def test_get_model_impact(client: FlaskClient, model_fixture: Model) -> None:
    response = client.get(models_root + "/" + str(model_fixture.id) + "/impact")
    assert response.status_code == 200


@mock.patch(
    "impacts_model.data_model.impact_source_factory",
    MagicMock(
        return_value=ImpactSource(
            id="testid", name="test", unit=SERVER, climate_change=1776 * KG_CO2E
        ),
    ),
)
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

    # # Test model with same name already exist
    # response = client.patch(
    #     models_root + "/" + str(model_fixture.id),
    #     json=[{"op": "replace", "path": "/name", "value": "newer name"}],
    # )
    # assert response.status_code == 403 # TODO

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
    model.root_task = task1
    db.session.add_all([task1, task2, model, project])
    db.session.commit()

    response = client.get(models_root + "/" + str(model.id) + "/tasks")
    assert response.status_code == 200
