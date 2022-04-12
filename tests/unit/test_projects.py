from model.impacts.impact_factors import ImpactFactor
from model.impacts.impacts import ImpactIndicator
from model.projects import Project, StandardProject
from model.quantities import KG_CO2E
from model.tasks import Task
from tests.unit.test_resources import TestResource  # type: ignore

###########
# Project #
###########

is1 = ImpactFactor(1000 * KG_CO2E)
is2 = ImpactFactor(776 * KG_CO2E)

r1 = TestResource(1, impacts=[is1, is2])  # Impacts = 1 * 1776
r2 = TestResource(1, impacts=[is1])  # Impacts = 1 * 1000

subtask = Task("Test", resources=[r1])  # 1776
task = Task("Task", subtasks=[subtask], resources=[r1, r2])  # 2776

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


###################
# StandardProject #
###################


def test_dev_days() -> None:
    """Test getter/setter of dev_days property"""
    s = StandardProject()
    assert s.dev_days  # exist
    s.dev_days = 1000  # setter
    assert s.dev_days == 1000  # getter


def test_design_days() -> None:
    """Test getter/setter of design_days property"""
    s = StandardProject()
    assert s.design_days  # exist
    s.design_days = 1000  # setter
    assert s.design_days == 1000  # getter


def test_spec_days() -> None:
    """Test getter/setter of spec_days property"""
    s = StandardProject()
    assert s.spec_days  # exist
    s.spec_days = 1000  # setter
    assert s.spec_days == 1000  # getter


def test_management_days() -> None:
    """Test getter/setter of management_days property"""
    s = StandardProject()
    assert s.management_days  # exist
    s.management_days = 1000  # setter
    assert s.management_days == 1000  # getter


def test_maintenance_days() -> None:
    """Test getter/setter of maintenance_days property"""
    s = StandardProject()
    assert s.maintenance_days  # exist
    s.maintenance_days = 1000  # setter
    assert s.maintenance_days == 1000  # getter


def test_electricity_mix() -> None:
    """Test getter/setter of electricity_mix property"""
    s = StandardProject()
    assert s.electricity_mix  # exist
    s.electricity_mix = 0.88707  # setter
    assert isinstance(
        s.electricity_mix, float
    )  # should be abstracted from electricity_mix unit
    assert s.electricity_mix == 0.88707  # getter


def test_pue() -> None:
    """Test getter/setter of pue property"""
    s = StandardProject()
    assert s.pue  # exist
    s.pue = 1.999  # setter
    assert isinstance(s.pue, float)  # should be abstracted from pue unit
    assert s.pue == 1.999  # getter


def test_servers_count() -> None:
    """Test getter/setter of servers_count property"""
    s = StandardProject()
    assert s.servers_count  # exist
    s.servers_count = 1000  # setter
    assert s.servers_count == 1000  # getter


def test_storage_size() -> None:
    """Test getter/setter of storage_size property"""
    s = StandardProject()
    assert s.storage_size  # exist
    s.storage_size = 1000  # setter
    assert s.storage_size == 1000  # getter


def test_run_duration() -> None:
    """Test getter/setter of run_duration property"""
    s = StandardProject()
    assert s.run_duration  # exist
    s.run_duration = 1000  # setter
    assert s.run_duration == 1000  # getter


def test_avg_user() -> None:
    """Test getter/setter of avg_user property"""
    s = StandardProject()
    assert s.avg_user  # exist
    s.avg_user = 1000  # setter
    assert s.avg_user == 1000  # getter


def test_avg_time() -> None:
    """Test getter/setter of avg_time property"""
    s = StandardProject()
    assert s.avg_time  # exist
    s.avg_time = 1000  # setter
    assert s.avg_time == 1000  # getter


def test_avg_data() -> None:
    """Test getter/setter of avg_data property"""
    s = StandardProject()
    assert s.avg_data  # exist
    s.avg_data = 1000.999  # setter
    assert s.avg_data == 1000.999  # getter
