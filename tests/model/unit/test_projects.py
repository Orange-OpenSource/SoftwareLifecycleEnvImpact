from model.impacts.impact_factors import ImpactFactor
from model.impacts.impacts import ImpactIndicator
from model.projects import Project
from model.quantities import KG_CO2E
from model.tasks import TaskTemplate
from tests.model.unit.test_resources import TestResource

###########
# Project #
###########

is1 = ImpactFactor(1000 * KG_CO2E)
is2 = ImpactFactor(776 * KG_CO2E)

r1 = TestResource(1, impacts=[is1, is2])  # Impacts = 1 * 1776
r2 = TestResource(1, impacts=[is1])  # Impacts = 1 * 1000

subtask = TaskTemplate("Test", resources=[r1])  # 1776
task = TaskTemplate("Task", subtasks=[subtask], resources=[r1, r2])  # 2776

project = Project(task)


def test_get_global_impact() -> None:
    """Test consistency with the tasks individual _impacts"""
    assert (
        project.root_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
        == project.get_co2_impact()
    )


def test_get_impact_by_task() -> None:
    """Test that project level impact_by_task is same as root_task one"""
    assert project.root_task.get_impacts() == project.get_impact_by_task()


def test_get_impact_by_resource() -> None:
    """Test that project level impact_by_resource is same as root_task one"""
    assert (
        project.root_task.get_impact_by_resource() == project.get_impact_by_resource()
    )


def test_get_impact_by_indicator() -> None:
    """Test that project level get_impact_by_indicator is same as root_task one"""
    assert project.root_task.get_impact_by_indicator(
        ImpactIndicator.CLIMATE_CHANGE
    ) == project.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
    assert (
        project.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
        == project.get_co2_impact()
    )