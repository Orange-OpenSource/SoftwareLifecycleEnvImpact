from __future__ import annotations

from abc import ABC
from typing import List

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

    def get_co2_impact(self) -> float:
        """
        Compute and return the impact of the task and those of the subtasks
        :return: co2 impact of task and subtasks
        """
        return sum(r.get_co2_impact() for r in self.resources) + sum(
            s.get_co2_impact() for s in self.subtasks
        )


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
        storage_size: int,
        network_gb: float,
        duration: int,
    ):
        self._electricity_mix = electricity_mix
        self._pue = pue
        self._servers_count = servers_count
        self._storage_size = storage_size
        self._network_gb = (network_gb,)
        self._duration = duration

        self.compute_resource = ComputeResource(
            self.electricity_mix, self.pue, self.server_days
        )
        self.storage_resource = StorageResource(
            self.electricity_mix, self.pue, self.storage_days
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
    def server_days(self) -> int:
        """Server days reserved by the application as number reserved * duration in days"""
        return self.servers_count * self.duration

    @property
    def storage_days(self) -> int:
        """Storage days reserved by the application as tb reserved * duration in days"""
        return self.storage_size * self.duration

    @property
    def servers_count(self) -> int:
        """Number of servers reserved"""
        return self._servers_count

    @servers_count.setter
    def servers_count(self, servers_count: int):
        self._servers_count = servers_count
        self.compute_resource.quantity = self.server_days

    @property
    def storage_size(self) -> int:
        """Tb reserved"""
        return self._storage_size

    @storage_size.setter
    def storage_size(self, storage_size: int):
        self._storage_size = storage_size
        self.storage_resource.quantity = self.storage_days

    @property
    def pue(self) -> float:
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
        self.compute_resource.server_impact.pue = pue
        self.storage_resource.storage_impact.pue = pue

    @property
    def electricity_mix(self) -> float:
        """Electricity mix CO2e emissions of the DC"""
        return self._electricity_mix

    @electricity_mix.setter
    def electricity_mix(self, electricity_mix: float):
        self._electricity_mix = electricity_mix
        self.compute_resource.server_impact.electricity_mix = self.electricity_mix
        self.storage_resource.storage_impact.electricity_mix = self.electricity_mix

    @property
    def duration(self) -> int:
        """Days of the phase"""
        return self._duration

    @duration.setter
    def duration(self, duration: int):
        """
        Setter for the phase run duration as days
        :param duration: run duration as days
        :return: None
        """
        self._duration = duration
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
        storage_size: int,
        duration: int,
        avg_user: int,
        avg_time: int,
        avg_data: float,
    ):

        self._duration = duration
        self._avg_user = avg_user
        self._avg_time = avg_time
        self._avg_data = avg_data
        self._storage_size = storage_size

        self.maintenance_task = MaintenanceTask(maintenance_days)
        self.hosting_task = HostingTask(
            electricity_mix,
            pue,
            servers_count,
            storage_size,
            self.users_data,
            duration,
        )

        self.user_device_res = UserDeviceResource(self.users_hours)

        super().__init__(
            "Run",
            resources=[self.user_device_res],
            subtasks=[self.maintenance_task, self.hosting_task],
        )

    @property
    def duration(self) -> int:
        """Run phase duration in days"""
        return self._duration

    @duration.setter
    def duration(self, duration: int):
        self._duration = duration
        self.hosting_task.duration = duration

    @property
    def avg_user(self) -> int:
        """Average users per day"""
        return self._avg_user

    @avg_user.setter
    def avg_user(self, avg_user: int):
        self._avg_user = avg_user
        self.user_device_res.quantity = self.users_hours
        self.hosting_task.network_resource.quantity = self.users_data

    @property
    def avg_time(self) -> int:
        """Average time per user per day"""
        return self._avg_time

    @avg_time.setter
    def avg_time(self, avg_time: int):
        self._avg_time = avg_time
        self.user_device_res.quantity = self.users_hours

    @property
    def avg_data(self) -> float:
        """Average data per user per day"""
        return self._avg_data

    @avg_data.setter
    def avg_data(self, avg_data: float):
        self._avg_data = avg_data
        self.hosting_task.network_resource.quantity = self.users_data

    @property
    def users_hours(self) -> float:
        """Hours users spend on the app during the entire phase"""
        return (self.avg_time / 60) * self.avg_user * self.duration

    @property
    def users_data(self) -> float:
        """Data transfer induced byt the app usage during the entire phase"""
        return self.avg_data * self.avg_user * self.duration


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
        storage_size: int,
        run_duration: int,
        avg_user: int,
        avg_time: int,
        avg_data: int,
    ):
        self.build_task = BuildTask(dev_days, design_days, spec_days, management_days)
        self.run_task = RunTask(
            maintenance_days,
            electricity_mix,
            pue,
            servers_count,
            storage_size,
            run_duration,
            avg_user,
            avg_time,
            avg_data,
        )
        super().__init__("Standard project", subtasks=[self.build_task, self.run_task])
