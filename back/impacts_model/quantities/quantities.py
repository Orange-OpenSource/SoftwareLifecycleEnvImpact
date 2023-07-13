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

import os as _os
from typing import Any, Optional, Union

from pint import Context, Quantity, Unit, UnitRegistry

abspath = _os.path.dirname(_os.path.abspath(__file__))
ureg = UnitRegistry()
ureg.load_definitions(_os.path.join(abspath, "model.pint"))
ureg.add_context(Context("test"))

Q_ = ureg.Quantity


def serialize_quantity(input: Quantity[Any]) -> str:
    """Serialize a pint quantity to a string"""
    if input is None:
        return None
    try:
        return str(input)
    except AttributeError:
        raise TypeError("Input must be a Quantity")


def deserialize_quantity(
    input: Union[str, Optional[Quantity[Any]]],
) -> Optional[Quantity[Any]]:
    """Deserialize a pint quantity"""
    if input is None:
        return None
    if isinstance(input, Quantity):
        return input
    return ureg(input)


def deserialize_unit(input: Union[str, Unit]) -> Unit:
    if input is None:
        return None
    if isinstance(input, Unit):
        return input
    return ureg.Unit(input)


############
# ALISASES #
############

ELECTRICITY_MIX = ureg.electricity_mix

BUSINESS_YEAR = ureg.business_year
BUSINESS_MONTH = ureg.business_month
BUSINESS_WEEK = ureg.business_week

YEAR = ureg.year
MONTH = ureg.month
WEEK = ureg.week
DAY = ureg.day
HOUR = ureg.hour
MINUTE = ureg.minute
WATT_HOUR = ureg.watt_hour
KWH = ureg.kilowatt_hour

KG_CO2E = ureg.kg_co2e
KG_SBE = ureg.kg_Sbe
MOL_HPOS = ureg.mol_Hpos
DISEASE_INCIDENCE = ureg.disease_incidence
KG_BQ_U235E = ureg.kg_Bq_u235e
CUBIC_METER = ureg.cubic_meter
KG_MIPS = ureg.kg_mips

USER_DEVICE = ureg.user_device
DEVICE = ureg.device
LAPTOP = ureg.laptop
SMARTPHONE = ureg.smartphone
TABLET = ureg.tablet
TELEVISION = ureg.television
SERVER = ureg.server

GIGABYTE = ureg.gigabyte
TERABYTE = ureg.terabyte

MAN_DAY = ureg.man_day
PEOPLE = ureg.people

TIME = "[time]"
