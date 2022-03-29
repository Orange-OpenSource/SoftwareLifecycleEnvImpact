from model.impact_sources import ImpactSource
from model.projects import StandardProject
from model.resources import PeopleResource
from model.tasks import (
    DesignTask,
    DevTask,
    HostingTask,
    MaintenanceTask,
    ManagementTask,
    RunTask,
    SpecTask,
    Task,
    UsageTask,
)
from model.units import Q_, ureg


########
# Task #
########


def test_get_co2_impact() -> None:
    """Test that task co2 impact is those of all _resources from itself and its children"""
    is1 = ImpactSource(Q_(1000, ureg.kg_co2e))
    is2 = ImpactSource(Q_(776, ureg.kg_co2e))

    r1 = PeopleResource(1)  # 1 quantity
    r1._impacts = [is1, is2]  # change _impacts to have static ones # 1776
    r2 = PeopleResource(1)
    r2._impacts = [is1]  # 1000

    subtask = Task("Test", resources=[r1])  # 1776
    task = Task("Task", subtasks=[subtask], resources=[r2])  # 1000 + 1776

    assert task.get_co2_impact() == 2776 * ureg.kg_co2e


def test_get_impact() -> None:
    """
    Test return value of get_impact is in form of
    {
        "name": xxx
        "CO2": xxx
        "subtasks": {
            "name": xxx
            "CO2": xxx
            "subtasks": }
        }
    }
    """
    is1 = ImpactSource(Q_(1000, ureg.kg_co2e))
    is2 = ImpactSource(Q_(776, ureg.kg_co2e))

    r1 = PeopleResource(1)  # 1 quantity
    r1._impacts = [is1, is2]  # change _impacts to have static ones # 1776
    r2 = PeopleResource(1)
    r2._impacts = [is1]  # 1000

    subtask = Task("Subtask", resources=[r1])  # 1776
    task = Task("Task", subtasks=[subtask], resources=[r2])  # 1000 + 1776

    impact = task.get_impact()
    assert isinstance(task.get_impact(), dict)
    assert impact["name"] == "Task"
    assert impact["CO2"] == task.get_co2_impact().magnitude

    # Test subtask
    assert impact["subtasks"][0]["name"] == "Subtask"  # type: ignore
    assert impact["subtasks"][0]["CO2"] == subtask.get_co2_impact().magnitude  # type: ignore


def test_get_impact_by_resource() -> None:
    """
    Test Task.get_impact_by_resource() method, by adding a new resource, an existing one, and adding a subtask
    :return:
    """
    is1 = ImpactSource(Q_(1000, ureg.kg_co2e))
    r2 = PeopleResource(1)
    r2._impacts = [is1]  # 1000

    # Test one res
    task = Task("Task", resources=[r2])  # 1000 + 1776
    res_dict = task.get_impact_by_resource()
    assert res_dict[r2.name]["CO2"] == task.get_co2_impact().magnitude

    # Test two resources
    task2 = Task("Task", resources=[r2, r2])  # 1000 + 1776
    res_dict = task2.get_impact_by_resource()
    assert res_dict[r2.name]["CO2"] == task2.get_co2_impact().magnitude

    # Test subtasks
    task3 = Task("Task", subtasks=[task, task2])
    res_dict = task3.get_impact_by_resource()
    assert res_dict[r2.name]["CO2"] == task3.get_co2_impact().magnitude


def test_get_impact_by_resource_quantity() -> None:
    """
    Assess that get_impact_by_resource() get all the co2 impact quantity for all the tasks/subtasks/resources
    :return:
    """
    p = StandardProject()
    co2 = 0.0
    d = p.root_task.get_impact_by_resource()
    for resource in d.keys():
        co2 += d[resource]["CO2"]
    assert p.get_global_impact().magnitude == co2


###########
# DevTask #
###########


def test_dev_days() -> None:
    """Test DevTask.dev_days property getters and setters"""
    d = DevTask(236)
    assert d.dev_days == 236  # check init/getter
    d.dev_days = 87623
    assert d.dev_days == 87623  # check setter


##############
# DesignTask #
##############


def test_design_days() -> None:
    """Test Design.design_days property getters and setters"""
    d = DesignTask(123)
    assert d.design_days == 123  # check init/getter
    d.design_days = 5342
    assert d.design_days == 5342  # check setter


############
# SpecTask #
############


def test_spec_days() -> None:
    """Test SpecTask.spec_days property getters and setters"""
    d = SpecTask(642)
    assert d.spec_days == 642  # check init/getter
    d.spec_days = 234
    assert d.spec_days == 234  # check setter


##################
# ManagementTask #
##################


def test_management_days() -> None:
    """Test ManagementTask.management_days property getters and setters"""
    d = ManagementTask(523)
    assert d.management_days == 523  # check init/getter
    d.management_days = 432
    assert d.management_days == 432  # check setter


##################
# MaintenanceTask #
##################


def test_maintenance_days() -> None:
    """Test MaintenanceTask.maintenance_days property getters and setters"""
    d = MaintenanceTask(4532)
    assert d.maintenance_days == 4532  # check init/getter
    d.maintenance_days = 23435
    assert d.maintenance_days == 23435  # check setter


###############
# HostingTask #
###############


def test_servers_count() -> None:
    """Test HostingTask.servers_count property getters and setters"""
    h = HostingTask(12, 124, 364)
    assert h.servers_count == 12  # check init/getter
    h.servers_count = 113
    assert h.servers_count == 113  # check setter


def test_storage_size() -> None:
    """Test HostingTask.storage_size property getters and setters"""
    h = HostingTask(12, 124, 364)
    assert h.storage_size == 124  # check init/getter
    h.storage_size = 113
    assert h.storage_size == 113  # check setter


def test_hosting_task_duration() -> None:
    """Test getter/setter and child updates for property duration"""
    h = HostingTask(12, 124, 364)
    assert h.duration == 364  # check init/getter
    h.duration = 726
    assert h.duration == 726  # check setter
    assert h._compute_resource.duration == 726
    assert h._storage_resource.duration == 726  # check children update


#############
# UsageTask #
#############


def test_avg_user() -> None:
    """Test UsageTask.avg_user property getters and setters and children update"""
    u = UsageTask(1200, 39, 1.235, 365)
    assert u.avg_user == 1200  # check init / getter
    u.avg_user = 4323
    assert u.avg_user == 4323  # check setter
    assert u._user_device_res.avg_user == 4323
    assert u._network_resource.avg_user == 4323  # check children update


def test_duration() -> None:
    """Test UsageTask. duration property getters and setters and children update"""
    u = UsageTask(1200, 39, 1.235, 365)
    assert u.duration == 365  # check init / getter
    u.duration = 5432
    assert u.duration == 5432  # check setter
    assert u._user_device_res.duration == 5432
    assert u._network_resource.duration == 5432  # check children update


def test_avg_time() -> None:
    """Test UsageTask.avg_time property getters and setters and children update"""
    u = UsageTask(1200, 39, 1.235, 365)
    assert u.avg_time == 39  # check init / getter
    u.avg_time = 120
    assert u.avg_time == 120  # check setter
    assert u._user_device_res.avg_time == 120  # check children update


def test_avg_data() -> None:
    """Test UsageTask.avg_data property getters and setters and children update"""
    u = UsageTask(1200, 39, 1.235, 365)
    assert u.avg_data == 1.235  # check init / getter
    u.avg_data = 12334.123876
    assert u.avg_data == 12334.123876  # check setter
    assert u._network_resource.avg_data == 12334.123876  # check children update


###########
# RunTask #
###########
def test_run_task_duration() -> None:
    """Test getter/setter and child updates for property duration"""
    maintenance_task = MaintenanceTask(123)
    hosting_task = HostingTask(15, 64, 365)
    usage_task = UsageTask(1, 1, 1, 365)

    run_task = RunTask(maintenance_task, hosting_task, usage_task)

    assert run_task.duration == 365  # check init/getter
    run_task.duration = 243
    assert run_task.duration == 243  # check setter
    assert hosting_task.duration == 243  # check children update
    assert usage_task.duration == 243  # check children update
