from model.impact_sources import (
    ImpactSource,
    ImpactsRegistry,
    ServerImpact,
    StorageImpact,
)



###################
# ImpactsRegistry #
###################
from model.quantities import ELECTRICITY_MIX, KG_CO2E


def test_impact_registry_singleton() -> None:
    """Test that ImpactRegistry follow the singleton pattern"""
    ir1 = ImpactsRegistry()
    ir2 = ImpactsRegistry()

    assert ir1 == ir2
    ir1.pue = 3.4
    assert ir2.pue == 3.4
    ir2.electricity_mix = 2.1234 * ELECTRICITY_MIX
    assert ir1.electricity_mix == 2.1234 * ELECTRICITY_MIX


################
# ImpactSource #
################


def test_co2() -> None:
    """Test ImpactSource co2 property getter"""
    i = ImpactSource(103.72 * KG_CO2E)
    assert i.co2 == 103.72 * KG_CO2E


def test_server_impact() -> None:
    """
    Test that ServerImpact co2 is updated when electricity_mix or pue changes, and that the output is the same with
    the same input
    :return: None
    """
    s = ServerImpact()
    impacts_registry = ImpactsRegistry()
    impacts_registry.electricity_mix = 0.7543 * ELECTRICITY_MIX
    impacts_registry.pue = 1.5
    first_co2 = s.co2

    old_co2 = s.co2
    impacts_registry.electricity_mix = 1.432 * ELECTRICITY_MIX
    assert s.co2 != old_co2

    old_co2 = s.co2
    impacts_registry.pue = 2.3
    assert s.co2 != old_co2

    impacts_registry.electricity_mix = 0.7543 * ELECTRICITY_MIX
    impacts_registry.pue = 1.5
    assert s.co2 == first_co2


def test_storage_impact() -> None:
    """
    Test that StorageImpact co2 is updated when electricity_mix or pue changes, and that the output is the same with
    the same input
    :return: None
    """
    s = StorageImpact()
    registry = ImpactsRegistry()
    registry.pue = 1.5
    registry.electricity_mix = 0.7543 * ELECTRICITY_MIX
    first_co2 = s.co2

    old_co2 = s.co2
    registry.electricity_mix = 1.432 * ELECTRICITY_MIX
    assert s.co2 != old_co2

    old_co2 = s.co2
    registry.pue = 2.3
    assert s.co2 != old_co2

    registry.electricity_mix = 0.7543 * ELECTRICITY_MIX
    registry.pue = 1.5
    assert s.co2 == first_co2
