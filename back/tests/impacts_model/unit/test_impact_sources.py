from pint import Quantity, Unit
import yaml
from impacts_model.impact_sources import (
    ImpactSource,
    ImpactSourceSchema,
    _get_all_impact_sources,
    impact_source_factory,
)
from impacts_model.impacts import ImpactValue

from impacts_model.quantities.quantities import (
    DAY,
    KG_CO2E,
    SERVER,
    deserialize_quantity,
)


def test_impact_source_has_time_input() -> None:
    """
    Test computation of function has_time_input that should
    return true if the ImpactSource has a time in its unit, else False
    """

    # Test without time
    assert (
        ImpactSource(
            id="testid",
            name="test",
            unit=SERVER,
            climate_change=ImpactValue(1776 * KG_CO2E),
        ).has_time_input
        == False
    )

    # Test with time first
    assert (
        ImpactSource(
            id="testid",
            name="test",
            unit=DAY * SERVER,
            climate_change=ImpactValue(use=1776 * KG_CO2E),
        ).has_time_input
        == True
    )

    # Test with time second
    assert (
        ImpactSource(
            id="testid",
            name="test",
            unit=SERVER * DAY,
            climate_change=ImpactValue(use=1776 * KG_CO2E),
        ).has_time_input
        == True
    )

    # Test double magnitude without time
    assert (
        ImpactSource(
            id="testid",
            name="test",
            unit=SERVER * SERVER,
            climate_change=ImpactValue(use=1776 * KG_CO2E),
        ).has_time_input
        == False
    )


def test_yaml_loading() -> None:
    impact_sources = _get_all_impact_sources()
    assert len(impact_sources) > 0
    for impact_source in impact_sources:
        # Test each can be retrieved via the factory
        assert isinstance(impact_source_factory(impact_source.id), ImpactSource)

        # Assert unit is converted to a pint Unit
        assert isinstance(impact_source.unit, Unit)

        # Assert that co2 is set for all
        assert impact_source.climate_change is not None

        for indicator in impact_source.environmental_impact.impacts:
            # Test all environmentalImpact to see if they're rightly typed as ImpactValue
            assert isinstance(
                impact_source.environmental_impact.impacts[indicator], ImpactValue
            )

            # Test that we retrieve an impact with the right quantity if we remove the impact unit, ie for one unit
            impact_value = impact_source.environmental_impact.impacts[indicator]
            # For manufacture
            if impact_value.manufacture is not None:
                tmp = impact_value.manufacture * impact_source.unit
                assert tmp.units == indicator.value or tmp.dimensionless

            if impact_value.use is not None:
                tmp = impact_value.use * impact_source.unit
                assert tmp.units == indicator.value or tmp.dimensionless


def test_impact_source_factory() -> None:
    """Test that all ids from the yaml can be retrieved and have the right format"""
    list = []
    with open("impacts_model/data/impact_sources/default.yaml", "r") as stream:
        data_loaded = yaml.load_all(stream, Loader=yaml.Loader)
        for data in data_loaded:
            list.append(data.id)

    assert len(list) > 0
    for d in list:
        loaded_impact = impact_source_factory(d)
        assert isinstance(loaded_impact, ImpactSource)
