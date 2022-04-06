from model.impact_sources import ImpactSource
from model.projects import Project, StandardProject
from model.quantities import ureg
from model.tasks import Task
from tests.unit.test_resources import TestResource  # type: ignore


###########
# Project #
###########


def test_get_global_impact() -> None:
    """Test consistency with the tasks individual _impacts"""

    is1 = ImpactSource(1000 * ureg.kg_co2e)
    is2 = ImpactSource(776 * ureg.kg_co2e)

    r1 = TestResource(1, impacts=[is1, is2])  # Impacts = 1 * 1776
    r2 = TestResource(1, impacts=[is1])  # Impacts = 1 * 1000

    subtask = Task("Test", resources=[r1])  # 1776
    task = Task("Task", subtasks=[subtask], resources=[r1, r2])  # 2776

    p = Project(task)
    assert p.root_task.get_co2_impact() == p.get_global_impact()


###################
# StandardProject #
###################
def test_get_impact_by_task() -> None:
    """Test that project level impact_by_task is same as root_task one"""
    s = StandardProject()
    assert s.get_impact_by_task() == s.root_task.get_impact()


def test_get_impact_by_resource() -> None:
    """Test that project level impact_by_resource is same as root_task one"""
    s = StandardProject()
    assert s.get_impact_by_resource() == s.root_task.get_impact_by_resource()


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
    )  # should be abstracted from ureg.electricity_mix
    assert s.electricity_mix == 0.88707  # getter


def test_pue() -> None:
    """Test getter/setter of pue property"""
    s = StandardProject()
    assert s.pue  # exist
    s.pue = 1.999  # setter
    assert isinstance(s.pue, float)  # should be abstracted from ureg.pue
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
