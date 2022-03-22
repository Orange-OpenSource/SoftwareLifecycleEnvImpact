from abc import ABC, abstractmethod
from typing import List

from model.impact_sources import (
    DeviceImpact,
    ImpactsList,
    ImpactSource,
    NetworkImpact,
    OfficeImpact,
    ServerImpact,
    StorageImpact,
    TransportImpact,
)

ResourceName = str
ResourcesList = dict[ResourceName, ImpactsList]


class Resource(ABC):
    """
    Abstract definition of a resource, with a quantity and one or multiple ImpactSource
    Should not be directly instantiated
    """

    def __init__(self, name: str, impacts: List[ImpactSource]):
        self.name = name
        self.impacts = impacts

    @property
    @abstractmethod
    def quantity(self) -> float:
        """Quantity consumed by the resource, define by implementations"""

    def get_co2_impact(self) -> float:
        """
        Compute and return the co2-equivalent impact associated to the given quantity
        :return: the impact
        """
        co2 = 0.0
        for impact in self.impacts:
            co2 += self.quantity * impact.co2
        return co2

    def get_impacts(self) -> ImpactsList:
        """
        Return all resource impact as an ImpactsLists
        :return: ImpactsList with all ImpactKind used by the resource
        """
        return {"CO2": self.get_co2_impact()}

    def add_to_list(self, resource_list: ResourcesList) -> ResourcesList:
        """
        Append a resource to a resource list if not in it, else append/add each of its impacts
        :param resource_list: the resource list to complete
        :return: resource list with the new resource added
        """

        if self.name in resource_list:
            new_impacts = self.get_impacts()
            for impact in new_impacts:
                if (
                    impact in resource_list[self.name]
                ):  # impact already in the list, add to it
                    resource_list[self.name][impact] += new_impacts[impact]
                else:
                    resource_list[self.name][impact] = new_impacts[
                        impact
                    ]  # impact not in the list, create it
        else:
            resource_list[self.name] = self.get_impacts()  # res not in the list

        return resource_list


class ComputeResource(Resource):
    """
    Computing resource, server days as quantity and servers as impact
    """

    def __init__(
            self, electricity_mix: float, pue: float, servers_count: int, duration: int
    ):
        self.servers_count = servers_count
        self.duration = duration
        self.server_impact = ServerImpact(electricity_mix, pue)
        super().__init__("Compute", impacts=[self.server_impact])

    @property
    def quantity(self) -> int:
        """Server days reserved by the application as number reserved * duration in days"""
        return self.servers_count * self.duration


class StorageResource(Resource):
    """
    Storage _resources, tb * duration as input, disks lifecycle as impact
    """

    def __init__(
        self, electricity_mix: float, pue: float, storage_size: int, duration: int
    ):
        self.storage_size = storage_size
        self.duration = duration
        self.storage_impact = StorageImpact(electricity_mix, pue)
        super().__init__("Storage", impacts=[self.storage_impact])

    @property
    def quantity(self) -> int:
        """Storage days reserved by the application as tb reserved * duration in days"""
        return self.storage_size * self.duration


class PeopleResource(Resource):
    """
    People _resources, man days as inputs, commuting and offices as impacts
    """

    def __init__(self, man_days: int) -> None:
        self._quantity = man_days
        self.office_impact = OfficeImpact()
        self.transport_impact = TransportImpact()
        super().__init__("People", [self.office_impact, self.transport_impact])

    @property
    def quantity(self) -> int:
        """Man-days as quantity"""
        return self._quantity

    @quantity.setter
    def quantity(self, man_days: int) -> None:
        self._quantity = man_days


class UserDeviceResource(Resource):
    """
    User devices _resources, hours as inputs and devices lifecycle as impacts
    """

    def __init__(self, avg_user: int, avg_time: int, duration: int) -> None:
        self.avg_user = avg_user
        self.avg_time = avg_time
        self.duration = duration

        self.device_source = DeviceImpact()
        super().__init__("UserDevice", [self.device_source])

    @property
    def quantity(self) -> float:
        """Hours users spend on the app during the entire phase"""
        return (self.avg_time / 60) * self.avg_user * self.duration


class NetworkResource(Resource):
    """
    Network resource, gb transferred as quantity and network as impact
    """

    def __init__(self, avg_user: int, avg_data: float, duration: int) -> None:
        self.avg_user = avg_user
        self.avg_data = avg_data
        self.duration = duration

        self._network_impact = NetworkImpact()
        super().__init__("Network", [self._network_impact])

    @property
    def quantity(self) -> float:
        """Data transfer induced byt the app usage during the entire phase"""
        return self.avg_data * self.avg_user * self.duration
