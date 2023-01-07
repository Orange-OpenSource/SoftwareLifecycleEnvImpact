from __future__ import annotations
from dataclasses import dataclass

from enum import Enum
from typing import Any, List, Optional
from marshmallow_sqlalchemy.fields import Nested
from marshmallow import fields, post_dump, Schema
from pint import Quantity, Unit

from impacts_model.quantities.quantities import (
    CUBIC_METER,
    DISEASE_INCIDENCE,
    ELECTRONIC_WASTE,
    KG_BQ_U235E,
    KG_CO2E,
    KG_SBE,
    MOL_HPOS,
    PRIMARY_MJ,
    TONNE_MIPS,
    deserialize_quantity,
)


class ImpactCategory(str, Enum):
    """
    Enum defining all the environmental impact categorys, as used in LCAs
    """

    CLIMATE_CHANGE = KG_CO2E
    RESOURCE_DEPLETION = KG_SBE
    ACIDIFICATION = MOL_HPOS
    FINE_PARTICLES = DISEASE_INCIDENCE
    IONIZING_RADIATIONS = KG_BQ_U235E
    WATER_DEPLETION = CUBIC_METER
    ELECTRONIC_WASTE = ELECTRONIC_WASTE
    PRIMARY_ENERGY = PRIMARY_MJ
    RAW_MATERIALS = TONNE_MIPS

    def __str__(self) -> Any:
        """
        Allow for Marshmallow to serialize the readable name
        Return not implemented if value cannot be found
        """
        return {
            "CLIMATE_CHANGE": "Climate change",
            "RESOURCE_DEPLETION": "Natural resources depletion",
            "ACIDIFICATION": "Acidification",
            "FINE_PARTICLES": "Fine particles",
            "IONIZING_RADIATIONS": "Ionizing radiations",
            "WATER_DEPLETION": "Water depletion",
            "ELECTRONIC_WASTE": "Electronic waste",
            "PRIMARY_ENERGY": "Primary energy consumption",
            "RAW_MATERIALS": "Raw materials",
        }.get(self.name, self.name + " not implemented")


###############
# ImpactValue #
###############
class ImpactValue:
    def __init__(
        self,
        manufacture: Optional[Quantity[Any]] = None,
        use: Optional[Quantity[Any]] = None,
    ) -> None:
        self.manufacture = deserialize_quantity(manufacture)
        self.use = deserialize_quantity(use)

    def add_impact(self, second_impact: ImpactValue) -> None:
        if second_impact.manufacture is not None:
            if self.manufacture is not None:
                self.manufacture += second_impact.manufacture
            else:
                self.manufacture = second_impact.manufacture

        if second_impact.use is not None:
            if self.use is not None:
                self.use += second_impact.use
            else:
                self.use = second_impact.use

    def divided_by(self, unit: Unit) -> ImpactValue:
        return ImpactValue(
            manufacture=(
                self.manufacture / unit if self.manufacture is not None else None
            ),
            use=(self.use / unit if self.use is not None else None),
        )

    def multiplied_by(self, value: Quantity[Any]) -> ImpactValue:
        return ImpactValue(
            manufacture=(
                (self.manufacture * value).to_reduced_units()
                if self.manufacture is not None
                else None
            ),
            use=(
                (self.use * value).to_reduced_units()
                if self.use is not None
                else None
            ),
        )


#######################
# EnvironmentalImpact #
#######################
class EnvironmentalImpact:
    """
    Class to aggregate impact categorys with their associated quantities
    Helpers method to easily add a single impact, a list or another EnvironmentalImpact object
    """

    def __init__(self, impacts: dict[ImpactCategory, ImpactValue] = None) -> None:
        # KEEP NONE IN CONSTRUCTOR, else reference errors
        self.impacts: dict[ImpactCategory, ImpactValue] = (
            impacts if impacts is not None else {}
        )

    def add(self, other: EnvironmentalImpact) -> None:
        """
        Add another aggregated impact into this one. For each of its ImpactCategory, append the quantity if it exists in the list, create it if not
        :param other: the EnvironmentalImpact object to add
        :return: None
        """
        self._add_dict(other.impacts)

    def _add_dict(self, dict_to_add: dict[ImpactCategory, ImpactValue]) -> None:
        """
        Add another dict with a quantity for an ImpactCategory to this object impacts
        For each of its ImpactCategorys, append the quantity if it exists in the list, create it if not
        :param dict_to_add: the dict to add with self impacts
        :return: None
        """
        for impact_category in dict_to_add:
            self.add_impact(impact_category, dict_to_add[impact_category])

    def add_impact(self, category: ImpactCategory, value: ImpactValue) -> None:
        """
        Add an ImpactCategory with this quantity in self impacts
        For each of its ImpactCategorys, append the quantity if it exists in the list, create it if not
        :param category: ImpactCategory to add
        :param value: corresponding quantity
        :return: None
        """
        if category not in self.impacts:
            self.impacts[category] = ImpactValue()
        self.impacts[category].add_impact(value)


class EnvironmentalImpactSchema(Schema):
    """Marshmallow schema to serialize a EnvironmentalImpactSchema object"""

    impacts = fields.Dict(keys=fields.Str(), values=Nested("QuantitySchema"))


class TaskImpact:
    def __init__(
        self,
        task_id: int,
        task_impact: EnvironmentalImpact,
        subtasks: List[TaskImpact],
        resources: EnvironmentalImpactByResource,
    ):
        self.task_id = task_id
        self.task_impact = task_impact
        self.subtasks = subtasks
        self.resources = resources


class TaskImpactSchema(Schema):
    task_id = fields.Integer()
    task_impact = fields.Nested("EnvironmentalImpactSchema")
    subtasks = fields.Nested("TaskImpactSchema", many=True)
    resources = fields.Dict(
        keys=fields.Str(), values=fields.Nested("EnvironmentalImpactSchema")
    )


##############################
# EnvironmentalImpactByResource #
##############################

ResourceName = str

EnvironmentalImpactByResource = dict[ResourceName, EnvironmentalImpact]
