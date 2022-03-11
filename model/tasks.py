from __future__ import annotations

from abc import ABC

from resources import (
    PeopleResource,
    ComputeResource,
    Resource,
    StorageResource,
    NetworkResource,
    UserDeviceResource,
)


class Task(ABC):
    def __init__(self, resources: [Resource] = None, subtasks: [Task] = None):
        if resources is None:
            resources = []
        if subtasks is None:
            subtasks = []
        self.subtasks = subtasks
        self.resources = resources

    def get_impact(self) -> float:
        return sum(r.get_impact() for r in self.resources) + sum(
            s.get_impact() for s in self.subtasks
        )


class BuildTask(Task):
    def __init__(
        self, dev_days: int, design_days: int, spec_days: int, management_days: int
    ) -> None:
        self.implementation_task = ImplementationTask(dev_days, design_days)
        self.spec_task = SpecTask(spec_days)
        self.management_task = ManagementTask(management_days)

        super().__init__(
            subtasks=[self.implementation_task, self.spec_task, self.management_task]
        )

    def set_dev_days(self, dev_days: int) -> None:
        self.implementation_task.set_dev_days(dev_days)

    def set_design_days(self, design_days: int) -> None:
        self.implementation_task.set_design_days(design_days)

    def set_spec_days(self, spec_days: int) -> None:
        self.spec_task.set_spec_days(spec_days)

    def set_management_days(self, management_days: int) -> None:
        self.management_task.set_management_days(management_days)


class DevTask(Task):
    def __init__(self, dev_days) -> None:
        self.people_resource = PeopleResource(dev_days)
        super().__init__(resources=[self.people_resource])

    def set_dev_days(self, dev_days) -> None:
        self.people_resource.set_quantity(dev_days)


class DesignTask(Task):
    def __init__(self, design_days) -> None:
        self.people_resource = PeopleResource(design_days)
        super().__init__(resources=[self.people_resource])

    def set_design_days(self, design_days) -> None:
        self.people_resource.set_quantity(design_days)


class HostingTask(Task):
    def __init__(self, server_hours, storage_hours, network_gb) -> None:
        self.compute_resource = ComputeResource(server_hours)
        self.storage_resource = StorageResource(storage_hours)
        self.network_resource = NetworkResource(network_gb)
        super().__init__(resources=[self.compute_resource, self.storage_resource])

    def set_server_hours(self, server_hours):
        self.compute_resource.set_quantity(server_hours)

    def set_storage_hours(self, storage_hours: int) -> None:
        self.storage_resource.set_quantity(storage_hours)

    def set_network_gb(self, network_gb):
        self.network_resource.set_quantity(network_gb)


class ImplementationTask(Task):
    def __init__(self, dev_days, design_days) -> None:
        self.dev_task = DevTask(dev_days)
        self.design_task = DesignTask(design_days)
        super().__init__(subtasks=[self.dev_task, self.design_task])

    def set_dev_days(self, dev_days: int) -> None:
        self.dev_task.set_dev_days(dev_days)

    def set_design_days(self, design_days: int) -> None:
        self.design_task.set_design_days(design_days)


class ManagementTask(Task):
    def __init__(self, management_days) -> None:
        self.people_resource = PeopleResource(management_days)
        super().__init__(resources=[self.people_resource])

    def set_management_days(self, management_days):
        self.people_resource.set_quantity(management_days)


class MaintenanceTask(Task):
    def __init__(self, maintenance_days) -> None:
        self.people_resource = PeopleResource(maintenance_days)
        super().__init__(resources=[self.people_resource])

    def set_maintenance_days(self, maintenance_days):
        self.people_resource.set_quantity(maintenance_days)


class RunTask(Task):
    def __init__(
        self, maintenance_days, user_hours, server_hours, storage_hours, network_gb
    ) -> None:
        self.maintenance_task = MaintenanceTask(maintenance_days)
        self.hosting_task = HostingTask(server_hours, storage_hours, network_gb)

        self.user_device_res = UserDeviceResource(user_hours)

        super().__init__(
            resources=[self.user_device_res],
            subtasks=[self.maintenance_task, self.hosting_task],
        )

    def set_maintenance_days(self, maintenance_days) -> None:
        self.maintenance_task.set_maintenance_days(maintenance_days)

    def set_user_hours(self, user_hours: int) -> None:
        self.user_device_res.set_quantity(user_hours)

    def set_server_hours(self, server_hours: int) -> None:
        self.hosting_task.set_server_hours(server_hours)

    def set_storage_hours(self, storage_hours: int) -> None:
        self.hosting_task.set_storage_hours(storage_hours)

    def set_network_gb(self, network_gb: int) -> None:
        self.hosting_task.set_network_gb(network_gb)


class SpecTask(Task):
    def __init__(self, spec_days: int) -> None:
        self.people_resource = PeopleResource(spec_days)
        super().__init__(resources=[self.people_resource])

    def set_spec_days(self, spec_days: int) -> None:
        self.people_resource.set_quantity(spec_days)


# TODO remove noinspection
# noinspection DuplicatedCode
class StandardProjectTask(Task):
    def __init__(
        self,
        dev_days: int,
        design_days: int,
        spec_days: int,
        management_days: int,
        maintenance_days: int,
        user_hours: int,
        server_hours: int,
        storage_hours: int,
        network_gb: int,
    ) -> None:
        self.build_task = BuildTask(dev_days, design_days, spec_days, management_days)
        self.run_task = RunTask(
            maintenance_days, user_hours, server_hours, storage_hours, network_gb
        )
        super().__init__(subtasks=[self.build_task, self.run_task])

    def set_dev_days(self, dev_days: int) -> None:
        self.build_task.set_dev_days(dev_days)

    def set_design_days(self, design_days: int) -> None:
        self.build_task.set_design_days(design_days)

    def set_spec_days(self, spec_days: int) -> None:
        self.build_task.set_spec_days(spec_days)

    def set_management_days(self, management_days: int) -> None:
        self.build_task.set_management_days(management_days)

    def set_maintenance_days(self, maintenance_days: int) -> None:
        self.run_task.set_maintenance_days(maintenance_days)

    def set_user_hours(self, user_hours: int) -> None:
        self.run_task.set_user_hours(user_hours)

    def set_server_hours(self, server_hours: int) -> None:
        self.run_task.set_server_hours(server_hours)

    def set_storage_hours(self, storage_hours: int) -> None:
        self.run_task.set_storage_hours(storage_hours)

    def set_network_gb(self, network_gb: int) -> None:
        self.run_task.set_network_gb(network_gb)
