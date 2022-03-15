from typing import Any, Union
from model.tasks import Task, StandardProjectTask


class Project:
    """
    Abstract project, contains the root task to model the lifecycle
    """

    def __init__(self, task: Task) -> None:
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

    def __init__(self) -> None:
        self.dev_days = 2000
        self.design_days = 130
        self.spec_days = 200
        self.management_days = 1000
        self.maintenance_days = 700
        self.user_hours = 150000
        # ADEME https://bilans-ges.ademe.fr/fr/accueil/documentation-gene/index/page/Electricite_reglementaire
        self.electricity_mix = 0.0599
        self.pue = 1.5
        self.servers_count = 6
        self.storage_tb = 40
        self.network_gb = 1000000
        self.run_duration_days = 365

        self.root_task = StandardProjectTask(
            self.dev_days,
            self.design_days,
            self.spec_days,
            self.management_days,
            self.maintenance_days,
            self.user_hours,
            self.electricity_mix,
            self.pue,
            self.servers_count,
            self.storage_tb,
            self.network_gb,
            self.run_duration_days,
        )
        super().__init__(self.root_task)

    def set_dev_days(self, dev_days: int) -> None:
        """
        Setter for development man-days
        :param dev_days: development days
        :return: None
        """
        self.dev_days = dev_days
        self.root_task.set_dev_days(dev_days)

    def set_design_days(self, design_days: int) -> None:
        """
        Setter for design man-days
        :param design_days: design man-days
        :return: None
        """
        self.design_days = design_days
        self.root_task.set_design_days(design_days)

    def set_spec_days(self, spec_days: int) -> None:
        """
        Setter for specification and requirements man-days
        :param spec_days: specification and requirements man-days
        :return: None
        """
        self.spec_days = spec_days
        self.root_task.set_spec_days(spec_days)

    def set_management_days(self, management_days: int) -> None:
        """
        Setter for management man-days
        :param management_days: management man-days
        :return: None
        """
        self.management_days = management_days
        self.root_task.set_management_days(management_days)

    def set_maintenance_days(self, maintenance_days: int) -> None:
        """
        Setter for maintenance man-days
        :param maintenance_days: management man-days
        :return: None
        """
        self.maintenance_days = maintenance_days
        self.root_task.set_maintenance_days(maintenance_days)

    def set_user_hours(self, user_hours: int) -> None:
        """
        Setter for user hours on the application
        :param user_hours: user hours on the app
        :return: None
        """
        self.user_hours = user_hours
        self.root_task.set_user_hours(user_hours)

    def set_servers_count(self, servers_count: int) -> None:
        """
        Setter for server quantity reserved by the application
        :param servers_count: servers reserved by the app
        :return: None
        """
        self.servers_count = servers_count
        self.root_task.set_servers_count(servers_count)

    def set_storage_tb(self, storage_tb: int) -> None:
        """
        Setter for storage tb reserved by the application
        :param storage_tb: storage tb reserved by the app
        :return: None
        """
        self.storage_tb = storage_tb
        self.root_task.set_storage_tb(storage_tb)

    def set_network_gb(self, network_gb: int) -> None:
        """
        Data transferred induced by the application
        :param network_gb: gb transferred
        :return: None
        """
        self.network_gb = network_gb
        self.root_task.set_network_gb(network_gb)

    def set_electricity_mix(self, electricity_mix: float) -> None:
        """
        Setter for electricity-mix co2e emissions used by application devices/datacenters
        :param electricity_mix: The mix
        :return: None
        """
        self.electricity_mix = electricity_mix
        self.root_task.set_electricity_mix(electricity_mix)

    def set_pue(self, pue: float) -> None:
        """
        Setter for the power usage effectiveness of the DC
        :param pue: the pue
        :return: None
        """
        self.pue = pue
        self.root_task.set_pue(pue)

    def set_run_duration(self, run_duration_days: int) -> None:
        """
        Setter for the phase run duration as days
        :param run_duration_days: run duration as days
        :return: None
        """
        self.run_duration_days = run_duration_days
        self.root_task.set_run_duration(run_duration_days)
