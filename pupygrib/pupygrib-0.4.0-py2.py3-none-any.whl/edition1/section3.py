"""Bit-map section of edition 1 GRIB messages."""

import numpy

from pupygrib import base
from pupygrib import fields


class BitMapField(base.Field):
    def get_value(self, section, offset):
        if section.tableReference > 0:
            raise NotImplementedError("pupygrib does not support catalogued bit-maps")

        try:
            bitmap = numpy.frombuffer(section._data, dtype="u1", offset=offset)
        except AttributeError:
            # See SimpleGridDataSection.values for why this is
            # necessary.
            buf = section._data.tobytes()
            bitmap = numpy.frombuffer(buf, dtype="u1", offset=offset)
        unused_bits = section.numberOfUnusedBitsAtEndOfSection3
        return numpy.unpackbits(bitmap)[:-unused_bits]


class BitMapSection(base.Section):
    """The bit-map section (3) of an edition 1 GRIB message."""

    section3Length = fields.Uint24Field(1)
    numberOfUnusedBitsAtEndOfSection3 = fields.Uint8Field(4)
    tableReference = fields.Uint16Field(5)
    bitmap = BitMapField(7)
