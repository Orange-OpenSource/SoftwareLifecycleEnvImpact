from __future__ import annotations

from enum import Enum
from typing import Any, List

from marshmallow import fields, post_dump, Schema
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
# AggregatedImpact #
#######################
class AggregatedImpact:
    """
    Class to aggregate impact indicators with their associated quantities
    Helpers method to easily merge_aggregated_impact a single impact, a list or another AggregatedImpact object
    """

    def __init__(self, impacts: dict[ImpactIndicator, Quantity[Any]] = None) -> None:
        self.impacts: dict[ImpactIndicator, Quantity[Any]] = (
            impacts if impacts is not None else {}
        )

    def merge_aggregated_impact(self, other: AggregatedImpact) -> None:
        """
        Merge another aggregated impact into this one. For each of its ImpactIndicators, append the quantity if it exists in the list, create it if not
        :param other: the AggregatedImpact object to merge
        :return: None
        """
        self.merge_dict(other.impacts)

    def merge_dict(self, dict_to_add: dict[ImpactIndicator, Quantity[Any]]) -> None:
        """
        Merge another dict with a quantity for an ImpactIndicator into this object impacts
        For each of its ImpactIndicators, append the quantity if it exists in the list, create it if not
        :param dict_to_add: the dict to merge with self impacts
        :return: None
        """
        for impact_indicator in dict_to_add:
            self.merge_impact(impact_indicator, dict_to_add[impact_indicator])

    def merge_impact(self, indicator: ImpactIndicator, value: Quantity[Any]) -> None:
        """
        Add an ImpactIndicator with this quantity in self impacts
        For each of its ImpactIndicators, append the quantity if it exists in the list, create it if not
        :param indicator: ImpactIndicator to merge
        :param value: corresponding quantity
        :return: None
        """
        if indicator in self.impacts:
            self.impacts[indicator] += value
        else:
            self.impacts[indicator] = value


class AggregatedImpactSchema(Schema):
    """Marshmallow schema to serialize a AggregatedImpactSchema object"""

    impacts = fields.Dict(keys=fields.Str(), values=fields.Str())

    @post_dump
    def translate_quantities(self, in_data, **kwargs) -> dict[str, str]:  # type: ignore
        """Translate pint quantities to str before serialization"""
        out_data: dict[str, str] = {}
        if "impacts" in in_data:
            for impact_indicator_name in in_data["impacts"]:
                out_data[impact_indicator_name.replace("ImpactIndicator.", "")] = str(
                    in_data["impacts"][impact_indicator_name])
        return out_data


class TaskImpact:
    def __init__(
            self,
            task_impact: AggregatedImpact,
            subtasks: List[AggregatedImpact],
            resources: AggregatedImpactByResource
    ):
        self.task_impact = task_impact
        self.subtasks = subtasks
        self.resources = resources


class TaskImpactSchema(Schema):
    task_impact = fields.Nested("AggregatedImpactSchema")
    subtasks = fields.Nested("AggregatedImpactSchema", many=True)
    resources = fields.Dict(keys=fields.Str(), values=fields.Nested("AggregatedImpactSchema"))


##############################
# AggregatedImpactByResource #
##############################

AggregatedImpactByResource = dict[str, AggregatedImpact]
