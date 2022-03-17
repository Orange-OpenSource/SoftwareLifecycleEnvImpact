from typing import Any, Union
from model.tasks import Task, StandardProjectTask


class Project:
    """
    Abstract project, contains the root task to model the lifecycle
    """

    def __init__(self, task: Task):
        self.root_task = task

    def get_global_impact(self) -> float:
        """
        Compute and return the project global CO2e footprint
        :return: project global impact
        """
        return self.root_task.get_impact()

    def get_impact_by_task(self) -> dict[str, Union[Union[float, list[None]], Any]]:
        """
        Compute the tasks impacts, regrouped by task/subtask
        :return: for each node the name, the associated co2 and the same thing for each  of its subtasks
        """
        return self.root_task.get_impact_by_task()


class StandardProject(Project):
    """
    Implementation of a standard base project
    """

    def __init__(self):
        dev_days = 2000
        design_days = 130
        spec_days = 200
        management_days = 1000
        maintenance_days = 700
        # ADEME https://bilans-ges.ademe.fr/fr/accueil/documentation-gene/index/page/Electricite_reglementaire
        electricity_mix = 0.0599
        pue = 1.5
        servers_count = 6
        storage_tb = 40
        run_duration = 365
        avg_user_day = 300
        avg_user_minutes = 30
        avg_user_data = 1

        self.root_task = StandardProjectTask(
            dev_days,
            design_days,
            spec_days,
            management_days,
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
        super().__init__(self.root_task)

    @property
    def dev_days(self):
        """Development man-days"""
        return (
            self.root_task.build_task.implementation_task.dev_task.people_resource.quantity
        )

    @dev_days.setter
    def dev_days(self, dev_days: int):
        self.root_task.build_task.implementation_task.dev_task.people_resource.quantity = (
            dev_days
        )

    @property
    def design_days(self):
        """Design man-days"""
        return (
            self.root_task.build_task.implementation_task.design_task.people_resource.quantity
        )

    @design_days.setter
    def design_days(self, design_days: int):
        self.root_task.build_task.implementation_task.design_task.people_resource.quantity = (
            design_days
        )

    @property
    def spec_days(self):
        """Specification and requirements man-days"""
        return self.root_task.build_task.spec_task.people_resource.quantity

    @spec_days.setter
    def spec_days(self, spec_days: int):
        self.root_task.build_task.spec_task.people_resource.quantity = spec_days

    @property
    def management_days(self):
        """Management man-days"""
        return self.root_task.build_task.management_task.people_resource.quantity

    @management_days.setter
    def management_days(self, management_days: int):
        self.root_task.build_task.management_task.people_resource.quantity = (
            management_days
        )

    @property
    def maintenance_days(self):
        """Maintenance man-days"""
        return self.root_task.run_task.maintenance_task.people_resource.quantity

    @maintenance_days.setter
    def maintenance_days(self, maintenance_days: int):
        self.root_task.run_task.maintenance_task.people_resource.quantity = (
            maintenance_days
        )

    @property
    def electricity_mix(self):
        """Electricity-mix co2e emissions used by application devices/datacenters"""
        return self.root_task.run_task.hosting_task.electricity_mix

    @electricity_mix.setter
    def electricity_mix(self, electricity_mix: float):
        self.root_task.run_task.hosting_task.electricity_mix = electricity_mix

    @property
    def pue(self):
        """Power usage effectiveness of the DC"""
        return self.root_task.run_task.hosting_task.pue

    @pue.setter
    def pue(self, pue: float):
        self.root_task.run_task.hosting_task.pue = pue

    @property
    def servers_count(self):
        """Number of servers reserved by the application"""
        return self.root_task.run_task

    @servers_count.setter
    def servers_count(self, servers_count: int):
        self.root_task.run_task = servers_count

    @property
    def storage_tb(self):
        """Storage tb reserved by the application"""
        return self.root_task.run_task.hosting_task.storage_tb

    @storage_tb.setter
    def storage_tb(self, storage_tb: int):
        self.root_task.run_task.hosting_task.storage_tb = storage_tb

    @property
    def run_duration(self):
        """Run phase duration as days"""
        return self.root_task.run_task.run_duration_days

    @run_duration.setter
    def run_duration(self, run_duration: int):
        self.root_task.run_task.duration_days = run_duration

    @property
    def avg_user_day(self):
        """Average number of user each day"""
        return self.root_task.run_task.avg_user_day

    @avg_user_day.setter
    def avg_user_day(self, avg_user_day: int):
        self.root_task.run_task.avg_user_day = avg_user_day

    @property
    def avg_user_minutes(self):
        """Average time user spend on app each day in minutes"""
        return self.root_task.run_task.avg_user_minutes

    @avg_user_minutes.setter
    def avg_user_minutes(self, avg_user_minutes: int):
        self.root_task.run_task.avg_user_minutes = avg_user_minutes

    @property
    def avg_user_data(self):
        """Average user data each day as float gb"""
        return self.root_task.run_task.avg_user_data

    @avg_user_data.setter
    def avg_user_data(self, avg_user_data: float):
        self.root_task.run_task.avg_user_data = avg_user_data
