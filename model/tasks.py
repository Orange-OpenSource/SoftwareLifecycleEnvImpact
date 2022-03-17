from __future__ import annotations

from abc import ABC
from typing import Any, List

from model.resources import (
    PeopleResource,
    ComputeResource,
    Resource,
    StorageResource,
    NetworkResource,
    UserDeviceResource,
)


class Task(ABC):
    """
    Define a Task/Phase as a node containing an ImpactSource and/or Subtask(s)
    """

    def __init__(self, name, resources: List[Resource] = None, subtasks: List[Task] = None):  # type: ignore
        self.name = name
        if resources is None:
            resources = []
        if subtasks is None:
            subtasks = []
        self.subtasks = subtasks
        self.resources = resources

    def get_impact(self) -> float:
        """
        Compute and return the impact of the task and those of the subtasks
        :return: co2 impact of task and subtasks
        """
        return sum(r.get_co2_impact() for r in self.resources) + sum(
            s.get_impact() for s in self.subtasks
        )

    def get_impact_by_task(self) -> dict[str, float | list[None] | Any]:
        """
        Function traversing the tree to retrieve all the impacts for the jupyter notebook
        :return: for each node the name, the associated co2 and the same thing for each  of its subtasks
        """
        return {
            "name": self.name,
            "co2e": self.get_impact(),
            "subtasks": [s.get_impact_by_task() for s in self.subtasks],
        }


class BuildTask(Task):
    """
    Build task, containing implementation (dev, design) specification and requirements, management
    """

    def __init__(
        self, dev_days: int, design_days: int, spec_days: int, management_days: int
    ):
        self.implementation_task = ImplementationTask(dev_days, design_days)
        self.spec_task = SpecTask(spec_days)
        self.management_task = ManagementTask(management_days)

        super().__init__(
            "Build",
            subtasks=[self.implementation_task, self.spec_task, self.management_task],
        )


class DevTask(Task):
    """
    Development task, containing man-days
    """

    def __init__(self, dev_days: int):
        self.people_resource = PeopleResource(dev_days)
        super().__init__("Development", resources=[self.people_resource])


class DesignTask(Task):
    """
    Design task containing man-days
    """

    def __init__(self, design_days: int):
        self.people_resource = PeopleResource(design_days)
        super().__init__("Design", resources=[self.people_resource])


class HostingTask(Task):
    """
    Hosting task representing datacenter (storage and compute) and network
    """

    def __init__(
        self,
        electricity_mix: float,
        pue: float,
        servers_count: int,
        storage_tb: int,
        network_gb: float,
        duration_days: int,
    ):
        self._pue = pue
        self._servers_count = servers_count
        self._storage_tb = storage_tb
        self._duration_days = duration_days
        self._electricity_mix = electricity_mix
        self.compute_resource = ComputeResource(
            self._electricity_mix, self.pue, self.server_days
        )  # TODO update server_days
        self.storage_resource = StorageResource(
            electricity_mix, pue, self.storage_days  # TODO update storage_days
        )

        self.network_resource = NetworkResource(network_gb)
        super().__init__(
            "Hosting",
            resources=[
                self.compute_resource,
                self.storage_resource,
                self.network_resource,
            ],
        )

    @property
    def server_days(self):
        """Server days reserved by the application as number reserved * duration in days"""
        return self._servers_count * self.duration_days

    @property
    def storage_days(self):
        """Storage days reserved by the application as tb reserved * duration in days"""
        return self._storage_tb * self.duration_days

    @property
    def pue(self):
        """Power Usage Effectiveness of the DC"""
        return self._pue

    @pue.setter
    def pue(self, pue: float):
        """
        Power usage effectiveness of the DC
        :param pue: the pue
        :return: None
        """
        self._pue = pue
        self.compute_resource.server_impact.pue = pue  # TODO remove
        self.storage_resource.storage_impact.pue = pue  # TODO remove

    @property
    def electricity_mix(self):
        """Electricity mix CO2e emissions of the DC"""
        return self._electricity_mix

    @electricity_mix.setter
    def electricity_mix(self, electricity_mix: float):
        self._electricity_mix = electricity_mix
        self.compute_resource.server_impact.pue = electricity_mix  # TODO remove
        self.storage_resource.storage_impact.pue = electricity_mix  # TODO remove

    @property
    def duration_days(self):
        """Days of the phase"""
        return self._duration_days

    @duration_days.setter
    def duration_days(self, duration_days: int):
        """
        Setter for the phase run duration as days
        :param duration_days: run duration as days
        :return: None
        """
        self._duration_days = duration_days
        self.compute_resource.quantity = self.server_days
        self.storage_resource.quantity = self.storage_days


class ImplementationTask(Task):
    """
    Implementation task containing development and design
    """

    def __init__(self, dev_days: int, design_days: int):
        self.dev_task = DevTask(dev_days)
        self.design_task = DesignTask(design_days)
        super().__init__("Implementation", subtasks=[self.dev_task, self.design_task])


class ManagementTask(Task):
    """
    Management task, containing man-days
    """

    def __init__(self, management_days: int):
        self.people_resource = PeopleResource(management_days)
        super().__init__("Management", resources=[self.people_resource])


class MaintenanceTask(Task):
    """
    Maintenance task, containing man-days
    """

    def __init__(self, maintenance_days: int):
        self.people_resource = PeopleResource(maintenance_days)
        super().__init__("Maintenance", resources=[self.people_resource])


class RunTask(Task):
    """
    Run  task including Maintenance and hosting task
    Also includes user device resources/impact
    """

    def __init__(
        self,
        maintenance_days: int,
        electricity_mix: float,
        pue: float,
        servers_count: int,
        storage_tb: int,
        duration_days: int,
        avg_user_day: int,
        avg_user_minutes: int,
        avg_user_data: float,
    ):

        self.avg_user_day = avg_user_day
        self.avg_user_minutes = avg_user_minutes
        self.avg_user_data = avg_user_data
        self.duration_days = duration_days  # TODO make as property
        self.storage_tb = storage_tb  # TODO make as a property

        self.maintenance_task = MaintenanceTask(maintenance_days)
        self.hosting_task = HostingTask(
            electricity_mix,
            pue,
            servers_count,
            storage_tb,
            self.users_data,
            duration_days,
        )

        self.user_device_res = UserDeviceResource(self.users_hours)

        super().__init__(
            "Run",
            resources=[self.user_device_res],
            subtasks=[self.maintenance_task, self.hosting_task],
        )

    @property
    def users_hours(self):
        """Hours users spend on the app during the entire phase"""
        return (self.avg_user_minutes / 60) * self.avg_user_day * self.duration_days

    @property
    def users_data(self):
        """Data transfer induced byt the app usage during the entire phase"""
        return self.avg_user_data * self.avg_user_day * self.duration_days


class SpecTask(Task):
    """
    Specification and requirements task, containing man-days
    """

    def __init__(self, spec_days: int):
        self.people_resource = PeopleResource(spec_days)
        super().__init__(
            "Specifications and requirements", resources=[self.people_resource]
        )


class StandardProjectTask(Task):
    """
    Root task of a standard project, with the structure:
    Build: Dev, design, spec, management
    Run: Maintenance, users, servers, storage, network
    """

    def __init__(
        self,
        dev_days: int,
        design_days: int,
        spec_days: int,
        management_days: int,
        maintenance_days: int,
        electricity_mix: float,
        pue: float,
        servers_count: int,
        storage_tb: int,
        run_duration: int,
        avg_user_day: int,
        avg_user_minutes: int,
        avg_user_data: int,
    ):
        self.build_task = BuildTask(dev_days, design_days, spec_days, management_days)
        self.run_task = RunTask(
            maintenance_days,
            electricity_mix,
            pue,
            servers_count,
            storage_tb,
            run_duration,
            avg_user_day,
            avg_user_minutes,
            avg_user_data,
        )
        super().__init__("Standard project", subtasks=[self.build_task, self.run_task])
