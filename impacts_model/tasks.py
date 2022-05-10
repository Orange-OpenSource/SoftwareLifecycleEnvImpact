from __future__ import annotations

from typing import Any, List, Union

from pint import Quantity

from impacts_model.impacts.impacts import ImpactIndicator, ImpactsList, merge_impacts_lists
from impacts_model.quantities import Q_
from impacts_model.resources import merge_resource_list, Resource, ResourcesList

TaskImpact = dict[str, Union[str, float, Any]]


class TaskTemplate:
    """
    Define a Task/Phase as a node containing an ImpactFactor and/or Subtask(s)
    """

    def __init__(self, name: str, resources: List[Resource] = None, subtasks: List[TaskTemplate] = None):  # type: ignore
        """
        Define a task with a name, resources and subtasks
        :param name: the name of the resource
        :param resources: optional list of resources
        :param subtasks: optional list of subtasks
        """
        self.name = name
        self.resources = resources if (resources is not None) else []
        self.subtasks = subtasks if (subtasks is not None) else []

    def get_impacts(self) -> TaskImpact:
        """
        Return a task impact for this one and its children
        :return: TaskImpact with name, impact sources and subtasks
        """
        return {
            "name": self.name,
            "impacts": self.get_impacts_list(),
            "subtasks": [r.get_impacts() for r in self.subtasks],
        }

    def get_impacts_list(self) -> ImpactsList:
        """
        Return the task impacts_list as an ImpactsList

        :return: an ImpactsList for this task impacts_list
        """
        impacts: ImpactsList = {}

        for r in self.resources:
            impacts = merge_impacts_lists(impacts, r.get_impacts())

        for s in self.subtasks:
            impacts = merge_impacts_lists(impacts, s.get_impacts_list())

        return impacts

    def get_impact_by_resource(self) -> ResourcesList:
        """
        Return all _impacts grouped by resource type, int the format of ResourcesList:

         {'People': {'CO2': 2000.0}}
         {'Build': {'CO2': 234325.0}}
        :return: ResourceList containing resources for this task
        """
        resource_list: ResourcesList = {}

        for r in self.resources:
            resource_list = merge_resource_list(
                resource_list, {r.name: r.get_impacts()}
            )

        for s in self.subtasks:
            resource_list = merge_resource_list(
                resource_list, s.get_impact_by_resource()
            )

        return resource_list

    def get_impact_by_indicator(self, indicator: ImpactIndicator) -> Quantity[Any]:
        """
        Return the computed impact passed as parameter of this task resources, and those of its subtasks
        :param indicator: Impact indicator
        :return: the quantity corresponding to the impact indicator
        """

        impacts_resources: List[Quantity[Any]] = [
            r.get_impact(indicator) for r in self.resources
        ]
        impacts_subtasks: List[Quantity[Any]] = [
            s.get_impact_by_indicator(indicator) for s in self.subtasks
        ]

        return Q_(sum(impacts_resources) + sum(impacts_subtasks))  # type: ignore
        # TODO why Q_ here ?
