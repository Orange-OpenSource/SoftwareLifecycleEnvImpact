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

from unittest import mock
from unittest.mock import MagicMock
from pint import Quantity, Unit
import yaml
from impacts_model.impact_sources import (
    ImpactSource,
    ImpactSourceSchema,
    _get_all_impact_sources,
    impact_source_factory,
)
from impacts_model.impacts import EnvironmentalImpact, ImpactCategory, ImpactValue

from impacts_model.quantities.quantities import (
    DAY,
    KG_CO2E,
    PEOPLE,
    SERVER,
)


def test_impact_source_has_time_input() -> None:
    """
    Test computation of function has_time_input that should
    return true if the ImpactSource has a time in its unit, else False
    """

    # Test without time
    assert (
        ImpactSource(
            id="testid",
            name="test",
            unit=SERVER,
            environmental_impact={
                ImpactCategory.CLIMATE_CHANGE: ImpactValue(use=1776 * KG_CO2E)
            },
        ).has_time_input
        == False
    )

    # Test with time first
    assert (
        ImpactSource(
            id="testid",
            name="test",
            unit=DAY * SERVER,
            environmental_impact={
                ImpactCategory.CLIMATE_CHANGE: ImpactValue(use=1776 * KG_CO2E)
            },
        ).has_time_input
        == True
    )

    # Test with time second
    assert (
        ImpactSource(
            id="testid",
            name="test",
            unit=SERVER * DAY,
            environmental_impact={
                ImpactCategory.CLIMATE_CHANGE: ImpactValue(use=1776 * KG_CO2E)
            },
        ).has_time_input
        == True
    )

    # Test double magnitude without time
    assert (
        ImpactSource(
            id="testid",
            name="test",
            unit=SERVER * SERVER,
            environmental_impact={
                ImpactCategory.CLIMATE_CHANGE: ImpactValue(use=1776 * KG_CO2E)
            },
        ).has_time_input
        == False
    )


def test_yaml_loading() -> None:
    impact_sources = _get_all_impact_sources()
    assert len(impact_sources) > 0
    for impact_source in impact_sources:
        # Test each can be retrieved via the factory
        assert isinstance(impact_source_factory(impact_source.id), ImpactSource)

        # Assert unit is converted to a pint Unit
        assert isinstance(impact_source.unit, Unit)

        # Retrieve own_impact
        try:
            own_impact = impact_source.get_impact().own_impact
        except Exception:
            print("a")

        # Assert that co2 is set for all
        assert own_impact[ImpactCategory.CLIMATE_CHANGE] is not None

        for indicator in own_impact:
            # Test all environmentalImpact to see if they're rightly typed as ImpactValue
            assert isinstance(
                own_impact[indicator],
                ImpactValue,
            )

            # Test that we retrieve an impact with the right quantity if we remove the impact unit, ie for one unit
            impact_value = own_impact[indicator]
            # For manufacture
            if impact_value.manufacture is not None:
                tmp = impact_value.manufacture * impact_source.unit
                assert tmp.units == indicator.value or tmp.dimensionless
            # For use
            if impact_value.use is not None:
                tmp = impact_value.use * impact_source.unit
                assert tmp.units == indicator.value or tmp.dimensionless


def test_impact_source_factory() -> None:
    """Test that all ids from the yaml can be retrieved and have the right format"""
    list = []
    with open("impacts_model/data/impact_sources/default.yaml", "r") as stream:
        data_loaded = yaml.load_all(stream, Loader=yaml.Loader)
        for data in data_loaded:
            list.append(data.id)

    assert len(list) > 0
    for d in list:
        loaded_impact = impact_source_factory(d)
        assert isinstance(loaded_impact, ImpactSource)


@mock.patch(
    "impacts_model.impact_sources.impact_source_factory",
    MagicMock(
        return_value=ImpactSource(
            id="testid",
            name="test",
            unit=SERVER,
            environmental_impact={
                ImpactCategory.CLIMATE_CHANGE: ImpactValue(use=999 * KG_CO2E)
            },
        ),
    ),
)
def test_impact_source_get_impact() -> None:
    # Test only direct impacts

    a = (
        ImpactSource(
            id="testidA",
            name="test",
            unit=SERVER,
            environmental_impact={
                ImpactCategory.CLIMATE_CHANGE: ImpactValue(use=1776 * KG_CO2E)
            },
        )
        .get_impact()
        .total_impact[ImpactCategory.CLIMATE_CHANGE]
        .use
    )
    assert a == 1776 * (KG_CO2E / SERVER)

    # Test when using other resources
    i = ImpactSource(
        id="testidB",
        name="test",
        unit=SERVER,
        uses=[
            {"quantity": "10 server", "resource_id": "testid"},
            {"quantity": "34 server", "resource_id": "testid"},
        ],
        environmental_impact={
            ImpactCategory.CLIMATE_CHANGE: ImpactValue(use=1776 * KG_CO2E)
        },
    )
    env_impact = i.get_impact()
    total_impact = env_impact.total_impact
    use = total_impact[ImpactCategory.CLIMATE_CHANGE].use

    assert use == 1776 * (KG_CO2E / SERVER) + 10 * (999 * KG_CO2E) + 34 * (
        999 * KG_CO2E
    )  # 45732


def test_impact_source_computation() -> None:
    # People
    people = (
        impact_source_factory("people")
        .get_impact()
        .total_impact[ImpactCategory.CLIMATE_CHANGE]
    )
    assert people.use + people.manufacture == 12.395184114767307 * KG_CO2E / (
        PEOPLE * DAY
    )

    # Transportation
    transportation = (
        impact_source_factory("transportation")
        .get_impact()
        .total_impact[ImpactCategory.CLIMATE_CHANGE]
    )
    assert (
        transportation.use + transportation.manufacture
        == 6.511784290772001 * KG_CO2E / (PEOPLE * DAY)
    )
