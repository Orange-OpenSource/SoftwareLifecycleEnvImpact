from genericpath import isfile
import json
from os import listdir
from os.path import isfile, join
from impacts_model.data_model import ProjectSchema
from impacts_model.impact_sources import (
    ImpactSource,
)

##########
# STATIC #
##########
from impacts_model.impacts import EnvironmentalImpact, ImpactCategory, ImpactValue
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


def test_impact_category_str() -> None:
    """
    Test for each category that it has an associated str
    """
    for e in ImpactCategory:
        assert e.name not in str(e)
        assert "not implemented" not in str(e)


def test_co2() -> None:
    """Test ImpactFactor co2 property getter"""
    i = ImpactSource(
        id=0,
        name="test",
        unit=SERVER / DAY,
        environmental_impact=EnvironmentalImpact(
            climate_change=ImpactValue(use=103.72 * KG_CO2E)
        ),
    )
    assert (
        i.environmental_impact.impacts[ImpactCategory.CLIMATE_CHANGE].use
        == 103.72 * KG_CO2E / i.unit
    )


def test_get_impacts_quantities() -> None:
    """
    Test .impacts_list property of ImpactFactor
    Test setter/getter of all kind of environmental impact
    Test also that unit is propagated to properties
    :return:
    """
    i = ImpactSource(
        id="testId",
        name="test",
        unit=SERVER / DAY,
        environmental_impact=EnvironmentalImpact(
            climate_change=ImpactValue(
                manufacture=103.72 * KG_CO2E, use=103.72 * KG_CO2E
            ),
            resource_depletion=ImpactValue(
                manufacture=312.23 * KG_SBE, use=312.23 * KG_SBE
            ),
            acidification=ImpactValue(
                manufacture=32443.2134 * MOL_HPOS, use=32443.2134 * MOL_HPOS
            ),
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


def test_example_impacts() -> None:
    """Test that all projects in example folder can be loaded and their impact computed"""
    path = "./examples"
    for file in [f for f in listdir(path) if isfile(join(path, f))]:
        f = open(path + "/" + file, "r")
        data = json.load(f)
        schema = ProjectSchema()
        new_project = schema.load(data)
        for model in new_project.models:
            model.root_task.get_impact()


def test_gitlab_computation() -> None:
    f = open("./examples/gitlab.json", "r")
    data = json.load(f)
    schema = ProjectSchema()
    new_project = schema.load(data)

    co2_nominal = 19364363.096746422 * KG_CO2E

    value = (
        new_project.models[0]
        .root_task.get_impact()
        .task_impact.impacts[ImpactCategory.CLIMATE_CHANGE]
    )
    if value.manufacture is not None and value.use is not None:
        assert value.manufacture + value.use == co2_nominal
    elif value.manufacture is not None:
        assert value.manufacture == co2_nominal
    elif value.use is not None:
        assert value.use == co2_nominal
    else:
        raise Exception("Gitlab value manufacture and use are None")
