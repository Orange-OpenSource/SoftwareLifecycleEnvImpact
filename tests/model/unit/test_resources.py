from typing import List

from impacts_model.impacts.impact_factors import ImpactFactor
from impacts_model.impacts.impacts import ImpactIndicator
from impacts_model.quantities import (
    CUBIC_METER,
    DISEASE_INCIDENCE,
    ELECTRONIC_WASTE,
    KG_BQ_U235E,
    KG_CO2E,
    KG_SBE,
    MOL_HPOS,
    PRIMARY_MJ,
    TONNE_MIPS,
)
from impacts_model.resources import (
    merge_resource_list,
    Resource,
    ResourcesList,
)


class TestResource(Resource):
    """
    Test resource implementation to fully control its quantity and ImpactSources
    """

    def __init__(self, quantity: float, impacts: List[ImpactFactor]):
        self._quantity = quantity
        super().__init__("TestResource", impacts)

    @property
    def quantity(self) -> float:
        """
        For testing purpose, give direct access to quantity property
        :return: quantity as float
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity: float) -> None:
        self._quantity = quantity


##########
# STATIC #
##########


def test_merge_resource_list() -> None:
    """
    Test merge_resource_list function, with edge cases to assess that the returned list is correct
    :return:
    """
    first_list: ResourcesList = {
        "first": {
            ImpactIndicator.CLIMATE_CHANGE: 1000 * KG_CO2E,
            ImpactIndicator.ELECTRONIC_WASTE: 1000 * ELECTRONIC_WASTE,
        },
    }
    second_list: ResourcesList = {}

    # test empty
    assert merge_resource_list(first_list, second_list) == {
        "first": {
            ImpactIndicator.CLIMATE_CHANGE: 1000 * KG_CO2E,
            ImpactIndicator.ELECTRONIC_WASTE: 1000 * ELECTRONIC_WASTE,
        },
    }

    # Test same impact

    second_list = {
        "first": {
            ImpactIndicator.CLIMATE_CHANGE: 1000 * KG_CO2E,
            ImpactIndicator.ELECTRONIC_WASTE: 1000 * ELECTRONIC_WASTE,
        }
    }
    assert merge_resource_list(first_list, second_list) == {
        "first": {
            ImpactIndicator.CLIMATE_CHANGE: 2000 * KG_CO2E,
            ImpactIndicator.ELECTRONIC_WASTE: 2000 * ELECTRONIC_WASTE,
        }
    }

    # Test new impact

    second_list = {
        "second": {
            ImpactIndicator.CLIMATE_CHANGE: 1000 * KG_CO2E,
            ImpactIndicator.ELECTRONIC_WASTE: 1000 * ELECTRONIC_WASTE,
        }
    }
    assert merge_resource_list(first_list, second_list) == {
        "first": {
            ImpactIndicator.CLIMATE_CHANGE: 1000 * KG_CO2E,
            ImpactIndicator.ELECTRONIC_WASTE: 1000 * ELECTRONIC_WASTE,
        },
        "second": {
            ImpactIndicator.CLIMATE_CHANGE: 1000 * KG_CO2E,
            ImpactIndicator.ELECTRONIC_WASTE: 1000 * ELECTRONIC_WASTE,
        },
    }


############
# Resource #
############


def test_quantity_setter() -> None:
    """
    Test quantity property of Resource setter and getter
    :return:
    """
    is1 = ImpactFactor(9999 * KG_CO2E)
    is2 = ImpactFactor(1.123 * KG_CO2E)

    test_resource = TestResource(1, impacts=[is1, is2])  # Impacts =  1 * 1776
    assert test_resource.quantity == 1
    test_resource.quantity = 342423.2134234
    assert test_resource.quantity == 342423.2134234


def test_get_co2_impact() -> None:
    """
    For Resource.get_co2_impact test computation, quantity change and resource adding
    :return: None
    """
    is1 = ImpactFactor(9999 * KG_CO2E)
    is2 = ImpactFactor(1.123 * KG_CO2E)

    test_resource = TestResource(1, impacts=[is1, is2])  # Impacts =  1 * 1776
    test_resource.quantity = 1
    # Test ImpactFactor computation
    assert (
        test_resource.get_impact(ImpactIndicator.CLIMATE_CHANGE)
        == (9999 + 1.123) * KG_CO2E
    )

    # Test quantity change
    test_resource._quantity = 123
    assert (
        test_resource.get_impact(ImpactIndicator.CLIMATE_CHANGE)
        == ((9999 + 1.123) * 123) * KG_CO2E
    )

    # Test add impact source
    is3 = ImpactFactor(432 * KG_CO2E)
    test_resource._impacts.append(is3)
    assert (
        test_resource.get_impact(ImpactIndicator.CLIMATE_CHANGE)
        == ((9999 + 1.123 + 432) * 123) * KG_CO2E
    )


def test_get_impacts() -> None:
    """
    Test get_impacts computation by changing quantity and impacts_list
    :return:
    """
    is1 = ImpactFactor(9999 * KG_CO2E)
    is2 = ImpactFactor(1.123 * KG_CO2E)

    test_resource = TestResource(1, impacts=[is1, is2])  # Impacts =  1 * 1776
    is2.raw_materials = 213.3 * TONNE_MIPS
    assert test_resource.get_impacts() == {
        ImpactIndicator.CLIMATE_CHANGE: 10000.123 * KG_CO2E,
        ImpactIndicator.RESOURCE_DEPLETION: 0 * KG_SBE,
        ImpactIndicator.ACIDIFICATION: 0 * MOL_HPOS,
        ImpactIndicator.FINE_PARTICLES: 0 * DISEASE_INCIDENCE,
        ImpactIndicator.IONIZING_RADIATIONS: 0 * KG_BQ_U235E,
        ImpactIndicator.WATER_DEPLETION: 0 * CUBIC_METER,
        ImpactIndicator.ELECTRONIC_WASTE: 0 * ELECTRONIC_WASTE,
        ImpactIndicator.PRIMARY_ENERGY: 0 * PRIMARY_MJ,
        ImpactIndicator.RAW_MATERIALS: 213.3 * TONNE_MIPS,
    }

    # Test quantity multiplication
    test_resource.quantity = 10
    assert test_resource.get_impacts() == {
        ImpactIndicator.CLIMATE_CHANGE: (10 * 10000.123) * KG_CO2E,
        ImpactIndicator.RESOURCE_DEPLETION: 0 * KG_SBE,
        ImpactIndicator.ACIDIFICATION: 0 * MOL_HPOS,
        ImpactIndicator.FINE_PARTICLES: 0 * DISEASE_INCIDENCE,
        ImpactIndicator.IONIZING_RADIATIONS: 0 * KG_BQ_U235E,
        ImpactIndicator.WATER_DEPLETION: 0 * CUBIC_METER,
        ImpactIndicator.ELECTRONIC_WASTE: 0 * ELECTRONIC_WASTE,
        ImpactIndicator.PRIMARY_ENERGY: 0 * PRIMARY_MJ,
        ImpactIndicator.RAW_MATERIALS: (10 * 213.3) * TONNE_MIPS,
    }