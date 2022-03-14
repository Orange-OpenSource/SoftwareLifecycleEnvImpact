from model.tasks import Task, StandardProjectTask


class Project:
    """
    Abstract project, contains the root task to model the lifecycle
    """

    def __init__(self, task: Task) -> None:
        self.root_task = task

    def get_impact_task(self) -> float:
        """
        Compute the tasks impacts, regrouped by task/subtask
        :return: the impact # TODO return float not grouped by impact
        """
        return float(self.root_task.get_impact())  # TODO check cast


# TODO remove noinspection
# noinspection DuplicatedCode
class StandardProject(Project):
    """
    Implementation of a standard base project
    """

    def __init__(self) -> None:
        dev_days = 3000
        design_days = 300
        spec_days = 300
        management_days = 1000
        maintenance_days = 100
        user_hours = 300000
        # ADEME https://bilans-ges.ademe.fr/fr/accueil/documentation-gene/index/page/Electricite_reglementaire
        electricity_mix = 0.0599
        pue = 1.5
        server_hours = 300
        storage_hours = 3000
        network_gb = 30000000

        self.root_task = StandardProjectTask(
            dev_days,
            design_days,
            spec_days,
            management_days,
            maintenance_days,
            user_hours,
            electricity_mix,
            pue,
            server_hours,
            storage_hours,
            network_gb,
        )
        super().__init__(self.root_task)

    def set_dev_days(self, dev_days: int) -> None:
        """
        Setter for development man-days
        :param dev_days: development days
        :return: None
        """
        self.root_task.set_dev_days(dev_days)

    def set_design_days(self, design_days: int) -> None:
        """
        Setter for design man-days
        :param design_days: design man-days
        :return: None
        """
        self.root_task.set_design_days(design_days)

    def set_spec_days(self, spec_days: int) -> None:
        """
        Setter for specification and requirements man-days
        :param spec_days: specification and requirements man-days
        :return: None
        """
        self.root_task.set_spec_days(spec_days)

    def set_management_days(self, management_days: int) -> None:
        """
        Setter for management man-days
        :param management_days: management man-days
        :return: None
        """
        self.root_task.set_management_days(management_days)

    def set_maintenance_days(self, maintenance_days: int) -> None:
        """
        Setter for maintenance man-days
        :param maintenance_days: management man-days
        :return: None
        """
        self.root_task.set_maintenance_days(maintenance_days)

    def set_user_hours(self, user_hours: int) -> None:
        """
        Setter for user hours on the application
        :param user_hours: user hours on the app
        :return: None
        """
        self.root_task.set_user_hours(user_hours)

    def set_server_hours(self, server_hours: int) -> None:
        """
        Setter for server hours reserved by the application
        :param server_hours: server hours reserved by the app
        :return: None
        """
        self.root_task.set_server_hours(server_hours)

    def set_storage_hours(self, storage_hours: int) -> None:
        """
        Setter for storage hours reserved by the application
        :param storage_hours: storage hours reserved by the app # TODO wrong unit
        :return: None
        """
        self.root_task.set_storage_hours(storage_hours)

    def set_network_gb(self, network_gb: int) -> None:
        """
        Data transferred induced by the application
        :param network_gb: gb transferred
        :return: None
        """
        self.root_task.set_network_gb(network_gb)
