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
        self.dev_days = 2000
        self.design_days = 130
        self.spec_days = 200
        self.management_days = 1000
        self.maintenance_days = 700
        # ADEME https://bilans-ges.ademe.fr/fr/accueil/documentation-gene/index/page/Electricite_reglementaire
        self.electricity_mix = 0.0599
        self.pue = 1.5
        self.servers_count = 6
        self.storage_tb = 40
        self.run_duration_days = 365
        self.avg_user_day = 300
        self.avg_user_minutes = 30
        self.avg_user_data = 1

        self.root_task = StandardProjectTask(
            self.dev_days,
            self.design_days,
            self.spec_days,
            self.management_days,
            self.maintenance_days,
            self.electricity_mix,
            self.pue,
            self.servers_count,
            self.storage_tb,
            self.run_duration_days,
            self.avg_user_day,
            self.avg_user_minutes,
            self.avg_user_data,
        )
        super().__init__(self.root_task)

    def set_dev_days(self, dev_days: int):
        """
        Setter for development man-days
        :param dev_days: development days
        :return: None
        """
        self.dev_days = dev_days
        self.root_task.set_dev_days(dev_days)

    def set_design_days(self, design_days: int):
        """
        Setter for design man-days
        :param design_days: design man-days
        :return: None
        """
        self.design_days = design_days
        self.root_task.set_design_days(design_days)

    def set_spec_days(self, spec_days: int):
        """
        Setter for specification and requirements man-days
        :param spec_days: specification and requirements man-days
        :return: None
        """
        self.spec_days = spec_days
        self.root_task.set_spec_days(spec_days)

    def set_management_days(self, management_days: int):
        """
        Setter for management man-days
        :param management_days: management man-days
        :return: None
        """
        self.management_days = management_days
        self.root_task.set_management_days(management_days)

    def set_maintenance_days(self, maintenance_days: int):
        """
        Setter for maintenance man-days
        :param maintenance_days: management man-days
        :return: None
        """
        self.maintenance_days = maintenance_days
        self.root_task.set_maintenance_days(maintenance_days)

    def set_servers_count(self, servers_count: int):
        """
        Setter for server quantity reserved by the application
        :param servers_count: servers reserved by the app
        :return: None
        """
        self.servers_count = servers_count
        self.root_task.set_servers_count(servers_count)

    def set_storage_tb(self, storage_tb: int):
        """
        Setter for storage tb reserved by the application
        :param storage_tb: storage tb reserved by the app
        :return: None
        """
        self.storage_tb = storage_tb
        self.root_task.set_storage_tb(storage_tb)

    def set_electricity_mix(self, electricity_mix: float):
        """
        Setter for electricity-mix co2e emissions used by application devices/datacenters
        :param electricity_mix: The mix
        :return: None
        """
        self.electricity_mix = electricity_mix
        self.root_task.set_electricity_mix(electricity_mix)

    def set_pue(self, pue: float):
        """
        Setter for the power usage effectiveness of the DC
        :param pue: the pue
        :return: None
        """
        self.pue = pue
        self.root_task.set_pue(pue)

    def set_run_duration(self, run_duration_days: int):
        """
        Setter for the phase run duration as days
        :param run_duration_days: run duration as days
        :return: None
        """
        self.run_duration_days = run_duration_days
        self.root_task.set_run_duration(run_duration_days)

    def set_avg_user_day(self, avg_user_day: int):
        """
        Setter for avg number of user each day
        :param avg_user_day: avg user each day
        :return: None
        """
        self.avg_user_day = avg_user_day
        self.root_task.set_avg_user_day(avg_user_day)

    def set_avg_user_minutes(self, avg_user_minutes: int):
        """
        Setter for avg time user spend on app each day in minutes
        :param avg_user_minutes: minutes per day per user
        :return: None
        """
        self.avg_user_minutes = avg_user_minutes
        self.root_task.set_avg_user_minutes(avg_user_minutes)

    def set_avg_user_data(self, avg_user_data: float):
        """
        Setter for avg user data each day as float gb
        :param avg_user_data: gb per day per user
        :return: None
        """
        self.avg_user_data = avg_user_data
        self.root_task.set_avg_user_data(avg_user_data)
