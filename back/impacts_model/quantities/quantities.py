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
ELECTRONIC_WASTE = ureg.electronic_waste
PRIMARY_MJ = ureg.primary_MJ
TONNE_MIPS = ureg.tonne_mips

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
