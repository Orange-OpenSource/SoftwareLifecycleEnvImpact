# BSD-3-Clause License
#
# Copyright 2017 Orange
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations
from copy import deepcopy
import re
from impacts_model.impacts import (
    EnvironmentalImpact,
    ImpactCategory,
    ImpactSourceId,
    ImpactSourceImpact,
    ImpactValue,
    merge_env_impact,
)
from pint import Unit
import yaml
from impacts_model.quantities.quantities import (
    deserialize_quantity,
    deserialize_unit,
)
from marshmallow import Schema, fields


class ImpactSource:
    """
    A source of environmental impact
    """

    def __init__(
        self,
        id: ImpactSourceId,
        name: str,
        unit: str | Unit,
        environmental_impact: EnvironmentalImpact,
        uses=[],
        source: str = "",
        methodology: str = "",
    ) -> None:

        self.id = id
        self.name = name
        self._own_impact = environmental_impact
        self.uses = uses if uses is not None else []
        self.unit = deserialize_unit(unit)

        self.source = source
        self.methodology = methodology

        # Set as impact per ImpactSource unit
        for impact in self._own_impact:
            self._own_impact[impact].divide_by(self.unit)

    def get_impact(self) -> ImpactSourceImpact:
        """
        Return this impact source impact for one unit
        """
        sub_impacts = self._get_sub_impacts()
        # total = self._get_total(sub_impacts)
        return ImpactSourceImpact(self.id, deepcopy(self._own_impact), sub_impacts)

    def _get_total(
        self, sub_impacts: dict[ImpactSourceId, ImpactSourceImpact]
    ) -> EnvironmentalImpact:
        """
        Return this ImpactSource EnvironmentalImpact, as the sum of its sub impact sources and own impact
        """
        # The result will always add this ImpactSource own impact
        total = deepcopy(self._own_impact)
        # Iterate though sub_impacts to sum them into the result
        for sub_impact in sub_impacts:
            total = merge_env_impact(total, sub_impacts[sub_impact].total_impact)
        return total

    def _get_sub_impacts(self) -> dict[ImpactSourceId, ImpactSourceImpact]:
        """
        Return a list of ImpactSourceImpact, for all the sub_impacts of this ImpactSource
        """
        result: dict[ImpactSourceId, ImpactSourceImpact] = {}

        # Iterate through impact source used
        for use in self.uses:
            # deserialize the impact source and amount
            impact_source = impact_source_factory(use["resource_id"])
            amount = deserialize_quantity(use["quantity"])

            if amount:
                impact = impact_source.get_impact()
                # Compute the other resource quantity consumed to remove its unit
                impact.multiply_by(amount)
                # Set as quantity per this ImpactSource unit
                impact.divide_by(self.unit)
                # Add to sub impacts list
                if impact_source.id in result:
                    result[impact_source.id].add(impact)
                else:
                    result[impact_source.id] = impact
        return result

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
    def impact_source_constructor(loader, node):
        fields = loader.construct_mapping(node, deep=True)
        return ImpactSource(**fields)

    def impact_value_constructor(loader, node) -> ImpactValue:
        fields = loader.construct_mapping(node, deep=True)
        return ImpactValue(**fields)

    def environmental_impact_constructor(loader, node) -> EnvironmentalImpact:
        """
        Useful to translate readable yaml categories to ImpactCategory
        Ex: climate_change to kg_co2
        """
        fields = loader.construct_mapping(node, deep=True)
        climate_change = fields["climate_change"]
        resource_depletion = fields["resource_depletion"]
        acidification = fields["acidification"]
        fine_particles = fields["fine_particles"]
        ionizing_radiations = fields["ionizing_radiations"]
        water_depletion = fields["water_depletion"]
        raw_materials = fields["raw_materials"]
        return {
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
            ImpactCategory.RAW_MATERIALS: raw_materials
            if raw_materials is not None
            else ImpactValue(),
        }

    yaml.add_constructor("!ImpactSource", impact_source_constructor)
    yaml.add_constructor("!ImpactValue", impact_value_constructor)
    yaml.add_constructor("!EnvironmentalImpact", environmental_impact_constructor)

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
        raise ImpactSourceError("No corresponding impact source: " + id)
    return res
