from abc import ABC, abstractmethod
from typing import List

from model.impact_sources import (
    ImpactSource,
    ServerImpact,
    NetworkImpact,
    OfficeImpact,
    TransportImpact,
    StorageImpact,
    DeviceImpact,
)


class Resource(ABC):
    """
    Define a resource, with a quantity and one or multiple ImpactSource
    """

    def __init__(self, quantity: float, impacts: List[ImpactSource]):
        self.quantity: float = quantity
        self.impacts = impacts

    def _set_quantity(self, quantity: float):
        """
        Set the resource quantity
        :param quantity: quantity of the resource
        :return: None
        """
        self.quantity = quantity

    @abstractmethod
    def get_co2_impact(self) -> float:
        """
        Compute and return the co2-equivalent impact associated to the given quantity
        :return: the impact
        """


class ComputeResource(Resource):
    """
    Computing resource, number of server * duration as quantity and servers as impact
    """

    def __init__(
        self, electricity_mix: float, pue: float, servers_count: int, duration_days: int
    ):
        self.server_impact = ServerImpact(electricity_mix, pue)
        self.servers_count = servers_count
        self.duration_days = duration_days
        super().__init__(self._compute_quantity(), impacts=[self.server_impact])

    def get_co2_impact(self) -> float:
        return self.server_impact.co2 * self.quantity

    def _compute_quantity(self):
        return self.duration_days * self.servers_count

    def set_electricity_mix(self, electricity_mix: float):
        """
        Setter for electricity-mix co2e emissions used by application devices/datacenters
        :param electricity_mix: The mix
        :return: None
        """
        self.server_impact.set_electricity_mix(electricity_mix)

    def set_pue(self, pue: float):
        """
        Setter for the power usage effectiveness of the DC
        :param pue: the pue
        :return: None
        """
        self.server_impact.set_pue(pue)

    def set_servers_count(self, servers_count: int):
        """
        Setter for server quantity reserved by the application
        :param servers_count: servers reserved by the app
        :return: None
        """
        self.servers_count = servers_count
        self.quantity = self._compute_quantity()

    def set_duration(self, duration_days: int):
        """
        Setter for the days used, update quantity
        :param duration_days: days reserved
        :return: None
        """
        self.duration_days = duration_days
        self.quantity = self._compute_quantity()


class NetworkResource(Resource):
    """
    Network resource, gb transferred as quantity and network as impact
    """

    def __init__(self, network_gb: int):
        self.network_impact = NetworkImpact()
        super().__init__(network_gb, impacts=[self.network_impact])

    def get_co2_impact(self) -> float:
        return self.network_impact.co2 * self.quantity

    def set_gb(self, network_gb: int):
        """
        Set resource quantity as gb transferred
        :param network_gb: gb transferred
        :return: None
        """
        self.quantity = network_gb


class PeopleResource(Resource):
    """
    People resources, man days as inputs, commuting and offices as impacts
    """

    def __init__(self, man_days: int):
        self.office_impact = OfficeImpact()
        self.transport_impact = TransportImpact()
        super().__init__(man_days, [self.office_impact, self.transport_impact])

    def get_co2_impact(self) -> float:
        return (
            self.quantity * self.office_impact.co2
            + self.quantity * self.transport_impact.co2
        )

    def set_man_days(self, man_days: int):
        """
        Setter for resource quantity as man-days
        :param man_days: man days for resource
        :return: None
        """
        self.quantity = man_days


class StorageResource(Resource):
    """
    Storage resources, tb * duration as input, disks lifecycle as impact
    """

    def __init__(
        self, electricity_mix: float, pue: float, storage_tb: int, days_reserved: int
    ):
        self.storage_impact = StorageImpact(electricity_mix, pue)
        self.storage_tb = storage_tb
        self.days_reserved = days_reserved
        super().__init__(self._compute_quantity(), impacts=[self.storage_impact])

    def get_co2_impact(self) -> float:
        return self.storage_impact.co2 * self.quantity

    def _compute_quantity(self):
        return self.days_reserved * self.storage_tb

    def set_duration(self, days_reserved: int):
        """
        Setter for the days used, update quantity
        :param days_reserved: days reserved
        :return: None
        """
        self.days_reserved = days_reserved
        self.quantity = self._compute_quantity()

    def set_storage_tb(self, storage_tb):
        """
        Setter for tb reserved, update quantity
        :param storage_tb: tb reserved
        :return: None
        """
        self.storage_tb = storage_tb
        self.quantity = self._compute_quantity()

    def set_electricity_mix(self, electricity_mix: float):
        """
        Setter for electricity-mix co2e emissions used by application devices/datacenters
        :param electricity_mix: The mix
        :return: None
        """
        self.storage_impact.set_electricity_mix(electricity_mix)

    def set_pue(self, pue: float):
        """
        Setter for the power usage effectiveness of the DC
        :param pue: the pue
        :return: None
        """
        self.storage_impact.set_pue(pue)


class UserDeviceResource(Resource):
    """
    User devices resources, hours as inputs and devices lifecycle as impacts
    """

    def __init__(self, user_hours: int):
        self.device_source = DeviceImpact()
        super().__init__(user_hours, [self.device_source])

    def get_co2_impact(self) -> float:
        return self.device_source.co2 * self.quantity

    def set_user_hours(self, user_hours: int):
        """
        Setter for user hours as resource quantity
        :param user_hours: users spend by users on app
        :return: None
        """
        self.quantity = user_hours
