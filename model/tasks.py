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
    ) -> None:
        self.implementation_task = ImplementationTask(dev_days, design_days)
        self.spec_task = SpecTask(spec_days)
        self.management_task = ManagementTask(management_days)

        super().__init__(
            "Build",
            subtasks=[self.implementation_task, self.spec_task, self.management_task],
        )

    def set_dev_days(self, dev_days: int) -> None:
        """
        Setter for development man-days
        :param dev_days: development man-days
        :return: None
        """
        self.implementation_task.set_dev_days(dev_days)

    def set_design_days(self, design_days: int) -> None:
        """
        Setter for design man-days
        :param design_days: design man-days
        :return: None
        """
        self.implementation_task.set_design_days(design_days)

    def set_spec_days(self, spec_days: int) -> None:
        """
        Setter for specification and requirements man-days
        :param spec_days: specification and requirements man-days
        :return: None
        """
        self.spec_task.set_spec_days(spec_days)

    def set_management_days(self, management_days: int) -> None:
        """
        Setter for management man-days
        :param management_days: management man-days
        :return: None
        """
        self.management_task.set_management_days(management_days)


class DevTask(Task):
    """
    Development task, containing man-days
    """

    def __init__(self, dev_days: int) -> None:
        self.people_resource = PeopleResource(dev_days)
        super().__init__("Development", resources=[self.people_resource])

    def set_dev_days(self, dev_days: int) -> None:
        """
        Setter for development man-days
        :param dev_days: development man-days
        :return: None
        """
        self.people_resource.set_man_days(dev_days)


class DesignTask(Task):
    """
    Design task containing man-days
    """

    def __init__(self, design_days: int) -> None:
        self.people_resource = PeopleResource(design_days)
        super().__init__("Design", resources=[self.people_resource])

    def set_design_days(self, design_days: int) -> None:
        """
        Setter for design man-days
        :param design_days: design man-days
        :return: None
        """
        self.people_resource.set_man_days(design_days)


class HostingTask(Task):
    """
    Hosting task representing datacenter (storage and compute) and network
    """

    def __init__(
        self,
        electricity_mix: float,
        pue: float,
        server_hours: int,
        storage_tb: int,
        network_gb: int,
        duration_days: int,
    ) -> None:
        self.compute_resource = ComputeResource(electricity_mix, pue, server_hours)
        self.storage_resource = StorageResource(
            electricity_mix, pue, storage_tb, duration_days
        )
        self.network_resource = NetworkResource(network_gb)
        super().__init__(
            "Hosting", resources=[self.compute_resource, self.storage_resource]
        )

    def set_server_hours(self, server_hours: int) -> None:
        """
        Setter for server hours reserved by the application
        :param server_hours: server hours reserved by the app
        :return: None
        """
        self.compute_resource.set_server_hours(server_hours)

    def set_storage_tb(self, storage_tb: int) -> None:
        """
        Setter for storage tb reserved by the application
        :param storage_tb: storage tb reserved by the app
        :return: None
        """
        self.storage_resource.set_storage_tb(storage_tb)

    def set_network_gb(self, network_gb: int) -> None:
        """
        Data transferred induced by the application
        :param network_gb: gb transferred
        :return: None
        """
        self.network_resource.set_gb(network_gb)

    def set_electricity_mix(self, electricity_mix: float) -> None:
        """
        Setter for electricity-mix co2e emissions used by application devices/datacenters
        :param electricity_mix: The mix
        :return: None
        """
        self.compute_resource.set_electricity_mix(electricity_mix)

    def set_pue(self, pue: float) -> None:
        """
        Setter for the power usage effectiveness of the DC
        :param pue: the pue
        :return: None
        """
        self.compute_resource.set_pue(pue)

    def set_run_duration(self, run_duration_days: int) -> None:
        """
        Setter for the phase run duration as days
        :param run_duration_days: run duration as days
        :return: None
        """
        self.storage_resource.set_duration(run_duration_days)


class ImplementationTask(Task):
    """
    Implementation task containing development and design
    """

    def __init__(self, dev_days: int, design_days: int) -> None:
        self.dev_task = DevTask(dev_days)
        self.design_task = DesignTask(design_days)
        super().__init__("Implementation", subtasks=[self.dev_task, self.design_task])

    def set_dev_days(self, dev_days: int) -> None:
        """
        Setter for development man-days
        :param dev_days: development man-days
        :return: None
        """
        self.dev_task.set_dev_days(dev_days)

    def set_design_days(self, design_days: int) -> None:
        """
        Setter for design man-days
        :param design_days: design man-days
        :return: None
        """
        self.design_task.set_design_days(design_days)


class ManagementTask(Task):
    """
    Management task, containing man-days
    """

    def __init__(self, management_days: int) -> None:
        self.people_resource = PeopleResource(management_days)
        super().__init__("Management", resources=[self.people_resource])

    def set_management_days(self, management_days: int) -> None:
        """
        Setter for management man-days
        :param management_days: management man-days
        :return: None
        """
        self.people_resource.set_man_days(management_days)


class MaintenanceTask(Task):
    """
    Maintenance task, containing man-days
    """

    def __init__(self, maintenance_days: int) -> None:
        self.people_resource = PeopleResource(maintenance_days)
        super().__init__("Maintenance", resources=[self.people_resource])

    def set_maintenance_days(self, maintenance_days: int) -> None:
        """
        Setter for maintenance man-days
        :param maintenance_days: management man-days
        :return: None
        """
        self.people_resource.set_man_days(maintenance_days)


class RunTask(Task):
    """
    Run  task including Maintenance and hosting task
    Also includes user device resources/impact
    """

    def __init__(
        self,
        maintenance_days: int,
        user_hours: int,
        electricity_mix: float,
        pue: float,
        server_tb: int,
        storage_tb: int,
        network_gb: int,
        duration_days: int,
    ) -> None:
        self.maintenance_task = MaintenanceTask(maintenance_days)
        self.hosting_task = HostingTask(
            electricity_mix, pue, server_tb, storage_tb, network_gb, duration_days
        )

        self.user_device_res = UserDeviceResource(user_hours)

        super().__init__(
            "Run",
            resources=[self.user_device_res],
            subtasks=[self.maintenance_task, self.hosting_task],
        )

    def set_maintenance_days(self, maintenance_days: int) -> None:
        """
        Setter for maintenance man-days
        :param maintenance_days: management man-days
        :return: None
        """
        self.maintenance_task.set_maintenance_days(maintenance_days)

    def set_user_hours(self, user_hours: int) -> None:
        """
        Setter for user hours on the application
        :param user_hours: user hours on the app
        :return: None
        """
        self.user_device_res.set_user_hours(user_hours)

    def set_server_hours(self, server_hours: int) -> None:
        """
        Setter for server hours reserved by the application
        :param server_hours: server hours reserved by the app
        :return: None
        """
        self.hosting_task.set_server_hours(server_hours)

    def set_storage_tb(self, storage_tb: int) -> None:
        """
        Setter for storage tb reserved by the application
        :param storage_tb: storage tb reserved by the app
        :return: None
        """
        self.hosting_task.set_storage_tb(storage_tb)

    def set_network_gb(self, network_gb: int) -> None:
        """
        Data transferred induced by the application
        :param network_gb: gb transferred
        :return: None
        """
        self.hosting_task.set_network_gb(network_gb)

    def set_electricity_mix(self, electricity_mix: float) -> None:
        """
        Setter for electricity-mix co2e emissions used by application devices/datacenters
        :param electricity_mix: The mix
        :return: None
        """
        self.hosting_task.set_electricity_mix(electricity_mix)
        # self.user_device_res.set_electricity_mix(electricity_mix)

    def set_pue(self, pue: float) -> None:
        """
        Setter for the power usage effectiveness of the DC
        :param pue: the pue
        :return: None
        """
        self.hosting_task.set_pue(pue)

    def set_run_duration(self, run_duration_days: int) -> None:
        """
        Setter for the phase run duration as days
        :param run_duration_days: run duration as days
        :return: None
        """
        self.hosting_task.set_run_duration(run_duration_days)


class SpecTask(Task):
    """
    Specification and requirements task, containing man-days
    """

    def __init__(self, spec_days: int) -> None:
        self.people_resource = PeopleResource(spec_days)
        super().__init__(
            "Specifications and requirements", resources=[self.people_resource]
        )

    def set_spec_days(self, spec_days: int) -> None:
        """
        Setter for specification and requirements man-days
        :param spec_days: specification and requirements man-days
        :return: None
        """
        self.people_resource.set_man_days(spec_days)


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
        user_hours: int,
        electricity_mix: float,
        pue: float,
        server_hours: int,
        storage_tb: int,
        network_gb: int,
        run_duration: int,
    ) -> None:
        self.build_task = BuildTask(dev_days, design_days, spec_days, management_days)
        self.run_task = RunTask(
            maintenance_days,
            user_hours,
            electricity_mix,
            pue,
            server_hours,
            storage_tb,
            network_gb,
            run_duration,
        )
        super().__init__("Standard project", subtasks=[self.build_task, self.run_task])

    def set_dev_days(self, dev_days: int) -> None:
        """
        Setter for development man-days
        :param dev_days: development days
        :return: None
        """
        self.build_task.set_dev_days(dev_days)

    def set_design_days(self, design_days: int) -> None:
        """
        Setter for design man-days
        :param design_days: design man-days
        :return: None
        """
        self.build_task.set_design_days(design_days)

    def set_spec_days(self, spec_days: int) -> None:
        """
        Setter for specification and requirements man-days
        :param spec_days: specification and requirements man-days
        :return: None
        """
        self.build_task.set_spec_days(spec_days)

    def set_management_days(self, management_days: int) -> None:
        """
        Setter for management man-days
        :param management_days: management man-days
        :return: None
        """
        self.build_task.set_management_days(management_days)

    def set_maintenance_days(self, maintenance_days: int) -> None:
        """
        Setter for maintenance man-days
        :param maintenance_days: management man-days
        :return: None
        """
        self.run_task.set_maintenance_days(maintenance_days)

    def set_user_hours(self, user_hours: int) -> None:
        """
        Setter for user hours on the application
        :param user_hours: user hours on the app
        :return: None
        """
        self.run_task.set_user_hours(user_hours)

    def set_server_hours(self, server_hours: int) -> None:
        """
        Setter for server hours reserved by the application
        :param server_hours: server hours reserved by the app
        :return: None
        """
        self.run_task.set_server_hours(server_hours)

    def set_storage_tb(self, storage_tb: int) -> None:
        """
        Setter for storage tb reserved by the application
        :param storage_tb: storage tb reserved by the app
        :return: None
        """
        self.run_task.set_storage_tb(storage_tb)

    def set_network_gb(self, network_gb: int) -> None:
        """
        Data transferred induced by the application
        :param network_gb: gb transferred
        :return: None
        """
        self.run_task.set_network_gb(network_gb)

    def set_electricity_mix(self, electricity_mix: float) -> None:
        """
        Setter for electricity-mix co2e emissions used by application devices/datacenters
        :param electricity_mix: The mix
        :return: None
        """
        self.run_task.set_electricity_mix(electricity_mix)

    def set_pue(self, pue: float) -> None:
        """
        Setter for the power usage effectiveness of the DC
        :param pue: the pue
        :return: None
        """
        self.run_task.set_pue(pue)

    def set_run_duration(self, run_duration_days: int) -> None:
        """
        Setter for the phase run duration as days
        :param run_duration_days: run duration as days
        :return: None
        """
        self.run_task.set_run_duration(run_duration_days)
