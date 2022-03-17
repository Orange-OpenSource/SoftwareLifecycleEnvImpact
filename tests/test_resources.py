from model.impact_sources import ImpactSource
from model.resources import Resource


def test_get_co2_impact():
    """
    For Resource.get_co2_impact test computation, quantity change and resource adding
    :return: None
    """
    is1 = ImpactSource(9999)
    is2 = ImpactSource(1.123)

    # Test ImpactSource computation
    r = Resource(1, impacts=[is1, is2])
    assert r.get_co2_impact() == 9999 + 1.123

    # Test quantity change
    r.quantity = 123
    assert r.get_co2_impact() == (9999 + 1.123) * 123

    # Test add impact source
    is3 = ImpactSource(432)
    r.impacts.append(is3)
    assert r.get_co2_impact() == (9999 + 1.123 + 432) * 123
