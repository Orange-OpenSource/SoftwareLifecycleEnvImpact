from typing import Any

from pint import Quantity

from model.impacts.impacts import ImpactIndicator, ImpactsList
from model.quantities import KG_CO2E
from model.resources import ResourcesList
from model.tasks import TaskImpact, TaskTemplate


class Project:
    """
    A project represent the complete lifecycle, contains the root task to model it
    """

    root_task: TaskTemplate

    def __init__(self, task: TaskTemplate):
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
        """
        Get the list of impact for the complete project
        :return:
        """
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
