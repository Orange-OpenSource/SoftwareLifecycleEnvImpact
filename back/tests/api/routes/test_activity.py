from unittest import mock
from unittest.mock import MagicMock

import pytest
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy

from impacts_model.data_model import Model, Project, Activity, ActivitySchema

activities_root_path = "/api/v1/activities"


@pytest.fixture(scope="function")
def activity_fixture(db: SQLAlchemy) -> Activity:
    """Test activity fixture"""
    project = Project(name="Project test_activity")
    model = Model(name="Model test_activity")
    project.models = [model]
    activity = Activity(name="Test activity")
    model.root_activity = activity
    db.session.add_all([project, model, activity])
    db.session.commit()
    return activity


def test_activity_schema(activity_fixture: Activity):
    """Test that a ActivitySchema can dump and load correctly"""
    schema = ActivitySchema()

    dump = schema.dump(activity_fixture)
    load = schema.load(dump)
    dump = schema.dump(load)


def test_get_activities(client: FlaskClient, activity_fixture: Activity) -> None:
    """
    Test response of GET /activities
    :param client: flask client fixture
    :param activity_fixture: Activity fixture
    """
    all_activities = Activity.query.all()
    response = client.get(activities_root_path)
    assert response.status_code == 200
    assert len(response.json) == len(all_activities)


@mock.patch(
    "api.routes.activity.get_activity_template_by_id",
    MagicMock(return_value=MagicMock()),
)
def test_post_activity(client: FlaskClient, activity_fixture: Activity) -> None:
    """
    Test response of POST /activities
    :param client: flask client fixture
    :param activity_fixture: Activity fixture
    """
    response = client.post(
        activities_root_path,
        json={"name": "Activity test post", "parent_activity_id": activity_fixture.id},
    )

    assert response.status_code == 201
    assert response.json["name"] == "Activity test post"
    assert response.json["id"] is not None

    # Test 409 project exists already
    response = client.post(
        activities_root_path,
        json={
            "name": "Activity test post",
            "parent_activity_id": activity_fixture.id,
        },
    )
    assert response.status_code == 409

    # Test subactivities intserstion
    response = client.post(
        activities_root_path,
        json={
            "name": "Activity with subactivity",
            "parent_activity_id": activity_fixture.id,
        },
    )

    assert response.status_code == 201


def test_get_one_activity(client: FlaskClient, db: SQLAlchemy, activity_fixture: Activity) -> None:
    """
    Test response of GET /activities/<id>
    :param client: flask client fixture
    :param activity_fixture: Activity fixture
    """
    # Test with one activity
    response = client.get(activities_root_path + "/" + str(activity_fixture.id))
    assert response.status_code == 200
    assert response.json["id"] is activity_fixture.id
    assert response.json["name"] == activity_fixture.name

    # Test no activity 404
    db.session.delete(activity_fixture)
    db.session.commit()
    response = client.get(activities_root_path + "/" + str(activity_fixture.id))
    assert response.status_code == 404


def test_patch_activity(client: FlaskClient, db: SQLAlchemy, activity_fixture: Activity) -> None:
    """
    Test response of PATCH /activities/<id>
    :param client: flask client fixture
    :param db: SQLAlchemy database fixture
    :param activity_fixture: Activity fixture
    """

    response = client.patch(
        activities_root_path + "/" + str(activity_fixture.id),
        json=[{"op": "replace", "path": "/name", "value": "newer name"}],
    )
    assert response.status_code == 200
    assert response.json["name"] == "newer name"

    # Test wrong patch format
    response = client.patch(
        activities_root_path + "/" + str(activity_fixture.id),
        json=[{"op": "replace", "path": "/nameqqsd", "value": "newer name"}],
    )
    assert response.status_code == 403

    # Test no activity 404
    db.session.delete(activity_fixture)
    db.session.commit()
    response = client.patch(
        activities_root_path + "/" + str(activity_fixture.id),
        json=[{"op": "replace", "path": "/name", "value": "newer name"}],
    )
    assert response.status_code == 404


def test_delete_activity(client: FlaskClient, db: SQLAlchemy, activity_fixture: Activity) -> None:
    """
    Test response of DELETE /activities/<id>
    :param client: flask client fixture
    :param db: SQLAlchemy database fixture
    :param activity_fixture: Activity fixture
    """

    # Test to delete root activity
    model = Model.query.filter(Model.root_activity_id == activity_fixture.id).one_or_none()
    model.root_activity = activity_fixture
    response = client.delete(activities_root_path + "/" + str(activity_fixture.id))
    assert response.status_code == 403
    model.root_activity = None

    # Test nominal

    response = client.delete(activities_root_path + "/" + str(activity_fixture.id))
    assert response.status_code == 200

    # Test that activity is deleted
    response = client.get(activities_root_path + "/" + str(activity_fixture.id))
    assert response.status_code == 404

    # Test no activity 404
    response = client.delete(activities_root_path + "/" + str(activity_fixture.id))
    assert response.status_code == 404


def test_get_activity_impacts(
    client: FlaskClient, db: SQLAlchemy, activity_fixture: Activity
) -> None:
    """
    Test response of GET /activities/<id>/impacts
    :param client: flask client fixture
    :param db: SQLAlchemy database fixture
    :param activity_fixture: Activity fixture
    """
    response = client.get(activities_root_path + "/" + str(activity_fixture.id) + "/impacts")
    assert response.status_code == 200
