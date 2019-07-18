import pint

#: Default unit registry for physical units. If you need this package's objects to operate on physical units from a
#: different registry, override this variable with your custom :class:`pint.UnitRegistry` instance before instantiating
#: anything else.
units = pint.UnitRegistry()
