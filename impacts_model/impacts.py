from __future__ import annotations

from enum import Enum
from typing import Any

from pint import Quantity


class ImpactIndicator(str, Enum):
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


#######################
# EnvironmentalImpact #
#######################
class EnvironmentalImpact:
    """
    EnvironmentalImpact class, encapsulating all ImpactIndicator as a list, with the corresponding quantity for each of them
    """
    def __init__(self, impacts: dict[ImpactIndicator, Quantity[Any]] = None) -> None:
        self.impacts: dict[
            ImpactIndicator, Quantity[Any]
        ] = (  # TODO impact_sources are accessed everytime ?
            impacts if impacts is not None else {}
        )

    def add(self, other: EnvironmentalImpact) -> None:
        """
        Merge another EnvironmentalObject into this one
        :param other: the EnvironmentalObject to get
        :return: None
        """
        self.add_dict(other.impacts)

    def add_dict(self, dict_to_add: dict[ImpactIndicator, Quantity[Any]]) -> None:
        """
        Merge another dict of ImpactIndicator with their corresponding quantity into self
        :param dict_to_add: the dict to merge with self.impacts
        :return: None
        """
        for impact_indicator in dict_to_add:
            self.add_impact(impact_indicator, dict_to_add[impact_indicator])

    def add_impact(self, indicator: ImpactIndicator, value: Quantity[Any]) -> None:
        """
        Add an ImpactIndicator with this value in self.impacts
        Add to corresponding value in self.impacts if it exists, create it else
        :param indicator: ImpactIndicator to add
        :param value: corresponding calue
        :return: None
        """
        if indicator in self.impacts:
            self.impacts[indicator] += value
        else:
            self.impacts[indicator] = value
