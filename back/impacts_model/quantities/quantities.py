import os as _os

from pint import Context, UnitRegistry

abspath = _os.path.dirname(_os.path.abspath(__file__))
ureg = UnitRegistry()
ureg.load_definitions(_os.path.join(abspath, "model.pint"))
ureg.add_context(Context("test"))

Q_ = ureg.Quantity

############
# ALISASES #
############

ELECTRICITY_MIX = ureg.electricity_mix

YEAR = ureg.year
HOUR = ureg.hour
DAY = ureg.day
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
LAPTOP = ureg.laptop
SMARTPHONE = ureg.smartphone
TABLET = ureg.tablet
TELEVISION = ureg.television
SERVER = ureg.server

GIGABYTE = ureg.gigabyte
TERABYTE = ureg.terabyte

MAN_DAY = ureg.man_day
