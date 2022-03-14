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

    def set_quantity(self, quantity: float) -> None:
        """
        Set the resource quantity
        :param quantity: quantity of the resource
        :return: None
        """
        self.quantity = quantity

    @abstractmethod
    def get_impact(self) -> float:
        """
        Compute and return the impact(s) associated to the given quantity
        :return: the impact
        """


class ComputeResource(Resource):
    """
    Computing resource, hours as quantity and servers as impact
    """

    def __init__(self, hours: int) -> None:
        self.server_impact = ServerImpact()
        super().__init__(hours, impacts=[self.server_impact])

    def get_impact(self) -> float:
        return float(self.server_impact.co2 * self.quantity)  # TODO check cast


class NetworkResource(Resource):
    """
    Network resource, gb transferred as quantity and network as impact
    """

    def __init__(self, network_gb: int) -> None:
        self.network_impact = NetworkImpact()
        super().__init__(network_gb, impacts=[self.network_impact])

    def get_impact(self) -> float:
        return float(self.network_impact.co2 * self.quantity)  # TODO check cast


class PeopleResource(Resource):
    """
    People resources, man days as inputs, commuting and offices as impacts
    """

    def __init__(self, man_days: int) -> None:
        self.office_impact = OfficeImpact()
        self.transport_impact = TransportImpact()
        super().__init__(man_days, [self.office_impact, self.transport_impact])

    def get_impact(self) -> float:
        return float(
            self.quantity * self.office_impact.co2
            + self.quantity * self.transport_impact.co2
        )  # TODO km and check cast


class StorageResource(Resource):
    """
    Storage resources, hours as input, disks lifecycle as impact # TODO change the input
    """

    def __init__(self, tb_hour: int) -> None:
        self.storage_impact = StorageImpact()
        super().__init__(tb_hour, impacts=[self.storage_impact])

    def get_impact(self) -> float:
        return float(self.storage_impact.co2 * self.quantity)  # TODO check cast


class UserDeviceResource(Resource):
    """
    User devices resources, hours as inputs and devices lifecycle as impacts
    """

    def __init__(self, user_hours: int) -> None:
        self.device_source = DeviceImpact()
        super().__init__(user_hours, [self.device_source])

    def get_impact(self) -> float:
        return float(self.device_source.co2 * self.quantity)  # TODO check cast
