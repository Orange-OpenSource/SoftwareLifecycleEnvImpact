from model.tasks import StandardProjectTask, Task


class Project:
    """
    Abstract project, contains the root task to model the lifecycle
    """

    root_task: Task

    def __init__(self, task: Task):
        self.root_task = task

    def get_global_impact(self) -> float:
        """
        Compute and return the project global CO2e footprint
        :return: project global impact
        """
        return self.root_task.get_co2_impact()


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
        # ADEME https://bilans-ges.ademe.fr/fr/accueil/documentation-gene/index/page/Electricite_reglementaire
        electricity_mix = 0.0599
        pue = 1.5
        servers_count = 6
        storage_size = 40
        run_duration = 365
        avg_user = 300
        avg_time = 30
        avg_data = 1

        self.root_task = StandardProjectTask(
            dev_days,
            design_days,
            spec_days,
            management_days,
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
        super().__init__(self.root_task)

    @property
    def dev_days(self) -> int:
        """Development man-days"""
        return self.root_task.build_task.implementation_task.dev_task.dev_days

    @dev_days.setter
    def dev_days(self, dev_days: int) -> None:
        self.root_task.build_task.implementation_task.dev_task.dev_days = dev_days

    @property
    def design_days(self) -> int:
        """Design man-days"""
        return self.root_task.build_task.implementation_task.design_task.design_days

    @design_days.setter
    def design_days(self, design_days: int) -> None:
        self.root_task.build_task.implementation_task.design_task.design_days = (
            design_days
        )

    @property
    def spec_days(self) -> int:
        """Specification and requirements man-days"""
        return self.root_task.build_task.spec_task.spec_days

    @spec_days.setter
    def spec_days(self, spec_days: int) -> None:
        self.root_task.build_task.spec_task.spec_days = spec_days

    @property
    def management_days(self) -> int:
        """Management man-days"""
        return self.root_task.build_task.management_task.management_days

    @management_days.setter
    def management_days(self, management_days: int) -> None:
        self.root_task.build_task.management_task.management_days = management_days

    @property
    def maintenance_days(self) -> int:
        """Maintenance man-days"""
        return self.root_task.run_task.maintenance_task.maintenance_days

    @maintenance_days.setter
    def maintenance_days(self, maintenance_days: int) -> None:
        self.root_task.run_task.maintenance_task.maintenance_days = maintenance_days

    @property
    def electricity_mix(self) -> float:
        """Electricity-mix co2e emissions used by application devices/datacenters"""
        return self.root_task.run_task.hosting_task.electricity_mix

    @electricity_mix.setter
    def electricity_mix(self, electricity_mix: float) -> None:
        self.root_task.run_task.hosting_task.electricity_mix = electricity_mix

    @property
    def pue(self) -> float:
        """Power usage effectiveness of the DC"""
        return self.root_task.run_task.hosting_task.pue

    @pue.setter
    def pue(self, pue: float) -> None:
        self.root_task.run_task.hosting_task.pue = pue

    @property
    def servers_count(self) -> int:
        """Number of servers reserved by the application"""
        return self.root_task.run_task.hosting_task.servers_count

    @servers_count.setter
    def servers_count(self, servers_count: int) -> None:
        self.root_task.run_task.hosting_task.servers_count = servers_count

    @property
    def storage_size(self) -> int:
        """Storage tb reserved by the application"""
        return self.root_task.run_task.hosting_task.storage_size

    @storage_size.setter
    def storage_size(self, storage_size: int) -> None:
        self.root_task.run_task.hosting_task.storage_size = storage_size

    @property
    def run_duration(self) -> int:
        """Run phase duration as days"""
        return self.root_task.run_task.duration

    @run_duration.setter
    def run_duration(self, run_duration: int) -> None:
        self.root_task.run_task.duration = run_duration

    @property
    def avg_user(self) -> int:
        """Average number of user each day"""
        return self.root_task.run_task.usage_task.avg_user

    @avg_user.setter
    def avg_user(self, avg_user: int) -> None:
        self.root_task.run_task.usage_task.avg_user = avg_user

    @property
    def avg_time(self) -> int:
        """Average time user spend on app each day in minutes"""
        return self.root_task.run_task.usage_task.avg_time

    @avg_time.setter
    def avg_time(self, avg_time: int) -> None:
        self.root_task.run_task.usage_task.avg_time = avg_time

    @property
    def avg_data(self) -> float:
        """Average user data each day as float gb"""
        return self.root_task.run_task.usage_task.avg_data

    @avg_data.setter
    def avg_data(self, avg_data: float) -> None:
        self.root_task.run_task.usage_task.avg_data = avg_data
