"""Internal state of emulated accelerometer firmware."""

import logging
import heapq
from collections import namedtuple
from iotile.core.exceptions import ArgumentError
from iotile.emulate.virtual import SerializableState
from iotile.emulate.constants import Error

from ..common import LSB, SAMPLE_RATE, MAX_SORTED_WAVEFORMS, TileState, Waveform


AccelerometerStatus = namedtuple("AccelerometerStatus", ['last_err', 'shock_counter', 'tile_state', 'flags1', 'state', 'flags2', 'x', 'y', 'z'])


class AccelerometerTileState(SerializableState):
    """Complete set of internal state variables for the accelerometer tile."""

    def __init__(self):
        super(AccelerometerTileState, self).__init__()

        self.threshold = int(1.0 / LSB)

        self.waveforms = []
        self.loaded_waveform = None
        self.sorted_waveforms = None
        self.erase_count = 0
        self.mode = TileState.Capturing
        self.is_recording = False
        self.should_record = False
        self.shock_cache = {
            'last': Waveform(),
            'max_g': Waveform(),
            'delta_v': Waveform()
        }

        self._logger = logging.getLogger(__name__)

        self.mark_typed_map('shock_cache', Waveform)
        self.mark_typed_list('waveforms', Waveform)
        self.mark_typed_object('loaded_waveform', Waveform)

    def control_recording(self, enabled):
        """Enable/disable recording."""

        self.should_record = enabled

        if self.mode == TileState.Capturing:
            self.is_recording = enabled

    def enter_streaming_mode(self):
        """Put the tile into streaming mode."""

        if self.mode == TileState.Streaming:
            return

        self.mode = TileState.Streaming
        self.loaded_waveform = None
        self.sorted_waveforms = None
        self.is_recording = False

    def leave_streaming_mode(self):
        """Put the tile into capture mode."""

        if self.mode == TileState.Capturing:
            return

        self.mode = TileState.Capturing
        self.loaded_waveform = None
        self.sorted_waveforms = None
        self.is_recording = self.should_record

    def enable_recording(self, enabled):
        """Enable or disable recording."""

        self.should_record = enabled
        if self.mode == TileState.Capturing:
            self.is_recording = enabled

    def sort_waveforms(self, count, sort_key, skip_id=0):
        """Find the top *count* waveforms according to sort_key."""

        if count > MAX_SORTED_WAVEFORMS:
            raise ArgumentError("Asked to sort too many waveforms, count=%d, max=%d" % (count, MAX_SORTED_WAVEFORMS))

        if self.mode != TileState.Streaming:
            raise ArgumentError("Asked to sort at invalid time, must be in streaming state")

        if sort_key == 0:
            key_extract = lambda x: x.max_g
        elif sort_key == 1:
            key_extract = lambda x: x.delta_v
        else:
            raise ArgumentError("Invalid sort key specified in sort_waveforms: %d" % sort_key)

        waveforms = self._filter_waveforms(skip_id)
        if count >= len(waveforms):
            count = len(waveforms)

        self.sorted_waveforms = heapq.nlargest(count, self.waveforms, key=key_extract)

    def _filter_waveforms(self, skip_id):
        erase_count = skip_id >> 16
        offset = skip_id & 0xFFFF

        waveforms = self.waveforms

        if erase_count < self.erase_count:
            return waveforms

        if erase_count > self.erase_count:
            raise ArgumentError("Invalid skip_id passed that is greater than the erase count")

        if offset == 0:
            return waveforms

        # The offsets are 1 based in the actual device since it stores
        # metadata in the space at index 0.
        offset -= 1
        if offset >= len(waveforms):
            return []

        return waveforms[offset:]

    def get_status(self):
        """Return the status of the tile."""

        return AccelerometerStatus(0, len(self.waveforms), self.mode, 0, 0, 0, 1, -13, 15)

    def add_shock(self, data):
        """Add a shock to our stored waveforms."""

        if len(data) != 1024:
            raise ArgumentError("Each shock must have 1024 samples: length=%d" % len(data))

        for i, item in enumerate(data):
            if len(item) != 3:
                raise ArgumentError("Each shock sample must have 3 components (x, y, z): item %d was %s" % (i, item))

        unique_id = (self.erase_count << 16) | (len(self.waveforms) + 1)
        wave = Waveform(data, SAMPLE_RATE, self.threshold, unique_id=unique_id)

        self.shock_cache['last'] = wave

        if wave.max_g > self.shock_cache['max_g'].max_g:
            self.shock_cache['max_g'] = wave

        if wave.delta_v > self.shock_cache['delta_v'].delta_v:
            self.shock_cache['delta_v'] = wave

        self.waveforms.append(wave)

    def load_shock(self, index):
        """Load a compressed waveform from flash into RAM for streaming."""

        if index >= len(self.waveforms):
            raise ArgumentError("Invalid shock index in load_shock: %d (count=%d)" % (index, len(self.waveforms)))

        self.loaded_waveform = self.waveforms[index].compress()
