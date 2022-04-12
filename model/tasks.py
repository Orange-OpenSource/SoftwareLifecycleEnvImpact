from __future__ import annotations

from abc import ABC
from typing import Any, List, Union

from pint import Quantity

from model.impacts.impacts import ImpactIndicator, ImpactsList, merge_impacts_lists
from model.quantities import Q_
from model.resources import (
    ComputeResource,
    merge_resource_list,
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
    Define a Task/Phase as a node containing an ImpactFactor and/or Subtask(s)
    """

    def __init__(self, name: str, resources: List[Resource] = None, subtasks: List[Task] = None):  # type: ignore
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

    def get_impacts(self) -> TaskImpact:
        """
        Return a task impact for this one and its children
        :return: TaskImpact with name, impact sources and subtasks
        """
        return {
            "name": self.name,
            "impacts": self.get_impacts_list(),
            "subtasks": [r.get_impacts() for r in self._subtasks],
        }

    def get_impacts_list(self) -> ImpactsList:
        """
        Return the task impacts_list as an ImpactsList

        :return: an ImpactsList for this task impacts_list
        """
        impacts: ImpactsList = {}

        for r in self._resources:
            impacts = merge_impacts_lists(impacts, r.get_impacts())

        for s in self._subtasks:
            impacts = merge_impacts_lists(impacts, s.get_impacts_list())

        return impacts

    def get_impact_by_resource(self) -> ResourcesList:
        """
        Return all _impacts grouped by resource type, int the format of ResourcesList:

         {'People': {'CO2': 2000.0}}
         {'Build': {'CO2': 234325.0}}
        :return: ResourceList containing resources for this task
        """
        resource_list: ResourcesList = {}

        for r in self._resources:
            resource_list = merge_resource_list(
                resource_list, {r.name: r.get_impacts()}
            )

        for s in self._subtasks:
            resource_list = merge_resource_list(
                resource_list, s.get_impact_by_resource()
            )

        return resource_list

    def get_impact_by_indicator(self, indicator: ImpactIndicator) -> Quantity[Any]:
        """
        Return the computed impact passed as parameter of this task resources, and those of its subtasks
        :param indicator: Impact indicator
        :return: the quantity corresponding to the impact indicator
        """

        impacts_resources: List[Quantity[Any]] = [
            r.get_impact(indicator) for r in self._resources
        ]
        impacts_subtasks: List[Quantity[Any]] = [
            s.get_impact_by_indicator(indicator) for s in self._subtasks
        ]

        return Q_(sum(impacts_resources) + sum(impacts_subtasks))  # type: ignore


class BuildTask(Task):
    """
    Build task, containing implementation (dev, design) specification and requirements, management
    """

    def __init__(
        self,
        implementation_task: ImplementationTask,
        spec_task: SpecTask,
        management_task: ManagementTask,
    ):
        """
        Initialize a BuildTask with implementation, specification and management as subtasks
        :param implementation_task: Implementation subtask
        :param spec_task: Specifications subtask
        :param management_task: Management subtask
        """
        self._implementation_task = implementation_task
        self._spec_task = spec_task
        self._management_task = management_task

        super().__init__(
            "Build",
            subtasks=[
                self._implementation_task,
                self._spec_task,
                self._management_task,
            ],
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

    def __init__(self, dev_task: DevTask, design_task: DesignTask):
        """
        Initialize a ImplementationTask with development and design
        :param dev_task: Development subtask
        :param design_task: Design subtask
        """

        self._dev_task = dev_task
        self._design_task = design_task
        super().__init__("Implementation", subtasks=[self._dev_task, self._design_task])


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
        servers_count: int,
        storage_size: int,
        duration: int,
    ):
        """
        Hosting task with Compute, Storage resources as impacts_sources
        :param servers_count: number of server used
        :param storage_size: terabytes reserved
        :param duration: duration of the phase
        """
        self._compute_resource = ComputeResource(servers_count, duration)
        self._storage_resource = StorageResource(storage_size, duration)

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
        maintenance_task: MaintenanceTask,
        hosting_task: HostingTask,
        usage_task: UsageTask,
    ):
        """
        Implement a RunTask with maintenance, hosting and usage subtasks
        :param maintenance_task: Maintenance subtask
        :param hosting_task: Hosting subtask
        :param usage_task: Usage subtask
        """
        self._maintenance_task = maintenance_task

        self._hosting_task = hosting_task
        self._usage_task = usage_task

        super().__init__(
            "Run",
            subtasks=[self._maintenance_task, self._hosting_task, self._usage_task],
        )

    @property
    def duration(self) -> int:
        """
        Phase duration in days
        :return: duration in days
        """
        return self._hosting_task.duration

    @duration.setter
    def duration(self, duration: int) -> None:
        self._hosting_task.duration = duration
        self._usage_task.duration = duration


class StandardProjectTask(Task):
    """
    Root task of a standard project, with the structure:
    Build: Dev, design, spec, management
    Run: Maintenance, users, servers, storage, network
    """

    def __init__(
        self,
        build_task: BuildTask,
        run_task: RunTask,
    ):
        self._build_task = build_task
        self._run_task = run_task
        super().__init__(
            "Standard project", subtasks=[self._build_task, self._run_task]
        )
