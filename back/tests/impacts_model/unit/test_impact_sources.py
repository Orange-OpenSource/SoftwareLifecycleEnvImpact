from pint import Quantity, Unit
import yaml
from impacts_model.impact_sources import (
    ImpactSource,
    _get_all_impact_sources,
    impact_source_factory,
)

from impacts_model.quantities.quantities import (
    deserialize_pint,
)

def test_yaml_loading() -> None:
    impact_sources = _get_all_impact_sources()
    assert(len(impact_sources) > 0)
    for impact_source in impact_sources:
        # Test each can be retrieved via the factory
        assert isinstance(impact_source_factory(impact_source.id), ImpactSource)

        # Assert unit is converted to a pint Unit
        assert isinstance(impact_source.unit, Unit)

        # Assert that co2 is set for all
        assert impact_source.climate_change is not None

        for indicator in impact_source.environmental_impact.impacts:
            # Test all environmentalImpact to see if they're rightly typed as quantities    
            assert isinstance(
                impact_source.environmental_impact.impacts[indicator], Quantity
            )

            # Test that we retrieve an impact with the right quantity if we remove the impact unit, ie for one unit
            tmp = (impact_source.environmental_impact.impacts[indicator] * impact_source.unit)
            assert tmp.units == indicator.value  or tmp.dimensionless


def test_impact_source_factory() -> None:
    """Test that all ids from the yaml can be retrieved and have the right format"""
    list = []
    with open("impacts_model/data/impact_sources/default.yaml", "r") as stream:
        data_loaded = yaml.load_all(stream, Loader=yaml.Loader)
        for data in data_loaded:
            list.append(data.id)
    
    assert len(list) > 0
    for d in data:
        loaded_impact = impact_source_factory(d.id)
        assert isinstance(loaded_impact, ImpactSource)
