from typing import Any, List, Union

from pint import Quantity

from api.data_model import Task
from impacts_model.impact_sources import ImpactIndicator, ImpactsList, merge_impacts_lists
from impacts_model.quantities.quantities import Q_
from impacts_model.resources import (get_resource_impact, get_resource_impact_list, merge_resource_list, ResourcesList)


########
# Task #
########


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


def get_task_impacts(task: Task) -> dict[str, Union[str, float, Any]]:  # TODO bad return value
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
