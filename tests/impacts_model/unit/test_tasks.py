#########
# Utils #
#########
from unittest import mock
from unittest.mock import MagicMock, patch

import pytest
from flask_sqlalchemy import SQLAlchemy

from api.data_model import Model, Project, Resource, Task
from impacts_model.impact_sources import ImpactIndicator, ImpactSource
from impacts_model.impacts import get_task_impact_by_indicator, get_task_impact_by_resource_type, get_task_impact_list, \
    get_task_impacts
from impacts_model.quantities.quantities import CUBIC_METER, DISEASE_INCIDENCE, ELECTRONIC_WASTE, KG_BQ_U235E, KG_CO2E, \
    KG_SBE, MOL_HPOS, PRIMARY_MJ, TONNE_MIPS


########
# Task #
########


@pytest.fixture(scope="function")
def single_task_fixture(db: SQLAlchemy) -> Task:
    project = Project(name="Project test_task")
    model = Model(name="Model test_task")
    project.models = [model]
    task = Task(name="Test task")

    resource1 = Resource(
        name="Resource 1 test task",
        type="TestResource",
        value=1,
    )
    resource2 = Resource(
        name="Resource 2 test task",
        type="TestResource",
        value=1,
    )
    task.resources = [resource1, resource2]
    model.tasks = [task]
    db.session.add_all([project, model, task, resource1, resource2])
    db.session.commit()
    return task


@pytest.fixture(scope="function")
def task_fixture_with_subtask(db: SQLAlchemy) -> Task:
    project = Project(name="Project test_task with subtask")
    model = Model(name="Model test_task with subtask")
    project.models = [model]
    task = Task(name="Test task with subtask")

    resource1 = Resource(
        name="Resource 1 test task",
        type="TestResource",
        value=1,
    )
    resource2 = Resource(
        name="Resource 2 test task",
        type="TestResource",
        value=1,
    )
    task.resources = [resource1, resource2]
    subtask = Task(name="Test task subtask")
    resource3 = Resource(
        name="Resource 3 test task subtask",
        type="TestResource",
        value=1,
    )
    subtask.resources = [resource3]

    task.subtasks = [subtask]
    model.tasks = [task, subtask]

    db.session.add_all([project, model, task, resource1, resource2])
    db.session.commit()
    return task


class MockOpen:
    builtin_open = open

    def open(self, *args, **kwargs):
        if args[0] == "impacts_model/res/resources/TestResource.yaml":
            with patch("impacts_model.impact_sources.impact_source_factory") as p1:
                return mock.mock_open(
                    read_data="name: Network\nunit: gb\nimpact_factors:\n- TestImpact"
                )(*args, **kwargs)
        return self.builtin_open(*args, **kwargs)


@mock.patch(
    "impacts_model.resources.load_resource_impacts",
    MagicMock(return_value=[ImpactSource(1000 * KG_CO2E), ImpactSource(776 * KG_CO2E)]),
)
def test_get_task_impact_by_indicator(
    single_task_fixture: Task, task_fixture_with_subtask: Task
) -> None:
    """Test that task co2 impact is those of all _resources from itself and its children"""

    # Mock task = 2 * TestResource (mocked) = 2 * (1000 + 776) = 3552
    assert (
        get_task_impact_by_indicator(
            single_task_fixture, ImpactIndicator.CLIMATE_CHANGE
        )
        == 3552 * KG_CO2E
    )

    # Test adding a subtask
    # Task = 3552, subtask = 1776 -> 5328
    assert (
        get_task_impact_by_indicator(
            task_fixture_with_subtask, ImpactIndicator.CLIMATE_CHANGE
        )
        == 5328 * KG_CO2E
    )


@mock.patch(
    "impacts_model.resources.load_resource_impacts",
    MagicMock(return_value=[ImpactSource(1000 * KG_CO2E)]),
)
def test_get_task_impact_list(
    single_task_fixture: Task, task_fixture_with_subtask: Task
) -> None:
    """
    Test that get_impact_list return the good format and compute well for task resource, and those of its subtasks
    :return:
    """
    # Test res
    assert get_task_impact_list(single_task_fixture) == {
        ImpactIndicator.CLIMATE_CHANGE: 2000 * KG_CO2E,
        ImpactIndicator.RESOURCE_DEPLETION: 0 * KG_SBE,
        ImpactIndicator.ACIDIFICATION: 0 * MOL_HPOS,
        ImpactIndicator.FINE_PARTICLES: 0 * DISEASE_INCIDENCE,
        ImpactIndicator.IONIZING_RADIATIONS: 0 * KG_BQ_U235E,
        ImpactIndicator.WATER_DEPLETION: 0 * CUBIC_METER,
        ImpactIndicator.ELECTRONIC_WASTE: 0 * ELECTRONIC_WASTE,
        ImpactIndicator.PRIMARY_ENERGY: 0 * PRIMARY_MJ,
        ImpactIndicator.RAW_MATERIALS: 0 * TONNE_MIPS,
    }

    # Test adding a subtask
    assert get_task_impact_list(task_fixture_with_subtask) == {
        ImpactIndicator.CLIMATE_CHANGE: (3000) * KG_CO2E,
        ImpactIndicator.RESOURCE_DEPLETION: 0 * KG_SBE,
        ImpactIndicator.ACIDIFICATION: 0 * MOL_HPOS,
        ImpactIndicator.FINE_PARTICLES: 0 * DISEASE_INCIDENCE,
        ImpactIndicator.IONIZING_RADIATIONS: 0 * KG_BQ_U235E,
        ImpactIndicator.WATER_DEPLETION: 0 * CUBIC_METER,
        ImpactIndicator.ELECTRONIC_WASTE: 0 * ELECTRONIC_WASTE,
        ImpactIndicator.PRIMARY_ENERGY: 0 * PRIMARY_MJ,
        ImpactIndicator.RAW_MATERIALS: 0 * TONNE_MIPS,
    }


@mock.patch(
    "impacts_model.resources.load_resource_impacts",
    MagicMock(return_value=[ImpactSource(1000 * KG_CO2E)]),
)
def test_get_task_impacts(task_fixture_with_subtask: Task) -> None:
    """
    Test return value of get_impact_quantity is in form of TaskImpact
    """
    impact = get_task_impacts(task_fixture_with_subtask)
    assert isinstance(impact, dict)

    assert impact["id"] == task_fixture_with_subtask.id
    assert impact["name"] == task_fixture_with_subtask.name

    # Test subtask
    subtask_dict = impact["subtasks"][0]
    assert subtask_dict == get_task_impacts(task_fixture_with_subtask.subtasks[0])


@mock.patch(
    "impacts_model.resources.load_resource_impacts",
    MagicMock(return_value=[ImpactSource(1000 * KG_CO2E)]),
)
def test_get_task_impact_by_resource_type(
    single_task_fixture: Task, task_fixture_with_subtask: Task
) -> None:
    # Test two res
    res_dict = get_task_impact_by_resource_type(single_task_fixture)
    assert res_dict["TestResource"][
        ImpactIndicator.CLIMATE_CHANGE
    ] == get_task_impact_by_indicator(single_task_fixture, ImpactIndicator.CLIMATE_CHANGE)

    # Test subtasks
    res_dict = get_task_impact_by_resource_type(task_fixture_with_subtask)
    assert res_dict["TestResource"][
        ImpactIndicator.CLIMATE_CHANGE
    ] == get_task_impact_by_indicator(task_fixture_with_subtask, ImpactIndicator.CLIMATE_CHANGE)


def test_get_impact_by_resource_quantity() -> None:
    """
    Assess that get_impact_by_resource() get all the co2 impact quantity for all the tasks/subtasks/res
    :return:
    """
    # p = StandardProject()
    # co2 = 0.0
    # d = p.root_task.get_impact_by_resource()

    # for resource in d:
    #     co2 += d[resource][ImpactIndicator.CLIMATE_CHANGE]
    #
    # assert round(p.get_co2_impact(), 5) == round(co2, 5)
    # TODO
