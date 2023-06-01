#########
# Utils #
#########
from unittest import mock
from unittest.mock import MagicMock

import pytest
from flask_sqlalchemy import SQLAlchemy
from pint import Quantity

from impacts_model.data_model import Model, Project, Resource, Activity
from impacts_model.impact_sources import ImpactSource
from impacts_model.impacts import ImpactCategory, ImpactValue
from impacts_model.quantities.quantities import (
    KG_CO2E,
    SERVER,
)


############
# Activity #
############


@pytest.fixture(scope="function")
def single_activity_fixture(db: SQLAlchemy) -> Activity:
    """Activity fixture without subactivity"""
    project = Project(name="Project test_activity")
    model = Model(name="Model test_activity")
    project.models = [model]
    activity = Activity(name="Test activity")

    resource1 = Resource(
        name="testResource 1",
        impact_source_id="testImpactSource",
        amount=1 * SERVER,
    )
    resource2 = Resource(
        name="testResource 2",
        impact_source_id="testImpactSource",
        amount=1 * SERVER,
    )
    activity.resources = [resource1, resource2]
    model.root_activity = activity
    db.session.add_all([project, model, activity, resource1, resource2])
    db.session.commit()
    return activity


@pytest.fixture(scope="function")
def activity_fixture_with_subactivity(db: SQLAlchemy) -> Activity:
    """Activity fixture with a subactivity"""
    project = Project(name="Project test_activity with subactivity")
    model = Model(name="Model test_activity with subactivity")
    project.models = [model]
    project.base_model = model
    activity = Activity(name="Test activity with subactivity")

    resource1 = Resource(
        name="testResource 3",
        impact_source_id="testImpactSource",
        amount=1 * SERVER,
    )
    resource2 = Resource(
        name="testResource 4",
        impact_source_id="testImpactSource",
        amount=1 * SERVER,
    )
    activity.resources = [resource1, resource2]
    subactivity = Activity(name="Test activity subactivity")
    resource3 = Resource(
        name="testResource 5",
        impact_source_id="testImpactSource",
        amount=1 * SERVER,
    )
    subactivity.resources = [resource3]

    activity.subactivities = [subactivity]
    model.root_activity = activity

    db.session.add_all([project, model, activity, resource1, resource2])
    db.session.commit()
    return activity


@mock.patch(
    "impacts_model.data_model.impact_source_factory",
    MagicMock(
        return_value=ImpactSource(
            id="testImpactSource",
            name="test",
            unit=SERVER,
            environmental_impact={
                ImpactCategory.CLIMATE_CHANGE: ImpactValue(manufacture=1776 * KG_CO2E)
            },
        ),
    ),
)
def test_get_activity_impact_by_category(
    single_activity_fixture: Activity, activity_fixture_with_subactivity: Activity
) -> None:
    """Test that activity co2 impact is those of all _resources from itself and its children"""

    # Mock activity = 2 * TestResource (mocked) = 2 * (1000 + 776) = 3552
    result = single_activity_fixture.get_impact().total[ImpactCategory.CLIMATE_CHANGE]
    assert isinstance(result, ImpactValue)
    assert result.manufacture is not None
    assert result.manufacture.units == KG_CO2E
    assert result.manufacture == 3552 * KG_CO2E

    # Test adding a subactivity
    # activity = 3552, subactivity = 1776 -> 5328
    result = activity_fixture_with_subactivity.get_impact().total[
        ImpactCategory.CLIMATE_CHANGE
    ]
    assert isinstance(result, ImpactValue)
    assert result.manufacture is not None
    assert result.manufacture.units == KG_CO2E
    assert result.manufacture == 5328 * KG_CO2E


@mock.patch(
    "impacts_model.data_model.impact_source_factory",
    MagicMock(
        return_value=ImpactSource(
            id="testImpactSource",
            name="test",
            unit=SERVER,
            environmental_impact={
                ImpactCategory.CLIMATE_CHANGE: ImpactValue(use=1000 * KG_CO2E)
            },
        )
    ),
)
def test_get_activity_impact_list(
    single_activity_fixture: Activity, activity_fixture_with_subactivity: Activity
) -> None:
    """
    Test that get_impact_list return the good format and compute well for activity resource, and those of its subactivities
    :return:
    """
    # Test res
    assert (
        single_activity_fixture.get_impact().total[ImpactCategory.CLIMATE_CHANGE].use
        == 2000 * KG_CO2E
    )

    # Test adding a subactivity
    assert (
        activity_fixture_with_subactivity.get_impact()
        .total[ImpactCategory.CLIMATE_CHANGE]
        .use
        == 3000 * KG_CO2E
    )


@mock.patch(
    "impacts_model.data_model.impact_source_factory",
    MagicMock(
        return_value=ImpactSource(
            id="testImpactSource",
            name="test",
            unit=SERVER,
            environmental_impact={
                ImpactCategory.CLIMATE_CHANGE: ImpactValue(use=1000 * KG_CO2E)
            },
        )
    ),
)
def test_get_activity_impact_by_impact_source(
    single_activity_fixture: Activity, activity_fixture_with_subactivity: Activity
) -> None:
    """
    Test the impact_source_impact property to get activity by impactsource id with two resources and a subactivity
    """
    # Test two resources
    res_dict = single_activity_fixture.get_impact().impact_sources
    assert (
        res_dict["testImpactSource"].total_impact[ImpactCategory.CLIMATE_CHANGE].use
        == 2000 * KG_CO2E
    )

    # Test subactivities

    res_dict = activity_fixture_with_subactivity.get_impact().impact_sources
    assert (
        res_dict["testImpactSource"].total_impact[ImpactCategory.CLIMATE_CHANGE].use
        == 3000 * KG_CO2E
    )
