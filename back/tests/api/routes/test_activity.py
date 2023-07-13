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


def test_get_one_activity(
    client: FlaskClient, db: SQLAlchemy, activity_fixture: Activity
) -> None:
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


def test_patch_activity(
    client: FlaskClient, db: SQLAlchemy, activity_fixture: Activity
) -> None:
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


def test_delete_activity(
    client: FlaskClient, db: SQLAlchemy, activity_fixture: Activity
) -> None:
    """
    Test response of DELETE /activities/<id>
    :param client: flask client fixture
    :param db: SQLAlchemy database fixture
    :param activity_fixture: Activity fixture
    """

    # Test to delete root activity
    model = Model.query.filter(
        Model.root_activity_id == activity_fixture.id
    ).one_or_none()
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
    response = client.get(
        activities_root_path + "/" + str(activity_fixture.id) + "/impacts"
    )
    assert response.status_code == 200
