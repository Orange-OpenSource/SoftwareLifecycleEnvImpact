import pytest
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from unittest import mock
from unittest.mock import MagicMock
from impacts_model.impact_sources import ImpactSource
from impacts_model.data_model import Resource, ResourceSchema
from impacts_model.data_model import Model, Project, Resource, Task
from impacts_model.quantities.quantities import (
    KG_CO2E,
    SERVER,
    DAY,
)

resources_root = "/api/v1/resources"


@pytest.fixture(scope="function")
def resource_fixture(db: SQLAlchemy):
    """Resource fixture"""
    project = Project(name="Project test_resource")
    model = Model(name="Model test_resource")
    project.models = [model]
    task = Task(name="test_resource task")

    resource = Resource(
        impact_source_id="testid",
        input=1 * SERVER,
        duration=1 * DAY,
    )
    task.resources = [resource]
    model.root_task = task
    db.session.add_all([project, model, task, resource])
    db.session.commit()
    return resource


@mock.patch(
    "impacts_model.data_model.impact_source_factory",
    MagicMock(
        return_value=ImpactSource(
            id="testid", name="test", unit=SERVER, climate_change=1776 * KG_CO2E
        ),
    ),
)
def test_resource_schema(resource_fixture: Resource) -> None:
    """Test that the resource schema     can be dumped and loaded"""
    schema = ResourceSchema()
    dump = schema.dump(resource_fixture)
    loaded = schema.load(dump)


def test_get_resources(client: FlaskClient, resource_fixture: Resource) -> None:
    """
    Test response of GET /resources
    :param client: flask client fixture
    :param resource_fixture: Resource fixture
    """

    resources = Resource.query.all()
    response = client.get(resources_root)
    assert response.status_code == 200
    assert len(response.json) == len(resources)


@mock.patch(
    "impacts_model.data_model.impact_source_factory",
    MagicMock(
        return_value=ImpactSource(
            id="testid", name="test", unit=SERVER, climate_change=1776 * KG_CO2E
        ),
    ),
)
def test_post_resources(
    client: FlaskClient, resource_fixture: Resource, db: SQLAlchemy
) -> None:
    """
    Test response of POST /resources
    :param client: flask client fixture
    :param resource_fixture: Resource fixture
    """
    response = client.post(
        resources_root,
        json={
            "task_id": resource_fixture.task_id,
            "impact_source_id": resource_fixture.impact_source_id,
            "input": {"value": 3, "unit": "server"},
        },
    )
    assert response.status_code == 201
    assert response.json["impact_source_id"] == resource_fixture.impact_source_id
    assert response.json["id"] is not None

    # Test 409 task does not  exists
    Task.query.filter_by(id=resource_fixture.task_id).delete()
    db.session.commit()
    response = client.post(
        resources_root,
        json={
            "task_id": resource_fixture.task_id,
            "impact_source_id": resource_fixture.impact_source_id,
        },
    )
    assert response.status_code == 409


def test_get_one_resource(
    client: FlaskClient, db: SQLAlchemy, resource_fixture: Resource
) -> None:
    """
    Test response of GET /resources/<id>
    :param client: flask client fixture
    :param db: SQLAlchemy database fixture
    :param resource_fixture: Resource fixture
    """

    response = client.get(resources_root + "/" + str(resource_fixture.id))
    assert response.status_code == 200
    assert response.json["id"] is resource_fixture.id
    assert response.json["impact_source_id"] == resource_fixture.impact_source_id

    # Test no reesource 404
    db.session.delete(resource_fixture)
    db.session.commit()
    response = client.get(resources_root + "/" + str(resource_fixture.id))
    assert response.status_code == 404


@mock.patch(
    "impacts_model.data_model.impact_source_factory",
    MagicMock(
        return_value=ImpactSource(
            id="testid", name="test", unit=SERVER, climate_change=2332 * KG_CO2E
        )
    ),
)
def test_patch_resource(
    client: FlaskClient, db: SQLAlchemy, resource_fixture: Resource
) -> None:
    """
    Test response of PATCH /resources/<id>
    :param client: flask client fixture
    :param db: SQLAlchemy database fixture
    :param resource_fixture: Resource fixture
    """

    # TODO update quantity in resource
    pass
    # response = client.patch(
    #     resources_root + "/" + str(resource_fixture.id),
    #     json=[{"op": "replace", "path": "/name", "value": "newer name"}],
    # )
    # assert response.status_code == 200
    # assert response.json["input"] == 2 * SERVER

    # Test wrong patch format
    response = client.patch(
        resources_root + "/" + str(resource_fixture.id),
        json=[{"op": "replace", "path": "/nameqqsd", "value": "newer name"}],
    )
    assert response.status_code == 403

    # Test no task 404
    db.session.delete(resource_fixture)
    db.session.commit()
    response = client.patch(
        resources_root + "/" + str(resource_fixture.id),
        json=[{"op": "replace", "path": "/name", "value": "newer name"}],
    )
    assert response.status_code == 404


def test_delete_resource(
    client: FlaskClient, db: SQLAlchemy, resource_fixture: Resource
) -> None:
    """
    Test response of DELETE /resources/<id>
    :param client: flask client fixture
    :param db: SQLAlchemy database fixture
    :param resource_fixture: Resource fixture
    """
    response = client.delete(resources_root + "/" + str(resource_fixture.id))
    assert response.status_code == 200

    # Test that task is deleted
    response = client.get(resources_root + "/" + str(resource_fixture.id))
    assert response.status_code == 404

    # Test no task 404
    response = client.delete(resources_root + "/" + str(resource_fixture.id))
    assert response.status_code == 404
