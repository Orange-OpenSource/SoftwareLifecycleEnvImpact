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

    def multiplied_by(self, value: Quantity[Any]) -> ImpactValue:
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


#######################
# EnvironmentalImpact #
#######################
class EnvironmentalImpact:
    """
    Class to aggregate impact categories with their associated quantities
    Helpers method to easily add a single impact, a list or another EnvironmentalImpact object
    """

    def __init__(
        self,
        climate_change: Optional[ImpactValue] = None,
        resource_depletion: Optional[ImpactValue] = None,
        acidification: Optional[ImpactValue] = None,
        fine_particles: Optional[ImpactValue] = None,
        ionizing_radiations: Optional[ImpactValue] = None,
        water_depletion: Optional[ImpactValue] = None,
        electronic_waste: Optional[ImpactValue] = None,
        primary_energy_consumption: Optional[ImpactValue] = None,
        raw_materials: Optional[ImpactValue] = None,
        impact_sources_impact: Optional[ImpactSourcesImpact] = None,
    ) -> None:
        """
        :param climate_change: Climate change as kgeqCO2
        :param resource_depletion: Depletion of natural abiotic resources as kgeqSb
        :param acidification: acidification (PEF-AP) as mol H+ eq
        :param ionizing_radiations: ionizing radiations ( PEF-IR) as kBq U235 eq
        :param water_depletion: Depletion of water resources (PEF-WU) as m3 world eq
        :param electronic_waste: mass of electrical and electronic waste generated as Tonne
        :param primary_energy_consumption: Primary energy consumed as MJ
        :param raw_materials: Raw materials consumed as Ton
        impact_sources_impact: sub impacts, with their respective impact_id as keys
        """
        # DO NOT PUT DIRECTLY IN PARAMETERS, pyyaml set them as None anyway
        self._impacts: dict[ImpactCategory, ImpactValue] = {
            ImpactCategory.CLIMATE_CHANGE: climate_change
            if climate_change is not None
            else ImpactValue(),
            ImpactCategory.RESOURCE_DEPLETION: resource_depletion
            if resource_depletion is not None
            else ImpactValue(),
            ImpactCategory.ACIDIFICATION: acidification
            if acidification is not None
            else ImpactValue(),
            ImpactCategory.FINE_PARTICLES: fine_particles
            if fine_particles is not None
            else ImpactValue(),
            ImpactCategory.IONIZING_RADIATIONS: ionizing_radiations
            if ionizing_radiations is not None
            else ImpactValue(),
            ImpactCategory.WATER_DEPLETION: water_depletion
            if water_depletion is not None
            else ImpactValue(),
            ImpactCategory.ELECTRONIC_WASTE: electronic_waste
            if electronic_waste is not None
            else ImpactValue(),
            ImpactCategory.PRIMARY_ENERGY: primary_energy_consumption
            if primary_energy_consumption is not None
            else ImpactValue(),
            ImpactCategory.RAW_MATERIALS: raw_materials
            if raw_materials is not None
            else ImpactValue(),
        }
        self.impact_sources_impact: ImpactSourcesImpact = (
            {} if impact_sources_impact is None else impact_sources_impact
        )

    def get_total(self) -> dict[ImpactCategory, ImpactValue]:
        """
        Compute and return the total of direct impacts as well as sub ones, i.e. classified by ImpactSource id
        """
        # Copy self impact to avoid data tempering
        result = deepcopy(self._impacts)

        # Iterate through impact_sources_impact to add their respective impacts to the total
        for impact_source_id in self.impact_sources_impact:
            # Retrieve the total impact for each ImpactSource
            total = self.impact_sources_impact[impact_source_id].get_total()

            # For each category, add to result
            for impact_category in total:
                if impact_category not in result:
                    result[impact_category] = ImpactValue()
                result[impact_category].add_impact(total[impact_category])
        return result

    def divide_by(self, unit: Unit) -> None:
        """
        Divide both _impacts and impact_sources_impact by given unit
        """
        for impact in self._impacts:
            self._impacts[impact].divide_by(unit)
        for resource in self.impact_sources_impact:
            self.impact_sources_impact[resource].divide_by(unit)

    def add(self, other: EnvironmentalImpact) -> None:
        """
        Merge another EnvironmentalImpact into this one.
        :param other: the EnvironmentalImpact object to add
        :return: None
        """
        # Add resource
        self.add_impact_source_impact(other.impact_sources_impact)
        # Add impact for each category
        for impact_category in other._impacts:
            self.add_impact(impact_category, other._impacts[impact_category])

    def add_impact_source_impact(self, other: ImpactSourcesImpact) -> None:
        """
        Merge another impact_source_impact into this one
        """
        for resource in other:
            if resource in self.impact_sources_impact:
                self.impact_sources_impact[resource].add(other[resource])
            else:
                self.impact_sources_impact[resource] = other[resource]

    def add_impact(self, category: ImpactCategory, value: ImpactValue) -> None:
        """
        Add an ImpactCategory with this quantity in self impacts
        For each of its ImpactCategorys, append the quantity if it exists in the list, create it if not
        :param category: ImpactCategory to add
        :param value: corresponding quantity
        :return: None
        """
        if category not in self._impacts:
            self._impacts[category] = ImpactValue()
        self._impacts[category].add_impact(value)


class EnvironmentalImpactSchema(Schema):
    """Marshmallow schema to serialize a EnvironmentalImpactSchema object"""

    impacts = fields.Dict(keys=fields.Str(), values=Nested("ImpactValueSchema"))


class TaskImpact:
    def __init__(
        self,
        task_id: int,
        task_impact: dict[ImpactCategory, ImpactValue],
        subtasks: List[TaskImpact],
        impact_sources: dict[ImpactSourceId, dict[ImpactCategory, ImpactValue]],
    ):
        self.task_id = task_id
        self.task_impact = task_impact
        self.subtasks = subtasks
        self.impact_sources = impact_sources


class TaskImpactSchema(Schema):
    task_id = fields.Integer()
    task_impact = fields.Dict(keys=fields.Str(), values=Nested("ImpactValueSchema"))
    subtasks = fields.Nested("TaskImpactSchema", many=True)
    impact_sources = fields.Dict(
        keys=fields.Str(),
        values=fields.Dict(keys=fields.Str(), values=Nested("ImpactValueSchema")),
    )


#######################
# ImpactSourcesImpact #
#######################

ImpactSourceId = str
ImpactSourcesImpact = dict[ImpactSourceId, EnvironmentalImpact]
