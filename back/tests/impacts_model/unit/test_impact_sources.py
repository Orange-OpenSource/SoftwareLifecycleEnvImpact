from unittest import mock
from unittest.mock import MagicMock
from pint import Quantity, Unit
import yaml
from impacts_model.impact_sources import (
    ImpactSource,
    ImpactSourceSchema,
    _get_all_impact_sources,
    impact_source_factory,
)
from impacts_model.impacts import EnvironmentalImpact, ImpactCategory, ImpactValue

from impacts_model.quantities.quantities import (
    DAY,
    KG_CO2E,
    PEOPLE,
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
            environmental_impact=EnvironmentalImpact(
                climate_change=ImpactValue(1776 * KG_CO2E)
            ),
        ).has_time_input
        == False
    )

    # Test with time first
    assert (
        ImpactSource(
            id="testid",
            name="test",
            unit=DAY * SERVER,
            environmental_impact=EnvironmentalImpact(
                climate_change=ImpactValue(use=1776 * KG_CO2E)
            ),
        ).has_time_input
        == True
    )

    # Test with time second
    assert (
        ImpactSource(
            id="testid",
            name="test",
            unit=SERVER * DAY,
            environmental_impact=EnvironmentalImpact(
                climate_change=ImpactValue(use=1776 * KG_CO2E)
            ),
        ).has_time_input
        == True
    )

    # Test double magnitude without time
    assert (
        ImpactSource(
            id="testid",
            name="test",
            unit=SERVER * SERVER,
            environmental_impact=EnvironmentalImpact(
                climate_change=ImpactValue(use=1776 * KG_CO2E)
            ),
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

        # Retrieve total
        total = impact_source.get_environmental_impact().get_total()

        # Assert that co2 is set for all
        assert total[ImpactCategory.CLIMATE_CHANGE] is not None

        for indicator in total:
            # Test all environmentalImpact to see if they're rightly typed as ImpactValue
            assert isinstance(
                total[indicator],
                ImpactValue,
            )

            # Test that we retrieve an impact with the right quantity if we remove the impact unit, ie for one unit
            impact_value = total[indicator]
            # For manufacture
            if impact_value.manufacture is not None:
                tmp = impact_value.manufacture * impact_source.unit
                assert tmp.units == indicator.value or tmp.dimensionless
            # For use
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


@mock.patch(
    "impacts_model.impact_sources.impact_source_factory",
    MagicMock(
        return_value=ImpactSource(
            id="testid",
            name="test",
            unit=SERVER,
            environmental_impact=EnvironmentalImpact(
                climate_change=ImpactValue(use=999 * KG_CO2E)
            ),
        ),
    ),
)
def test_impact_source_get_environmental_impact() -> None:
    # Test only direct impacts

    a = (
        ImpactSource(
            id="testid",
            name="test",
            unit=SERVER,
            environmental_impact=EnvironmentalImpact(
                climate_change=ImpactValue(use=1776 * KG_CO2E)
            ),
        )
        .get_environmental_impact()
        .get_total()[ImpactCategory.CLIMATE_CHANGE]
        .use
    )
    assert a == 1776 * (KG_CO2E / SERVER)

    # Test when using other resources
    i = ImpactSource(
        id="testid",
        name="test",
        unit=SERVER,
        uses=[
            {"quantity": "10 server", "resource_id": "testid"},
            {"quantity": "34 server", "resource_id": "testid"},
        ],
        environmental_impact=EnvironmentalImpact(
            climate_change=ImpactValue(use=1776 * KG_CO2E)
        ),
    )
    env_impact = i.get_environmental_impact()
    total = env_impact.get_total()
    use = total[ImpactCategory.CLIMATE_CHANGE].use

    assert use == 1776 * (KG_CO2E / SERVER) + 10 * (999 * KG_CO2E) + 34 * (
        999 * KG_CO2E
    )  # 45732


def test_impact_source_computation() -> None:
    assert impact_source_factory("people").get_environmental_impact().get_total()[
        ImpactCategory.CLIMATE_CHANGE
    ].use == 12.26836154188304 * KG_CO2E / (PEOPLE * DAY)
    assert impact_source_factory(
        "transportation"
    ).get_environmental_impact().get_total()[
        ImpactCategory.CLIMATE_CHANGE
    ].use == 6.583113447812001 * KG_CO2E / (
        PEOPLE * DAY
    )
