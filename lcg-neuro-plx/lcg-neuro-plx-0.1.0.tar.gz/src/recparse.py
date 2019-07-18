"""This module offers higher-level functionality over the standard :mod:`struct` module for parsing binary files that
store information in a two-level abstraction that consists in a series of *records*, which are in turn composed of
*fields*. A record type may be specified by creating a subclass from :class:`recparse.Record` and declaring a ``FIELDS``
class attribute with a list of :class:`recparse.FieldSpec` instance that specify the names and binary encodings of the
corresponding fields. The resulting subclass will feature methods that allow to compute the size of records, read and
write series of records from a binary file, and instantiate records from other convenient Python objects, like
dictionaries and lists. Example:

.. code:: pycon

    >>> class Pearson(Record):
    FIELDS = [
        FieldSpec('name', '10s'),
        FieldSpec('age', 'I'),
    ]
    >>> Pearson.fields()
    OrderedDict([
        ('name', FieldSpec(name='name', struct_format='100s', property_name=None, offset=0)),
        ('age', FieldSpec(name='age', struct_format='I', property_name=None, offset=100))
    ])
    >>> Pearson.total_size()
    14
    >>> p = Pearson.from_mapping({'name': b'May', 'age': 56})
    >>> p
    Pearson(name=b'May', age=56)
    >>> p.buffer
    bytearray(b'May\x00\x00\x00\x00\x00\x00\x00\x00\x008\x00\x00\x00')

There is also the :class:`recparse.RecordArray` class, which allows to read/write a series of records of a given type
from/to open streams.
"""

import collections
import struct


class FieldSpec(
    collections.namedtuple("FieldSpec", "name struct_format property_name offset")
):
    """Specifies a single field's name and binary representation within a record.

    Parameters
    ----------
    name: str
        Name of field. It will be accessible within the resulting record type as :code:`rec[name]`.

    struct_format: str
        A format code compatible with the :mod:`struct` module.

    property_name: str, optional
        If this is specified, a read/write property for accessing this field will be created in the resulting record
        type. The field will be accessible as :code:`rec.property_name`.

    offset: int, ignored
        This parameter is ignored during record specification. It is modified by the :class:`recparse.RecordMeta` metaclass
        during record class creation to reflect the correct offset of each field, which depends on the order in which
        fields are specified.
    """

    def __new__(cls, name, struct_format, property_name=None, offset=None):
        return super().__new__(cls, name, struct_format, property_name, offset)

    @property
    def size(self):
        """Size (in bytes) of this field.
        """
        return struct.calcsize(self.struct_format)

    def property_getter(self, record):
        return record[self.name]

    def with_offset(self, offset):
        return self.__class__(*self[:3], offset=offset)


class RecordArray:
    @classmethod
    def from_iterable(cls, iterable, record_type):
        buffer = bytearray(record_type.total_size() * len(iterable))
        for i, record in enumerate(iterable):
            buffer_slice = slice(
                i * record_type.total_size(), (i + 1) * record_type.total_size()
            )
            buffer[buffer_slice] = bytes(record)
        return cls(buffer, record_type=record_type)

    @classmethod
    def from_stream(cls, stream, record_type):
        buffer = bytearray()
        while True:
            record_bytes = stream.read(record_type.total_size())
            if len(record_bytes) == record_type.total_size():
                buffer.extend(record_bytes)
            else:
                break
        return cls(buffer, record_type=record_type)

    def __init__(self, buffer, record_type):
        self.buffer = buffer
        self.record_type = record_type

        assert len(self.buffer) % record_type.total_size() == 0

    def __repr__(self):
        return "{}(record_type={}, buffer={})".format(
            self.__class__.__name__, self.record_type, self.buffer
        )

    def __bytes__(self):
        return bytes(self.buffer)

    def __delitem__(self, item):
        del self.buffer[self._buffer_slice(item)]

    def __eq__(self, other):
        return bytes(self) == bytes(other)

    def __getitem__(self, item):
        return self.record_type(self.buffer[self._buffer_slice(item)])

    def __iter__(self):
        return (self[i] for i in range(len(self)))

    def __len__(self):
        return len(self.buffer) // self.record_type.total_size()

    def __setitem__(self, item, value):
        self.buffer[self._buffer_slice(item)] = bytes(value)

    def _buffer_slice(self, item_or_slice):
        try:
            return slice(
                item_or_slice.start * self.record_type.total_size(),
                (item_or_slice.stop - item_or_slice.start)
                * self.record_type.total_size(),
                item_or_slice.step * self.record_type.total_size(),
            )
        except AttributeError:
            return slice(
                item_or_slice * self.record_type.total_size(),
                (item_or_slice + 1) * self.record_type.total_size(),
            )


class RecordMeta(type):
    """Helper meta-class for implementing the :class:`recparse.Record` class.

    Defines the following class methods on classes derived from :class:`recparse.Record`:

    * :meth:`fields`
    * :meth:`padding`
    * :meth:`total_size`
    * :meth:`struct_format`
    * :meth:`used_size`

    Also defines the following instance methods:

    * :meth:`keys`

    """

    def __new__(metaname, classname, bases, attrs):
        if "FIELDS" not in attrs:
            raise AttributeError(
                "{} does not define the 'FIELDS' attribute".format(classname)
            )

        fields_dict = collections.OrderedDict()
        field_offset = 0
        for field_spec in attrs["FIELDS"]:
            field_spec = field_spec.with_offset(field_offset)
            fields_dict[field_spec.name] = field_spec
            field_offset = field_offset + field_spec.size

        used_size = sum(field_spec.size for field_spec in attrs["FIELDS"])

        if "SIZE" in attrs and "PADDING" in attrs:
            size = attrs["SIZE"]
            padding = attrs["PADDING"]
        elif "SIZE" in attrs:
            size = attrs["SIZE"]
            padding = size - used_size
        elif "PADDING" in attrs:
            padding = attrs["PADDING"]
            size = used_size + padding
        else:
            size = used_size
            padding = 0

        struct_format = "".join(
            [field_spec.struct_format for field_spec in attrs["FIELDS"]]
        )
        if padding > 0:
            struct_format += "{}x".format(padding)

        @classmethod
        def fields_classmethod(cls):
            """Field details for this record type, as an ordered dictionary.

            Returns
            -------
            :class:`collections.OrderedDict`
                An ordered dictionary that maps field names (:class:`str`) into field details
                (:class:`recparse.FieldDetails`), in the order in which they were specified when overriding the
                :attr:`FIELDS` class attribute.

            Notes
            -----
            This class method should be used instead of directly accessing the :attr:`FIELDS` class attribute.
            """
            return fields_dict

        @classmethod
        def padding_classmethod(cls):
            """Number of padding bytes at the end of every record.

            See also
            --------
            * :meth:`recparse.Record.total_size`
            * :meth:`recparse.Record.used_size`
            """
            return padding

        @classmethod
        def total_size_classmethod(cls):
            """Total record size, i.e. the sum of field sizes with the padding size (if any).

            See also
            --------
            * :meth:`recparse.Record.padding`
            * :meth:`recparse.Record.used_size`
            """
            return size

        @classmethod
        def struct_format_classmethod(cls):
            """Format string used with the :meth:`struct.pack` and :meth:`struct.unpack` methods for writing/reading.
            """
            return struct_format

        @classmethod
        def used_size_classmethod(cls):
            """The sum of field sizes, which is smaller or equal than the total record size.

            See also
            --------
            * :meth:`recparse.Record.padding`
            * :meth:`recparse.Record.total_size`
            """
            return used_size

        def keys_method(self):
            return fields_dict.keys()

        del attrs["FIELDS"]
        if "SIZE" in attrs:
            del attrs["SIZE"]
        if "PADDING" in attrs:
            del attrs["PADDING"]

        class_type = super().__new__(metaname, classname, bases, attrs)
        class_type.fields = fields_classmethod
        class_type.padding = padding_classmethod
        class_type.total_size = total_size_classmethod
        class_type.struct_format = struct_format_classmethod
        class_type.used_size = used_size_classmethod
        class_type.keys = keys_method

        def prop_getter(field_details):
            @property
            def wrapped(self):
                return field_details.property_getter(record=self)

            return wrapped

        for field_details in class_type.fields().values():
            prop = field_details.property_name
            if prop is not None:
                setattr(class_type, prop, prop_getter(field_details))

        return class_type


class Record(metaclass=RecordMeta):
    """Record specification for decoding/encoding values from/to a binary buffer or file.

    This is a base class that is only really useful if you derive from it. You should define the following class
    attributes in your derived class:

    * :attr:`FIELDS`: List of :class:`recparse.FieldSpec` objects specifying individual field details.
    * :attr:`SIZE`: An optional integer that specifies the total record size. Should be greater that the sum of field
      sizes.
    * :attr:`PADDING`: An optional integer that specifies the number of padding bytes immediately following the record.

    The :attr:`SIZE` and :attr:`PADDING` attributes are mutually influencing: if none is given, padding is assumed to be
    zero and the total size equal to the sum of field sizes. If a single one of them is given, the other is deduced.
    Specifying both is possible, but unnecessary. During instantiation, these numbers are verified for consistency, and
    an :exc:`AssertionError` is raised if this verification fails.

    These class attributes are erased by the meta-class (:class:`recparse.RecordMeta`) during class instantiation so, if
    you need to query a derived type's total size or padding size, do so through the

    * :meth:`recparse.Record.total_size` and
    * :meth:`recparse.Record.padding`

    class methods. Check your derived type's docstring for additional methods defined by the meta-class.

    A working constructor and convenience alternative constructors are provided. More information about them is given
    below. Subclasses are mapping types (compatible with the :class:`collections.abc.Mapping` interface) that map field
    names into field values.

    Parameters
    ----------
    buffer: :class:`bytearray` or :class:`mmap.mmap`
        Any object supporting byte-slicing semantics is acceptable. Buffer size is not checked, but the buffer must be
        at least as large as the :attr:`recparse.Record.SIZE` attribute for correct operation. An offset of 0 from the
        buffer start is implicitly assumed. Writing to the fields is supported as long as the buffer.

    See also
    --------
    * :meth:`recparse.Record.from_bytes`
    * :meth:`recparse.Record.from_iterable`
    * :meth:`recparse.Record.from_mapping`
    * :meth:`recparse.Record.from_stream`
    """

    FIELDS = []
    PADDING = 0
    SIZE = 0

    @classmethod
    def empty(cls):
        """Alternative constructor: creates a record filled with zeroes.
        """
        return cls(bytearray(cls.total_size()))

    @classmethod
    def from_bytes(cls, bytes):
        """Alternative constructor: decodes a record by reading it directly from the given bytes.

        Use this instead of the default constructor if you want read/write capability without overwriting the
        original buffer.

        Parameters
        ----------
        bytes: :class:`bytes` or :class:`bytearray`
            A file-like stream open in binary reading mode.
        """
        return cls(bytearray(bytes[: cls.total_size()]))

    @classmethod
    def from_iterable(cls, iterable):
        """Alternative constructor: creates a record from an iterable.

        The iterable must contain at least as many items as the fields, and they must be position-compatible. Extraneous
        items are ignored.

        Parameters
        ----------
        mapping: :class:`collections.abc.Iterable`
            A list- or tuple-like object.
        """
        mapping = {
            field_name: element for field_name, element in zip(cls.fields(), iterable)
        }
        return cls.from_mapping(mapping)

    @classmethod
    def from_mapping(cls, mapping):
        """Alternative constructor: creates a record from a mapping with keys that match the field names.

        Extraneous keys are ignored.

        Parameters
        ----------
        mapping: :class:`collections.abc.Mapping`
            A dict-like object.
        """
        values = [mapping[field_name] for field_name in cls.fields()]
        buffer = bytearray(struct.pack(cls.struct_format(), *values))
        return cls(buffer)

    @classmethod
    def from_stream(cls, stream):
        """Alternative constructor: decodes a record by reading it directly from the given stream.

        The original stream will be preserved, and the object will have read/write capability. If you want to write
        to the original stream, wrap it a :class:`mmap.mmap` object or similar.

        Parameters
        ----------
        stream: stream
            A file-like stream open in binary reading mode.
        """
        return cls(bytearray(stream.read(cls.total_size())))

    def __init__(self, buffer):
        self.buffer = buffer

        assert self.padding() >= 0, "Negative padding: record type is ill-defined"
        assert self.total_size() >= 0, "Negative total size: record type is ill-defined"
        assert (
            self.total_size() == self.used_size() + self.padding()
        ), "Record type is ill-defined"

    def __repr__(self):
        return "{}({})".format(
            self.__class__.__name__,
            ", ".join(f"{field}={self[field]!r}" for field in self.keys()),
        )

    def __bytes__(self):
        return bytes(self.buffer)

    def __eq__(self, other):
        return bytes(self) == bytes(other)

    def __getitem__(self, item):
        if item in self.keys():
            the_slice = slice(
                self.fields()[item].offset,
                self.fields()[item].offset + self.fields()[item].size,
            )
            values = struct.unpack(
                self.fields()[item].struct_format, self.buffer[the_slice]
            )
            if self.fields()[item].struct_format[-1] == "s":
                value = values[0].replace(b"\x00", b" ").decode("utf-8").strip()
            elif len(values) > 1:
                value = list(values)
            else:
                value = values[0]
            return value
        else:
            raise KeyError("%r object has no key %r" % (self.__class__.__name__, item))

    def __len__(self):
        return len(self.fields())

    def __setitem__(self, item, value):
        if item in self.keys():
            the_slice = slice(
                self.fields()[item].offset,
                self.fields()[item].offset + self.fields()[item].size,
            )
            if self.fields()[item].struct_format[-1] == "s":
                length = int(self.fields()[item].struct_format[:-1])
                value = value.encode("utf-8").replace(b" ", b"\x00")
                value = value + (length - len(value)) * b"\x00"
            self.buffer[the_slice] = struct.pack(
                self.fields()[item].struct_format, value
            )
        else:
            raise KeyError(
                "%r object does not support assignment to key %r"
                % (self.__class__.__name__, item)
            )

    def items(self):
        return zip(self.keys(), self.values())

    def values(self):
        return (self[key] for key in self.keys())
