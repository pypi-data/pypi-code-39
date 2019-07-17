"""This module holds the :class:`pint.UnitRegistry` instance to be used in case of Pint_
interoperability. Import this module and override the :attr:`units` global variable with your
pre-defined unit registry, or simply use the default one, before you import the patched Marshmallow_
module :mod:`marshmallow_patch.marshmallow`.

Examples
--------

.. code:: python

    import marshmallow_patch.config as marsh_conf
    import pint
    
    # A default unit registry, like the one already defined.
    marsh_conf.units = pint.UnitRegistry()

    from marshmallow_patch import marshmallow

    # Fields used from now on have support for Pint_ units from the registry above.
"""

try:
    import pint

    #: Global unit registry.
    units = pint.UnitRegistry()
except ImportError:
    units = None
