from __future__ import annotations

from enum import Enum
from typing import Any

from marshmallow import fields, post_dump, Schema
from pint import Quantity


class ImpactCategory(str, Enum):
    """
    Enum defining all the environmental impact categorys, as used in LCAs
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

    def __str__(self) -> Any:
        """Allow for Marshmallow to serialize the value, not the name"""
        return self.value


#######################
# AggregatedImpact #
#######################
class AggregatedImpact:
    """
    Class to aggregate impact categorys with their associated quantities
    Helpers method to easily merge_aggregated_impact a single impact, a list or another AggregatedImpact object
    """

    def __init__(self, impacts: dict[ImpactCategory, Quantity[Any]] = None) -> None:
        self.impacts: dict[ImpactCategory, Quantity[Any]] = (
            impacts if impacts is not None else {}
        )

    def merge_aggregated_impact(self, other: AggregatedImpact) -> None:
        """
        Merge another aggregated impact into this one. For each of its ImpactCategory, append the quantity if it exists in the list, create it if not
        :param other: the AggregatedImpact object to merge
        :return: None
        """
        self.merge_dict(other.impacts)

    def merge_dict(self, dict_to_add: dict[ImpactCategory, Quantity[Any]]) -> None:
        """
        Merge another dict with a quantity for an ImpactCategory into this object impacts
        For each of its ImpactCategorys, append the quantity if it exists in the list, create it if not
        :param dict_to_add: the dict to merge with self impacts
        :return: None
        """
        for impact_category in dict_to_add:
            self.merge_impact(impact_category, dict_to_add[impact_category])

    def merge_impact(self, category: ImpactCategory, value: Quantity[Any]) -> None:
        """
        Add an ImpactCategory with this quantity in self impacts
        For each of its ImpactCategorys, append the quantity if it exists in the list, create it if not
        :param category: ImpactCategory to merge
        :param value: corresponding quantity
        :return: None
        """
        if category in self.impacts:
            self.impacts[category] += value
        else:
            self.impacts[category] = value


class AggregatedImpactSchema(Schema):
    """Marshmallow schema to serialize a AggregatedImpactSchema object"""

    impacts = fields.Dict(keys=fields.Str(), values=fields.Str())

    @post_dump
    def translate_quantities(self, in_data, **kwargs) -> dict[str, dict[str, float | str]]:  # type: ignore
        """Translate pint quantities to dict before serialization, example for one ImpactCategory entry:
        {
            'value': 12421.4213,
            'unit': "KG_CO2E",
        }
        """
        out_data: dict[str, dict[str, float | str]] = {}
        if "impacts" in in_data:
            for impact_category_name in in_data["impacts"]:
                split = str(in_data["impacts"][impact_category_name]).split()
                out_data[
                    impact_category_name.replace("ImpactCategory.", "")
                ] = {  # TODO what is this, should be tested
                    "value": round(float(split[0]), 2),
                    "unit": split[1],
                }
        return out_data


class TaskImpact:
    def __init__(
        self,
        task_id: int,
        task_impact: AggregatedImpact,
        subtasks: dict[int, AggregatedImpact],
        resources: AggregatedImpactByResource,
    ):
        self.task_id = task_id
        self.task_impact = task_impact
        self.subtasks = subtasks
        self.resources = resources


class TaskImpactSchema(Schema):
    task_id = fields.Integer()
    task_impact = fields.Nested("AggregatedImpactSchema")
    subtasks = fields.Dict(
        keys=fields.Integer(), values=fields.Nested("AggregatedImpactSchema")
    )
    resources = fields.Dict(
        keys=fields.Str(), values=fields.Nested("AggregatedImpactSchema")
    )


##############################
# AggregatedImpactByResource #
##############################

AggregatedImpactByResource = dict[str, AggregatedImpact]
