# BSD-3-Clause License
#
# Copyright 2017 Orange
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

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
    KG_BQ_U235E,
    KG_CO2E,
    KG_SBE,
    MOL_HPOS,
    KG_MIPS,
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
        id="0",
        name="test",
        unit=SERVER / DAY,
        environmental_impact={
            ImpactCategory.CLIMATE_CHANGE: ImpactValue(use=103.72 * KG_CO2E)
        },
    )
    assert (
        i.get_impact().own_impact[ImpactCategory.CLIMATE_CHANGE].use
        == 103.72 * KG_CO2E / i.unit
    )


def test_get_impacts_quantities() -> None:
    """
    Test impacts_list property of ImpactFactor
    Test setter/getter of all kind of environmental impact
    Test also that unit is propagated to properties
    :return:
    """
    i = ImpactSource(
        id="testId",
        name="test",
        unit=SERVER / DAY,
        environmental_impact={
            ImpactCategory.CLIMATE_CHANGE: ImpactValue(
                manufacture=103.72 * KG_CO2E, use=103.72 * KG_CO2E
            ),
            ImpactCategory.RESOURCE_DEPLETION: ImpactValue(
                manufacture=312.23 * KG_SBE, use=312.23 * KG_SBE
            ),
            ImpactCategory.ACIDIFICATION: ImpactValue(
                manufacture=32443.2134 * MOL_HPOS, use=32443.2134 * MOL_HPOS
            ),
            ImpactCategory.FINE_PARTICLES: ImpactValue(
                manufacture=24324.234324 * DISEASE_INCIDENCE,
                use=24324.234324 * DISEASE_INCIDENCE,
            ),
            ImpactCategory.IONIZING_RADIATIONS: ImpactValue(
                manufacture=421312.123 * KG_BQ_U235E, use=421312.123 * KG_BQ_U235E
            ),
            ImpactCategory.WATER_DEPLETION: ImpactValue(
                manufacture=124.123 * CUBIC_METER, use=124.123 * CUBIC_METER
            ),
            ImpactCategory.RAW_MATERIALS: ImpactValue(
                manufacture=124.123441 * KG_MIPS, use=124.123441 * KG_MIPS
            ),
        },
    )
    total = i.get_impact().own_impact
    assert total[ImpactCategory.CLIMATE_CHANGE].manufacture == 103.72 * KG_CO2E / i.unit
    assert (
        total[ImpactCategory.RESOURCE_DEPLETION].manufacture == 312.23 * KG_SBE / i.unit
    )
    assert (
        total[ImpactCategory.ACIDIFICATION].manufacture
        == 32443.2134 * MOL_HPOS / i.unit
    )
    assert (
        total[ImpactCategory.FINE_PARTICLES].manufacture
        == 24324.234324 * DISEASE_INCIDENCE / i.unit
    )
    assert (
        total[ImpactCategory.IONIZING_RADIATIONS].manufacture
        == 421312.123 * KG_BQ_U235E / i.unit
    )
    assert (
        total[ImpactCategory.WATER_DEPLETION].manufacture
        == 124.123 * CUBIC_METER / i.unit
    )
    assert (
        total[ImpactCategory.RAW_MATERIALS].manufacture == 124.123441 * KG_MIPS / i.unit
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
            model.root_activity.get_impact()


def test_gitlab_computation() -> None:
    f = open("./examples/gitlab.json", "r")
    data = json.load(f)
    schema = ProjectSchema()
    new_project = schema.load(data)

    # co2_nominal = 19784699.84920407 * KG_CO2E
    co2_nominal = 14224422.988546003 * KG_CO2E

    impact = new_project.models[0].root_activity.get_impact()

    value = impact.total[ImpactCategory.CLIMATE_CHANGE]
    if value.manufacture is not None and value.use is not None:
        assert value.manufacture + value.use == co2_nominal
    else:
        raise Exception("Gitlab value manufacture or use is None")
