from model.impact_sources import (
    ImpactSource,
    ImpactsRegistry,
    ServerImpact,
    StorageImpact,
)

from model.units import Q_, ureg


###################
# ImpactsRegistry #
###################


def test_impact_registry_singleton() -> None:
    """Test that ImpactRegistry follow the singleton pattern"""
    ir1 = ImpactsRegistry()
    ir2 = ImpactsRegistry()

    assert ir1 == ir2
    ir1.pue = Q_(3.4, ureg.pue)
    assert ir2.pue == 3.4 * ureg.pue
    ir2.electricity_mix = Q_(2.1234, ureg.electricity_mix)
    assert ir1.electricity_mix == 2.1234 * ureg.electricity_mix


################
# ImpactSource #
################


def test_co2() -> None:
    """Test ImpactSource co2 property getter"""
    i = ImpactSource(Q_(103.72, ureg.kg_co2e))
    assert i.co2 == 103.72 * ureg.kg_co2e


def test_server_impact() -> None:
    """
    Test that ServerImpact co2 is updated when electricity_mix or pue changes, and that the output is the same with
    the same input
    :return: None
    """
    s = ServerImpact()
    impacts_registry = ImpactsRegistry()
    impacts_registry.electricity_mix = Q_(0.7543, ureg.electricity_mix)
    impacts_registry.pue = Q_(1.5, ureg.pue)
    first_co2 = s.co2

    old_co2 = s.co2
    impacts_registry.electricity_mix = Q_(1.432, ureg.electricity_mix)
    assert s.co2 != old_co2

    old_co2 = s.co2
    impacts_registry.pue = Q_(2.3, ureg.pue)
    assert s.co2 != old_co2

    impacts_registry.electricity_mix = Q_(0.7543, ureg.electricity_mix)
    impacts_registry.pue = Q_(1.5, ureg.pue)
    assert s.co2 == first_co2


def test_storage_impact() -> None:
    """
    Test that StorageImpact co2 is updated when electricity_mix or pue changes, and that the output is the same with
    the same input
    :return: None
    """
    s = StorageImpact()
    registry = ImpactsRegistry()
    registry.pue = Q_(1.5, ureg.pue)
    registry.electricity_mix = Q_(0.7543, ureg.electricity_mix)
    first_co2 = s.co2

    old_co2 = s.co2
    registry.electricity_mix = Q_(1.432, ureg.electricity_mix)
    assert s.co2 != old_co2

    old_co2 = s.co2
    registry.pue = Q_(2.3, ureg.pue)
    assert s.co2 != old_co2

    registry.electricity_mix = Q_(0.7543, ureg.electricity_mix)
    registry.pue = Q_(1.5, ureg.pue)
    assert s.co2 == first_co2
