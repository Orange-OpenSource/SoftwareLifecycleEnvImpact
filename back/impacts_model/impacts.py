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

    def divide_by(self, unit: Unit) -> None:
        self.manufacture = (
            self.manufacture / unit if self.manufacture is not None else None
        )
        self.use = self.use / unit if self.use is not None else None

    def multiplied_by(self, value: Quantity[Any]) -> ImpactValue:
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
    Class to aggregate impact categorys with their associated quantities
    Helpers method to easily add a single impact, a list or another EnvironmentalImpact object
    """

    def __init__(
        self,
        climate_change: ImpactValue = None,
        resource_depletion: ImpactValue = None,
        acidification: ImpactValue = None,
        fine_particles: ImpactValue = None,
        ionizing_radiations: ImpactValue = None,
        water_depletion: ImpactValue = None,
        electronic_waste: ImpactValue = None,
        primary_energy_consumption: ImpactValue = None,
        raw_materials: ImpactValue = None,
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
        """
        # Do not put in constructor, pyyaml set them as None anyway
        if climate_change is None:
            climate_change = ImpactValue(
                manufacture="0 " + ImpactCategory.CLIMATE_CHANGE.value,
                use="0 " + ImpactCategory.CLIMATE_CHANGE.value,
            )
        if resource_depletion is None:
            resource_depletion = ImpactValue(
                manufacture="0 " + ImpactCategory.RESOURCE_DEPLETION.value,
                use="0 " + ImpactCategory.RESOURCE_DEPLETION.value,
            )
        if acidification is None:
            acidification = ImpactValue(
                manufacture="0 " + ImpactCategory.ACIDIFICATION.value,
                use="0 " + ImpactCategory.ACIDIFICATION.value,
            )
        if fine_particles is None:
            fine_particles = ImpactValue(
                manufacture="0 " + ImpactCategory.FINE_PARTICLES.value,
                use="0 " + ImpactCategory.FINE_PARTICLES.value,
            )
        if ionizing_radiations is None:
            ionizing_radiations = ImpactValue(
                manufacture="0 " + ImpactCategory.IONIZING_RADIATIONS.value,
                use="0 " + ImpactCategory.IONIZING_RADIATIONS.value,
            )
        if water_depletion is None:
            water_depletion = ImpactValue(
                manufacture="0 " + ImpactCategory.WATER_DEPLETION.value,
                use="0 " + ImpactCategory.WATER_DEPLETION.value,
            )
        if electronic_waste is None:
            electronic_waste = ImpactValue(
                manufacture="0 " + ImpactCategory.ELECTRONIC_WASTE.value,
                use="0 " + ImpactCategory.ELECTRONIC_WASTE.value,
            )
        if primary_energy_consumption is None:
            primary_energy_consumption = ImpactValue(
                manufacture="0 " + ImpactCategory.PRIMARY_ENERGY.value,
                use="0 " + ImpactCategory.PRIMARY_ENERGY.value,
            )
        if raw_materials is None:
            raw_materials = ImpactValue(
                "0 " + ImpactCategory.RAW_MATERIALS.value,
                "0 " + ImpactCategory.RAW_MATERIALS.value,
            )

        self.impacts: dict[ImpactCategory, ImpactValue] = {
            ImpactCategory.CLIMATE_CHANGE: climate_change,
            ImpactCategory.RESOURCE_DEPLETION: resource_depletion,
            ImpactCategory.ACIDIFICATION: acidification,
            ImpactCategory.FINE_PARTICLES: fine_particles,
            ImpactCategory.IONIZING_RADIATIONS: ionizing_radiations,
            ImpactCategory.WATER_DEPLETION: water_depletion,
            ImpactCategory.ELECTRONIC_WASTE: electronic_waste,
            ImpactCategory.PRIMARY_ENERGY: primary_energy_consumption,
            ImpactCategory.RAW_MATERIALS: raw_materials,
        }

    def divide_by(self, unit: Unit) -> None:
        for impact in self.impacts:
            self.impacts[impact].divide_by(unit)

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

    impacts = fields.Dict(keys=fields.Str(), values=Nested("ImpactValueSchema"))


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
