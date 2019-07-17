"""Extensions of the Marshmallow_ library. This module imports the whole Marshmallow_ library, and
imports some submodules into its namespace, so the recommended way of using it is 

.. code:: python

    import marshmallow_patch.marshmallow as marshmallow

or

.. code:: python

    from marshmallow_patch import marshmallow

Enhancements:

* Patched :class:`fields.Nested`,
* Additional field types (:class:`fields.NumpyArray`, :class:`fields.NumpyDtype`, :class:`fields.PhysicalQuantity`, and
  :class:`fields.PhysicalUnit`), and
* Automatic registration of additional field types with :mod:`marshmallow_annotations` for automatic schema generation
  from :mod:`dataclasses` or :attr:`attr.s` *data-classes*.

.. _Marshmallow: https://marshmallow.readthedocs.io/en/stable
"""

from . import fields as _fields
from marshmallow import *

fields = _fields
