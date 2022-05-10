from __future__ import annotations

from enum import Enum
from typing import Any

from pint import Quantity


class ImpactIndicator(Enum):
    """
    Enum defining all the environmental impact indicators, as used in LCAs
    """

    CLIMATE_CHANGE = "Climate change"
    RESOURCE_DEPLETION = "Natural resources depletion"
    ACIDIFICATION = "Acidification"
    FINE_PARTICLES = "Fine particles"
    IONIZING_RADIATIONS = "Ionizing radiations"
    WATER_DEPLETION = "Water depletion"
    ELECTRONIC_WASTE = "Electronic waste"
    PRIMARY_ENERGY = "Primary energy consumption"
    RAW_MATERIALS = "Raw materials"


ImpactsList = dict[ImpactIndicator, Quantity[Any]]


def merge_impacts_lists(
    first_list: ImpactsList, second_list: ImpactsList
) -> ImpactsList:
    """
    Merge two list of impacts_list, adding them if they are in each list or merge them
    :param first_list: first list to merge
    :param second_list: second list to merge with
    :return: a new list containing the parameters merged
    """
    result = {**first_list, **second_list}
    for impact_indicator, _ in result.items():
        if impact_indicator in first_list and impact_indicator in second_list:
            result[impact_indicator] = (
                first_list[impact_indicator] + second_list[impact_indicator]
            )
    return result
