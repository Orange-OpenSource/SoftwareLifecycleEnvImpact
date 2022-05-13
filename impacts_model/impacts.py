from __future__ import annotations

from typing import Any, List, Union

from pint import Quantity

from api.data_model import Resource, Task
from impacts_model.impact_sources import ImpactIndicator
from impacts_model.quantities.quantities import Q_
from impacts_model.templates import load_resource_impacts_source


#######################
# EnvironmentalImpact #
#######################

class EnvironmentalImpact:
    def __init__(self, impacts: dict[ImpactIndicator, Quantity[Any]] = None) -> None:
        self.impacts: dict[ImpactIndicator, Quantity[Any]] = impacts if impacts is not None else {}

    def add(self, other: EnvironmentalImpact) -> None:
        result = {**self.impacts, **other.impacts}
        for impact_indicator, _ in result.items():
            if impact_indicator in self.impacts and impact_indicator in other.impacts:
                result[impact_indicator] = (
                        self.impacts[impact_indicator] + other.impacts[impact_indicator]
                )
        self.impacts = result

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

def get_task_environmental_impact(task: Task) -> EnvironmentalImpact:
    environmental_impact = EnvironmentalImpact()

    for r in task.resources:
        environmental_impact.add(get_resource_environmental_impact(r))

    for s in task.subtasks:
        environmental_impact.add(get_task_environmental_impact(s))

    return environmental_impact

'''
def get_task_impact_list(
        task: Task,
) -> ImpactsList:  # TODO clarify the difference with get_task_impacts()
    impacts: ImpactsList = {}

    for r in task.resources:
        impacts = merge_impacts_lists(impacts, get_resource_impact_list(r))

    for s in task.subtasks:
        impacts = merge_impacts_lists(impacts, get_task_impact_list(s))

    return impacts
'''

def get_task_impacts(
        task: Task,
) -> dict[str, Union[str, float, Any]]:  # TODO bad return value
    """
    Return a task impact for this one and its children
    :param: The Task to get the impacts from
    :return: TaskImpact with name, impact sources and subtasks
    """
    return {
        "id": task.id,
        "name": task.name,
        "impacts": [
            {key.value: str(value)} for key, value in get_task_environmental_impact(task).impacts.items() #TODO . . . . .
        ],
        "subtasks": [get_task_impacts(r) for r in task.subtasks],
    }


def get_task_impact_by_resource_type(task: Task) -> dict[str, EnvironmentalImpact]:
    """
    Return all _impacts grouped by resource type, int the format of ResourcesList:

     {'People': {'CO2': 2000.0}}
     {'Build': {'CO2': 234325.0}}
    :return: ResourceList containing resources for this task
    """

    def merge_resource_list(
            first_list: dict[str, EnvironmentalImpact], second_list: dict[str, EnvironmentalImpact]
    ) -> dict[str, EnvironmentalImpact]:
        """
        Merge two list of Resource, adding them if they are in each list or merge them
        :param first_list: first list to merge
        :param second_list: second list to merge with
        :return: a new list containing the parameters merged
        """

        result_list = {**first_list, **second_list}
        for resource_type, _ in result.items():
            if resource_type in first_list and resource_type in second_list:
                result_list[resource_type].add(second_list[resource_type])
        return result_list

    result: dict[str, EnvironmentalImpact] = {}

    for r in task.resources:
        result = merge_resource_list(
            result, {r.type: get_resource_environmental_impact(r)}
        )

    for s in task.subtasks:
        result = merge_resource_list(
            result, get_task_impact_by_resource_type(s)
        )

    return result


############
# Resource #
############


def get_resource_impact(
        resource: Resource, impact_indicator: ImpactIndicator
) -> Quantity[Any]:
    resource_impacts = load_resource_impacts_source(resource.type)

    impacts: List[Quantity[Any]] = [
        i.impacts_list[impact_indicator] * resource.value for i in resource_impacts
    ]

    return Q_(sum(impacts))

def get_resource_environmental_impact(resource: Resource) -> EnvironmentalImpact:
    resource_impacts = load_resource_impacts_source(resource.type)
    environmental_impact = EnvironmentalImpact()

    for impact_source in resource_impacts:
        impact_source_quantities = EnvironmentalImpact() # TODO why do we create two objects ?

        for impact_indicator in impact_source.impacts_list:
            impact_source_quantities.impacts[impact_indicator] = (
                    impact_source.impacts_list[impact_indicator] * resource.value
            )

        environmental_impact.add(impact_source_quantities)

    return environmental_impact

'''
def get_resource_impact_list(
        resource: Resource,
) -> ImpactsList:
    resource_impacts = load_resource_impacts_source(resource.type)
    impacts: ImpactsList = {}

    for impact_source in resource_impacts:
        impact_source_quantities = {}

        for impact_indicator in impact_source.impacts_list:
            impact_source_quantities[impact_indicator] = (
                    impact_source.impacts_list[impact_indicator] * resource.value
            )

        impacts = merge_impacts_lists(impacts, impact_source_quantities)

    return impacts
'''