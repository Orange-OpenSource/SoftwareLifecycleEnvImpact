from __future__ import annotations

from abc import ABC
from typing import Any, List, Union

from model.resources import (
    ComputeResource,
    NetworkResource,
    PeopleResource,
    Resource,
    ResourcesList,
    StorageResource,
    UserDeviceResource,
)

TaskImpact = dict[str, Union[str, float, Any]]


class Task(ABC):
    """
    Define a Task/Phase as a node containing an ImpactSource and/or Subtask(s)
    """

    def __init__(self, name, resources: List[Resource] = None, subtasks: List[Task] = None):  # type: ignore
        """
        Define a task with a name, resources and subtasks
        :param name: the name of the resource
        :param resources: optional list of resources
        :param subtasks: optional list of subtasks
        """
        self.name = name
        if resources is None:
            resources = []
        if subtasks is None:
            subtasks = []
        self._subtasks = subtasks
        self._resources = resources

    def get_co2_impact(self) -> float:
        """
        Return the computed co2 of this task resources, and those of its subtasks
        :return: complete co2 of task + its subtasks
        """
        return sum(r.get_co2_impact() for r in self._resources) + sum(
            s.get_co2_impact() for s in self._subtasks
        )

    def get_impact(self) -> TaskImpact:
        """
        All impacts of the task, and those of its subtasks

        :return: impacts of task and subtasks with format TaskImpact

        Example:
                {
                    "name": xxx
                    "CO2": xxx
                    "subtasks": {
                        "name": xxx
                        "CO2": xxx
                        "subtasks": }
                }
        }
        """
        return {
            "name": self.name,
            "CO2": self.get_co2_impact(),
            "subtasks": [r.get_impact() for r in self._subtasks],
        }

    def get_impact_by_resource(self, resources: ResourcesList = None) -> ResourcesList:  # type: ignore
        """
        Return all _impacts grouped by resource type, int the format of ResourcesList:

         {'People': {'CO2': 2000.0}}
         {'Build': {'CO2': 234325.0}}

        :param resources: Optional ResourceList to add to
        :return: ResourceList containing resources for this task + those passed as parameter
        """
        if resources is None:
            resources = {}

        for r in self._resources:
            resources = r.add_to_list(resources)

        for s in self._subtasks:
            s.get_impact_by_resource(resources)

        return resources


class BuildTask(Task):
    """
    Build task, containing implementation (dev, design) specification and requirements, management
    """

    def __init__(
            self, dev_days: int, design_days: int, spec_days: int, management_days: int
    ):
        """
        Define a build task with an implementation, spec and management subtasks
        :param dev_days: development man days
        :param design_days: design man days
        :param spec_days: specifications man days
        :param management_days: management man days
        """
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
        """
        Development task with people resources as impact and development days as quantity
        :param dev_days: development man days
        """
        self._people_resource = PeopleResource(dev_days)
        super().__init__("Development", resources=[self._people_resource])

    @property
    def dev_days(self) -> int:
        """
        Define development resource quantity as man-days
        :return: development man days
        """
        return self._people_resource.quantity

    @dev_days.setter
    def dev_days(self, dev_days: int) -> None:
        self._people_resource.quantity = dev_days


class DesignTask(Task):
    """
    Design task containing man-days
    """

    def __init__(self, design_days: int):
        """
        Design task with people resources as impact and design days as quantity
        :param design_days: design man days
        """
        self._people_resource = PeopleResource(design_days)
        super().__init__("Design", resources=[self._people_resource])

    @property
    def design_days(self) -> int:
        """
        Define design resource quantity as man-days
        :return: design man days
        """
        return self._people_resource.quantity

    @design_days.setter
    def design_days(self, dev_days: int) -> None:
        self._people_resource.quantity = dev_days


class SpecTask(Task):
    """
    Specification and requirements task, containing man-days
    """

    def __init__(self, spec_days: int):
        """
        Spec task with people resources as impact and spec days as quantity
        :param spec_days: spec man days
        """
        self._people_resource = PeopleResource(spec_days)
        super().__init__(
            "Specifications and requirements", resources=[self._people_resource]
        )

    @property
    def spec_days(self) -> int:
        """
        Define specification resource quantity as man-days
        :return: Specifications man days
        """
        return self._people_resource.quantity

    @spec_days.setter
    def spec_days(self, spec_days: int) -> None:
        self._people_resource.quantity = spec_days


class ImplementationTask(Task):
    """
    Implementation task containing development and design
    """

    def __init__(self, dev_days: int, design_days: int):
        """
        Define ImplementationTask regrouping development and design
        :param dev_days: development man days
        :param design_days: design man days
        """
        self.dev_task = DevTask(dev_days)
        self.design_task = DesignTask(design_days)
        super().__init__("Implementation", subtasks=[self.dev_task, self.design_task])


class ManagementTask(Task):
    """
    Management task, containing man-days
    """

    def __init__(self, management_days: int):
        """
        Management task with people resources as impact and management days as quantity
        :param management_days: Management man days
        """
        self._people_resource = PeopleResource(management_days)
        super().__init__("Management", resources=[self._people_resource])

    @property
    def management_days(self) -> int:
        """
        Define management resource quantity as man-days
        :return: Management man days
        """
        return self._people_resource.quantity

    @management_days.setter
    def management_days(self, management_days: int) -> None:
        self._people_resource.quantity = management_days


class MaintenanceTask(Task):
    """
    Maintenance task, containing man-days
    """

    def __init__(self, maintenance_days: int):
        """
        Maintenance task with people resources as impact and maintenance days as quantity
        :param maintenance_days: Maintenance man days
        """
        self._people_resource = PeopleResource(maintenance_days)
        super().__init__("Maintenance", resources=[self._people_resource])

    @property
    def maintenance_days(self) -> int:
        """
        Define maintenance resource quantity as man-days
        :return: Maintenance man days
        """
        return self._people_resource.quantity

    @maintenance_days.setter
    def maintenance_days(self, maintenance_days: int) -> None:
        self._people_resource.quantity = maintenance_days


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
            duration: int,
    ):
        """
        Hosting task with Compute, Storage resources as impacts
        :param electricity_mix: dc electricity mix
        :param pue: dc power usage effectiveness
        :param servers_count: number of server used
        :param storage_size: terabytes reserved
        :param duration: duration of the phase
        """
        self._compute_resource = ComputeResource(
            electricity_mix, pue, servers_count, duration
        )
        self._storage_resource = StorageResource(
            electricity_mix, pue, storage_size, duration
        )

        super().__init__(
            "Hosting",
            resources=[
                self._compute_resource,
                self._storage_resource,
            ],
        )

    @property
    def servers_count(self) -> int:
        """
        NUmber of server reserved
        :return: server reserved quantity
        """
        return self._compute_resource.servers_count

    @servers_count.setter
    def servers_count(self, servers_count: int) -> None:
        self._compute_resource.servers_count = servers_count

    @property
    def storage_size(self) -> int:
        """
        Terabytes reserved
        :return: tb reserved
        """
        return self._storage_resource.storage_size

    @storage_size.setter
    def storage_size(self, storage_size: int) -> None:
        self._storage_resource.storage_size = storage_size

    @property
    def pue(self) -> float:
        """
        Power usage effectiveness of the datacenter
        :return: PUE of the DC
        """
        return self._compute_resource.server_impact.pue

    @pue.setter
    def pue(self, pue: float) -> None:
        self._compute_resource.server_impact.pue = pue
        self._storage_resource.storage_impact.pue = pue

    @property
    def electricity_mix(self) -> float:
        """
        Electricity mix of the dc
        :return: eectricity mix float
        """
        return self._compute_resource.server_impact.electricity_mix

    @electricity_mix.setter
    def electricity_mix(self, electricity_mix: float) -> None:
        self._compute_resource.server_impact.electricity_mix = electricity_mix
        self._storage_resource.storage_impact.electricity_mix = electricity_mix

    @property
    def duration(self) -> int:
        """
        Duration of the phase as days
        :return: days of the phase
        """
        return self._compute_resource.duration

    @duration.setter
    def duration(self, duration: int) -> None:
        self._compute_resource.duration = duration
        self._storage_resource.duration = duration


class UsageTask(Task):
    """
    Usage task representing network and devices use by the users
    """

    def __init__(self, avg_user: int, avg_time: int, avg_data: float, duration: int):
        """
        UsageTask with user devices and networks as resources
        :param avg_user: avg user per day
        :param avg_time: avg time spent by user per day
        :param avg_data: avg data transferred by user per day
        :param duration: task duration in days
        """
        self._user_device_res = UserDeviceResource(avg_user, avg_time, duration)
        self._network_resource = NetworkResource(avg_user, avg_data, duration)

        super().__init__(
            "Usage", resources=[self._user_device_res, self._network_resource]
        )

    @property
    def avg_user(self) -> int:
        """
        Average user each day
        :return: avg user per day
        """
        return self._user_device_res.avg_user

    @avg_user.setter
    def avg_user(self, avg_user: int) -> None:
        self._user_device_res.avg_user = avg_user
        self._network_resource.avg_user = avg_user

    @property
    def duration(self) -> int:
        """
        Phase duration
        :return: duration in days
        """
        return self._user_device_res.duration

    @duration.setter
    def duration(self, duration: int) -> None:
        self._user_device_res.duration = duration
        self._network_resource.duration = duration

    @property
    def avg_time(self) -> int:
        """
        Average time spent by one user per day
        :return: avg time as minutes
        """
        return self._user_device_res.avg_time

    @avg_time.setter
    def avg_time(self, avg_time: int) -> None:
        self._user_device_res.avg_time = avg_time

    @property
    def avg_data(self) -> float:
        """
        Average data transferred by user per day
        :return: gb transferred per day
        """
        return self._network_resource.avg_data

    @avg_data.setter
    def avg_data(self, avg_data: float) -> None:
        self._network_resource.avg_data = avg_data


class RunTask(Task):
    """
    Run  task including Maintenance and hosting task
    Also includes user device _resources/impact
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
        self.maintenance_task = MaintenanceTask(maintenance_days)
        self.hosting_task = HostingTask(
            electricity_mix,
            pue,
            servers_count,
            storage_size,
            duration,
        )
        self.usage_task = UsageTask(avg_user, avg_time, avg_data, duration)

        super().__init__(
            "Run",
            subtasks=[self.maintenance_task, self.hosting_task, self.usage_task],
        )

    @property
    def duration(self) -> int:
        """
        Phase duration in days
        :return: duration in days
        """
        return self.hosting_task.duration

    @duration.setter
    def duration(self, duration: int) -> None:
        self.hosting_task.duration = duration
        self.usage_task.duration = duration


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
