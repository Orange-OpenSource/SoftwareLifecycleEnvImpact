try:
    from pint import UnitRegistry, Context
    import os as _os

    abspath = _os.path.dirname(_os.path.abspath(__file__))
    ureg = UnitRegistry()
    ureg.load_definitions(_os.path.join(abspath, "model.pint"))
    ureg.add_context(Context('test'))

    ELECTRICITY_MIX = ureg.electricity_mix
    KG_CO2E = ureg.kg_co2e
    YEAR = ureg.year
    HOUR = ureg.hour
    DAY = ureg.day
    WATT_HOUR = ureg.watt_hour
except ImportError:
    print("Pint not installed")
