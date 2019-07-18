# -*-coding: utf-8 -*-
#
# projectv2 - Visual investigations of electrical recordings on the primate secondary visual cortex
# Copyright (C) 2019 Laboratório de Computação Gráfica
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# If you have any questions or suggestions regarding this software, visit
# <http://gitlab.com/lcg/v2/projectv2>.

"""This module contains supporting functionality for exporting a *PLX* file into smaller parts that can be more easily
and efficiently parsed than the original file format (completely defined in :mod:`plx.parsing`, accompanying with
a brief explanation). The actual exporting may be done either by

* The :meth:`plx.PlxFile.export_file` method,
* The :meth:`plx.PlxFile.export_channels` method (just exports channel data, not headers), or
* The :mod:`plx.cli` command-line interface.

Some additional definitions are provided for exported channel types:

* Event data blocks are exported as specified in :class:`ExportedEvent`,
* Spikes as in the types returned by :func:`ExportedSpike`, and
* Slow waveform data blocks are exported into a contiguous file that may be read as the Numpy data type
  :data:`exported_slow_dtype`.

Event data blocks contain an additional padding field for 8-byte alignment, and exported spike formats may also include
an additional padding field (depending on the number of waveform samples, indicated by the
:attr:`plx.parsing.Header.num_points_wave` header field), also aiming at 8-byte alignment. However, the
:func:`export_file` function (and hence the command-line interface, which is based on it), ensure that padding bytes are
always zero, such that reading back exported data files using Numpy arrays, for instance, results in padding fields
appear as empty, null-terminated, 8-bit ASCII strings, *i.e.* :code:`b''`.

Other exported parts (header sections, channel headers) are exported as in the record types defined in
:mod:`plx.parsing`. The paths for the exported parts are given by the :mod:`plx.export.paths` submodule.
File exporting has two equivalent implementations: a fast C++ implementation, provided by the :mod:`_plx`
module, and used by default, and an original Python implementation, kept for reference and fallback (implemented by the
hidden :func:`_export_file` function) behavior, in the absence of the C++ extension.

.. _Numpy data-type: https://docs.scipy.org/doc/numpy-1.15.1/reference/arrays.dtypes.html
"""

import numpy
import pathlib
import struct

from . import paths
from .. import parsing
from recparse import FieldSpec, Record

#: `Numpy data-type`_ for slow waveform samples, exported as contiguous data.
exported_slow_dtype = numpy.dtype(numpy.int16)


class ExportedEvent(Record):
    """Record definition for exported event blocks.
    """

    FIELDS = [
        FieldSpec("Timestamp", "q", property_name="timestamp"),
        FieldSpec("Channel", "h", property_name="channel"),
        FieldSpec("Unit", "h", property_name="unit"),
        FieldSpec("Padding", "4s", property_name="padding"),
    ]
    dtype = numpy.dtype(
        [
            ("timestamp", parsing.TIMESTAMP_ATTR_DTYPE),
            ("channel", numpy.int16),
            ("unit", numpy.int16),
            ("padding", "S4"),
        ]
    )


# TODO: This should be refactored into an abstract property of plx.AbstractPlxFile:
#       * In the cas of plx.PlxFile, this can be deduced from the header (should actually be computed in the
#         _plx extension module)
#       * In the case of plx.ExportedPlxFile, this type could be reported in a metadata file.
def ExportedSpike(plx_file=None, num_points_wave=None):
    """Defines the data-type (padding and fields) of exported spike data for a given *PLX* file.

    Either a :class:`plx.AbstractPlxFile` must be supplied through the ``plx_file`` parameter, or the number of
    waveform points must be informed through ``num_points_wave`` (higher precedence).

    .. todo: Check type of parameter
    """

    if num_points_wave is None:
        if plx_file is None:
            raise ValueError("Either ")
        else:
            num_points_wave = plx_file.header["NumPointsWave"]

    fields = [
        FieldSpec("Timestamp", "q", property_name="timestamp"),
        FieldSpec("Unit", "h", property_name="unit"),
        FieldSpec("Waveform", f"{num_points_wave}h"),
    ]
    dtype_fields = [
        ("timestamp", parsing.TIMESTAMP_ATTR_DTYPE),
        ("unit", numpy.int16),
        ("waveform", f"({num_points_wave},)i2"),
    ]

    used_size = struct.calcsize("".join(spec.struct_format for spec in fields))
    total_size = 8 * ((used_size - 1) // 8 + 1)
    padding = total_size - used_size

    if padding:
        fields.append(FieldSpec("Padding", f"{padding}s", property_name="padding"))
        dtype_fields.append(("padding", f"S{padding}"))

    class ExportedSpike(Record):
        FIELDS = fields
        dtype = numpy.dtype(dtype_fields)

        @property
        def waveform(self):
            return numpy.array(self["Waveform"], dtype=numpy.int16)

    return ExportedSpike


# TODO: Since this function is private and operates on plx.PlxFile instances, we can safely remove the base_dir
#       parameter and use the plx_file.export_base_dir attribute, instead.
def _export_channels(plx_file, base_dir):
    class EventChannelParser:
        def __init__(self):
            self.events_file = open(paths.event_data(base_dir), "wb")

        def parse_data_block(self, data_header, data_block):
            record = numpy.zeros(1, dtype=ExportedEvent.dtype)
            record["timestamp"] = data_header.timestamp
            record["channel"] = data_header["Channel"]
            record["unit"] = data_header["Unit"]
            record.tofile(self.events_file)
            file_dict["events"] = True

        def save(self):
            self.events_file.close()

    class SlowChannelParser:
        def __init__(self):
            self.signal_files = {}

        def parse_data_block(self, data_header, data_block):
            channel = data_header["Channel"]
            timestamp = data_header.timestamp
            signal_patch = numpy.frombuffer(data_block, dtype=exported_slow_dtype)

            if channel not in self.signal_files:
                file_dict["slow"].append(channel)
                self.signal_files[channel] = numpy.memmap(
                    paths.slow_channel(base_dir, data_header["Channel"]),
                    dtype=exported_slow_dtype,
                    mode="w+",
                    shape=int(plx_file.header["LastTimestamp"]),
                )

            self.signal_files[channel][
                timestamp : timestamp + len(signal_patch)
            ] = signal_patch

        def save(self):
            for numpy_memmap in self.signal_files.values():
                numpy_memmap.flush()

    class SpikeChannelParser:
        def __init__(self):
            self.spikes_files = {}

        def parse_data_block(self, data_header, data_block):
            channel = data_header["Channel"]
            if channel not in self.spikes_files:
                file_dict["spikes"].append(channel)
                self.spikes_files[channel] = open(
                    paths.spike_channel(base_dir, data_header["Channel"]), mode="wb"
                )
            record = numpy.zeros(1, dtype=ExportedSpike(plx_file).dtype)
            record["timestamp"] = data_header.timestamp
            record["waveform"] = numpy.frombuffer(
                data_block, dtype=record.dtype.fields["waveform"][0].base
            )
            record["unit"] = data_header["Unit"]
            record.tofile(self.spikes_files[channel])

        def save(self):
            for spikes_file in self.spikes_files.values():
                spikes_file.close()

    base_dir = pathlib.Path(base_dir or plx_file.path)
    parsers = {
        parsing.DataBlockHeader.Type.EVENT: EventChannelParser(),
        parsing.DataBlockHeader.Type.SLOW: SlowChannelParser(),
        parsing.DataBlockHeader.Type.SPIKE: SpikeChannelParser(),
    }
    file_dict = {"events": False, "slow": [], "spikes": []}

    with open(plx_file.path, "rb") as plx_stream:
        plx_stream.seek(plx_file.data_section_offset)

        while plx_stream.tell() < plx_file.size:
            data_header = parsing.DataBlockHeader.from_stream(plx_stream)
            data_block = plx_stream.read(data_header.bytes_following)

            parsers[data_header["Type"]].parse_data_block(
                data_header=data_header, data_block=data_block
            )

    parsers[parsing.DataBlockHeader.Type.EVENT].save()
    parsers[parsing.DataBlockHeader.Type.SLOW].save()
    parsers[parsing.DataBlockHeader.Type.SPIKE].save()

    return file_dict


def make_dirs(base_dir):
    """Make sure all subdirectories required to export a *PLX* to the designated base directory exist.
    """
    paths.counts(base_dir).parent.mkdir(parents=True, exist_ok=True)
    paths.event_data(base_dir).parent.mkdir(parents=True, exist_ok=True)
    paths.event_headers(base_dir).parent.mkdir(parents=True, exist_ok=True)
    paths.header(base_dir).parent.mkdir(parents=True, exist_ok=True)
    paths.slow_headers(base_dir).parent.mkdir(parents=True, exist_ok=True)
    paths.spike_headers(base_dir).parent.mkdir(parents=True, exist_ok=True)

    paths.slow_channels_dir(base_dir).mkdir(parents=True, exist_ok=True)
    paths.spike_channels_dir(base_dir).mkdir(parents=True, exist_ok=True)
