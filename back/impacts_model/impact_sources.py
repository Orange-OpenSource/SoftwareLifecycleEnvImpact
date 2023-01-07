from __future__ import annotations

import importlib
import inspect
import re
from impacts_model.impacts import EnvironmentalImpact, ImpactCategory, ImpactValue
from pint import Quantity, Unit
from typing import Any, Optional
import yaml
from impacts_model.quantities.quantities import (
    deserialize_quantity,
    deserialize_unit,
)
from marshmallow import Schema, fields


class ImpactSource:
    """
    A source of environmental impact_sources
    """

    def __init__(
        self,
        id: str,
        name: str,
        unit: str | Unit,
        climate_change: ImpactValue,
        resource_depletion: ImpactValue = ImpactValue(
            manufacture="0 " + ImpactCategory.RESOURCE_DEPLETION.value,
            use="0 " + ImpactCategory.RESOURCE_DEPLETION.value,
        ),
        acidification: ImpactValue = ImpactValue(
            manufacture="0 " + ImpactCategory.ACIDIFICATION.value,
            use="0 " + ImpactCategory.ACIDIFICATION.value,
        ),
        fine_particles: ImpactValue = ImpactValue(
            manufacture="0 " + ImpactCategory.FINE_PARTICLES.value,
            use="0 " + ImpactCategory.FINE_PARTICLES.value,
        ),
        ionizing_radiations: ImpactValue = ImpactValue(
            manufacture="0 " + ImpactCategory.IONIZING_RADIATIONS.value,
            use="0 " + ImpactCategory.IONIZING_RADIATIONS.value,
        ),
        water_depletion: ImpactValue = ImpactValue(
            manufacture="0 " + ImpactCategory.WATER_DEPLETION.value,
            use="0 " + ImpactCategory.WATER_DEPLETION.value,
        ),
        electronic_waste: ImpactValue = ImpactValue(
            manufacture="0 " + ImpactCategory.ELECTRONIC_WASTE.value,
            use="0 " + ImpactCategory.ELECTRONIC_WASTE.value,
        ),
        primary_energy_consumption: ImpactValue = ImpactValue(
            manufacture="0 " + ImpactCategory.PRIMARY_ENERGY.value,
            use="0 " + ImpactCategory.PRIMARY_ENERGY.value,
        ),
        raw_materials: ImpactValue = ImpactValue(
            "0 " + ImpactCategory.RAW_MATERIALS.value,
            "0 " + ImpactCategory.RAW_MATERIALS.value,
        ),
        source: str = "",
        methodology: str = "",
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

        # TODO why this here ? Try to remove parts in yaml and see
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

        self.id = id
        self.name = name
        self.unit = deserialize_unit(unit)

        self.climate_change = climate_change.divided_by(self.unit)
        self.resource_depletion = resource_depletion.divided_by(self.unit)
        self.acidification = acidification.divided_by(self.unit)
        self.fine_particles = fine_particles.divided_by(self.unit)
        self.ionizing_radiations = ionizing_radiations.divided_by(self.unit)
        self.water_depletion = water_depletion.divided_by(self.unit)
        self.electronic_waste = electronic_waste.divided_by(self.unit)
        self.primary_energy_consumption = primary_energy_consumption.divided_by(
            self.unit
        )
        self.raw_materials = raw_materials.divided_by(self.unit)

        self.source = source
        self.methodology = methodology

    @property
    def environmental_impact(
        self,
    ) -> EnvironmentalImpact:
        """
        Getter for co2 property
        :return: co2 as float
        """
        return EnvironmentalImpact(
            impacts={
                ImpactCategory.CLIMATE_CHANGE: self.climate_change,
                ImpactCategory.RESOURCE_DEPLETION: self.resource_depletion,
                ImpactCategory.ACIDIFICATION: self.acidification,
                ImpactCategory.FINE_PARTICLES: self.fine_particles,
                ImpactCategory.IONIZING_RADIATIONS: self.ionizing_radiations,
                ImpactCategory.WATER_DEPLETION: self.water_depletion,
                ImpactCategory.ELECTRONIC_WASTE: self.electronic_waste,
                ImpactCategory.PRIMARY_ENERGY: self.primary_energy_consumption,
                ImpactCategory.RAW_MATERIALS: self.raw_materials,
            }
        )

    @property
    def has_time_input(self) -> bool:
        units_split = re.split(r"[*,/]", str(self.unit))
        units_split_len = len(units_split)
        if units_split_len < 2:
            return False
        else:
            return deserialize_quantity(1 * units_split[0]).check(
                "[time]"
            ) or deserialize_quantity(1 * units_split[1]).check("[time]")


class ImpactSourceSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    unit = fields.Str()
    source = fields.Str(
        allow_none=True,
    )
    methodology = fields.Str(
        allow_none=True,
    )


def _get_all_impact_sources() -> list[ImpactSource]:
    def constructor(loader, node):
        fields = loader.construct_mapping(node)
        return ImpactSource(**fields)

    def constructor2(loader, node) -> ImpactValue:
        fields = loader.construct_mapping(node)
        return ImpactValue(**fields)

    yaml.add_constructor("!ImpactSource", constructor)
    yaml.add_constructor("!ImpactValue", constructor2)

    list = []
    with open("impacts_model/data/impact_sources/default.yaml", "r") as stream:
        data_loaded = yaml.load_all(stream, Loader=yaml.Loader)
        for data in data_loaded:
            list.append(data)
    return list


impact_sources = _get_all_impact_sources()


class ImpactSourceError(Exception):
    pass


def impact_source_factory(id: str) -> ImpactSource:
    """
    Factory class to create an ImpactSource object from its id
    :param id: id of the ImpactSource to create
    :return: an ImpactSource object
    """
    res = next((x for x in impact_sources if x.id == id), None)
    if res is None:
        raise ImpactSourceError("No corresponding impact source")
    return res
