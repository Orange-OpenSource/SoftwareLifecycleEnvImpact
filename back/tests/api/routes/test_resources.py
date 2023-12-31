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

from marshmallow import ValidationError
import pytest
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from unittest import mock
from unittest.mock import MagicMock
from impacts_model.impact_sources import ImpactSource, ImpactSourceError
from impacts_model.data_model import QuantitySchema, Resource, ResourceSchema
from impacts_model.data_model import Model, Project, Resource, Activity
from impacts_model.impacts import ImpactCategory, ImpactValue
from impacts_model.quantities.quantities import (
    KG_CO2E,
    MINUTE,
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
    activity = Activity(name="test_resource activity")

    resource = Resource(
        name="testResource",
        impact_source_id="testid",
        amount=1 * SERVER,
    )
    activity.resources = [resource]
    model.root_activity = activity
    db.session.add_all([project, model, activity, resource])
    db.session.commit()
    return resource


def test_quantity_schema():
    """Test that the quantity schema can be dumped and loaded"""
    schema = QuantitySchema()
    dump = schema.dump("3 server")
    load = schema.load(dump)
    dump = schema.dump(load)


@mock.patch(
    "impacts_model.data_model.impact_source_factory",
    MagicMock(
        return_value=ImpactSource(
            id="testid",
            name="test",
            unit=SERVER,
            environmental_impact={
                ImpactCategory.CLIMATE_CHANGE: ImpactValue(use=1776 * KG_CO2E)
            },
        ),
    ),
)
def test_resource_schema(resource_fixture: Resource) -> None:
    """Test that the resource schema can be dumped and loaded"""
    schema = ResourceSchema()

    dump = schema.dump(resource_fixture)
    load = schema.load(dump)
    dump = schema.dump(load)


@mock.patch(
    "impacts_model.data_model.impact_source_factory",
    MagicMock(
        return_value=ImpactSource(
            id="testid",
            name="test",
            unit=SERVER,
            environmental_impact={
                ImpactCategory.CLIMATE_CHANGE: ImpactValue(use=1776 * KG_CO2E)
            },
        ),
    ),
)
def test_resource_schema_validation_no_time_impactsource() -> None:
    """
    Test marshamllow validation when not time in ImpactSource unit for:
        Frequency AND period OR none of them
    """
    schema = ResourceSchema()

    # Wrong amount unit should raise error
    with pytest.raises(ValidationError):
        dump = schema.dump(
            Resource(
                impact_source_id="testid",
                amount=1 * SERVER * DAY,
            )
        )
        schema.load(dump)

    # Only frequency should raise error
    with pytest.raises(ValidationError):
        dump = schema.dump(
            Resource(impact_source_id="testid", amount=1 * SERVER, frequency=1 * DAY)
        )
        schema.load(dump)

    # Only period should raise error
    with pytest.raises(ValidationError):
        dump = schema.dump(
            Resource(impact_source_id="testid", amount=1 * SERVER, period=1 * DAY)
        )
        schema.load(dump)


@mock.patch(
    "impacts_model.data_model.impact_source_factory",
    MagicMock(
        return_value=ImpactSource(
            id="testid",
            name="test",
            unit=SERVER * DAY,
            environmental_impact={
                ImpactCategory.CLIMATE_CHANGE: ImpactValue(use=1776 * KG_CO2E)
            },
        ),
    ),
)
def test_resource_schema_validation_time_impactsource() -> None:
    """
    Test marshamllow validation when time in ImpactSource unit for:
        - Period is mandatory
        - Frequency and duration, or none of them
        -
    """
    schema = ResourceSchema()

    # Wrong amount unit should raise error
    with pytest.raises(ValidationError):
        dump = schema.dump(
            Resource(
                impact_source_id="testid",
                amount=1 * SERVER * DAY,
            )
        )
        schema.load(dump)

    # No period should raise error
    with pytest.raises(ValidationError):
        dump = schema.dump(Resource(impact_source_id="testid", amount=1 * SERVER))
        schema.load(dump)

    # No frequency when duration should raise error
    with pytest.raises(ValidationError):
        dump = schema.dump(
            Resource(impact_source_id="testid", amount=1 * SERVER, duration=1 * MINUTE)
        )
        schema.load(dump)

    # No duration when frequency should raise error
    with pytest.raises(ValidationError):
        dump = schema.dump(
            Resource(impact_source_id="testid", amount=1 * SERVER, frequency=1 * MINUTE)
        )
        schema.load(dump)


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
            id="testid",
            name="test",
            unit=SERVER,
            environmental_impact={
                ImpactCategory.CLIMATE_CHANGE: ImpactValue(use=1776 * KG_CO2E)
            },
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
            "name": "testName",
            "activity_id": resource_fixture.activity_id,
            "impact_source_id": resource_fixture.impact_source_id,
            "amount": {"value": 3, "unit": "server"},
        },
    )
    assert response.status_code == 201
    assert response.json["impact_source_id"] == resource_fixture.impact_source_id
    assert response.json["id"] is not None

    # Test 409 activity does not  exists
    Activity.query.filter_by(id=resource_fixture.activity_id).delete()
    db.session.commit()
    response = client.post(
        resources_root,
        json={
            "name": "testName",
            "activity_id": resource_fixture.activity_id,
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
            id="testid",
            name="test",
            unit=SERVER,
            environmental_impact={
                ImpactCategory.CLIMATE_CHANGE: ImpactValue(use=2332 * KG_CO2E)
            },
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
    # Change id
    response = client.patch(
        resources_root + "/" + str(resource_fixture.id),
        json=[{"op": "replace", "path": "/impact_source_id", "value": "server"}],
    )
    assert response.status_code == 200
    assert response.json["impact_source_id"] == "server"

    # Patch a quantity
    response = client.patch(
        resources_root + "/" + str(resource_fixture.id),
        json=[
            {
                "op": "replace",
                "path": "/amount",
                "value": {"value": 8, "unit": "server"},
            },
        ],
    )
    assert response.status_code == 200
    assert response.json["amount"] == {"value": 8, "unit": "server"}

    # Test wrong patch format
    response = client.patch(
        resources_root + "/" + str(resource_fixture.id),
        json=[{"op": "replace", "path": "/nameqqsd", "value": "newer name"}],
    )
    assert response.status_code == 403

    # Test no activity 404
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

    # Test that activity is deleted
    response = client.get(resources_root + "/" + str(resource_fixture.id))
    assert response.status_code == 404

    # Test no activity 404
    response = client.delete(resources_root + "/" + str(resource_fixture.id))
    assert response.status_code == 404
