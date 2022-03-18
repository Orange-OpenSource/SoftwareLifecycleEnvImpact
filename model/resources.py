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


class Resource:
    """
    Define a resource, with a quantity and one or multiple ImpactSource
    """

    def __init__(self, quantity: float, impacts: List[ImpactSource]):
        self.quantity = quantity
        self.impacts = impacts

    def get_co2_impact(self) -> float:
        """
        Compute and return the co2-equivalent impact associated to the given quantity
        :return: the impact
        """
        co2 = 0.0
        for impact in self.impacts:
            co2 += self.quantity * impact.co2
        return co2


class ComputeResource(Resource):
    """
    Computing resource, server days as quantity and servers as impact
    """

    def __init__(self, electricity_mix: float, pue: float, server_days: int):
        self.server_impact = ServerImpact(electricity_mix, pue)
        super().__init__(server_days, impacts=[self.server_impact])


class StorageResource(Resource):
    """
    Storage resources, tb * duration as input, disks lifecycle as impact
    """

    def __init__(self, electricity_mix: float, pue: float, tb_days: float):
        self.storage_impact = StorageImpact(electricity_mix, pue)
        super().__init__(tb_days, impacts=[self.storage_impact])


class NetworkResource(Resource):
    """
    Network resource, gb transferred as quantity and network as impact
    """

    def __init__(self, network_gb: float):
        self.network_impact = NetworkImpact()
        super().__init__(network_gb, impacts=[self.network_impact])


class PeopleResource(Resource):
    """
    People resources, man days as inputs, commuting and offices as impacts
    """

    def __init__(self, man_days: int):
        self.office_impact = OfficeImpact()
        self.transport_impact = TransportImpact()
        super().__init__(man_days, [self.office_impact, self.transport_impact])


class UserDeviceResource(Resource):
    """
    User devices resources, hours as inputs and devices lifecycle as impacts
    """

    def __init__(self, user_hours: float):
        self.device_source = DeviceImpact()
        super().__init__(user_hours, [self.device_source])
