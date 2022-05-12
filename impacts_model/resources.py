from typing import Any, List

import yaml
from pint import Quantity

from api.data_model import Resource
from impacts_model.impact_sources import (
    impact_source_factory,
    ImpactIndicator,
    ImpactsList,
    ImpactSource,
    merge_impacts_lists,
)
from impacts_model.quantities import Q_


class ResourceTemplate:
    def __init__(self, name: str, impacts: List[ImpactSource]):
        self.name = name
        self.impacts = impacts

def load_resource_impacts(name: str) -> List[ImpactSource]:
    name = name.replace(".yaml", "")
    with open("impacts_model/res/resources/" + name + ".yaml", "r") as stream:
        data_loaded = yaml.safe_load(stream)
        impacts_list = []
        for impact_name in data_loaded["impact_factors"]:
            impacts_list.append(impact_source_factory(impact_name))
        return impacts_list


def get_resource_impact(
    resource: Resource, impact_indicator: ImpactIndicator
) -> Quantity[Any]:
    resource_impacts = load_resource_impacts(resource.type)

    impacts: List[Quantity[Any]] = [
        i.impacts_list[impact_indicator] * resource.value
        for i in resource_impacts
    ]

    return Q_(sum(impacts))


def get_resource_impact_list(
    resource: Resource,
) -> ImpactsList:
    resource_impacts = load_resource_impacts(resource.type)
    impacts: ImpactsList = {}

    for impact_source in resource_impacts:
        impact_source_quantities = {}

        for impact_indicator in impact_source.impacts_list:
            impact_source_quantities[impact_indicator] = (
                impact_source.impacts_list[impact_indicator] * resource.value
            )

        impacts = merge_impacts_lists(impacts, impact_source_quantities)

    return impacts


ResourceName = str
ResourcesList = dict[ResourceName, ImpactsList]


def merge_resource_list(
    first_list: ResourcesList, second_list: ResourcesList
) -> ResourcesList:
    """
    Merge two list of Resource, adding them if they are in each list or merge them
    :param first_list: first list to merge
    :param second_list: second list to merge with
    :return: a new list containing the parameters merged
    """

    result = {**first_list, **second_list}
    for resource_name, _ in result.items():
        if resource_name in first_list and resource_name in second_list:
            result[resource_name] = merge_impacts_lists(
                first_list[resource_name], second_list[resource_name]
            )
    return result
