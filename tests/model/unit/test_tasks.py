#########
# Utils #
#########
import pytest

from model.impacts.impact_factors import ImpactFactor
from model.impacts.impacts import ImpactIndicator
from model.quantities import (
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
from model.resources import Resource
from model.tasks import TaskTemplate


########
# Task #
########


@pytest.fixture(scope="function")
def task_fixture() -> TaskTemplate:
    is1 = ImpactFactor(1000 * KG_CO2E)
    is2 = ImpactFactor(776 * KG_CO2E)

    r1 = Resource(name="Test resource", impacts=[is1, is2], quantity=1)  # 1776
    r2 = Resource(name="Test resource 2", impacts=[is1], quantity=1)  # 1000

    subtask = TaskTemplate("Subtask", resources=[r1])  # 1776
    return TaskTemplate("Task", subtasks=[subtask], resources=[r2])  # 1000 + 1776


def test_get_co2_impact(task_fixture: TaskTemplate) -> None:
    """Test that task co2 impact is those of all _resources from itself and its children"""

    assert (
        task_fixture.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
        == 2776 * KG_CO2E
    )


def test_get_impacts(task_fixture: TaskTemplate) -> None:
    """
    Test return value of get_impact_quantity is in form of TaskImpact
    """
    impact = task_fixture.get_impacts()
    assert isinstance(task_fixture.get_impacts(), dict)
    assert impact["name"] == "Task"
    assert impact["impacts"] == task_fixture.get_impacts_list()

    # Test subtask
    subtask = task_fixture.subtasks[0]
    subtask_dict = impact["subtasks"][0]  # type: ignore
    assert subtask_dict["name"] == "Subtask"
    assert subtask_dict["impacts"] == subtask.get_impacts_list()


def test_get_impacts_list(task_fixture: TaskTemplate) -> None:
    """
    Test that get_impact_list return the good format and compute well for task resource, and those of its subtasks
    :return:
    """
    task_fixture.subtasks.clear()
    # Test res
    assert task_fixture.get_impacts_list() == {
        ImpactIndicator.CLIMATE_CHANGE: 1000 * KG_CO2E,
        ImpactIndicator.RESOURCE_DEPLETION: 0 * KG_SBE,
        ImpactIndicator.ACIDIFICATION: 0 * MOL_HPOS,
        ImpactIndicator.FINE_PARTICLES: 0 * DISEASE_INCIDENCE,
        ImpactIndicator.IONIZING_RADIATIONS: 0 * KG_BQ_U235E,
        ImpactIndicator.WATER_DEPLETION: 0 * CUBIC_METER,
        ImpactIndicator.ELECTRONIC_WASTE: 0 * ELECTRONIC_WASTE,
        ImpactIndicator.PRIMARY_ENERGY: 0 * PRIMARY_MJ,
        ImpactIndicator.RAW_MATERIALS: 0 * TONNE_MIPS,
    }

    # Test subtasks
    subtask = TaskTemplate("Subtask", resources=task_fixture.resources)
    task_fixture.subtasks.append(subtask)

    assert task_fixture.get_impacts_list() == {
        ImpactIndicator.CLIMATE_CHANGE: (1000 * 2) * KG_CO2E,
        ImpactIndicator.RESOURCE_DEPLETION: 0 * KG_SBE,
        ImpactIndicator.ACIDIFICATION: 0 * MOL_HPOS,
        ImpactIndicator.FINE_PARTICLES: 0 * DISEASE_INCIDENCE,
        ImpactIndicator.IONIZING_RADIATIONS: 0 * KG_BQ_U235E,
        ImpactIndicator.WATER_DEPLETION: 0 * CUBIC_METER,
        ImpactIndicator.ELECTRONIC_WASTE: 0 * ELECTRONIC_WASTE,
        ImpactIndicator.PRIMARY_ENERGY: 0 * PRIMARY_MJ,
        ImpactIndicator.RAW_MATERIALS: 0 * TONNE_MIPS,
    }


def test_get_impact_by_resource(task_fixture: TaskTemplate) -> None:
    """
    Test Task.get_impact_by_resource() method, by adding a new resource, an existing one, and adding a subtask
    :return:
    """
    is1 = ImpactFactor(1000 * KG_CO2E)
    resource = Resource(name="Test resource", impacts=[is1], quantity=1)  # 1000

    # Test one res
    task = TaskTemplate("Task", resources=[resource])  # 1000
    res_dict = task.get_impact_by_resource()
    assert res_dict[resource.name][
        ImpactIndicator.CLIMATE_CHANGE
    ] == task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)

    # Test two res
    task2 = TaskTemplate("Task", resources=[resource, resource])  # 1000 + 1000
    res_dict = task2.get_impact_by_resource()
    assert res_dict[resource.name][
        ImpactIndicator.CLIMATE_CHANGE
    ] == task2.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)

    # Test subtasks
    task3 = TaskTemplate("Task", subtasks=[task, task2])  # 2000 + 1000
    res_dict = task3.get_impact_by_resource()
    assert res_dict[resource.name][
        ImpactIndicator.CLIMATE_CHANGE
    ] == task3.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)


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

