from typing import Any, List

from pint import Quantity

from api.data_model import Resource, Task
from impacts_model.impacts.impacts import ImpactIndicator
from impacts_model.quantities import Q_
from impacts_model.templates import resource_factory


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
