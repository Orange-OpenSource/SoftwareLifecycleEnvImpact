from typing import Any

from pint import Quantity

from model.impacts.impact_factors import ImpactsFactorsRegistry
from model.impacts.impacts import ImpactIndicator, ImpactsList
from model.quantities import ELECTRICITY_MIX, KG_CO2E
from model.resources import ResourcesList
from model.tasks import (
    BuildTask,
    DesignTask,
    DevTask,
    HostingTask,
    ImplementationTask,
    MaintenanceTask,
    ManagementTask,
    RunTask,
    SpecTask,
    StandardProjectTask,
    Task,
    TaskImpact,
    UsageTask,
)


class Project:
    """
    A project represent the complete lifecycle, contains the root task to model it
    """

    root_task: Task

    def __init__(self, task: Task):
        """
        Project constructor, define the root task hosting all the others as a tree
        :param task: the root task of the tree
        """
        self.root_task = task

    def get_co2_impact(self) -> KG_CO2E:
        """
        Compute and return the project global CO2e footprint
        :return: project global impact
        """
        return self.root_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)

    def get_impacts(self) -> ImpactsList:
        return self.root_task.get_impacts_list()

    def get_impact_by_task(self) -> TaskImpact:
        """
        Return all impacts_sources regrouped by task
        :return: impacts_sources regrouped under format TaskImpact

        Example:
                >>> StandardProject().get_impact_by_task()
                {'name': 'Standard project', 'CO2': 59669.01716074775, 'subtasks': [
                    {'name': 'Build', 'CO2': 40220.476196086754, 'subtasks': [
                        {'name': 'Implementation', 'CO2': 25726.610900199637, 'subtasks': [
                            {'name': 'Development', 'CO2': 24156.442159811868, 'subtasks': []},
                            {'name': 'Design', 'CO2': 1570.1687403877713, 'subtasks': []}]},
                        {'name': 'Specifications and requirements', 'CO2': 2415.644215981187, 'subtasks': []},
                        {'name': 'Management', 'CO2': 12078.221079905934, 'subtasks': []}]},
                    {'name': 'Run', 'CO2': 19448.540964660995, 'subtasks': [
                        {'name': 'Maintenance', 'CO2': 8454.754755934153, 'subtasks': []},
                        {'name': 'Hosting', 'CO2': 9004.016113902313, 'subtasks': []},
                        {'name': 'Usage', 'CO2': 1989.7700948245304, 'subtasks': []}]}]}
        """
        return self.root_task.get_impacts()

    def get_impact_by_resource(self) -> ResourcesList:

        """
        Return project-level ResourcesList (_impacts grouped by resource)

        Example:
        {
            'People': {'CO2': 48675.23095202091},
            'Compute': {'CO2': 6456.161285102313},
            'Storage': {'CO2': 2547.8548288},
            'UserDevice': {'CO2': 1825.5200948245304},
            'Network': {'CO2': 164.25}
        }
        :return: impacts_sources regrouped under format ResourcesList
        """
        return self.root_task.get_impact_by_resource()

    def get_impact_by_indicator(self, indicator: ImpactIndicator) -> Quantity[Any]:
        """
        Return all project impacts for one indicator, for example ImpactIndicator.CLIMATE_CHANGE
        :param indicator: the ImpactIndicator to retrieve values for
        :return: Quantity of impacts
        """
        return self.root_task.get_impact_by_indicator(indicator)


class StandardProject(Project):
    """
    Implementation of a standard base project
    """

    root_task: StandardProjectTask  # Enforce root_task type

    def __init__(self) -> None:
        dev_days = 2000
        design_days = 130
        spec_days = 200
        management_days = 1000
        maintenance_days = 700
        servers_count = 6
        storage_size = 40
        run_duration = 365
        avg_user = 300
        avg_time = 30
        avg_data = 1

        # Build Task
        self.dev_task = DevTask(dev_days)
        self.design_task = DesignTask(design_days)
        self.implementation_task = ImplementationTask(self.dev_task, self.design_task)

        self.spec_task = SpecTask(spec_days)
        self.management_task = ManagementTask(management_days)

        self.build_task = BuildTask(
            self.implementation_task, self.spec_task, self.management_task
        )

        # Run Task
        self.maintenance_task = MaintenanceTask(maintenance_days)
        self.hosting_task = HostingTask(servers_count, storage_size, run_duration)
        self.usage_task = UsageTask(avg_user, avg_time, avg_data, run_duration)
        self.run_task = RunTask(
            self.maintenance_task, self.hosting_task, self.usage_task
        )
        self.root_task = StandardProjectTask(self.build_task, self.run_task)
        self._impacts_registry = ImpactsFactorsRegistry()

        super().__init__(self.root_task)

    @property
    def dev_days(self) -> int:
        """
        Development man days
        :return: Dev man days of the project
        """
        return self.dev_task.dev_days

    @dev_days.setter
    def dev_days(self, dev_days: int) -> None:
        self.dev_task.dev_days = dev_days

    @property
    def design_days(self) -> int:
        """
        Design man days
        :return: Design man days of the project
        """
        return self.design_task.design_days

    @design_days.setter
    def design_days(self, design_days: int) -> None:
        self.design_task.design_days = design_days

    @property
    def spec_days(self) -> int:
        """
        Specification and requirements man days
        :return: Specification and requirements man days of the project
        """
        return self.spec_task.spec_days

    @spec_days.setter
    def spec_days(self, spec_days: int) -> None:
        self.spec_task.spec_days = spec_days

    @property
    def management_days(self) -> int:
        """
        Management man days
        :return: Management man days of the project
        """
        return self.management_task.management_days

    @management_days.setter
    def management_days(self, management_days: int) -> None:
        self.management_task.management_days = management_days

    @property
    def maintenance_days(self) -> int:
        """
        Maintenance man days
        :return: Maintenance man days of the project
        """
        return self.maintenance_task.maintenance_days

    @maintenance_days.setter
    def maintenance_days(self, maintenance_days: int) -> None:
        self.maintenance_task.maintenance_days = maintenance_days

    @property
    def electricity_mix(self) -> float:
        """
        Electricity-mix co2e emissions used by application devices/datacenters
        :return: The electricity mix
        """
        return float(self._impacts_registry.electricity_mix.magnitude)

    @electricity_mix.setter
    def electricity_mix(self, mix: float) -> None:
        self._impacts_registry.electricity_mix = mix * ELECTRICITY_MIX

    @property
    def pue(self) -> float:
        """
        Power usage effectiveness of the DC
        :return: the PUE
        """
        return self._impacts_registry.pue

    @pue.setter
    def pue(self, pue: float) -> None:
        self._impacts_registry.pue = pue

    @property
    def servers_count(self) -> int:
        """
        Number of servers reserved by the application
        :return: nb of servers
        """
        return self.hosting_task.servers_count

    @servers_count.setter
    def servers_count(self, servers_count: int) -> None:
        self.hosting_task.servers_count = servers_count

    @property
    def storage_size(self) -> int:
        """
        Storage tb reserved by the application
        :return: storage as terabytes
        """
        return self.hosting_task.storage_size

    @storage_size.setter
    def storage_size(self, storage_size: int) -> None:
        self.hosting_task.storage_size = storage_size

    @property
    def run_duration(self) -> int:
        """
        Run phase duration as days
        :return: number of days in the running phase
        """
        return self.run_task.duration

    @run_duration.setter
    def run_duration(self, run_duration: int) -> None:
        self.run_task.duration = run_duration

    @property
    def avg_user(self) -> int:
        """
        Average number of user each day of the running phase
        :return: avg user each day
        """
        return self.usage_task.avg_user

    @avg_user.setter
    def avg_user(self, avg_user: int) -> None:
        self.usage_task.avg_user = avg_user

    @property
    def avg_time(self) -> int:
        """
        Average time user spend on app each day in minutes
        :return: average daily time in minutes
        """
        return self.usage_task.avg_time

    @avg_time.setter
    def avg_time(self, avg_time: int) -> None:
        self.usage_task.avg_time = avg_time

    @property
    def avg_data(self) -> float:
        """
        Average gigabyte transferred by user by day
        :return: User data each day as gigabyte
        """
        return self.usage_task.avg_data

    @avg_data.setter
    def avg_data(self, avg_data: float) -> None:
        self.usage_task.avg_data = avg_data
