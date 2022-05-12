from __future__ import annotations

import os
from typing import Any, List, Union

import yaml
from pint import Quantity

from api.data_model import Task
from impacts_model.impact_sources import ImpactIndicator, ImpactsList, merge_impacts_lists
from impacts_model.quantities.quantities import Q_
from impacts_model.resources import (get_resource_impact, get_resource_impact_list, merge_resource_list, Resource,
                                     resource_template_factory, ResourcesList)

TaskImpact = dict[str, Union[str, float, Any]]


def get_tasks_templates() -> [TaskTemplate]:
    tasks_template = []
    for filename in os.listdir("impacts_model/data/tasks"):
        tasks_template.append(task_template_factory(filename))
    return tasks_template


def task_template_factory(name: str) -> TaskTemplate:
    name = name.replace(".yaml", "")
    with open("impacts_model/data/tasks/" + name + ".yaml", "r") as stream:
        data_loaded = yaml.safe_load(stream)

        resources_list = []
        if data_loaded["resources"] is not None:
            for resource_name in data_loaded["resources"]:
                resources_list.append(resource_template_factory(resource_name))

        subtasks_list = []
        if data_loaded["subtasks"] is not None:
            for resource_name in data_loaded["subtasks"]:
                subtasks_list.append(task_template_factory(resource_name))

        return TaskTemplate(
            name=data_loaded["name"], resources=resources_list, subtasks=subtasks_list
        )


def get_task_impact_by_indicator(
    task: Task, indicator: ImpactIndicator
) -> Quantity[Any]:
    impacts_resources: List[Quantity[Any]] = [
        get_resource_impact(r, indicator) for r in task.resources
    ]
    impacts_subtasks: List[Quantity[Any]] = [
        get_task_impact_by_indicator(s, indicator) for s in task.subtasks
    ]

    return Q_(sum(impacts_resources) + sum(impacts_subtasks))
    # TODO why Q_ here ?


def get_task_impact_list(
    task: Task,
) -> ImpactsList:  # TODO clarify the difference with get_task_impacts()
    impacts: ImpactsList = {}

    for r in task.resources:
        impacts = merge_impacts_lists(impacts, get_resource_impact_list(r))

    for s in task.subtasks:
        impacts = merge_impacts_lists(impacts, get_task_impact_list(s))

    return impacts


def get_task_impacts(task: Task) -> TaskImpact:
    """
    Return a task impact for this one and its children
    :param: The Task to get the impacts from
    :return: TaskImpact with name, impact sources and subtasks
    """
    return {
        "id": task.id,
        "name": task.name,
        "impacts": [
            {key.value: str(value)} for key, value in get_task_impact_list(task).items()
        ],
        "subtasks": [get_task_impacts(r) for r in task.subtasks],
    }


def get_task_impact_by_resource_type(task: Task) -> ResourcesList:
    """
    Return all _impacts grouped by resource type, int the format of ResourcesList:

     {'People': {'CO2': 2000.0}}
     {'Build': {'CO2': 234325.0}}
    :return: ResourceList containing resources for this task
    """
    resource_list: ResourcesList = {}

    for r in task.resources:
        resource_list = merge_resource_list(resource_list, {r.type: get_resource_impact_list(r)})

    for s in task.subtasks:
        resource_list = merge_resource_list(resource_list, get_task_impact_by_resource_type(s))

    return resource_list


class TaskTemplate:
    """
    Define a Task/Phase as a node containing an ImpactFactor and/or Subtask(s)
    """

    def __init__(self, name: str, resources: List[Resource] = None, subtasks: List[TaskTemplate] = None):
        """
        Define a task with a name, resources and subtasks
        :param name: the name of the resource
        :param resources: optional list of resources
        :param subtasks: optional list of subtasks
        """
        self.name = name
        self.resources = resources if (resources is not None) else []
        self.subtasks = subtasks if (subtasks is not None) else []

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
