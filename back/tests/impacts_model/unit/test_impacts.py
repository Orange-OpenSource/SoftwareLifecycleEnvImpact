from impacts_model.impact_sources import (
    BikeImpactSource,
    CarImpactSource,
    ImpactSource,
    ImpactsSourceRegistry,
    LaptopImpactSource,
    MotorbikeImpactSource,
    OfficeImpactSource,
    PublicTransportImpactSource,
    ServerImpactSource,
    SmartphoneImpactSource,
    StorageImpactSource,
    TabletImpactSource,
    TelevisionImpactSource,
    TransportImpactSource,
    UserDeviceImpactSource,
)

##########
# STATIC #
##########
from impacts_model.impacts import ImpactIndicator
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
)

'''
def test_merge_impacts_lists() -> None:
    """
    Test the merge_impacts_lists list function, assessing empty list, same types and different types merging are correct
    :return:
    """
    first_list: ImpactsList = {}
    second_list: ImpactsList = {
        ImpactIndicator.CLIMATE_CHANGE: 1000 * KG_CO2E,
        ImpactIndicator.ELECTRONIC_WASTE: 1000 * ELECTRONIC_WASTE,
    }

    # test with empty list
    assert merge_impacts_lists(first_list, second_list) == {
        ImpactIndicator.CLIMATE_CHANGE: 1000 * KG_CO2E,
        ImpactIndicator.ELECTRONIC_WASTE: 1000 * ELECTRONIC_WASTE,
    }

    # test with same types
    first_list = {
        ImpactIndicator.CLIMATE_CHANGE: 1000 * KG_CO2E,
        ImpactIndicator.ELECTRONIC_WASTE: 1000 * ELECTRONIC_WASTE,
    }
    assert merge_impacts_lists(first_list, second_list) == {
        ImpactIndicator.CLIMATE_CHANGE: 2000 * KG_CO2E,
        ImpactIndicator.ELECTRONIC_WASTE: 2000 * ELECTRONIC_WASTE,
    }

    # Test with other type
    second_list = {
        ImpactIndicator.CLIMATE_CHANGE: 1000 * KG_CO2E,
        ImpactIndicator.ELECTRONIC_WASTE: 1000 * ELECTRONIC_WASTE,
        ImpactIndicator.WATER_DEPLETION: 21323 * CUBIC_METER,
    }

    assert merge_impacts_lists(first_list, second_list) == {
        ImpactIndicator.CLIMATE_CHANGE: 2000 * KG_CO2E,
        ImpactIndicator.ELECTRONIC_WASTE: 2000 * ELECTRONIC_WASTE,
        ImpactIndicator.WATER_DEPLETION: 21323 * CUBIC_METER,
    }
'''

###################
# ImpactsSourceRegistry #
###################


def test_impact_registry_singleton() -> None:
    """Test that ImpactRegistry follow the singleton pattern"""
    ir1 = ImpactsSourceRegistry()
    ir2 = ImpactsSourceRegistry()

    assert ir1 == ir2
    ir1.pue = 3.4
    assert ir2.pue == 3.4
    ir2.electricity_mix = 2.1234 * ELECTRICITY_MIX
    assert ir1.electricity_mix == 2.1234 * ELECTRICITY_MIX

    ir1.electricity_mix = 2.12312312 * ELECTRICITY_MIX
    assert ir2.electricity_mix == 2.12312312 * ELECTRICITY_MIX

    assert ImpactsSourceRegistry().electricity_mix == 2.12312312 * ELECTRICITY_MIX
    ImpactsSourceRegistry().electricity_mix = 214234.31232 * ELECTRICITY_MIX
    assert ImpactsSourceRegistry().electricity_mix == 214234.31232 * ELECTRICITY_MIX


################
# ImpactFactor #
################


def test_co2() -> None:
    """Test ImpactFactor co2 property getter"""
    i = ImpactSource(103.72 * KG_CO2E)
    assert i.co2 == 103.72 * KG_CO2E


def test_impact_source_parameters() -> None:
    """
    Test setter/getter of all kind of environmental impact
    :return:
    """
    i = ImpactSource(
        climate_change=103.72 * KG_CO2E,
        resource_depletion=312.23 * KG_SBE,
        acidification=32443.2134 * MOL_HPOS,
        fine_particles=24324.234324 * DISEASE_INCIDENCE,
        ionizing_radiations=421312.123 * KG_BQ_U235E,
        water_depletion=124.123 * CUBIC_METER,
        electronic_waste=134242.12341 * ELECTRONIC_WASTE,
        primary_energy_consumption=1234.23123 * PRIMARY_MJ,
        raw_materials=124.123441 * TONNE_MIPS,
    )
    assert i.co2 == 103.72 * KG_CO2E
    assert i.resource_depletion == 312.23 * KG_SBE
    assert i.acidification == 32443.2134 * MOL_HPOS
    assert i.fine_particles == 24324.234324 * DISEASE_INCIDENCE
    assert i.ionizing_radiations == 421312.123 * KG_BQ_U235E
    assert i.water_depletion == 124.123 * CUBIC_METER
    assert i.electronic_waste == 134242.12341 * ELECTRONIC_WASTE
    assert i.primary_energy_consumption == 1234.23123 * PRIMARY_MJ
    assert i.raw_materials == 124.123441 * TONNE_MIPS


def test_get_impacts_quantities() -> None:
    """
    Test .impacts_list property of ImpactFactor
    :return:
    """
    i = ImpactSource(
        climate_change=103.72 * KG_CO2E,
        resource_depletion=312.23 * KG_SBE,
        acidification=32443.2134 * MOL_HPOS,
        fine_particles=24324.234324 * DISEASE_INCIDENCE,
        ionizing_radiations=421312.123 * KG_BQ_U235E,
        water_depletion=124.123 * CUBIC_METER,
        electronic_waste=134242.12341 * ELECTRONIC_WASTE,
        primary_energy_consumption=1234.23123 * PRIMARY_MJ,
        raw_materials=124.123441 * TONNE_MIPS,
    )

    assert i.environmental_impact.impacts == {
        ImpactIndicator.CLIMATE_CHANGE: 103.72 * KG_CO2E,
        ImpactIndicator.RESOURCE_DEPLETION: 312.23 * KG_SBE,
        ImpactIndicator.ACIDIFICATION: 32443.2134 * MOL_HPOS,
        ImpactIndicator.FINE_PARTICLES: 24324.234324 * DISEASE_INCIDENCE,
        ImpactIndicator.IONIZING_RADIATIONS: 421312.123 * KG_BQ_U235E,
        ImpactIndicator.WATER_DEPLETION: 124.123 * CUBIC_METER,
        ImpactIndicator.ELECTRONIC_WASTE: 134242.12341 * ELECTRONIC_WASTE,
        ImpactIndicator.PRIMARY_ENERGY: 1234.23123 * PRIMARY_MJ,
        ImpactIndicator.RAW_MATERIALS: 124.123441 * TONNE_MIPS,
    }


####################
# UserDeviceImpactSource #
####################


def test_user_device_impact_co2() -> None:
    """
    Test that user device correspond to the ratio of devices by their impact
    :return:
    """
    user_device_impact = UserDeviceImpactSource()
    assert user_device_impact.co2 == (
        user_device_impact.RATIO_TABLET * TabletImpactSource().co2
        + user_device_impact.RATIO_PC * LaptopImpactSource().co2
        + user_device_impact.RATIO_TV * TelevisionImpactSource().co2
        + user_device_impact.RATIO_SMARTPHONE * SmartphoneImpactSource().co2
    )


################
# LaptopImpactSource #
################


def test_laptop_impact() -> None:
    """
    Test laptop impact with amortization, with computation by hand instead of pint day/years translation
    :return:
    """
    l = LaptopImpactSource()
    amortization_day = l.FABRICATION_CO2.magnitude / (l.LIFE_EXPECTANCY.magnitude * 365)
    amortization_hour = amortization_day / l.DAILY_USE.magnitude
    assert round(l.co2, 2) == round(amortization_hour * KG_CO2E, 2)


####################
# SmartphoneImpactSource #
####################


def test_smartphone_impact() -> None:
    """
    Test smartphone impact with amortization, with computation by hand instead of pint day/years translation
    :return:
    """
    s = SmartphoneImpactSource()
    amortization_day = s.FABRICATION_CO2.magnitude / (s.LIFE_EXPECTANCY.magnitude * 365)
    amortization_hour = amortization_day / s.DAILY_USE.magnitude
    assert round(s.co2, 2) == round(amortization_hour * KG_CO2E, 2)


################
# TabletImpactSource #
################


def test_tablet_impact() -> None:
    """
    Test tablet impact with amortization, with computation by hand instead of pint day/years translation
    :return:
    """
    t = TabletImpactSource()
    amortization_day = t.FABRICATION_CO2.magnitude / (t.LIFE_EXPECTANCY.magnitude * 365)
    amortization_hour = amortization_day / t.DAILY_USE.magnitude
    assert round(t.co2, 2) == round(amortization_hour * KG_CO2E, 2)


####################
# TelevisionImpactSource #
####################


def test_television_impact() -> None:
    """
    Test television impact with amortization, with computation by hand instead of pint day/years translation
    :return:
    """
    t = TelevisionImpactSource()
    amortization_day = t.FABRICATION_CO2.magnitude / (t.LIFE_EXPECTANCY.magnitude * 365)
    amortization_hour = amortization_day / t.DAILY_USE.magnitude
    assert round(t.co2, 2) == round(amortization_hour * KG_CO2E, 2)


################
# OfficeImpactSource #
################


def test_office_impact() -> None:
    """
    Test office emission /person computation by hand without pint
    :return:
    """
    o = OfficeImpactSource()
    one_person_office_size = o.OFFICE_SIZE / o.OFFICES_OCCUPANCY
    square_meter_co2_day = o.BUILDING_EMISSIONS.magnitude / (o.LIFE_EXPECTANCY * 365)
    assert o.co2 == (one_person_office_size * square_meter_co2_day) * KG_CO2E


################
# ServerImpactSource #
################


def test_server_impact() -> None:
    """
    Test that ServerImpactSource co2 is updated when electricity_mix or pue changes, and that the output is the same with
    the same input
    :return: None
    """
    s = ServerImpactSource()
    impacts_registry = ImpactsSourceRegistry()
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


#################
# StorageImpactSource #
#################


def test_storage_impact() -> None:
    """
    Test that StorageImpactSource co2 is updated when electricity_mix or pue changes, and that the output is the same with
    the same input
    :return: None
    """

    s = StorageImpactSource()
    registry = ImpactsSourceRegistry()
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


###################
# TransportImpactSource #
###################


def test_transport_impact() -> None:
    """
    Test that transport impact correspond to a standard ratio of all impacts_list, multiplied by the average travel distance
    :return:
    """
    u = TransportImpactSource()
    assert (
        u.co2
        == (
            (
                u.FOOT_PERCENTAGE * 0
                + u.BIKE_PERCENTAGE * BikeImpactSource().co2.magnitude
                + u.PUBLIC_TRANSPORT_PERCENTAGE
                * PublicTransportImpactSource().co2.magnitude
                + u.CAR_PERCENTAGE * CarImpactSource().co2.magnitude
                + u.MOTORBIKE_PERCENTAGE * MotorbikeImpactSource().co2.magnitude
            )
            / 100
        )
        * u.MEAN_DISTANCE
        * KG_CO2E
    )