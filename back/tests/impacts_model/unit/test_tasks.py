#########
# Utils #
#########
from unittest import mock
from unittest.mock import MagicMock

import pytest
from flask_sqlalchemy import SQLAlchemy
from pint import Quantity

from impacts_model.data_model import Model, Project, Resource, Task
from impacts_model.impact_sources import ImpactSource
from impacts_model.impacts import EnvironmentalImpact, ImpactCategory, ImpactValue
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
    SERVER,
)


########
# Task #
########


@pytest.fixture(scope="function")
def single_task_fixture(db: SQLAlchemy) -> Task:
    """Task fixture without subtask"""
    project = Project(name="Project test_task")
    model = Model(name="Model test_task")
    project.models = [model]
    task = Task(name="Test task")

    resource1 = Resource(
        name="testResource 1",
        impact_source_id="TestImpactSource",
        amount=1 * SERVER,
    )
    resource2 = Resource(
        name="testResource 2",
        impact_source_id="TestImpactSource",
        amount=1 * SERVER,
    )
    task.resources = [resource1, resource2]
    model.root_task = task
    db.session.add_all([project, model, task, resource1, resource2])
    db.session.commit()
    return task


@pytest.fixture(scope="function")
def task_fixture_with_subtask(db: SQLAlchemy) -> Task:
    """Task fixture with a subtask"""
    project = Project(name="Project test_task with subtask")
    model = Model(name="Model test_task with subtask")
    project.models = [model]
    project.base_model = model
    task = Task(name="Test task with subtask")

    resource1 = Resource(
        name="testResource 3",
        impact_source_id="TestImpactSource",
        amount=1 * SERVER,
    )
    resource2 = Resource(
        name="testResource 4",
        impact_source_id="TestImpactSource",
        amount=1 * SERVER,
    )
    task.resources = [resource1, resource2]
    subtask = Task(name="Test task subtask")
    resource3 = Resource(
        name="testResource 4",
        impact_source_id="TestImpactSource",
        amount=1 * SERVER,
    )
    subtask.resources = [resource3]

    task.subtasks = [subtask]
    model.root_task = task

    db.session.add_all([project, model, task, resource1, resource2])
    db.session.commit()
    return task


@mock.patch(
    "impacts_model.data_model.impact_source_factory",
    MagicMock(
        return_value=ImpactSource(
            id="testid",
            name="test",
            unit=SERVER,
            environmental_impact=EnvironmentalImpact(
                climate_change=ImpactValue(manufacture=1776 * KG_CO2E)
            ),
        ),
    ),
)
def test_get_task_impact_by_category(
    single_task_fixture: Task, task_fixture_with_subtask: Task
) -> None:
    """Test that task co2 impact is those of all _resources from itself and its children"""

    # Mock task = 2 * TestResource (mocked) = 2 * (1000 + 776) = 3552
    result = single_task_fixture.get_category_impact(ImpactCategory.CLIMATE_CHANGE)
    assert isinstance(result, ImpactValue)
    assert result.manufacture is not None
    assert result.manufacture.units == KG_CO2E
    assert result.manufacture == 3552 * KG_CO2E

    # Test adding a subtask
    # Task = 3552, subtask = 1776 -> 5328
    result = task_fixture_with_subtask.get_category_impact(
        ImpactCategory.CLIMATE_CHANGE
    )
    assert isinstance(result, ImpactValue)
    assert result.manufacture is not None
    assert result.manufacture.units == KG_CO2E
    assert result.manufacture == 5328 * KG_CO2E


@mock.patch(
    "impacts_model.data_model.impact_source_factory",
    MagicMock(
        return_value=ImpactSource(
            id="testid",
            name="test",
            unit=SERVER,
            environmental_impact=EnvironmentalImpact(
                climate_change=ImpactValue(use=1000 * KG_CO2E)
            ),
        )
    ),
)
def test_get_task_impact_list(
    single_task_fixture: Task, task_fixture_with_subtask: Task
) -> None:
    """
    Test that get_impact_list return the good format and compute well for task resource, and those of its subtasks
    :return:
    """
    # Test res
    single_task_fixture.get_environmental_impact().impacts[
        ImpactCategory.CLIMATE_CHANGE
    ].manufacture == 2000 * KG_CO2E

    # Test adding a subtask
    single_task_fixture.get_environmental_impact().impacts[
        ImpactCategory.CLIMATE_CHANGE
    ].manufacture == 3000 * KG_CO2E


@mock.patch(
    "impacts_model.data_model.impact_source_factory",
    MagicMock(
        return_value=ImpactSource(
            id="testImpactSource",
            name="test",
            unit=SERVER,
            environmental_impact=EnvironmentalImpact(
                climate_change=ImpactValue(use=1000 * KG_CO2E)
            ),
        )
    ),
)
def test_get_task_impact_by_resource_type(
    single_task_fixture: Task, task_fixture_with_subtask: Task
) -> None:
    """
    Test the function get_impact_by_resource_type with two resources and a subtask
    """
    # Test two res
    res_dict = single_task_fixture.get_impact_by_resource_type()
    assert (
        res_dict["TestImpactSource"].impacts[ImpactCategory.CLIMATE_CHANGE].use
        == single_task_fixture.get_category_impact(ImpactCategory.CLIMATE_CHANGE).use
    )

    # Test subtasks
    res_dict = task_fixture_with_subtask.get_impact_by_resource_type()
    assert (
        res_dict["TestImpactSource"].impacts[ImpactCategory.CLIMATE_CHANGE].use
        == task_fixture_with_subtask.get_category_impact(
            ImpactCategory.CLIMATE_CHANGE
        ).use
    )
