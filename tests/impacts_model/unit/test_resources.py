from unittest import mock
from unittest.mock import MagicMock

import pytest
from flask_sqlalchemy import SQLAlchemy

from api.data_model import Model, Project, Resource, Task
from impacts_model.impact_sources import ImpactIndicator, ImpactSource, merge_resource_list, ResourcesList
from impacts_model.impacts import get_resource_impact, get_resource_impact_list
from impacts_model.quantities.quantities import (
    CUBIC_METER,
    DISEASE_INCIDENCE,
    ELECTRONIC_WASTE,
    KG_BQ_U235E,
    KG_CO2E,
    KG_SBE,
    MOL_HPOS,
    PRIMARY_MJ,
    TONNE_MIPS,
)


##########
# STATIC #
##########


def test_merge_resource_list() -> None:
    """
    Test merge_resource_list function, with edge cases to assess that the returned list is correct
    :return:
    """
    first_list: ResourcesList = {
        "first": {
            ImpactIndicator.CLIMATE_CHANGE: 1000 * KG_CO2E,
            ImpactIndicator.ELECTRONIC_WASTE: 1000 * ELECTRONIC_WASTE,
        },
    }
    second_list: ResourcesList = {}

    # test empty
    assert merge_resource_list(first_list, second_list) == {
        "first": {
            ImpactIndicator.CLIMATE_CHANGE: 1000 * KG_CO2E,
            ImpactIndicator.ELECTRONIC_WASTE: 1000 * ELECTRONIC_WASTE,
        },
    }

    # Test same impact

    second_list = {
        "first": {
            ImpactIndicator.CLIMATE_CHANGE: 1000 * KG_CO2E,
            ImpactIndicator.ELECTRONIC_WASTE: 1000 * ELECTRONIC_WASTE,
        }
    }
    assert merge_resource_list(first_list, second_list) == {
        "first": {
            ImpactIndicator.CLIMATE_CHANGE: 2000 * KG_CO2E,
            ImpactIndicator.ELECTRONIC_WASTE: 2000 * ELECTRONIC_WASTE,
        }
    }

    # Test new impact

    second_list = {
        "second": {
            ImpactIndicator.CLIMATE_CHANGE: 1000 * KG_CO2E,
            ImpactIndicator.ELECTRONIC_WASTE: 1000 * ELECTRONIC_WASTE,
        }
    }
    assert merge_resource_list(first_list, second_list) == {
        "first": {
            ImpactIndicator.CLIMATE_CHANGE: 1000 * KG_CO2E,
            ImpactIndicator.ELECTRONIC_WASTE: 1000 * ELECTRONIC_WASTE,
        },
        "second": {
            ImpactIndicator.CLIMATE_CHANGE: 1000 * KG_CO2E,
            ImpactIndicator.ELECTRONIC_WASTE: 1000 * ELECTRONIC_WASTE,
        },
    }


############
# Resource #
############


@pytest.fixture(scope="function")
def resource_fixture(db: SQLAlchemy) -> Resource:
    project = Project(name="Project test_resources")
    model = Model(name="Model test_resourcess")
    project.models = [model]
    task = Task(name="Test_resources task")

    resource = Resource(
        name="Resource test",
        type="TestResource",
        value=2312,
    )
    task.resources = [resource]
    model.tasks = [task]
    db.session.add_all([project, model, task])
    db.session.commit()
    return resource


@mock.patch(
    "impacts_model.impacts.load_resource_impacts",
    MagicMock(
        return_value=[
            ImpactSource(1000 * KG_CO2E),
            ImpactSource(999 * KG_CO2E),
            ImpactSource(333 * KG_CO2E),
        ]
    ),
)
def test_get_resource_impact(resource_fixture: Resource) -> None:
    """
    For Resource.get_co2_impact test computation, quantity change and resource adding
    :return: None
    """
    assert (
        get_resource_impact(resource_fixture, ImpactIndicator.CLIMATE_CHANGE)
        == (1000 + 999 + 333) * resource_fixture.value * KG_CO2E
    )

    # Test quantity change
    resource_fixture.value = 12321.423
    assert (
        get_resource_impact(resource_fixture, ImpactIndicator.CLIMATE_CHANGE)
        == (1000 + 999 + 333) * 12321.423 * KG_CO2E
    )


@mock.patch(
    "impacts_model.impacts.load_resource_impacts",
    MagicMock(
        return_value=[
            ImpactSource(10000.123 * KG_CO2E, raw_materials=213.3 * TONNE_MIPS),
        ]
    ),
)
def test_get_resource_impact_list(resource_fixture: Resource) -> None:
    """
    Test get_impacts computation by changing quantity and impacts_list
    :return:
    """
    resource_fixture.value = 1
    assert get_resource_impact_list(resource_fixture) == {
        ImpactIndicator.CLIMATE_CHANGE: 10000.123 * KG_CO2E,
        ImpactIndicator.RESOURCE_DEPLETION: 0 * KG_SBE,
        ImpactIndicator.ACIDIFICATION: 0 * MOL_HPOS,
        ImpactIndicator.FINE_PARTICLES: 0 * DISEASE_INCIDENCE,
        ImpactIndicator.IONIZING_RADIATIONS: 0 * KG_BQ_U235E,
        ImpactIndicator.WATER_DEPLETION: 0 * CUBIC_METER,
        ImpactIndicator.ELECTRONIC_WASTE: 0 * ELECTRONIC_WASTE,
        ImpactIndicator.PRIMARY_ENERGY: 0 * PRIMARY_MJ,
        ImpactIndicator.RAW_MATERIALS: 213.3 * TONNE_MIPS,
    }

    # Test quantity multiplication
    resource_fixture.value = 10
    assert get_resource_impact_list(resource_fixture) == {
        ImpactIndicator.CLIMATE_CHANGE: (10 * 10000.123) * KG_CO2E,
        ImpactIndicator.RESOURCE_DEPLETION: 0 * KG_SBE,
        ImpactIndicator.ACIDIFICATION: 0 * MOL_HPOS,
        ImpactIndicator.FINE_PARTICLES: 0 * DISEASE_INCIDENCE,
        ImpactIndicator.IONIZING_RADIATIONS: 0 * KG_BQ_U235E,
        ImpactIndicator.WATER_DEPLETION: 0 * CUBIC_METER,
        ImpactIndicator.ELECTRONIC_WASTE: 0 * ELECTRONIC_WASTE,
        ImpactIndicator.PRIMARY_ENERGY: 0 * PRIMARY_MJ,
        ImpactIndicator.RAW_MATERIALS: (10 * 213.3) * TONNE_MIPS,
    }
