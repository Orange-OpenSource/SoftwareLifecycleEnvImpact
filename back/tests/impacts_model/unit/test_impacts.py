from impacts_model.impact_sources import (
    ImpactSource,
)

##########
# STATIC #
##########
from impacts_model.impacts import ImpactCategory, ImpactValue
from impacts_model.quantities.quantities import (
    CUBIC_METER,
    DISEASE_INCIDENCE,
    ELECTRICITY_MIX,
    ELECTRONIC_WASTE,
    KG_BQ_U235E,
    KG_CO2E,
    KG_SBE,
    MOL_HPOS,
    PRIMARY_MJ,
    TONNE_MIPS,
    DAY,
    SERVER,
)

'''
def test_merge_impacts_lists() -> None:
    """
    Test the merge_impacts_lists list function, assessing empty list, same types and different types merging are correct
    :return:
    """
    first_list: ImpactsList = {}
    second_list: ImpactsList = {
        ImpactCategory.CLIMATE_CHANGE: 1000 * KG_CO2E,
        ImpactCategory.ELECTRONIC_WASTE: 1000 * ELECTRONIC_WASTE,
    }

    # test with empty list
    assert merge_impacts_lists(first_list, second_list) == {
        ImpactCategory.CLIMATE_CHANGE: 1000 * KG_CO2E,
        ImpactCategory.ELECTRONIC_WASTE: 1000 * ELECTRONIC_WASTE,
    }

    # test with same types
    first_list = {
        ImpactCategory.CLIMATE_CHANGE: 1000 * KG_CO2E,
        ImpactCategory.ELECTRONIC_WASTE: 1000 * ELECTRONIC_WASTE,
    }
    assert merge_impacts_lists(first_list, second_list) == {
        ImpactCategory.CLIMATE_CHANGE: 2000 * KG_CO2E,
        ImpactCategory.ELECTRONIC_WASTE: 2000 * ELECTRONIC_WASTE,
    }

    # Test with other type
    second_list = {
        ImpactCategory.CLIMATE_CHANGE: 1000 * KG_CO2E,
        ImpactCategory.ELECTRONIC_WASTE: 1000 * ELECTRONIC_WASTE,
        ImpactCategory.WATER_DEPLETION: 21323 * CUBIC_METER,
    }

    assert merge_impacts_lists(first_list, second_list) == {
        ImpactCategory.CLIMATE_CHANGE: 2000 * KG_CO2E,
        ImpactCategory.ELECTRONIC_WASTE: 2000 * ELECTRONIC_WASTE,
        ImpactCategory.WATER_DEPLETION: 21323 * CUBIC_METER,
    }
'''


def test_impact_category_str() -> None:
    """
    Test for each category that it has an associated str
    """
    for e in ImpactCategory:
        assert e.name not in str(e)
        assert "not implemented" not in str(e)


###################
# ImpactsSourceRegistry #
###################


# def test_impact_registry_singleton() -> None:
#     """Test that ImpactRegistry follow the singleton pattern"""
#     ir1 = ImpactsSourceRegistry()
#     ir2 = ImpactsSourceRegistry()

#     assert ir1 == ir2
#     ir1.pue = 3.4
#     assert ir2.pue == 3.4
#     ir2.electricity_mix = 2.1234 * ELECTRICITY_MIX
#     assert ir1.electricity_mix == 2.1234 * ELECTRICITY_MIX

#     ir1.electricity_mix = 2.12312312 * ELECTRICITY_MIX
#     assert ir2.electricity_mix == 2.12312312 * ELECTRICITY_MIX

#     assert ImpactsSourceRegistry().electricity_mix == 2.12312312 * ELECTRICITY_MIX
#     ImpactsSourceRegistry().electricity_mix = 214234.31232 * ELECTRICITY_MIX
#     assert ImpactsSourceRegistry().electricity_mix == 214234.31232 * ELECTRICITY_MIX


################
# ImpactFactor #
################


def test_co2() -> None:
    """Test ImpactFactor co2 property getter"""
    i = ImpactSource(
        id=0,
        name="test",
        unit=SERVER / DAY,
        climate_change=ImpactValue(use=103.72 * KG_CO2E),
    )
    assert i.climate_change.use == 103.72 * KG_CO2E / i.unit


def test_impact_source_parameters() -> None:
    """
    Test setter/getter of all kind of environmental impact
    Test also that unit is propagated to properties
    :return:
    """
    i = ImpactSource(
        id="0",
        name="test",
        unit=SERVER / DAY,
        climate_change=ImpactValue(manufacture=103.72 * KG_CO2E, use=999103.72 * KG_CO2E),
        resource_depletion=ImpactValue(manufacture=312.23 * KG_SBE, use=999312.23 * KG_SBE),
        acidification=ImpactValue(
            manufacture=32443.2134 * MOL_HPOS, use=99932443.2134 * MOL_HPOS
        ),
        fine_particles=ImpactValue(
            manufacture=24324.234324 * DISEASE_INCIDENCE,
            use=99924324.234324 * DISEASE_INCIDENCE,
        ),
        ionizing_radiations=ImpactValue(
            manufacture=421312.123 * KG_BQ_U235E,
            use=999421312.123 * KG_BQ_U235E,
        ),
        water_depletion=ImpactValue(
            manufacture=124.123 * CUBIC_METER, use=999124.123 * CUBIC_METER
        ),
        electronic_waste=ImpactValue(
            manufacture=134242.12341 * ELECTRONIC_WASTE,
            use=999134242.12341 * ELECTRONIC_WASTE,
        ),
        primary_energy_consumption=ImpactValue(
            manufacture=1234.23123 * PRIMARY_MJ,
            use=9991234.23123 * PRIMARY_MJ,
        ),
        raw_materials=ImpactValue(
            manufacture=124.123441 * TONNE_MIPS,
            use=999124.123441 * TONNE_MIPS,
        ),
    )
    assert i.unit == SERVER / DAY
    assert i.climate_change.manufacture == 103.72 * KG_CO2E / i.unit
    assert i.climate_change.use == 999103.72 * KG_CO2E / i.unit

    assert i.resource_depletion.manufacture == 312.23 * KG_SBE / i.unit
    assert i.resource_depletion.use == 999312.23 * KG_SBE / i.unit

    assert i.acidification.manufacture == 32443.2134 * MOL_HPOS / i.unit
    assert i.acidification.use == 99932443.2134 * MOL_HPOS / i.unit

    assert i.fine_particles.manufacture == 24324.234324 * DISEASE_INCIDENCE / i.unit
    assert i.fine_particles.use == 99924324.234324 * DISEASE_INCIDENCE / i.unit

    assert i.ionizing_radiations.manufacture == 421312.123 * KG_BQ_U235E / i.unit
    assert i.ionizing_radiations.use == 999421312.123 * KG_BQ_U235E / i.unit

    assert i.water_depletion.manufacture == 124.123 * CUBIC_METER / i.unit
    assert i.water_depletion.use == 999124.123 * CUBIC_METER / i.unit

    assert i.electronic_waste.manufacture == 134242.12341 * ELECTRONIC_WASTE / i.unit
    assert i.electronic_waste.use == 999134242.12341 * ELECTRONIC_WASTE / i.unit

    assert i.primary_energy_consumption.manufacture == 1234.23123 * PRIMARY_MJ / i.unit
    assert i.primary_energy_consumption.use == 9991234.23123 * PRIMARY_MJ / i.unit

    assert i.raw_materials.manufacture == 124.123441 * TONNE_MIPS / i.unit
    assert i.raw_materials.use == 999124.123441 * TONNE_MIPS / i.unit


def test_get_impacts_quantities() -> None:
    """
    Test .impacts_list property of ImpactFactor
    :return:
    """
    i = ImpactSource(
        id="testId",
        name="test",
        unit=SERVER / DAY,
        climate_change=ImpactValue(manufacture=103.72 * KG_CO2E, use=103.72 * KG_CO2E),
        resource_depletion=ImpactValue(manufacture=312.23 * KG_SBE, use=312.23 * KG_SBE),
        acidification=ImpactValue(manufacture=32443.2134 * MOL_HPOS, use=32443.2134 * MOL_HPOS),
        fine_particles=ImpactValue(
            manufacture=24324.234324 * DISEASE_INCIDENCE,
            use=24324.234324 * DISEASE_INCIDENCE,
        ),
        ionizing_radiations=ImpactValue(
            manufacture=421312.123 * KG_BQ_U235E, use=421312.123 * KG_BQ_U235E
        ),
        water_depletion=ImpactValue(
            manufacture=124.123 * CUBIC_METER, use=124.123 * CUBIC_METER
        ),
        electronic_waste=ImpactValue(
            manufacture=134242.12341 * ELECTRONIC_WASTE,
            use=134242.12341 * ELECTRONIC_WASTE,
        ),
        primary_energy_consumption=ImpactValue(
            manufacture=1234.23123 * PRIMARY_MJ, use=1234.23123 * PRIMARY_MJ
        ),
        raw_materials=ImpactValue(
            manufacture=124.123441 * TONNE_MIPS, use=124.123441 * TONNE_MIPS
        ),
    )
    assert (
        i.environmental_impact.impacts[ImpactCategory.CLIMATE_CHANGE].manufacture
        == 103.72 * KG_CO2E / i.unit
    )
    assert (
        i.environmental_impact.impacts[ImpactCategory.RESOURCE_DEPLETION].manufacture
        == 312.23 * KG_SBE / i.unit
    )
    assert (
        i.environmental_impact.impacts[ImpactCategory.ACIDIFICATION].manufacture
        == 32443.2134 * MOL_HPOS / i.unit
    )
    assert (
        i.environmental_impact.impacts[ImpactCategory.FINE_PARTICLES].manufacture
        == 24324.234324 * DISEASE_INCIDENCE / i.unit
    )
    assert (
        i.environmental_impact.impacts[ImpactCategory.IONIZING_RADIATIONS].manufacture
        == 421312.123 * KG_BQ_U235E / i.unit
    )
    assert (
        i.environmental_impact.impacts[ImpactCategory.WATER_DEPLETION].manufacture
        == 124.123 * CUBIC_METER / i.unit
    )
    assert (
        i.environmental_impact.impacts[ImpactCategory.ELECTRONIC_WASTE].manufacture
        == 134242.12341 * ELECTRONIC_WASTE / i.unit
    )
    assert (
        i.environmental_impact.impacts[ImpactCategory.PRIMARY_ENERGY].manufacture
        == 1234.23123 * PRIMARY_MJ / i.unit
    )
    assert (
        i.environmental_impact.impacts[ImpactCategory.RAW_MATERIALS].manufacture
        == 124.123441 * TONNE_MIPS / i.unit
    )
