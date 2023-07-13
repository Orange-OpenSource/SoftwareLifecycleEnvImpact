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

from copy import copy
from unittest import mock
from unittest.mock import MagicMock

import pytest
from flask_sqlalchemy import SQLAlchemy
from pint import Quantity

from impacts_model.data_model import Model, Project, Resource, Activity
from impacts_model.impact_sources import ImpactSource
from impacts_model.impacts import EnvironmentalImpact, ImpactCategory, ImpactValue
from impacts_model.quantities.quantities import (
    CUBIC_METER,
    DISEASE_INCIDENCE,
    KG_BQ_U235E,
    KG_CO2E,
    KG_SBE,
    MOL_HPOS,
    KG_MIPS,
    DAY,
    SERVER,
    HOUR,
    MONTH,
    YEAR,
)

############
# Resource #
############


@pytest.fixture(scope="function")
def resource_fixture(db: SQLAlchemy) -> Resource:
    """Resource fixture object"""
    project = Project(name="Project test_resources")
    model = Model(name="Model test_resourcess")
    project.models = [model]
    project.base_model = model
    activity = Activity(name="Test_resources activity")

    resource = Resource(
        name="testResource",
        impact_source_id="testid",
        amount=2312 * SERVER,
    )

    activity.resources = [resource]
    model.root_activity = activity
    db.session.add_all([project, model, activity, resource])
    db.session.commit()
    return resource


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
def test_resource_impact_source(resource_fixture: Resource):
    """Tests for resource impact_source hybrid property"""
    assert isinstance(resource_fixture.impact_source, ImpactSource)


def test_resource_amount(resource_fixture: Resource):
    """Tests for resource amount hybrid property"""

    assert resource_fixture.amount is None or isinstance(
        resource_fixture.amount, Quantity
    )

    # Test setter and getter
    resource_fixture.amount = 3 * SERVER
    assert resource_fixture.amount == 3 * SERVER

    # Test that an exception is raised in setting a wrong value
    with pytest.raises(TypeError):
        resource_fixture.amount = "oui"


def test_resource_duration(resource_fixture: Resource):
    """Tests for resource duration hybrid property"""

    assert resource_fixture.duration is None or isinstance(
        resource_fixture.duration, Quantity
    )

    # Test setter and getter
    resource_fixture.duration = 3 * YEAR
    assert resource_fixture.duration == 3 * YEAR

    # Test that an exception is raised in setting a wrong value
    with pytest.raises(TypeError):
        resource_fixture.duration = "oui"


def test_resource_frequency(resource_fixture: Resource):
    """Tests for resource frequency hybrid property"""

    assert resource_fixture.frequency is None or isinstance(
        resource_fixture.frequency, Quantity
    )

    # Test setter and getter
    resource_fixture.frequency = 3 * YEAR
    assert resource_fixture.frequency == 3 * YEAR

    # Test that an exception is raised in setting a wrong value
    with pytest.raises(TypeError):
        resource_fixture.frequency = "oui"


def test_resource_peiord(resource_fixture: Resource):
    """Tests for resource period hybrid property"""

    assert resource_fixture.period is None or isinstance(
        resource_fixture.period, Quantity
    )

    # Test setter and getter
    resource_fixture.period = 3 * YEAR
    assert resource_fixture.period == 3 * YEAR

    # Test that an exception is raised in setting a wrong value
    with pytest.raises(TypeError):
        resource_fixture.period = "oui"


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
def test_resource_value(resource_fixture: Resource):
    """Test computation of function value()"""
    assert isinstance(resource_fixture.value(), Quantity)

    # Test with only amount ( 3 servers)
    resource_fixture.amount = 3 * SERVER
    assert resource_fixture.value() == 3 * SERVER

    # Test with period (3 servers during one month)
    resource_fixture.period = 1 * MONTH
    assert resource_fixture.value() == (3 * SERVER) * (1 * MONTH)

    # Test with period and frequency (3 servers per day during one month)
    # Value should not have time in it
    resource_fixture.frequency = 1 * DAY
    assert resource_fixture.value() == (3 * SERVER) * (1 * MONTH).to("day").magnitude

    # Test with duration and frequency and period (3 servers 2 hours per day during one month)
    resource_fixture.duration = 2 * HOUR
    assert (
        resource_fixture.value()
        == (3 * SERVER) * ((2 * HOUR) / (1 * DAY) * (1 * MONTH)).to_reduced_units()
    )


def test_resource_copy(resource_fixture: Resource):
    """Test the copy function, that should only copy values, not ids"""

    resource_copy = copy(resource_fixture)

    # Should not be the same
    assert resource_copy.id != resource_fixture.id
    assert resource_copy.activity_id != resource_fixture.activity_id
    assert resource_copy.created_at != resource_fixture.created_at
    assert resource_copy.updated_at != resource_fixture.updated_at

    # Should be the same
    assert resource_copy.impact_source_id == resource_fixture.impact_source_id
    assert resource_copy._amount == resource_fixture._amount
    assert resource_copy._duration == resource_fixture._duration
    assert resource_copy._frequency == resource_fixture._frequency
    assert resource_copy._period == resource_fixture._period


@mock.patch(
    "impacts_model.data_model.impact_source_factory",
    MagicMock(
        return_value=ImpactSource(
            id="testid",
            name="test",
            unit=SERVER,
            environmental_impact={
                ImpactCategory.CLIMATE_CHANGE: ImpactValue(
                    manufacture=2332 * KG_CO2E, use=12332 * KG_CO2E
                )
            },
        )
    ),
)
def test_resource_get_impact(resource_fixture: Resource) -> None:
    """
    For Resource.get_co2_impact test computation, quantity change and resource adding
    :return: None
    """
    res_impact = resource_fixture.get_impact()
    assert res_impact is not None  # Test that dict contains the resource

    impact = res_impact.own_impact
    co2 = impact[ImpactCategory.CLIMATE_CHANGE]
    assert co2.manufacture is not None
    assert co2.manufacture.units == KG_CO2E
    assert co2.manufacture == (2332) * resource_fixture.value() * KG_CO2E
    assert co2.use == (12332) * resource_fixture.value() * KG_CO2E

    # Test quantity change
    resource_fixture.amount = 12321.423 * SERVER
    res_impact = resource_fixture.get_impact()
    assert res_impact is not None  # Test that dict contains the resource

    impact = res_impact.own_impact
    co2 = impact[ImpactCategory.CLIMATE_CHANGE]
    assert co2.manufacture is not None
    assert co2.manufacture.units == KG_CO2E
    assert co2.manufacture == (2332) * 12321.423 * KG_CO2E
    assert co2.use == (12332) * resource_fixture.value() * KG_CO2E


@mock.patch(
    "impacts_model.data_model.impact_source_factory",
    MagicMock(
        return_value=ImpactSource(
            id="testid",
            name="test",
            unit=SERVER,
            environmental_impact={
                ImpactCategory.CLIMATE_CHANGE: ImpactValue(use=10000.123 * KG_CO2E),
                ImpactCategory.RAW_MATERIALS: ImpactValue(use=213.3 * KG_MIPS),
            },
        ),
    ),
)
def test_resource_get_category_impact(resource_fixture: Resource) -> None:
    """
    Test get_impacts computation by changing quantity and impacts_list
    :return:
    """
    resource_fixture.amount = 1 * SERVER
    assert resource_fixture.get_impact().total == {
        ImpactCategory.CLIMATE_CHANGE: 10000.123 * KG_CO2E,
        ImpactCategory.RESOURCE_DEPLETION: 0 * KG_SBE,
        ImpactCategory.ACIDIFICATION: 0 * MOL_HPOS,
        ImpactCategory.FINE_PARTICLES: 0 * DISEASE_INCIDENCE,
        ImpactCategory.IONIZING_RADIATIONS: 0 * KG_BQ_U235E,
        ImpactCategory.WATER_DEPLETION: 0 * CUBIC_METER,
        ImpactCategory.RAW_MATERIALS: 213.3 * KG_MIPS,
    }

    # Test quantity multiplication
    resource_fixture.amount = 10 * SERVER
    assert resource_fixture.get_impact.total == {
        ImpactCategory.CLIMATE_CHANGE: (10 * 10000.123) * KG_CO2E,
        ImpactCategory.RESOURCE_DEPLETION: 0 * KG_SBE,
        ImpactCategory.ACIDIFICATION: 0 * MOL_HPOS,
        ImpactCategory.FINE_PARTICLES: 0 * DISEASE_INCIDENCE,
        ImpactCategory.IONIZING_RADIATIONS: 0 * KG_BQ_U235E,
        ImpactCategory.WATER_DEPLETION: 0 * CUBIC_METER,
        ImpactCategory.RAW_MATERIALS: (10 * 213.3) * KG_MIPS,
    }


def test_resource_get_category_impact():
    pass  # TODO
