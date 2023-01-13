from __future__ import annotations
from copy import deepcopy
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
        """
        Add another impact_value to this one
        """
        if second_impact.manufacture is not None:
            if self.manufacture is not None:
                self.manufacture += second_impact.manufacture
            else:
                # If self.manufacture is None, set it a the one to add
                self.manufacture = second_impact.manufacture

        if second_impact.use is not None:
            if self.use is not None:
                self.use += second_impact.use
            else:
                # If self.use is None, set it a the one to add
                self.use = second_impact.use

    def divide_by(self, unit: Unit) -> None:
        """
        Divide both manufacture and use by a unit, if they exists
        """
        self.manufacture = (
            self.manufacture / unit if self.manufacture is not None else None
        )
        self.use = self.use / unit if self.use is not None else None

    def divided_by(
        self, unit: Unit
    ) -> ImpactValue:  # TODO regarder pour changer cettre cfonction et update direct
        """
        Divide both manufacture and use by a unit, if they exists
        """
        return ImpactValue(
            manufacture=(
                self.manufacture / unit if self.manufacture is not None else None
            ),
            use=(self.use / unit if self.use is not None else None),
        )

    def multiplied_by(
        self, value: Quantity[Any]
    ) -> ImpactValue:  # TODO regarder pour changer cettre cfonction et update direct
        """
        Return a a new ImpactValue multiplied by the Quantity as parameter
        """
        return ImpactValue(
            manufacture=(
                (self.manufacture * value).to_reduced_units()
                if self.manufacture is not None
                else None
            ),
            use=(
                (self.use * value).to_reduced_units() if self.use is not None else None
            ),
        )


class ImpactValueSchema(Schema):
    manufacture = Nested("QuantitySchema")
    use = Nested("QuantitySchema")


class ImpactSourceImpact:
    def __init__(
        self,
        impact_source_id: str,
        total: EnvironmentalImpact,
        sub_impacts: dict[ImpactSourceId, ImpactSourceImpact],
    ) -> None:
        self.impact_source_id = impact_source_id
        self.total = total
        self.sub_impacts = sub_impacts

    def add(self, other: ImpactSourceImpact) -> None:
        """
        Add another ImpactSourceImpact into this one
        """
        self.total = merge_env_impact(self.total, other.total)

        for sub_impact in other.sub_impacts:
            if sub_impact in self.sub_impacts:
                self.sub_impacts[sub_impact].add(other.sub_impacts[sub_impact])
            else:
                self.sub_impacts[sub_impact] = other.sub_impacts[sub_impact]

    def multiply_by(self, amount: Quantity[Any]) -> None:
        """
        Multiply all impacts, and sub ones, by given amount
        """
        # Multiply all category of total
        for category in self.total:
            self.total[category] = self.total[category].multiplied_by(amount)

        # Multiply sub impacts as well
        for sub_impact in self.sub_impacts:
            self.sub_impacts[sub_impact].multiply_by(amount)

    def divide_by(self, unit: Unit) -> None:
        """
        Divide all impacts, and sub ones, by given amount
        """
        # Divide all category of total
        for category in self.total:
            self.total[category] = self.total[category].divided_by(unit)

        # Divide sub impacts as well
        for sub_impact in self.sub_impacts:
            self.sub_impacts[sub_impact].divide_by(unit)


class ImpactSourceImpactSchema(Schema):
    impact_source_id = fields.Str()
    total = fields.Dict(keys=fields.Str(), values=Nested("ImpactValueSchema"))
    sub_impacts = fields.Dict(
        keys=fields.Str(), values=Nested("ImpactSourceImpactSchema")
    )


class TaskImpact:
    def __init__(
        self,
        task_id: str,
        total: EnvironmentalImpact,
        sub_tasks: list[TaskImpact],
        impact_sources: dict[ImpactSourceId, ImpactSourceImpact],
    ) -> None:
        self.task_id = task_id
        self.total = total
        self.sub_tasks = sub_tasks
        self.impact_sources = impact_sources


class TaskImpactSchema(Schema):
    task_id = fields.Str()
    total = fields.Dict(keys=fields.Str(), values=Nested("ImpactValueSchema"))
    sub_tasks = fields.Nested("TaskImpactSchema", many=True)
    impact_sources = fields.Dict(
        keys=fields.Str(), values=Nested("ImpactSourceImpactSchema")
    )


EnvironmentalImpact = dict[ImpactCategory, ImpactValue]


ImpactSourceId = str


def merge_env_impact(
    first: EnvironmentalImpact, second: EnvironmentalImpact
) -> EnvironmentalImpact:
    """
    Merge two EnvironmentalImpact into one
    """
    # Init an empty EnvironmentalImpact to return
    result: EnvironmentalImpact = {}

    # Add all items from first EnvironmentalImpact
    for category, value in first.items():
        add_impact(result, category, value)

    # Add all items from second EnvironmentalImpact
    for category, value in second.items():
        add_impact(result, category, value)

    return result


def add_impact(
    environmental_impact: EnvironmentalImpact,
    category: ImpactCategory,
    value: ImpactValue,
) -> EnvironmentalImpact:
    """
    Add an ImpactCategory with this quantity in self impacts
    For each of its ImpactCategorys, append the quantity if it exists in the list, create it if not
    :param category: ImpactCategory to add
    :param value: corresponding quantity
    :return: None
    """
    if category not in environmental_impact:
        environmental_impact[category] = ImpactValue()
    environmental_impact[category].add_impact(value)

    return environmental_impact
