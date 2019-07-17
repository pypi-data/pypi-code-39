"""In addition to importing all the :mod:`base marshmallow field types <marshmallow.fields>`, this module defines some
additional field types:

* :class:`Nested`, for replacing the existing :class:`marshmallow.fields.Nested` with automatic recursive missing-value
  completion,
* :class:`NumpyArray`, for serializing :class:`numpy arrays <numpy.ndarray>` (requires the
  ``[numpy]`` option during installation),
* :class:`NumpyDtype`, for serializing :class:`numpy data types <numpy.dtype>` (requires the
  ``[numpy]`` option during installation),
* :class:`PhysicalQuantity`, for serializing :class:`physical quantities <units.Quantity>` (requires
  the ``[pint]`` option during installation), and
* :class:`PhysicalUnit`, for serializing :class:`physical units <units.Unit>` (requires the ``[pint]``
  option during installation).

An additional feature of this module is that these additional field types (except for :class:`Nested`) are registered
with :attr:`marshmallow_annotations.registry` for automatic *data-class* schema generation (using either
:class:`marshmallow_annotations.AnnotationSchema` :class:`marshmallow_annotations.AttrsSchema`).

Pint_ support requires that you use the default :class:`unit registry <units.UnitRegistry>` defined
in :mod:`marshmallow_patch.conf` or manually override it with your custom instance. In the last
case, you should do it before importing this module, like so:

.. code:: python

    import marshmallow_patch.conf as marsh_conf
    import pint

    # Replace this with your custom instance, whatever it may be.
    marsh_conf.units = units.UnitRegistry()

    from marshmallow_patch.marshmallow import fields

.. _Pint: http://pint.readthedocs.io/en/latest
"""

import marshmallow.fields as mf
import marshmallow.validate

from marshmallow.fields import *
from marshmallow_annotations import registry

__all__ = ["Nested", "oneOf"] + mf.__all__

_Nested = Nested


def _register_for(class_type):
    """Returns a decorator that registers the decorated class as the default :class:`marshmallow.fields.Field` type for
    ``class_type`` in :attr:`marshmallow_annotations.registry`. This allows, for instance, the automatic generation of
    :class:`marshmallow.Schema` classes from *data classes* created with :mod:`dataclasses` (via
    :class:`marshmallow_annotations.AnnotationSchema`) or :attr:`attr.s` (via
    :class:`marshamllow_annotations.AttrsSchema`).

    Parameters
    ----------
    class_type: type
        A type that, when found in a data class, will be automatically converted to the
        :class:`marshmallow.fields.Field` that is decorated with the returned decorator during schema generation
        (via :class:`marshmallow_annotations.AnnotationSchema` or :class:`marshmallow_annotations.AttrsSchema`).

    Returns
    -------
    decorator: function
        The decorator that, when applied to a :class:`marshmallow.fields.Field` sub-type, registers this type as the
        field-type created for attributes of type ``class_type``, and returns the sub-type unmodified.
    """

    def decorator(field_type):
        def field_constructor(converter, subtypes, options):
            return field_type(**options)

        registry.register(class_type, field_constructor)
        return field_type

    return decorator


class Nested(_Nested):
    """Patches the :class:`marshmallow.fields.Nested` field type to provide ``missing`` values based on nested fields'
    missing values, if an explicit ``missing`` parameter is not passed to the constructor.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.missing is marshmallow.missing:
            self.missing = {
                field.name: field.missing
                for field in self.schema.fields.values()
                if field.missing is not marshmallow.missing
            }


try:
    import numpy

    @_register_for(numpy.ndarray)
    class NumpyArray(Field):
        """Custom :class:`marshmallow field type <marshmallow.fields.Field` for (de)serializing :class:`Numpy arrays
        <numpy.ndarray>`. Requires the ``[numpy]`` option during installation.

        .. warning::

            The previous implementation only supported plain Numpy arrays (that is, those with arbitrary shapes and any
            underlying numeric data-type) and record arrays with plain fields (that is, fields with numeric data-types). For
            instance, (de)serializing arrays like

            .. code:: python

                import numpy as np
                import numpy.random as npr

                a = npr.randint(1, 10, size=(3, 4, 5))
                b = np.empty(shape=(3, 4), dtype=[('a', int), ('b', float)])

            was, and still is, absolutely supported. The current implementation relies on a smarter serialization process --
            in particular, the existence of a :class:`(de)serializer for Numpy data-types <NumpyDtype>` -- so **it is likely
            that any scalar array will now be correctly (de)serialized**, that is, **arrays containing generic object fields
            are still not supported**. Since the current test suite contains few test cases, you are advised to **use this
            feature with caution**. Please file a bug report if you find any issues.

        Parameters
        ----------
        without_dtype: bool, optional
            If ``True``, the data-type will be discarded and arrays will be serialized simply as (possibly nested) lists,
            instead of as a dictionaries. Likewise, when deserializing, this field type will consider serialized arrays to
            be lists. That means that the data-type will be guessed by the :func:`numpy.array` constructor.
        """

        def __init__(self, without_dtype=False, **kwargs):
            super().__init__(**kwargs)
            self.withtout_dtype = without_dtype

        def _deserialize(self, value, attr, data):
            if self.withtout_dtype:
                return numpy.array(value)
            else:
                deserialized_dtype = NumpyDtype().deserialize(value["dtype"])
                return numpy.array(value["array"], dtype=deserialized_dtype)

        def _serialize(self, value, attr, obj):
            array = numpy.array(value)
            serialized_array = array.tolist()
            if self.withtout_dtype:
                return serialized_array
            else:
                serialized_dtype = NumpyDtype().serialize(
                    "value", {"value": array.dtype}
                )
                return {"array": serialized_array, "dtype": serialized_dtype}

    @_register_for(numpy.dtype)
    class NumpyDtype(Field):
        """Custom :class:`marshmallow field type <marshmallow.fields.Field` for (de)serializing :class:`Numpy data types
        <numpy.dtype>`. Requires the ``[numpy]`` option during installation.

        Data types are serialized according to a simple recursive dictionary structure, fundamentally composed of the
        ``'base'`` and ``'fields'`` keys. For a given data type,

        * If The type is a plain type, *i.e.* a scalar type without any sub-fields, the ``'base'`` key maps to the string
          representation of the data-type, and the ``'fiels'`` key maps to an empty dictionary (recursion tail), and
        * If the type is composed, *i.e.* it contains sub-fields, the ``'base'`` key maps to None, and the ``'fields'`` key
          maps to a dictionary of field names to serialized field data types (recursive step).

        For instance, the serialized form of the ``'i8'`` field specifier -- or, equivalently, :code:`numpy.dtype('i8')`, or
        :code:`numpy.dtype(numpy.int64)` -- is

        .. code:: python

            {'base': 'int64', 'fields': {}}

        where as the serialized form of the structured-array data-type ``[('a', 'i8'), ('b', 'f4'), ('c', 'U10')]`` would be

        .. code:: python

            {
                'base': None,
                'fields': {
                    'a': {'base': 'int64', 'fields': {}},
                    'b': {'base': 'float32', 'fields': {}},
                    'c': {'base': '<U10', 'fields': {}}
                }
            }

        Note
        ----
        Arbitrary nested data-types are supported, but serialization of :class:`Numpy arrays <numpy.ndarray>` via
        :class:`NumpyArray` is limited to scalar data types (that is, fields of generic object types are not supported).
        """

        def _deserialize(self, value, attr, data):
            def deserialize(dtype):
                if dtype["base"]:
                    return numpy.dtype(dtype["base"])
                else:
                    return numpy.dtype(
                        [
                            (field_name, deserialize(field_spec))
                            for field_name, field_spec in dtype["fields"].items()
                        ]
                    )

            try:
                return deserialize(value)
            except Exception as exc:
                raise marshmallow.ValidationError(str(exc))

        def _serialize(self, value, attr, obj):
            def serialize(dtype):
                if dtype.fields:
                    return {
                        "base": None,
                        "fields": {
                            field_name: serialize(field_dtype)
                            for field_name, (
                                field_dtype,
                                field_offset,
                            ) in dtype.fields.items()
                        },
                    }
                else:
                    return {"base": str(dtype), "fields": {}}

            try:
                return serialize(numpy.dtype(value))
            except Exception as exc:
                raise marshmallow.ValidationError(str(exc))

    __all__.extend(["NumpyArray", "NumpyDtype"])

except ImportError:
    pass


try:
    import pint.errors
    from ..config import units as _units

    #: This is the unit registry defined in :data:`marshmallow_patch.config.units`.
    units = _units

    @_register_for(units.Quantity)
    class PhysicalQuantity(Field):
        """Custom :class:`marshmallow field type <marshmallow.fields.Field` for (de)serializing :class:`units.Quantity` objects
        using either strings, or a simple dictionary structure.

        :class:`Physical quantities <units.Quantity>` with numeric magnitudes may be (de)serialized in a very simple way, by
        simply converting :class:`units.Quantity` objects to/from strings. However, Pint_'s parser cannot account for more
        structured magnitude types by itself, which requires separating unit (:class:`PhysicalUnit`) from magnitude (using
        whatever field type) serialization. Hence, the default behavior supports the most general case, and consists in
        using a dictionary structure with two keys:

        * ``'magnitude'``, which maps to the value of :attr:`units.Quantity.m`, as a simple Python number or other nested field
          type (*e.g.* :class:`NumpyArray`), and
        * ``'unit'``, which maps to the value of :attr:`units.Quantity.u` as a string (using :class:`PhysicalUnit` behind the
          scenes).

        For instance, the object :code:`45 * units.second`, in the most general setting, is serialized as

        .. code:: python

            {'magnitude': 45, 'unit': 'second'}

        However, if string serialization is explicitly requested via ``as_string=True``, it will be serialized as
        ``'45 second'``. When deserializing, :class:`int` and :class:`float` are automatically disambiguated, but
        non-trivial magnitude types, like :class:`fractions <fractions.Fraction>` or :class:`Numpy arrays <numpy.ndarray>`,
        need to be manually specified through the ``magnitude_type`` parameter.

        .. todo::
            The classes in this module are useful enough to be worth publishing as a stand-alone library. In this case, it
            would be appropriate to modify this class' behavior to account for a specific *unit registry*
            (:class:`units.UnitRegistry`), by leveraging `field context
            <https://marshmallow.readthedocs.io/en/2.x-line/extending.html#using-context>`_ to point to the registry that
            should be used when deserializing.

        Warning
        -------
        :class:`Complex <complex>` magnitudes are currently not supported.

        Parameters
        ----------
        unit: units.Unit, or str, optional
            Unit type that this field should be compatible with. For instance if ``'second'`` is passed, the field will fail
            on validation of a value measured in meters. The serialized/deserialized value will also be converted to this
            specific unit, *e.g.*, if ``'millisecond'`` is passed, the value ``'10 second'`` will be deserialized to
            :code:`units.Quantity(10000, 'millisecond')` and *mutatis mutandis* if serialized. Must be a valid unit in the
            :attr:`units` registry, otherwise a :class:`pint.UndefinedUnitError` will be raised.

        magnitude_type: marshmallow.fields.Field, or callable, optional
            A field specifier that describes how the physical quantity's magnitude should be (de)serialized. Does not need
            to be informed if the magnitude's type is :class:`int` or :class:`float`. If a callable is given, it will be
            called to get the field specifier. If a value is passe and ``as_string`` is ``True``, :class:`ValueError` will
            be raised.

        as_string: bool, optional
            Specifies that (de)serialization should use a string representation, instead of a dictionary. This is suitable
            for simple scalar quantities (and useful for parsing physical quantities from URL query variables, for instance)
            but more elaborate types should keep it ``False`` and specify a custom :class:`field type
            <marshmallow.fields.Field>` in ``magnitude_type``.

        *args
            Additional positional arguments to pass to :class:`marshmallow.fields.Field`'s constructor.

        **kwargs
            Additional keyword arguments to pass to :class:`marshmallow.fields.Field`'s constructor.

        Raises
        ------
        ValueError
            If ``magnitude`` is passed and ``as_string`` is ``True``.

        pint.UndefinedUnitError
            If an unknown ``unit`` is passed.
        """

        def __init__(self, unit=None, magnitude_type=None, as_string=False, **kwargs):
            if magnitude_type is not None and as_string:
                raise ValueError("magnitude_type was passed with as_string=True")

            super().__init__(**kwargs)

            if callable(magnitude_type):
                self._magnitude_type = magnitude_type()
            else:
                self._magnitude_type = magnitude_type

            if unit:
                self._unit = units.Unit(unit)
            else:
                self._unit = None

            self._as_string = as_string

        def _deserialize(self, value, attr, data):
            try:
                if self._as_string:

                    if self._unit:
                        quantity = units.Quantity(value).to(self._unit)
                    else:
                        quantity = units.Quantity(value)
                    self._validate(quantity)
                    return quantity
                else:
                    unit = PhysicalUnit().deserialize(value["unit"])

                    if self._magnitude_type:
                        magnitude = self._magnitude_type.deserialize(value["magnitude"])
                    else:
                        magnitude = value["magnitude"]

                    if self._unit:
                        quantity = (magnitude * unit).to(self._unit)
                    else:
                        quantity = magnitude * unit

                    return quantity
            except (
                pint.errors.DimensionalityError,
                pint.errors.UndefinedUnitError,
            ) as exc:
                raise marshmallow.ValidationError(str(exc))

        def _serialize(self, value, attr, obj):
            try:
                if self._as_string:
                    quantity = units.Quantity(value)
                    if self._unit:
                        return str(quantity.to(self._unit))
                    else:
                        return str(quantity)
                else:
                    if self._unit:
                        quantity = units.Quantity(value).to(self._unit)
                    else:
                        quantity = units.Quantity(value)

                    if self._magnitude_type:
                        magnitude = self._magnitude_type.serialize("", {"": quantity.m})
                    else:
                        magnitude = quantity.m

                    return {
                        "magnitude": magnitude,
                        "unit": PhysicalUnit().serialize("", {"": quantity.u}),
                    }
            except (
                pint.errors.DimensionalityError,
                pint.errors.UndefinedUnitError,
            ) as exc:
                raise marshmallow.ValidationError(str(exc))

    @_register_for(units.Unit)
    class PhysicalUnit(Field):
        """Custom :class:`marshmallow field type <marshmallow.fields.Field` for (de)serializing :class:`units.Unit` objects
        as strings.

        Parameters
        ----------
        unit: units.Unit or str, optional
            Unit type that this field should be compatible with. For instance if ``'second'`` is passed, the field will fail
            on validation of a unit of spatial type. However, any other time unit will be compatible.

        *args: tuple, optional
            Additional positional arguments to pass to :class:`marshmallow.fields.Field`'s constructor.

        **kwargs: dict, optional
            Additional keyword arguments to pass to :class:`marshmallow.fields.Field`'s constructor.
        """

        def __init__(self, *args, unit=None, **kwargs):
            super().__init__(*args, **kwargs)
            if unit:
                self._unit = units.Unit(unit)
            else:
                self._unit = None

        def _deserialize(self, value, attr, data):
            try:
                unit = units.Unit(value)
            except pint.errors.UndefinedUnitError as exc:
                raise marshmallow.ValidationError(str(exc))
            self._validate(unit)
            return unit

        def _serialize(self, value, attr, obj):
            self._validate(value)
            unit = units.Unit(value)
            return str(unit)

        def _validate(self, value):
            try:
                unit = units.Unit(value)
            except BaseException as exc:
                raise marshmallow.ValidationError(str(exc))
            if self._unit and unit.dimensionality != self._unit.dimensionality:
                raise marshmallow.ValidationError(
                    f"{unit!s} is not compatible with unit type {self._unit!s}"
                )

    __all__.extend(["PhysicalQuantity", "PhysicalUnit"])

except ImportError:
    pass


def oneOf(field, choices):
    """Sets up a :class:`marshmallow field specifier <marshmallow.field.Field>` with validation from a set of possible
    choices and sets up the field's ``choice`` metadata key 

    Parameters
    ----------
    field: marshmallow.fields.Field

    choices: sequence
        A sequence of allowed choices for the field.

    Examples
    --------
    Suppose we have the following initialization code in a module that implements an API namespace:

    .. code:: python

        from v2.server.rest import Resource
        from v2.ext.marshmallow import Schema
        from marshmallow.validate import OneOf
        from v2.server.rest import Namespace, fields

    Then, we declare a schema like this

    .. code:: python

        class HellowWorldVars(Schema):
            a = fields.Integer(
                default=2,
                validate=OneOf([1, 2, 3, 4]),   # The choices must be specified twice: once to the validator and another
                choices=[1, 2, 3, 4],           # to attach them as field metadata for parser generation below.
                help='An optional query param.'
            )

    and use it for :meth:`annotating and providing parsing capabilities <v2.server.rest.Namespace.use_args>`) to a
    resourceful class, like

    .. code:: python

        @ns.route('/')
        class HelloWorld(Resource):
            @ns.use_args(HelloWorldVars())    # Here, automatic parser generation requires the 'choices' metadata.
            def get(self, args):
                ...

    What this function allows is to rewrite the query variables' schema avoiding repetition of the choices, like so:

    .. code:: python

        class HellowWorldVars(Schema):
            a = fields.oneOf(
                field=fields.Integer(               # Basic field properties, like default value and help string are
                    default=2,                      # specified here...
                    help='An optional query param.'
                ),
                choices=[1, 2, 3, 4],               # ... and choices are specified here, only once.
            )
    """
    field.validate = marshmallow.validate.OneOf(choices)
    field.metadata["choices"] = choices
    return field
