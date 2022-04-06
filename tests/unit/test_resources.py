from typing import List

from model.impact_sources import ImpactSource
from model.quantities import KG_CO2E
from model.resources import (
    ComputeResource,
    NetworkResource,
    PeopleResource,
    Resource,
    ResourcesList,
    StorageResource,
    UserDeviceResource,
)


class TestResource(Resource):
    """
    Test resource implementation to fully control its quantity and ImpactSources
    """

    def __init__(self, quantity: float, impacts: List[ImpactSource]):
        self._quantity = quantity
        super().__init__("TestResource", impacts)

    @property
    def quantity(self) -> float:
        """
        For testing purpose, give direct access to quantity property
        :return: quantity as float
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity: float) -> None:
        self._quantity = quantity


############
# Resource #
############


def test_get_co2_impact() -> None:
    """
    For Resource.get_co2_impact test computation, quantity change and resource adding
    :return: None
    """
    is1 = ImpactSource(9999 * KG_CO2E)
    is2 = ImpactSource(1.123 * KG_CO2E)

    r = TestResource(1, impacts=[is1, is2])  # Impacts =  1 * 1776

    # Test ImpactSource computation
    assert r.get_co2_impact() == (9999 + 1.123) * KG_CO2E

    # Test quantity change
    r._quantity = 123
    assert r.get_co2_impact() == ((9999 + 1.123) * 123) * KG_CO2E

    # Test add impact source
    is3 = ImpactSource(432 * KG_CO2E)
    r._impacts.append(is3)
    assert r.get_co2_impact() == ((9999 + 1.123 + 432) * 123) * KG_CO2E


def test_add_to_dict() -> None:
    """
    Test Resource.add_to_list() method, by adding a new resource, an existing one, and new impact and assessing
    the value returned the corresponding ResourceList
    :return:
    """
    resource_list: ResourcesList = {
        "FirstRes": {"CO2": 234.567},
        "SecondRes": {"CO2": 999.999},
    }
    new_res = PeopleResource(1)

    # Test new one
    assert len(resource_list) == 2
    resource_list = new_res.add_to_list(resource_list)
    assert len(resource_list) == 3
    assert resource_list[new_res.name]["CO2"] == new_res.get_co2_impact().magnitude

    # Test existing one
    resource_list = new_res.add_to_list(resource_list)
    assert len(resource_list) == 3
    assert resource_list[new_res.name]["CO2"] == new_res.get_co2_impact().magnitude * 2

    # Test new impact
    # Only co2 impact for now, test here for new _impacts (water, kwh...)


###################
# ComputeResource #
###################


def test_compute_res_quantity() -> None:
    """Test quantity properties of ComputeResource and the update of its components"""
    c = ComputeResource(13, 365)
    assert c.quantity == 13 * 365  # check init/getter
    c.servers_count = 432
    assert c.quantity == 432 * 365  # check servers_count update
    c.duration = 723
    assert c.quantity == 432 * 723  # check duration update


###################
# StorageResource #
###################


def test_storage_res_quantity() -> None:
    """Test quantity properties of StorageResource and the update of its components"""
    c = StorageResource(250, 365)
    assert c.quantity == 250 * 365  # check init/getter
    c.storage_size = 34
    assert c.quantity == 34 * 365  # check storage size update
    c.duration = 2321
    assert c.quantity == 34 * 2321  # check duration update


###################
# PeopleResource #
###################


def test_man_days() -> None:
    """Test quantity properties of PeopleResource"""
    p = PeopleResource(2343)
    assert p.quantity == 2343  # check init/getter
    p.quantity = 23
    assert p.quantity == 23  # check setter


######################
# UserDeviceResource #
######################


def test_user_device_res_quantity() -> None:
    """Test quantity properties of UserDeviceResource and the update of its components"""
    u = UserDeviceResource(123, 32, 365)
    assert u.quantity == (32 / 60) * 123 * 365  # check init/getter
    u.avg_user = 532
    assert u.quantity == (32 / 60) * 532 * 365  # check avg_user change
    u.avg_time = 60
    assert u.quantity == (60 / 60) * 532 * 365  # check avg_time change
    u.duration = 700
    assert u.quantity == (60 / 60) * 532 * 700  # check duration change


###################
# NetworkResource #
###################


def test_network_res_quantity() -> None:
    """Test quantity properties of NetworkResource and the update of its components"""
    n = NetworkResource(233, 1.723, 364)
    assert n.quantity == 233 * 1.723 * 364  # check init/getter
    n.avg_user = 4322
    assert n.quantity == 4322 * 1.723 * 364  # check avg_user change
    n.avg_data = 123.2332423
    assert n.quantity == 4322 * 123.2332423 * 364  # check avg_data change
    n.duration = 7654
    assert n.quantity == 4322 * 123.2332423 * 7654  # check duration change
