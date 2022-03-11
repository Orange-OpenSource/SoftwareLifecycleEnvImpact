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
    def __init__(self, quantity: float, impacts: List[ImpactSource]) -> None:
        self.quantity: float = quantity
        self.impacts = impacts

    def set_quantity(self, quantity: float) -> None:
        self.quantity = quantity

    @abstractmethod
    def get_impact(self) -> float:
        pass


class ComputeResource(Resource):
    def __init__(self, hours: int) -> None:
        self.server_impact = ServerImpact()
        super().__init__(hours, impacts=[self.server_impact])

    def get_impact(self) -> float:
        return float(self.server_impact.co2 * self.quantity)  # TODO check cast


class NetworkResource(Resource):
    def __init__(self, hours: int) -> None:
        self.network_impact = NetworkImpact()
        super().__init__(hours, impacts=[self.network_impact])

    def get_impact(self) -> float:
        return float(self.network_impact.co2 * self.quantity)  # TODO check cast


class PeopleResource(Resource):
    def __init__(self, quantity: int) -> None:
        self.office_impact = OfficeImpact()
        self.transport_impact = TransportImpact()
        super().__init__(quantity, [self.office_impact, self.transport_impact])

    def get_impact(self) -> float:
        return float(
                self.quantity * self.office_impact.co2
                + self.quantity * self.transport_impact.co2
        )  # TODO km and check cast


class StorageResource(Resource):
    def __init__(self, tb_hour: int) -> None:
        self.storage_impact = StorageImpact()
        super().__init__(tb_hour, impacts=[self.storage_impact])

    def get_impact(self) -> float:
        return float(self.storage_impact.co2 * self.quantity)  # TODO check cast


class UserDeviceResource(Resource):
    def __init__(self, user_hours: int) -> None:
        self.device_source = DeviceImpact()
        super().__init__(user_hours, [self.device_source])

    def get_impact(self) -> float:
        return float(self.device_source.co2 * self.quantity)  # TODO check cast
