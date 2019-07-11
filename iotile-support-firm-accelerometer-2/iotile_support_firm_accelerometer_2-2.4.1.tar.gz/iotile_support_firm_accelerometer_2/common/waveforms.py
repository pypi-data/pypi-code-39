import struct
import itertools
import logging
from collections import namedtuple
from base64 import b64encode, b64decode

from iotile.core.exceptions import ArgumentError

from .constants import LSB, G_CONST, SAMPLE_RATE
from .heatshrink import Heatshrink
from .utilities import convert_axis


ShockSummary = namedtuple("ShockSummary", ['peak_axis', 'duration', 'delta_v_x', 'delta_v_y', 'delta_v_z'])
CompressedWaveform = namedtuple("CompressedWaveform", ['load_error', 'index', 'crc_code', 'header', 'data'])


class Waveform(object):
    """A single shock waveform with 1024 x,y,z samples and processing methods."""

    def __init__(self, data=None, sampling_rate=SAMPLE_RATE, threshold=int(1.0/LSB), unique_id=0):
        if data is None:
            self.x = [0]*1024
            self.y = [0]*1024
            self.z = [0]*1024
        else:
            if not isinstance(data, list):
                data = list(data)

            self.x = [int(x[0]) for x in data]
            self.y = [int(x[1]) for x in data]
            self.z = [int(x[2]) for x in data]

        self.sampling_rate = sampling_rate
        self.threshold = threshold
        self.summary = self._summarize_waveform()
        self._logger = logging.getLogger(__name__)
        self.unique_id = unique_id
        self.index = unique_id & 0xFFFF


    @property
    def delta_v(self):
        return max(abs(self.summary['delta_v_x']), abs(self.summary['delta_v_y']), 
                   abs(self.summary['delta_v_z']))

    @property
    def max_g(self):
        return self.summary['peak']

    @property
    def duration(self):
        return self.summary['duration']

    def packed_summary(self):
        """Return a ShockSummary namedtuple with packed information."""

        peak_axis = (int(self.max_g / LSB) << 2) | convert_axis(self.summary['axis'])
        duration = int(self.duration)
        delta_v_x = int(self.summary['delta_v_x']) << 16
        delta_v_y = int(self.summary['delta_v_y']) << 16
        delta_v_z = int(self.summary['delta_v_z']) << 16

        return ShockSummary(peak_axis, duration, delta_v_x, delta_v_y, delta_v_z)

    def dump(self):
        return {
            'sampling_rate': self.sampling_rate,
            'threshold': self.threshold,
            'x_data': b64encode(struct.pack("<1024h", *self.x)).decode('utf-8'),
            'y_data': b64encode(struct.pack("<1024h", *self.y)).decode('utf-8'),
            'z_data': b64encode(struct.pack("<1024h", *self.z)).decode('utf-8')
        }

    @classmethod
    def Restore(cls, data):
        """Restore a Waveform from the results of dump()."""

        x_data = struct.unpack("<1024h", b64decode(data['x_data']))
        y_data = struct.unpack("<1024h", b64decode(data['y_data']))
        z_data = struct.unpack("<1024h", b64decode(data['z_data']))

        assert len(x_data) == 1024
        assert len(y_data) == 1024
        assert len(z_data) == 1024

        return Waveform(zip(x_data, y_data, z_data), data['sampling_rate'], data['threshold'])

    @classmethod
    def Build(cls, peak, duration, rise_time, axis='x', start=200):
        """Build a shock waveform for injecting into the tile.

        Args:
            peak (float): The peak value of the shock in G's
            duration (float): The duration of the shock in ms
            rise_time (float): The rise and fall times of the shock in ms
            axis (str): The axis to build the waveform on: x, y or z
        """

        data = build_waveform(peak, duration, rise_time, axis, start)
        return Waveform(data)

    def _summarize_waveform(self):
        """Create summary data for a waveform."""

        x_data = self.x
        y_data = self.y
        z_data = self.z

        assert len(x_data) == 1024
        assert len(y_data) == 1024
        assert len(z_data) == 1024

        max_x = max(_abslist(x_data))
        max_y = max(_abslist(y_data))
        max_z = max(_abslist(z_data))

        max_g = max(max_x, max(max_y, max_z))

        if max_g == max_x:
            axis = 'x'
        elif max_g == max_y:
            axis = 'y'
        else:
            axis = 'z'

        dur_x = _time_above_threshold(x_data, self.threshold, self.sampling_rate)
        dur_y = _time_above_threshold(y_data, self.threshold, self.sampling_rate)
        dur_z = _time_above_threshold(z_data, self.threshold, self.sampling_rate)

        dur = max(dur_x, max(dur_y, dur_z))

        return {
            'peak': max_g * LSB,
            'axis': axis,
            'duration': dur,
            'delta_v_x': _delta_v(x_data, self.threshold, self.sampling_rate),
            'delta_v_y': _delta_v(y_data, self.threshold, self.sampling_rate),
            'delta_v_z': _delta_v(z_data, self.threshold, self.sampling_rate)
        }

    def encode(self):
        """Encode this waveform for streaming.

        This method will perform the following transformations:

        1. It will pack the 3 axis sequentially so all of x, all
           of y, all of z.
        2. It will delta encode all of the data
        3. It will apply a variable length integer encoding to
           each number.
        4. It will pass the result through a Heatshrink compressor.

        Returns:
            bytes: The compressed and encoded bytes.
        """

        out = bytearray(1024)
        out_ctr = 0

        last = 0
        for curr in itertools.chain(iter(self.x), iter(self.y), iter(self.z)):
            curr -= last
            last += curr

            zigzag = (curr >> 15) ^ (curr << 1)
            while zigzag > 127:
                if out_ctr == len(out):
                    old_data = out
                    out = bytearray(2*len(out))
                    out[:len(old_data)] = old_data

                out[out_ctr] = (zigzag & ((1 << 7) - 1)) | 0x80
                zigzag >>= 7
                out_ctr += 1

            if out_ctr == len(out):
                old_data = out
                out = bytearray(2*len(out))
                out[:len(old_data)] = old_data

            out[out_ctr] = zigzag
            out_ctr += 1

        out = out[:out_ctr]
        data = Heatshrink().encode(out)
        return data

    def compress(self):
        """Create a CompresedWavefrom from this Waveform.

        Compressed waveforms are what are sent via the tracing interface out
        of a device.

        Returns:
            CompressedWaveform: The compressed waveform data
        """

        data = self.encode()

        try:
            import crcmod
            crc32_func = crcmod.mkCrcFun(0x104C11DB7, initCrc=0xFFFFFFFF, rev=False, xorOut=0)
            checksum = crc32_func(bytes(data)) & 0xFFFFFFFF
        except ImportError:
            self._logger.warning("Not calculting crc code of compressed waveform because crcmod package is not installed")
            checksum = 0xFFFFFFFF

        index = self.unique_id & 0xFFFF
        header = struct.pack("<BBHLLLL", 1, 0, len(data), self.unique_id, 0xFFFFFFFF, checksum, 0)

        return CompressedWaveform(0, index, checksum, header, data)


def _time_above_threshold(data, thresh, sampling_rate):
    """Return the number of ms that a given time series is above a threshold."""

    max_count = 0
    curr_count = 0
    above = False
    last_sample = 0.0

    for sample in data:
        if above is False and abs(sample) >= thresh:
            above = True
            curr_count = 0
        elif above:
            curr_count += 1
            if abs(sample) < thresh or last_sample*sample < 0.0:
                above = False
                if curr_count > max_count:
                    max_count = curr_count

        last_sample = sample

    if above and curr_count > max_count:
        max_count = curr_count

    return max_count / sampling_rate * 1000.0


def _delta_v(data, thresh, sampling_rate):
    """Calculate the largest delta_v for the timeseries.

    This assumes data is in ADC units and returns an answer in m/s.
    """

    max_dv = 0
    curr_dv = 0
    above = False
    last_sample = 0.0

    for sample in data:
        if above is False and abs(sample) >= thresh:
            above = True
            curr_dv = sample*LSB
        elif above:
            curr_dv += sample*LSB
            if abs(sample) < thresh or last_sample*sample < 0.0:
                above = False
                if abs(curr_dv) > abs(max_dv):
                    max_dv = curr_dv

        last_sample = sample

    if above and abs(curr_dv) > abs(max_dv):
        max_dv = curr_dv

    return max_dv * G_CONST / sampling_rate


def _abslist(indata):
    return [abs(x) for x in indata]


def build_waveform(peak, duration, rise_time, axis='x', start=200, total=1024):
    """Build a shock waveform for injecting into the tile.

    Args:
        peak (float): The peak value of the shock in G's
        duration (float): The duration of the shock in ms
        rise_time (float): The rise and fall times of the shock in ms
        axis (str): The axis to build the waveform on: x, y or z
    """

    sample_time = 1.0/SAMPLE_RATE*1000.0

    samples = []

    rise_samples = int(rise_time / sample_time)
    top_samples = int(duration / sample_time)

    if (start + rise_samples + top_samples) >= total:
        raise ArgumentError("Specified waveform would not fit in %d samples" % total)

    for i in range(0, start):
        samples.append(0)

    for i in range(0, rise_samples):
        value = int(peak / LSB * (float(i) / rise_samples))
        samples.append(value)

    for i in range(0, top_samples):
        value = int(peak / LSB)
        samples.append(value)

    for i in range(0, rise_samples):
        value = int(peak / LSB * (float(rise_samples - i - 1) / rise_samples))
        samples.append(value)

    while len(samples) < total:
        samples.append(0)

    other = [0]*total

    if axis == 'x':
        iterator = zip(samples, other, other)
    elif axis == 'y':
        iterator = zip(other, samples, other)
    else:
        iterator = zip(other, other, samples)

    return list(iterator)
