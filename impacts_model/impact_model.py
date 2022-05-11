from typing import Any, List

from pint import Quantity

from api.data_model import Resource, Task
from impacts_model.impacts.impacts import ImpactIndicator, ImpactsList, merge_impacts_lists
from impacts_model.quantities import Q_
from impacts_model.templates import resource_factory


def get_project_impact_by_resource(root_task: Task):
    return {
        "id": root_task.id,
        "name": root_task.name,
        "impacts": [{key.value: str(value)} for key, value in get_task_impact_list(root_task).items()],
        "subtasks": [get_project_impact_by_task(r) for r in root_task.subtasks],
    }

def get_project_impact_by_task(root_task: Task):
    return {
        "id": root_task.id,
        "name": root_task.name,
        "impacts": [{key.value: str(value)} for key, value in get_task_impact_list(root_task).items()],
        "subtasks": [get_project_impact_by_task(r) for r in root_task.subtasks],
    }


def get_task_impact_list(task: Task):
    impacts: ImpactsList = {}

    for r in task.resources:
        impacts = merge_impacts_lists(impacts, get_resource_impact_list(r))

    for s in task.subtasks:
        impacts = merge_impacts_lists(impacts, get_task_impact_list(s))

    return impacts


def get_impact_by_indicator(task: Task, indicator: ImpactIndicator) -> Quantity[Any]:
    impacts_resources: List[Quantity[Any]] = [
        get_resource_impact(r, indicator) for r in task.resources
    ]
    impacts_subtasks: List[Quantity[Any]] = [
        get_impact_by_indicator(s, indicator) for s in task.subtasks
    ]

    return Q_(sum(impacts_resources) + sum(impacts_subtasks))  # type: ignore
    # TODO why Q_ here ?


def get_resource_impact(resource: Resource, impact_indicator: ImpactIndicator) -> Quantity[Any]:
    resource_impacts = resource_factory(resource.type)

    impacts: List[Quantity[Any]] = [
        i.impacts_list[impact_indicator] * resource.value for i in resource_impacts._impacts
    ]

    return Q_(sum(impacts))

def get_resource_impact_list(resource: Resource,) -> ImpactsList:
    resource_impacts = resource_factory(resource.type)
    impacts: ImpactsList = {}

    for impact_source in resource_impacts._impacts:
        impact_source_quantities = {}

        for impact_indicator in impact_source.impacts_list:
            impact_source_quantities[impact_indicator] = (
                    impact_source.impacts_list[impact_indicator] * resource.value
            )

        impacts = merge_impacts_lists(impacts, impact_source_quantities)

    return impacts
