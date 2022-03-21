from model.impact_sources import ImpactSource, ServerImpact, StorageImpact


################
# ImpactSource #
################


def test_co2() -> None:
    """Test ImpactSource co2 property getter"""
    i = ImpactSource(103.72)
    assert i.co2 == 103.72


def test_server_impact() -> None:
    """
    Test that ServerImpact co2 is updated when electricity_mix or pue changes, and that the output is the same with
    the same input
    :return: None
    """
    s = ServerImpact(0.7543, 1.5)
    first_co2 = s.co2

    old_co2 = s.co2
    s.electricity_mix = 1.432
    assert s.co2 != old_co2

    old_co2 = s.co2
    s.pue = 2.3
    assert s.co2 != old_co2

    s.electricity_mix = 0.7543
    s.pue = 1.5
    assert s.co2 == first_co2


def test_storage_impact() -> None:
    """
    Test that StorageImpact co2 is updated when electricity_mix or pue changes, and that the output is the same with
    the same input
    :return: None
    """
    s = StorageImpact(0.7543, 1.5)
    first_co2 = s.co2

    old_co2 = s.co2
    s.electricity_mix = 1.432
    assert s.co2 != old_co2

    old_co2 = s.co2
    s.pue = 2.3
    assert s.co2 != old_co2

    s.electricity_mix = 0.7543
    s.pue = 1.5
    assert s.co2 == first_co2
