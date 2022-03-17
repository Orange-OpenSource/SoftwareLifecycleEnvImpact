from model.impact_sources import ImpactSource
from model.resources import Resource
from model.tasks import HostingTask, RunTask, Task


########
# Task #
########


def test_get_co2_impact():
    """Test that task co2 impact is those of all resources from itself and its childrens"""
    is1 = ImpactSource(1000)
    is2 = ImpactSource(776)
    r1 = Resource(quantity=1, impacts=[is1, is2])  # 1776
    r2 = Resource(quantity=1, impacts=[is1])  # 1000
    subtask = Task("Test", resources=[r1])  # 1776
    task = Task("Task", subtasks=[subtask], resources=[r2])  # 1000 + 1776

    assert task.get_co2_impact() == 2776


###############
# HostingTask #
###############


def test_server_days():
    """Test consistency with update of values for server_days"""
    h = HostingTask(0.6, 1.5, 12, 13, 14, 364)
    assert h.server_days == 364 * 12  # check init
    h.duration = 26
    assert h.server_days == 26 * 12  # check duration change
    h.servers_count = 16
    assert h.server_days == 26 * 16  # check number of servers  change


def test_storage_days():
    """Test computation for storage_days property and its update"""
    h = HostingTask(0.6, 1.5, 12, 124, 14, 364)
    assert h.storage_days == 364 * 124  # check init
    h.duration = 26
    assert h.storage_days == 26 * 124  # check duration change
    h.storage_size = 432
    assert h.storage_days == 26 * 432  # check number of servers  change


def test_servers_count():
    """Test getter/setter and child updates for property server_count"""
    h = HostingTask(0.6, 1.5, 12, 124, 14, 364)
    assert h.servers_count == 12  # check init/getter
    h.servers_count = 113
    assert h.servers_count == 113  # check setter
    assert h.compute_resource.quantity == h.server_days  # check children update


def test_storage_tb():
    """Test getter/setter and child updates for property storage"""
    h = HostingTask(0.6, 1.5, 12, 124, 14, 364)
    assert h.storage_size == 124  # check init/getter
    h.storage_size = 113
    assert h.storage_size == 113  # check setter
    assert h.storage_resource.quantity == h.storage_days  # check children update


def test_pue():
    """Test getter/setter and child updates for property pue"""
    h = HostingTask(0.6, 1.5, 12, 124, 14, 364)
    assert h.pue == 1.5  # check init/getter
    h.pue = 2.37946587
    assert h.pue == 2.37946587  # check setter
    assert h.compute_resource.server_impact.pue == 2.37946587  # check children update
    assert h.storage_resource.storage_impact.pue == 2.37946587  # check children update


def test_electricity_mix():
    """Test getter/setter and child updates for property electricity_mix"""
    h = HostingTask(0.6, 1.5, 12, 124, 14, 364)
    assert h.electricity_mix == 0.6  # check init/getter
    h.electricity_mix = 0.727
    assert h.electricity_mix == 0.727  # check setter
    assert (
        h.compute_resource.server_impact.electricity_mix == 0.727
    )  # check children update
    assert (
        h.storage_resource.storage_impact.electricity_mix == 0.727
    )  # check children update


def test_duration_days():
    """Test getter/setter and child updates for property duration"""
    h = HostingTask(0.6, 1.5, 12, 124, 14, 364)
    assert h.duration == 364  # check init/getter
    h.duration = 726
    assert h.duration == 726  # check setter
    assert h.storage_resource.quantity == h.storage_days
    assert h.compute_resource.quantity == h.server_days  # check children update


###########
# RunTask #
###########
def test_duration():
    """Test getter/setter and child updates for property duration"""
    r = RunTask(100, 0.6, 1.5, 15, 500, 365, 3000, 23, 0.4)
    assert r.duration == 365  # check init/getter
    r.duration = 243
    assert r.duration == 243  # check setter
    assert r.hosting_task.duration == 243  # check children update


def test_avg_user():
    """Test getter/setter and child updates for property avg_user"""
    r = RunTask(100, 0.6, 1.5, 15, 500, 365, 3000, 23, 0.4)
    assert r.avg_user == 3000  # check init/getter
    r.avg_user = 15345
    assert r.avg_user == 15345  # check setter
    assert r.user_device_res.quantity == r.users_hours  # check children update
    assert (
        r.hosting_task.network_resource.quantity == r.users_data
    )  # check children update


def test_avg_time():
    """Test getter/setter and child updates for property avg_time"""
    r = RunTask(100, 0.6, 1.5, 15, 500, 365, 3000, 23, 0.4)
    assert r.avg_time == 23  # check init/getter
    r.avg_time = 15345
    assert r.avg_time == 15345  # check setter
    assert r.user_device_res.quantity == r.users_hours


def test_avg_data():
    """Test getter/setter and child updates for property avg_data"""
    r = RunTask(100, 0.6, 1.5, 15, 500, 365, 3000, 23, 0.4)
    assert r.avg_data == 0.4  # check init/getter
    r.avg_data = 1.24
    assert r.avg_data == 1.24  # check setter
    assert r.hosting_task.network_resource.quantity == r.users_data


def test_users_hours():
    """Test computation for user_hours property and its update"""
    r = RunTask(100, 0.6, 1.5, 15, 500, 365, 3000, 23, 0.4)
    assert r.users_hours == (23 / 60) * 3000 * 365  # check init computation
    r.avg_time = 32
    assert r.users_hours == (32 / 60) * 3000 * 365  # check avg_time change
    r.avg_user = 1232
    assert r.users_hours == (32 / 60) * 1232 * 365  # check avg_user change
    r.duration = 3
    assert r.users_hours == (32 / 60) * 1232 * 3  # check duration change


def test_users_data():
    """Test computation for user_data property and its update"""
    r = RunTask(100, 0.6, 1.5, 15, 500, 365, 3000, 23, 0.4)
    assert r.users_data == 0.4 * 3000 * 365  # check init computation
    r.avg_data = 1.7
    assert r.users_data == 1.7 * 3000 * 365  # check avg_data change
    r.avg_user = 1232
    assert r.users_data == 1.7 * 1232 * 365  # check avg_user change
    r.duration = 3
    assert r.users_data == 1.7 * 1232 * 3  # check duration change
