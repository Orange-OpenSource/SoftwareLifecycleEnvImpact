from __future__ import annotations

from typing import Any, List

from pint import Quantity

from api.data_model import Resource, Task
from impacts_model.impacts import EnvironmentalImpact, EnvironmentalImpactTree, ImpactIndicator
from impacts_model.templates import ResourceTemplate


########
# Task #
########
def get_task_environmental_impact(task: Task) -> EnvironmentalImpact:
    """
    Get a Task complete Environmental impact via an EnvironmentalImpact object
    :param task:the Task object to get the impact from
    :return: an EnvironmentImpact object with all the task environmental impacts
    """
    environmental_impact = EnvironmentalImpact()

    for r in task.resources:
        environmental_impact.add(get_resource_environmental_impact(r))

    for s in task.subtasks:
        environmental_impact.add(get_task_environmental_impact(s))

    return environmental_impact


def get_task_impact_by_indicator(
        task: Task, indicator: ImpactIndicator
) -> Quantity[Any]:
    """
    Compute and return a Task impact for a given ImpactIndicator
    :param task:the Task object to get the impact from
    :param indicator: the ImpactIndicator to get the value for the task
    :return: A quantity corresponding to the task ImpactIndicator chosen
    """
    impacts_resources: List[Quantity[Any]] = [
        get_resource_impact(r, indicator) for r in task.resources
    ]
    impacts_subtasks: List[Quantity[Any]] = [
        get_task_impact_by_indicator(s, indicator) for s in task.subtasks
    ]

    return sum(impacts_resources) + sum(impacts_subtasks)

def get_task_environmental_impact_tree(
        task: Task,
) -> EnvironmentalImpactTree:
    """
    Get a Task complete Environmental impact via an EnvironmentalImpact object as well as those of its subtasks
    Returns an EnvironmentalTree object
    :param task:the Task object to get the impact from
    :return: an EnvironmentImpactTree object with all the task environmental impacts
    """
    return EnvironmentalImpactTree(
        task=task,
        environmental_impact=get_task_environmental_impact(task),
        subtasks_impacts=[get_task_environmental_impact_tree(r) for r in task.subtasks]
    )


def get_task_impact_by_resource_type(task: Task) -> ResourcesEnvironmentalImpact:
    """
    Return a class environmental impact classified by its Resource types
    :param task: task to get the impact from
    :return: ResourcesEnvironmentalImpact object, with EnvironmentalImpact objects by resource type
    """
    result: ResourcesEnvironmentalImpact = {}

    for r in task.resources:
        impacts_to_add = get_resource_environmental_impact(r)
        if r.type in result:
            result[r.type].add(impacts_to_add)
        else:
            result[r.type] = impacts_to_add

    for s in task.subtasks:
        subtasks_impacts = get_task_impact_by_resource_type(s)
        for resource_type in subtasks_impacts:
            if resource_type in result:
                result[resource_type].add(subtasks_impacts[resource_type])
            else:
                result[resource_type] = subtasks_impacts[resource_type]

    return result


############
# Resource #
############
def get_resource_environmental_impact(resource: Resource) -> EnvironmentalImpact:
    """
    Get a resource complete environmental impact as an EnvironementalImapct object
    :param resource: the resource to get the impact from
    :return: an EnvironmentalImpact object with all resource impacts
    """
    resource_template = ResourceTemplate(resource.type)
    environmental_impact = EnvironmentalImpact()

    for impact_source in resource_template.impact_sources:
        for key in impact_source.environmental_impact.impacts:
            environmental_impact.add_impact(
                key, impact_source.environmental_impact.impacts[key] * resource.value
            )

    return environmental_impact


def get_resource_impact(
        resource: Resource, impact_indicator: ImpactIndicator
) -> Quantity[Any]:
    """
    Compute and return a resource environmental impct for an ImpactIndicator
    :param resource: the Resource object to view to impact from
    :param impact_indicator: The ImpactIndicator to retrieve the impact
    :return: A quantity corresponding to the resource ImpactIndicator quantity
    """
    resource_template = ResourceTemplate(resource.type)

    impacts: List[Quantity[Any]] = [
        i.environmental_impact.impacts[impact_indicator] * resource.value
        for i in resource_template.impact_sources
    ]

    return sum(impacts)
