from unittest import mock
from unittest.mock import MagicMock

import pytest
from flask_sqlalchemy import SQLAlchemy
from pint import Quantity

from impacts_model.data_model import Model, Project, Resource, Task
from impacts_model.impact_sources import ImpactSource
from impacts_model.impacts import ImpactCategory
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
    DAY,
    SERVER,
    HOUR,
    MONTH
)

##########
# STATIC #
##########

'''
def test_merge_resource_list() -> None:
    """
    Test merge_resource_list function, with edge cases to assess that the returned list is correct
    :return:
    """
    first_list: ResourcesList = {
        "first": {
            ImpactCategory.CLIMATE_CHANGE: 1000 * KG_CO2E,
            ImpactCategory.ELECTRONIC_WASTE: 1000 * ELECTRONIC_WASTE,
        },
    }
    second_list: ResourcesList = {}

    # test empty
    assert merge_resource_list(first_list, second_list) == {
        "first": {
            ImpactCategory.CLIMATE_CHANGE: 1000 * KG_CO2E,
            ImpactCategory.ELECTRONIC_WASTE: 1000 * ELECTRONIC_WASTE,
        },
    }

    # Test same impact

    second_list = {
        "first": {
            ImpactCategory.CLIMATE_CHANGE: 1000 * KG_CO2E,
            ImpactCategory.ELECTRONIC_WASTE: 1000 * ELECTRONIC_WASTE,
        }
    }
    assert merge_resource_list(first_list, second_list) == {
        "first": {
            ImpactCategory.CLIMATE_CHANGE: 2000 * KG_CO2E,
            ImpactCategory.ELECTRONIC_WASTE: 2000 * ELECTRONIC_WASTE,
        }
    }

    # Test new impact

    second_list = {
        "second": {
            ImpactCategory.CLIMATE_CHANGE: 1000 * KG_CO2E,
            ImpactCategory.ELECTRONIC_WASTE: 1000 * ELECTRONIC_WASTE,
        }
    }
    assert merge_resource_list(first_list, second_list) == {
        "first": {
            ImpactCategory.CLIMATE_CHANGE: 1000 * KG_CO2E,
            ImpactCategory.ELECTRONIC_WASTE: 1000 * ELECTRONIC_WASTE,
        },
        "second": {
            ImpactCategory.CLIMATE_CHANGE: 1000 * KG_CO2E,
            ImpactCategory.ELECTRONIC_WASTE: 1000 * ELECTRONIC_WASTE,
        },
    }
'''

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
    task = Task(name="Test_resources task")

    resource = Resource(
        name="Resource test",
        impact_source_id="server",
        input=2312 * SERVER ,  # TODO pas mettre server en id mais mock
    )

    task.resources = [resource]
    model.root_task = task
    db.session.add_all([project, model, task, resource])
    db.session.commit()
    return resource


def test_resource_value(resource_fixture: Resource):
    """Test computation of function value()"""
    assert isinstance(resource_fixture.value(), Quantity)

    # Test with only input ( 3 servers)
    resource_fixture.input = 3 * SERVER
    assert resource_fixture.value() == 3 * SERVER

    # Test with duration (3 servers during one month)
    resource_fixture.duration = 1 * MONTH
    assert resource_fixture.value() == (3 * SERVER) * (1 * MONTH) 

    # Test with duration and frequency (3 servers per day during one month)
    resource_fixture.frequency = 1 * DAY
    assert resource_fixture.value() == (3 * SERVER) / (1 * DAY) * (1 * MONTH) 

    # Test with time_use and frequency and duration (3 servers 2 hours per day during one month)
    resource_fixture.time_use = 2 * HOUR
    assert resource_fixture.value() == (3 * SERVER) * (2 * HOUR) / (1 * DAY) * (1 * MONTH) 


def test_resource_copy():
    pass  # TODO


@mock.patch(
    "impacts_model.data_model.impact_source_factory",
    MagicMock(
        return_value=ImpactSource(
            id="testid", name="test", unit=SERVER, climate_change=2332 * KG_CO2E
        )
    ),
)
def test_get_resource_impact(resource_fixture: Resource) -> None:
    """
    For Resource.get_co2_impact test computation, quantity change and resource adding
    :return: None
    """
    impact = resource_fixture.get_category_impact(ImpactCategory.CLIMATE_CHANGE)
    assert isinstance(impact, Quantity)
    assert impact == (2332) * resource_fixture.value() * KG_CO2E

    # Test quantity change
    resource_fixture.input = 12321.423 * SERVER
    impact = resource_fixture.get_category_impact(ImpactCategory.CLIMATE_CHANGE)
    assert isinstance(impact, Quantity)
    assert impact == (2332) * 12321.423 * KG_CO2E


@mock.patch(
    "impacts_model.data_model.impact_source_factory",
    MagicMock(
        return_value=ImpactSource(
            id="testid",
            name="test",
            unit=SERVER,
            climate_change=10000.123 * KG_CO2E,
            raw_materials=213.3 * TONNE_MIPS,
        ),
    ),
)
def test_get_resource_environmental_impact(resource_fixture: Resource) -> None:
    """
    Test get_impacts computation by changing quantity and impacts_list
    :return:
    """
    resource_fixture.input = 1 * SERVER
    assert resource_fixture.get_environmental_impact().impacts == {
        ImpactCategory.CLIMATE_CHANGE: 10000.123 * KG_CO2E,
        ImpactCategory.RESOURCE_DEPLETION: 0 * KG_SBE,
        ImpactCategory.ACIDIFICATION: 0 * MOL_HPOS,
        ImpactCategory.FINE_PARTICLES: 0 * DISEASE_INCIDENCE,
        ImpactCategory.IONIZING_RADIATIONS: 0 * KG_BQ_U235E,
        ImpactCategory.WATER_DEPLETION: 0 * CUBIC_METER,
        ImpactCategory.ELECTRONIC_WASTE: 0 * ELECTRONIC_WASTE,
        ImpactCategory.PRIMARY_ENERGY: 0 * PRIMARY_MJ,
        ImpactCategory.RAW_MATERIALS: 213.3 * TONNE_MIPS,
    }

    # Test quantity multiplication
    resource_fixture.input = 10 * SERVER
    assert resource_fixture.get_environmental_impact().impacts == {
        ImpactCategory.CLIMATE_CHANGE: (10 * 10000.123) * KG_CO2E,
        ImpactCategory.RESOURCE_DEPLETION: 0 * KG_SBE,
        ImpactCategory.ACIDIFICATION: 0 * MOL_HPOS,
        ImpactCategory.FINE_PARTICLES: 0 * DISEASE_INCIDENCE,
        ImpactCategory.IONIZING_RADIATIONS: 0 * KG_BQ_U235E,
        ImpactCategory.WATER_DEPLETION: 0 * CUBIC_METER,
        ImpactCategory.ELECTRONIC_WASTE: 0 * ELECTRONIC_WASTE,
        ImpactCategory.PRIMARY_ENERGY: 0 * PRIMARY_MJ,
        ImpactCategory.RAW_MATERIALS: (10 * 213.3) * TONNE_MIPS,
    }


def test_resource_get_category_impact():
    pass  # TODO
