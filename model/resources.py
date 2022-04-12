from abc import ABC, abstractmethod
from typing import Any, List

from pint import Quantity

from model.impacts.impact_factors import (
    ImpactFactor,
    NetworkImpact,
    OfficeImpact,
    ServerImpact,
    StorageImpact,
    TransportImpact,
    UserDeviceImpact,
)
from model.impacts.impacts import ImpactIndicator, ImpactsList, merge_impacts_lists
from model.quantities import Q_

ResourceName = str

ResourcesList = dict[ResourceName, ImpactsList]


def merge_resource_list(
    first_list: ResourcesList, second_list: ResourcesList
) -> ResourcesList:
    """
    Merge two list of Resource, adding them if they are in each list or merge them
    :param first_list: first list to merge
    :param second_list: second list to merge with
    :return: a new list containing the parameters merged
    """

    result = {**first_list, **second_list}
    for resource_name, _ in result.items():
        if resource_name in first_list and resource_name in second_list:
            result[resource_name] = merge_impacts_lists(
                first_list[resource_name], second_list[resource_name]
            )
    return result


class Resource(ABC):

    """
    Abstract definition of a resource, with a quantity and one or multiple ImpactFactor
    Should not be directly instantiated
    """

    def __init__(self, name: ResourceName, impacts: List[ImpactFactor]):
        """
        Should only be used by implementations, define the name and impacts_sources of the resource
        :param name: name of the resource
        :param impacts: list of resource ImpactSources
        """
        self.name = name
        self._impacts = impacts

    @property
    @abstractmethod
    def quantity(self) -> float:
        """
        Quantity consumed by the resource, define by implementations
        :return: implementation quantity
        """

    def get_impact(self, impact_indicator: ImpactIndicator) -> Quantity[Any]:
        """
        Compute and return the corresponding indicator impact associated to the given quantity
        :return: the impact
        """
        impacts: List[Quantity[Any]] = [
            i.impacts_list[impact_indicator] * self.quantity for i in self._impacts
        ]

        return Q_(sum(impacts))

    def get_impacts(self) -> ImpactsList:
        """
        Return all impacts_list for the resource, with the format ImpactsList For each impact kind, it's multiplied by the
        resource quantity example:
        >>> self.get_impacts()
         {
            'Climate change': <Quantity(10000.123, 'kg_co2e')>,
            'Natural resources depletion': <Quantity(0, 'kg_Sbe')>,
            'Acidification': <Quantity(0,'mol_Hpos')>,
            'Fine particles': <Quantity(0, 'disease_incidence')>,
            'Ionizing radiations': <Quantity(0, 'kg_Bq_u235e')>,
            'Water depletion': <Quantity(0, 'cubic_meter')>,
            'Electronic waste': <Quantity(0, 'electronic_waste')>,
            'Primary energy consumption': <Quantity(0, 'primary_MJ')>,
            'Raw materials': <Quantity(213.3, 'tonne_mips')>
         }
        :return: ImpactsList for the resource
        """
        impacts: ImpactsList = {}

        for impact_source in self._impacts:
            impact_source_quantities = {}

            for impact_indicator in impact_source.impacts_list:
                impact_source_quantities[impact_indicator] = (
                    impact_source.impacts_list[impact_indicator] * self.quantity
                )

            impacts = merge_impacts_lists(impacts, impact_source_quantities)

        return impacts


class ComputeResource(Resource):
    """
    Computing resource, server days as quantity and servers as impact
    """

    def __init__(self, servers_count: int, duration: int):
        """
        Instantiate a ComputeResource with a ServerImpact
        :param servers_count: number of server used
        :param duration: duration of the resource as days
        """
        self.servers_count = servers_count
        self.duration = duration
        self.server_impact = ServerImpact()
        super().__init__("Compute", impacts=[self.server_impact])

    @property
    def quantity(self) -> int:
        """
        Server days reserved by the application as number reserved * duration in days
        :return: server days reserved
        """

        return self.servers_count * self.duration


class StorageResource(Resource):
    """
    Storage _resources, tb * duration as input, disks lifecycle as impact
    """

    def __init__(self, storage_size: int, duration: int):
        """
        Instantiate a storage resource with a storage impact
        :param storage_size: terabytes reserved
        :param duration: duration of the resource as days
        """
        self.storage_size = storage_size
        self.duration = duration
        self.storage_impact = StorageImpact()
        super().__init__("Storage", impacts=[self.storage_impact])

    @property
    def quantity(self) -> int:
        """
        Storage days reserved by the application as tb reserved * duration in days
        :return: storage days reserved
        """
        return self.storage_size * self.duration


class PeopleResource(Resource):
    """
    People _resources, man days as inputs, commuting and offices as _impacts
    """

    def __init__(self, man_days: int) -> None:
        """
        Instantiate a PeopleResource with offices and transports impacts_sources
        :param man_days: man days as quantity
        """
        self._quantity = man_days
        self.office_impact = OfficeImpact()
        self.transport_impact = TransportImpact()
        super().__init__("People", [self.office_impact, self.transport_impact])

    @property
    def quantity(self) -> int:
        """
        Resource quantity as man days
        :return: man days
        """
        return self._quantity

    @quantity.setter
    def quantity(self, man_days: int) -> None:
        self._quantity = man_days


class UserDeviceResource(Resource):
    """
    User devices _resources, hours as inputs and devices lifecycle as _impacts
    """

    def __init__(self, avg_user: int, avg_time: int, duration: int) -> None:
        """
        Instantiate a UserDeviceResource with device as impact
        :param avg_user: average user per day
        :param avg_time: average time spent by user on the app per day
        :param duration: number of day
        """
        self.avg_user = avg_user
        self.avg_time = avg_time
        self.duration = duration

        self.device_source = UserDeviceImpact()
        super().__init__("UserDevice", [self.device_source])

    @property
    def quantity(self) -> float:
        """
        Hours-equivalent users spend on the app during the entire phase
        :return: total hours spent by users on app
        """
        return (self.avg_time / 60) * self.avg_user * self.duration


class NetworkResource(Resource):
    """
    Network resource, gb transferred as quantity and network as impact
    """

    def __init__(self, avg_user: int, avg_data: float, duration: int) -> None:
        """
        Instantiate a NetworkResource with network as impact
        :param avg_user: average user per day
        :param avg_data: average data transferred by user on the app per day
        :param duration: number of day
        """
        self.avg_user = avg_user
        self.avg_data = avg_data
        self.duration = duration

        self._network_impact = NetworkImpact()
        super().__init__("Network", [self._network_impact])

    @property
    def quantity(self) -> float:
        """
        Total gigabytes transferred by all users during the duration
        :return: total gigabytes transferred
        """
        return self.avg_data * self.avg_user * self.duration
