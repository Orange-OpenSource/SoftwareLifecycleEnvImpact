from __future__ import annotations
from copy import deepcopy
import re
from impacts_model.impacts import (
    EnvironmentalImpact,
    ImpactSourceId,
    ImpactValue,
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
    A source of environmental impact_sources
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
        self._environmental_impact = environmental_impact
        self.uses = uses if uses is not None else []
        self.unit = deserialize_unit(unit)

        # Set as impact per ImpactSource unit
        self._environmental_impact.divide_by(self.unit)

        self.source = source
        self.methodology = methodology

    def get_environmental_impact(self) -> EnvironmentalImpact:
        # If does not have element is uses, directly return the impact
        if len(self.uses) == 0:
            return self._environmental_impact

        # Else, add impacts from uses

        # Copy the ImpactSource impact to avoid modifying it directly
        result = deepcopy(self._environmental_impact)

        # Itearate through uses
        for use in self.uses:
            # deserialize the impact source and amount
            impact_source = impact_source_factory(use["resource_id"])
            amount = deserialize_quantity(use["quantity"])

            if amount:
                resource_impact = EnvironmentalImpact()
                # For each impact
                for (category, value,) in (
                    impact_source.get_environmental_impact().get_total().items()
                ):
                    # Compute the other resource quantity consumed
                    res = value.multiplied_by(amount)
                    # Set as quantity per this ImpactSource unit
                    res.divide_by(self.unit)
                    # Add category and value to EnvironmentalImpact
                    resource_impact.add_impact(category, res)

                # Add this impact source and its impact to the result
                result.add_impact_source_impact({impact_source.id: resource_impact})
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
        fields = loader.construct_mapping(node, deep=True)
        return EnvironmentalImpact(**fields)

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
        raise ImpactSourceError("No corresponding impact source")
    return res
