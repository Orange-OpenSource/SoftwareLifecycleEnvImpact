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

    def __init__(self, quantity: float, impacts: List[ImpactSource]) -> None:
        self.quantity: float = quantity
        self.impacts = impacts

    def _set_quantity(self, quantity: float) -> None:
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
    Computing resource, hours as quantity and servers as impact
    """

    def __init__(self, electricity_mix: float, pue: float, hours: int) -> None:
        self.server_impact = ServerImpact(electricity_mix, pue)
        super().__init__(hours, impacts=[self.server_impact])

    def get_co2_impact(self) -> float:
        return self.server_impact.co2 * self.quantity

    def set_electricity_mix(self, electricity_mix: float) -> None:
        """
        Setter for electricity-mix co2e emissions used by application devices/datacenters
        :param electricity_mix: The mix
        :return: None
        """
        self.server_impact.set_electricity_mix(electricity_mix)

    def set_pue(self, pue: float) -> None:
        """
        Setter for the power usage effectiveness of the DC
        :param pue: the pue
        :return: None
        """
        self.server_impact.set_pue(pue)

    def set_server_hours(self, server_hours: float):
        """
        Setter for server hours reserved by the application
        :param server_hours: server hours reserved by the app
        :return: None
        """
        self.quantity = server_hours


class NetworkResource(Resource):
    """
    Network resource, gb transferred as quantity and network as impact
    """

    def __init__(self, network_gb: int) -> None:
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

    def __init__(self, man_days: int) -> None:
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
    Storage resources, hours as input, disks lifecycle as impact
    """

    def __init__(
        self, electricity_mix: float, pue: float, storage_tb: int, days_reserved: int
    ) -> None:
        self.storage_impact = StorageImpact(electricity_mix, pue)
        self.storage_tb = storage_tb
        self.days_reserved = days_reserved
        super().__init__(self._compute_quantity(), impacts=[self.storage_impact])

    def get_co2_impact(self) -> float:
        return self.storage_impact.co2 * self.quantity

    def _compute_quantity(self):
        return self.days_reserved * self.storage_tb

    def set_duration(self, days_reserved: int) -> None:
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


class UserDeviceResource(Resource):
    """
    User devices resources, hours as inputs and devices lifecycle as impacts
    """

    def __init__(self, user_hours: int) -> None:
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
