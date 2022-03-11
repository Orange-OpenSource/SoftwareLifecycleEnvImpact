from tasks import Task, StandardProjectTask


class Project:
    def __init__(self, task: Task):
        self.root_task = task

    def get_impact_task(self):
        return self.root_task.get_impact()


# TODO remove noinspection
# noinspection DuplicatedCode
class StandardProject(Project):
    def __init__(self):
        dev_days = 3000
        design_days = 300
        spec_days = 300
        management_days = 1000
        maintenance_days = 100
        user_hours = 300000
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
            server_hours,
            storage_hours,
            network_gb,
        )
        super().__init__(self.root_task)

    def set_dev_days(self, dev_days):
        self.root_task.set_dev_days(dev_days)

    def set_design_days(self, design_days):
        self.root_task.set_design_days(design_days)

    def set_spec_days(self, spec_days):
        self.root_task.set_spec_days(spec_days)

    def set_management_days(self, management_days):
        self.root_task.set_management_days(management_days)

    def set_maintenance_days(self, maintenance_days):
        self.root_task.set_maintenance_days(maintenance_days)

    def set_user_hours(self, user_hours):
        self.root_task.set_user_hours(user_hours)

    def set_server_hours(self, server_hours):
        self.root_task.set_server_hours(server_hours)

    def set_storage_hours(self, storage_hours):
        self.root_task.set_storage_hours(storage_hours)

    def set_network_gb(self, network_gb):
        self.root_task.set_network_gb(network_gb)
