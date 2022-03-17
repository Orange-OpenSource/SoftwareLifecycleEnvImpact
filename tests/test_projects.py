###########
# Project #
###########
from model.impact_sources import ImpactSource
from model.projects import Project, StandardProject
from model.resources import Resource
from model.tasks import Task


def test_get_global_impact():
    """Test consistency with the tasks individual impacts"""
    is1 = ImpactSource(1000)
    is2 = ImpactSource(776)
    r1 = Resource(quantity=1, impacts=[is1, is2])  # 1776
    r2 = Resource(quantity=1, impacts=[is1])  # 1000
    subtask = Task("Test", resources=[r1])  # 1776
    task = Task("Task", subtasks=[subtask], resources=[r1, r2])  # 2776

    p = Project(task)
    assert p.root_task.get_co2_impact() == p.get_global_impact()


###################
# StandardProject #
###################
def test_dev_days():
    """Test getter/setter of dev_days property"""
    s = StandardProject()
    s.dev_days = 1000  # setter
    assert s.dev_days == 1000  # getter


def test_design_days():
    """Test getter/setter of design_days property"""
    s = StandardProject()
    s.design_days = 1000  # setter
    assert s.design_days == 1000  # getter


def test_spec_days():
    """Test getter/setter of spec_days property"""
    s = StandardProject()
    s.spec_days = 1000  # setter
    assert s.spec_days == 1000  # getter


def test_management_days():
    """Test getter/setter of management_days property"""
    s = StandardProject()
    s.management_days = 1000  # setter
    assert s.management_days == 1000  # getter


def test_maintenance_days():
    """Test getter/setter of maintenance_days property"""
    s = StandardProject()
    s.maintenance_days = 1000  # setter
    assert s.maintenance_days == 1000  # getter


def test_electricity_mix():
    """Test getter/setter of electricity_mix property"""
    s = StandardProject()
    s.electricity_mix = 0.88707  # setter
    assert s.electricity_mix == 0.88707  # getter


def test_pue():
    """Test getter/setter of pue property"""
    s = StandardProject()
    s.pue = 1.999  # setter
    assert s.pue == 1.999  # getter


def test_servers_count():
    """Test getter/setter of servers_count property"""
    s = StandardProject()
    s.servers_count = 1000  # setter
    assert s.servers_count == 1000  # getter


def test_storage_tb():
    """Test getter/setter of storage_tb property"""
    s = StandardProject()
    s.storage_tb = 1000  # setter
    assert s.storage_tb == 1000  # getter


def test_run_duration():
    """Test getter/setter of run_duration property"""
    s = StandardProject()
    s.run_duration = 1000  # setter
    assert s.run_duration == 1000  # getter


def test_avg_user_day():
    """Test getter/setter of avg_user_day property"""
    s = StandardProject()
    s.avg_user = 1000  # setter
    assert s.avg_user == 1000  # getter


def test_avg_user_minutes():
    """Test getter/setter of avg_user_minutes property"""
    s = StandardProject()
    s.avg_time = 1000  # setter
    assert s.avg_time == 1000  # getter


def test_avg_user_data():
    """Test getter/setter of avg_user_data property"""
    s = StandardProject()
    s.avg_data = 1000.999  # setter
    assert s.avg_data == 1000.999  # getter
