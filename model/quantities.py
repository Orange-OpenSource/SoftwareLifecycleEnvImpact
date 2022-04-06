try:
    from pint import UnitRegistry, Context
    import os as _os

    abspath = _os.path.dirname(_os.path.abspath(__file__))
    ureg = UnitRegistry()
    ureg.load_definitions(_os.path.join(abspath, "model.pint"))
    ureg.add_context(Context('test'))
    # Q_ = ureg.Quantity
except ImportError:
    print("Pint not installed")
