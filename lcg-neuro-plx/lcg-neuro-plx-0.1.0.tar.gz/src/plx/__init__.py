"""Classes for reading raw PLX files, exporting their contents for fast access, and for reading exported contents. The
:class:`AbstractPlxFile` defines a high-level interface for accessing the contents of *PLX* files (that is, inspecting
the values of header fields, or accessing data channels as Numpy arrays). Two concrete classes implementing this
interface are available: :class:`PlxFile`, which reads this information directly from *PLX* files (relying on a
description of this structure provided by the record types in :mod:`plx.parsing`), and :class:`ExportedPlxFile`,
which actually parses information from sub-parts of *PLX* files exported to separate files using functionality from the
:mod:`plx.export` module.
"""

import abc
import functools
import json
import mmap
import numpy
import os.path
import pathlib
import tempfile
import warnings

from . import export, parsing, schemas
from attrs_patch import attr
from recparse import RecordArray


__version__ = "0.1.0"


@attr.autodoc
@attr.s
class SlowChannel:
    header: parsing.SlowHeader = attr.ib(metadata={"help": "Recording settings."})
    data: numpy.array = attr.ib(
        metadata={
            "help": "Continuous A/D samples. The Numpy data-type is given by "
            ":data:`plx.export.exported_slow_dtype`."
        }
    )


@attr.s
class SpikeChannel:
    header: parsing.SpikeHeader = attr.ib(metadata={"help": "Recording settings."})
    data: numpy.array = attr.ib(
        metadata={
            "help": "Spike record array. The Numpy data-type is given by the ``dtype`` "
            "attribute of the type returned by "
            ":attr:`plx.export.ExportedSpike`."
        }
    )


class AbstractPlxFile(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def counts(self):
        """A record containing partial event, timestamp, and waveform counts.

        :rtype: :class:`plx.parsing.Counts`
        """
        pass

    @property
    @abc.abstractmethod
    def event_headers(self):
        """An array of event channel headers.

        :rtype: :class:`recparse.RecordArray` of :class:`plx.parsing.EventHeader`
        """
        pass

    @property
    @abc.abstractmethod
    def header(self):
        """A record containing information from the main file header.

        :rtype: :class:`plx.parsing.Header`
        """
        pass

    @property
    @abc.abstractmethod
    def slow_headers(self):
        """An array of continuous channel headers.

        :rtype: :class:`recparse.RecordArray` of :class:`plx.parsing.SlowHeader`
        """
        pass

    @property
    @abc.abstractmethod
    def spike_headers(self):
        """An array of spike channel headers.

        :rtype: :class:`recparse.RecordArray` of :class:`plx.parsing.SpikeHeader`
        """
        pass

    @abc.abstractmethod
    def close(self):
        """Close any file descriptors, memmaps, and temporary directories associated with this object.
        """
        pass

    @abc.abstractmethod
    def event_data(self, channel=None):
        """A numpy record array of all concatenated events.

        The array's data type is :attr:`plx.parsing.ExportedEvent.dtype`, a type that records channel numbers,
        units (used for strobed event channels), and timestamps.
        """
        pass

    @abc.abstractmethod
    def slow_channel(self, channel) -> SlowChannel:
        """Header and recorded data of a slow (continuous A/D) channel.
        """
        pass

    @abc.abstractmethod
    def spike_channel(self, channel) -> SpikeChannel:
        """Header and recorded data of a spike (continuous A/D) channel.
        """
        pass


class PlxFile(AbstractPlxFile):
    """Support class that can directly read/parse PLX file headers and extract their channels.

    This class is meant to be used in conjunction with :class:`plx.ExportedPlxFile` (now currently
    :class:`recparse.HighLevelFile`).
    """

    def __init__(self, path, export_base_dir=None, use_c_ext=True):
        self.path = pathlib.Path(path)
        if export_base_dir is None:
            self.export_base_dir = self.path.parent
        else:
            self.export_base_dir = pathlib.Path(export_base_dir)
        self.use_c_ext = use_c_ext

    @property
    def _exported_channels(self):
        return self.export_channels()

    @property
    def data_section_offset(self):
        """Number of bytes until start of data blocks section."""
        return sum(
            [
                parsing.Header.total_size(),
                parsing.Counts.fields()["TSCounts"].size,
                parsing.Counts.fields()["WFCounts"].size,
                parsing.Counts.fields()["EVCounts"].size,
                # parsing.Counts.total_size(),
                self.header["NumDSPChannels"] * parsing.SpikeHeader.total_size(),
                self.header["NumEventChannels"] * parsing.EventHeader.total_size(),
                self.header["NumSlowChannels"] * parsing.SlowHeader.total_size(),
            ]
        )

    @property
    @functools.lru_cache(maxsize=None)
    def counts(self):
        with open(self.path, "rb") as plxfile:
            plxfile.seek(parsing.Header.total_size(), 0)
            return parsing.Counts.from_stream(plxfile)

    @property
    @functools.lru_cache(maxsize=None)
    def event_headers(self):
        return self._parse_headers(
            seek=sum(
                [
                    parsing.Header.total_size(),
                    parsing.Counts.fields()["TSCounts"].size,
                    parsing.Counts.fields()["WFCounts"].size,
                    parsing.Counts.fields()["EVCounts"].size,
                    self.header["NumDSPChannels"] * parsing.SpikeHeader.total_size(),
                ]
            ),
            buffer_length=self.header["NumEventChannels"]
            * parsing.EventHeader.total_size(),
            record_type=parsing.EventHeader,
        )

    @property
    @functools.lru_cache(maxsize=None)
    def header(self):
        with open(self.path, "rb") as plxfile:
            return parsing.Header.from_stream(plxfile)

    @property
    @functools.lru_cache(maxsize=None)
    def size(self):
        """Size of file, in bytes."""
        return os.stat(self.path).st_size

    @property
    @functools.lru_cache(maxsize=None)
    def slow_headers(self):
        return self._parse_headers(
            seek=sum(
                [
                    parsing.Header.total_size(),
                    parsing.Counts.fields()["TSCounts"].size,
                    parsing.Counts.fields()["WFCounts"].size,
                    parsing.Counts.fields()["EVCounts"].size,
                    self.header["NumDSPChannels"] * parsing.SpikeHeader.total_size(),
                    self.header["NumEventChannels"] * parsing.EventHeader.total_size(),
                ]
            ),
            buffer_length=self.header["NumSlowChannels"]
            * parsing.SlowHeader.total_size(),
            record_type=parsing.SlowHeader,
        )

    @property
    @functools.lru_cache(maxsize=None)
    def spike_headers(self):
        return self._parse_headers(
            seek=sum(
                [
                    parsing.Header.total_size(),
                    parsing.Counts.fields()["TSCounts"].size,
                    parsing.Counts.fields()["WFCounts"].size,
                    parsing.Counts.fields()["EVCounts"].size,
                ]
            ),
            buffer_length=self.header["NumDSPChannels"]
            * parsing.SpikeHeader.total_size(),
            record_type=parsing.SpikeHeader,
        )

    def _parse_counts(self, seek, size, dtype, count):
        with open(self.path, "rb") as plxfile:
            plxfile.seek(seek, 0)
            buffer = plxfile.read(size)
        return numpy.frombuffer(buffer, dtype=dtype, count=count)

    def _parse_headers(self, seek, buffer_length, record_type):
        with open(self.path, "rb") as plxfile:
            plxfile.seek(seek, 0)
            buffer = plxfile.read(buffer_length)
        return RecordArray(buffer, record_type=record_type)
        # header_array = RecordArray(buffer, record_type=record_type)
        # return {
        #     header['Channel']: header
        #     for header in header_array
        # }

    def close(self):
        self.export_channels.cache_clear()
        self.export_file.cache_clear()

        self.__class__.counts.fget.cache_clear()
        self.__class__.event_headers.fget.cache_clear()
        self.__class__.header.fget.cache_clear()
        self.__class__.size.fget.cache_clear()
        self.__class__.slow_headers.fget.cache_clear()
        self.__class__.spike_headers.fget.cache_clear()

        if isinstance(self.export_base_dir, tempfile.TemporaryDirectory):
            self.export_base_dir.cleanup()
            self.export_base_dir = tempfile.TemporaryDirectory(
                prefix=f"{self.__class__.__name__}.export", suffix=self.path.stem
            )

    def event_data(self, channel=None):
        whole_data = self._exported_channels["events"]
        if channel is None:
            return whole_data
        else:
            selection = whole_data["channel"] == channel
            return whole_data[selection]

    @functools.lru_cache(maxsize=None)
    def export_channels(self):
        """Export events, spikes, and slow waveform channel data channels into separate files and returns memory-mapped
        Numpy arrays.

        Returns
        -------
        memory_mapped_arrays: dict of :class:`numpy.memmap`
            A dictionary of memory-mapped arrays (opened in :code:`'r+b'` mode) to the exported data. This dictionary
            follows the layout

            .. code:: python

                {
                    'events': numpy.memmap(...),
                    'slow': {
                        1: numpy.memmap(...),
                        2: numpy.memmap(...),
                        ...
                    },
                    'spikes': {
                        1: numpy.memmap(...),
                        2: numpy.memmap(...),
                        ...
                    },
                }

            in which the set of keys for the slow and spike signals correspond to the channel numbers. These
            dictionaries may be empty if no data is exported from the source file, though an events file is always
            generated event if no event timestamps were recorded (it is an empty file, in this case).
        """
        export.make_dirs(self.export_base_dir)

        if self.use_c_ext:
            import _plx as _plx

            exported_channels = _plx.export_channels(
                str(self.path),
                str(export.paths.event_data(self.export_base_dir)),
                str(export.paths.slow_channels_dir(self.export_base_dir)),
                str(export.paths.spike_channels_dir(self.export_base_dir)),
            )
        else:
            exported_channels = export._export_channels(self, self.export_base_dir)

        channel_arrays = {"slow": {}, "spikes": {}}

        if exported_channels["events"]:
            channel_arrays["events"] = numpy.memmap(
                filename=str(export.paths.event_data(self.export_base_dir)),
                dtype=export.ExportedEvent.dtype,
                mode="r+",
            )
            channel_arrays["events"].sort(order="timestamp")
        else:
            channel_arrays["events"] = numpy.array([], dtype=export.ExportedEvent.dtype)

        for channel in exported_channels["slow"]:
            channel_arrays["slow"][channel] = numpy.memmap(
                filename=str(export.paths.slow_channel(self.export_base_dir, channel)),
                dtype=export.exported_slow_dtype,
                mode="r+",
            )

        for channel in exported_channels["spikes"]:
            channel_arrays["spikes"][channel] = numpy.memmap(
                filename=str(export.paths.spike_channel(self.export_base_dir, channel)),
                dtype=export.ExportedSpike(self).dtype,
                mode="r+",
            )
            channel_arrays["spikes"][channel].sort(order="timestamp")

        return channel_arrays

    @functools.lru_cache(maxsize=None)
    def export_file(self, format="bin"):
        """Export a *PLX* file into multiple smaller files.

        The exported parts may be parsed using the other definitions in this module and in :mod:`plx.parsing`, or by
        instantiating a :class:`plx.ExportedPlxFile` object with the same base directory that was passed.

        Parameters
        ----------
        format: str, optional
            Admits two values:

                ``'bin'``:
                    Export file parts defined in :mod:`plx.parsing` and :mod:`plx.export` with a binary interface
                    that preserves most of the layout of the original file, only with split parts.

                ``'json'``:
                    Export file parts to json files using schema definitions from :mod:`plx.schemas`.

        Returns
        -------
        exported: ExportedPlxFile
            An instance of :class:`ExportedPlxFile` opened in the same directory to where files where exported.
        """

        def export_part(part, schema, path):
            if format == "bin":
                content = bytes(part)
            elif format == "json":
                content = json.dumps(schema.dump(part).data, indent=2).encode()
            else:
                raise ValueError(f'Unsuported "format": {format}')

            with open(path, "wb") as file:
                file.write(content)

        export_part(
            self.header,
            schemas.Header(),
            export.paths.header(self.export_base_dir, extension=format),
        )
        export_part(
            self.counts,
            schemas.Counts(),
            export.paths.counts(self.export_base_dir, extension=format),
        )
        export_part(
            self.event_headers,
            schemas.EventHeader(many=True),
            export.paths.event_headers(self.export_base_dir, extension=format),
        )
        export_part(
            self.slow_headers,
            schemas.SlowHeader(many=True),
            export.paths.slow_headers(self.export_base_dir, extension=format),
        )
        export_part(
            self.spike_headers,
            schemas.SpikeHeader(many=True),
            export.paths.spike_headers(self.export_base_dir, extension=format),
        )

        if format == "bin":
            self.export_channels()
        if format == "json":
            warnings.warn(
                "plx.PlxFile.export_file() JSON-exports do not yet support event/slow/spike channel data!"
            )

        return ExportedPlxFile(self.export_base_dir)

    def slow_channel(self, channel):
        slow_header = self.slow_headers[channel - 1]
        try:
            slow_data = self._exported_channels["slow"][channel]
        except KeyError:
            slow_data = numpy.array([], dtype=export.exported_slow_dtype)
        return SlowChannel(header=slow_header, data=slow_data)

    def spike_channel(self, channel):
        spike_header = self.spike_headers[channel - 1]
        try:
            spike_data = self._exported_channels["spikes"][channel]
        except KeyError:
            spike_data = numpy.array([], dtype=export.ExportedSpike(self).dtype)
        return SpikeChannel(header=spike_header, data=spike_data)


class ExportedPlxFile(AbstractPlxFile):
    """Each instance of this class represents a *PLX* file that was split into several smaller files.

    Files are exported by either

    * Calling the :meth:`PlxFile.export_file` method , or
    * Using the command-line interface of the :mod:`plx` module.

    An instance of this class, which gives access to basically the same information as :class:`PlxFile`, may be
    created by calling the constructor with a path to the base directory to where files were exported. The exported
    parts are described by the record types (subclasses of :class:`recparse.Record` or
    :class:`recparse.RecordArray`) defined in modules :mod:`plx.parsing` and :mod:`plx.export` and the
    corresponding paths starting at the base directory are given by the functions in :mod:`plx.export.paths`.

    Warning
    -------
    Headers of all sorts, (*e.g.* :class:`plx.parsing.Header`, :class:`plx.parsing.EventHeader`) are
    opened in *read-only* mode, but channel data (event, spike, or slow) are opened using memory-mapped Numpy arrays
    (:class:`numpy.memmap`) in *read-write* mode, so headers cannot be modified, but channel data can. The rationale
    behind this type of behavior is two-fold:

    * It makes more sense to edit channel data on exported files, *e.g.* if applying some filtering of the data, than
      the headers, which reflect structural aspects of a *PLX* file and its channels that only make sense to change if
      recording a new file, which this library currently does not support.
    * Some sorting in this library's test suite implicitly rely on reading properties from exported headers present in the
      dataset's annex in order to correctly load reference data files that are included for evaluating library features
      (like using :attr`plx.parsing.Header.NumPointsWave` to guess the Numpy data-type of exported spike channel
      files), and these sorting fail if the library attempts to load exported header files in *read-write* mode (on some
      platforms).

    However, a reasonable alternative would be opening both headers and channel data in *copy-on-write* mode, to allow
    making changes to in-memory data without harming the original files. Both :func:`mmap.mmap` (used for loading
    exported header files) and :class:`numpy.memmap` (used for loading channel data) support this feature. This might be
    changed in a future version of the library, for instance, by including a constructor flag that specify a common
    opening mode for all exported files.

    Parameters
    ----------
    base_dir: str or pathlib.Path
        Path to base directory
    """

    def __init__(self, base_dir):
        self.base_dir = pathlib.Path(base_dir)
        self._counts_file = None
        self._header_file = None
        self._event_data = None

    @property
    @functools.lru_cache(maxsize=None)
    def counts(self):
        self._counts_file = open(export.paths.counts(self.base_dir), "rb")
        return parsing.Counts(
            mmap.mmap(
                self._counts_file.fileno(),
                length=parsing.Counts.total_size(),
                access=mmap.ACCESS_READ,
            )
        )

    @property
    @functools.lru_cache(maxsize=None)
    def header(self):
        self._header_file = open(export.paths.header(self.base_dir), "rb")
        return parsing.Header(
            mmap.mmap(
                self._header_file.fileno(),
                length=parsing.Header.total_size(),
                access=mmap.ACCESS_READ,
            )
        )

    @property
    @functools.lru_cache(maxsize=None)
    def event_headers(self):
        return self._parse_headers(
            file_name=export.paths.event_headers(self.base_dir),
            record_type=parsing.EventHeader,
        )

    @property
    @functools.lru_cache(maxsize=None)
    def slow_headers(self):
        return self._parse_headers(
            file_name=export.paths.slow_headers(self.base_dir),
            record_type=parsing.SlowHeader,
        )

    @property
    @functools.lru_cache(maxsize=None)
    def spike_headers(self):
        return self._parse_headers(
            file_name=export.paths.spike_headers(self.base_dir),
            record_type=parsing.SpikeHeader,
        )

    def _parse_headers(self, file_name, record_type):
        with open(file_name, "rb") as header_file:
            header_array = RecordArray.from_stream(header_file, record_type=record_type)
        return header_array
        # return {
        #     header['Channel']: header
        #     for header in header_array
        # }

    def close(self):
        if self._counts_file is not None:
            self._counts_file.close()

        if self._header_file is not None:
            self._header_file.close()

        self.__class__.counts.fget.cache_clear()
        self.__class__.header.fget.cache_clear()

        self.__class__.event_headers.fget.cache_clear()
        self.__class__.slow_headers.fget.cache_clear()
        self.__class__.spike_headers.fget.cache_clear()

        self.event_data.cache_clear()
        self.slow_channel.cache_clear()
        self.spike_channel.cache_clear()

        self._event_data = None

    @functools.lru_cache(maxsize=None)
    def event_data(self, channel=None):
        if self._event_data is None:
            self._event_data = numpy.fromfile(
                str(export.paths.event_data(self.base_dir)),
                dtype=export.ExportedEvent.dtype,
            )
        if channel is None:
            return self._event_data
        else:
            selection = self._event_data["channel"] == channel
            return self._event_data[selection]

    @functools.lru_cache(maxsize=None)
    def slow_channel(self, channel):
        slow_dtype = export.exported_slow_dtype

        slow_header = self.slow_headers[channel - 1]
        slow_path = export.paths.slow_channel(self.base_dir, channel=channel)
        if slow_path.exists():
            slow_data = numpy.memmap(
                filename=str(slow_path), mode="r", dtype=slow_dtype
            )
        else:
            slow_data = numpy.array([], dtype=slow_dtype)

        return SlowChannel(header=slow_header, data=slow_data)

    @functools.lru_cache(maxsize=None)
    def spike_channel(self, channel):
        spike_dtype = export.ExportedSpike(self).dtype

        spike_header = self.spike_headers[channel - 1]
        spike_path = export.paths.spike_channel(self.base_dir, channel=channel)
        if spike_path.exists():
            spike_data = numpy.memmap(
                filename=str(spike_path), mode="r", dtype=spike_dtype
            )
        else:
            spike_data = numpy.array([], dtype=spike_dtype)

        return SpikeChannel(header=spike_header, data=spike_data)
