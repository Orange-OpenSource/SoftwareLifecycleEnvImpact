from model.impact_sources import ImpactSource
from model.projects import Project, StandardProject
from model.resources import PeopleResource
from model.tasks import Task

###########
# Project #
###########


def test_get_global_impact():
    """Test consistency with the tasks individual impacts"""
    is1 = ImpactSource(1000)
    is2 = ImpactSource(776)

    r1 = PeopleResource(1)  # 1 quantity
    r1.impacts = [is1, is2]  # change impacts to have static ones # 1776
    r2 = PeopleResource(1)
    r2.impacts = [is1]  # 1000

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
    assert s.dev_days  # exist
    s.dev_days = 1000  # setter
    assert s.dev_days == 1000  # getter


def test_design_days():
    """Test getter/setter of design_days property"""
    s = StandardProject()
    assert s.design_days  # exist
    s.design_days = 1000  # setter
    assert s.design_days == 1000  # getter


def test_spec_days():
    """Test getter/setter of spec_days property"""
    s = StandardProject()
    assert s.spec_days  # exist
    s.spec_days = 1000  # setter
    assert s.spec_days == 1000  # getter


def test_management_days():
    """Test getter/setter of management_days property"""
    s = StandardProject()
    assert s.management_days  # exist
    s.management_days = 1000  # setter
    assert s.management_days == 1000  # getter


def test_maintenance_days():
    """Test getter/setter of maintenance_days property"""
    s = StandardProject()
    assert s.maintenance_days  # exist
    s.maintenance_days = 1000  # setter
    assert s.maintenance_days == 1000  # getter


def test_electricity_mix():
    """Test getter/setter of electricity_mix property"""
    s = StandardProject()
    assert s.electricity_mix  # exist
    s.electricity_mix = 0.88707  # setter
    assert s.electricity_mix == 0.88707  # getter


def test_pue():
    """Test getter/setter of pue property"""
    s = StandardProject()
    assert s.pue  # exist
    s.pue = 1.999  # setter
    assert s.pue == 1.999  # getter


def test_servers_count():
    """Test getter/setter of servers_count property"""
    s = StandardProject()
    assert s.servers_count  # exist
    s.servers_count = 1000  # setter
    assert s.servers_count == 1000  # getter


def test_storage_size():
    """Test getter/setter of storage_size property"""
    s = StandardProject()
    assert s.storage_size  # exist
    s.storage_size = 1000  # setter
    assert s.storage_size == 1000  # getter


def test_run_duration():
    """Test getter/setter of run_duration property"""
    s = StandardProject()
    assert s.run_duration  # exist
    s.run_duration = 1000  # setter
    assert s.run_duration == 1000  # getter


def test_avg_user():
    """Test getter/setter of avg_user property"""
    s = StandardProject()
    assert s.avg_user  # exist
    s.avg_user = 1000  # setter
    assert s.avg_user == 1000  # getter


def test_avg_time():
    """Test getter/setter of avg_time property"""
    s = StandardProject()
    assert s.avg_time  # exist
    s.avg_time = 1000  # setter
    assert s.avg_time == 1000  # getter


def test_avg_data():
    """Test getter/setter of avg_data property"""
    s = StandardProject()
    assert s.avg_data  # exist
    s.avg_data = 1000.999  # setter
    assert s.avg_data == 1000.999  # getter
