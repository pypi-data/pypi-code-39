"""Emulator for Accelerometer Tile."""

import logging
from iotile.core.hw.virtual import tile_rpc
from iotile.core.hw.virtual.common_types import pack_rpc_payload
from iotile.emulate.virtual import EmulatedPeripheralTile
from iotile.core.hw.exceptions import AsynchronousRPCResponse
from iotile.emulate.constants import Error

from .emulator import AccelerometerTileState
from .common import MAX_WAVEFORMS, TileState, build_waveform


class AccelerometerTile(EmulatedPeripheralTile):
    """Emulator for accelerometer tile."""

    name = b'accel1'

    def __init__(self, address, _args, device=None):
        EmulatedPeripheralTile.__init__(self, address, device)

        self.state = AccelerometerTileState()
        self.register_scenario('load_shocks', self.load_shocks)
        self._work = self._device.emulator.create_queue(register=False)
        self._logger = logging.getLogger(__name__)
        self._should_cancel_streaming = False

    async def _trace_waveform(self, compressed):
        self._logger.debug("Tracing waveform with length=%d", len(compressed.data))

        success = await self._device.trace_sync(compressed.header)

        if not success:
            return

        for i in range(0, len(compressed.data), 20):
            chunk = compressed.data[i:i + 20]

            success = await self._device.trace_sync(chunk)
            if not success:
                return

        self._logger.debug("Finished tracing waveform successfully")

    async def _worker_trace_one(self):
        if self.state.loaded_waveform is None:
            self._logger.error("Trace waveform called without a loaded waveform")
            return

        await self._trace_waveform(self.state.loaded_waveform)

    async def _worker_trace_sorted(self):
        self._device.emulator.finish_async_rpc(self.address, 0x803e, "HHH", Error.NO_ERROR, len(self.state.sorted_waveforms), 0)

        for waveform in self.state.sorted_waveforms:
            if self._should_cancel_streaming:
                self._should_cancel_streaming = False
                self._logger.debug("Cancelling waveform streaming")
                break

            self.state.load_shock(waveform.index - 1)
            await self._trace_waveform(self.state.loaded_waveform)

    def _worker_enter_streaming(self):
        self.state.enter_streaming_mode()
        self._device.emulator.finish_async_rpc(self.address, 0x8038, "L", Error.NO_ERROR)

    def _worker_leave_streaming(self):
        self.state.leave_streaming_mode()
        self._device.emulator.finish_async_rpc(self.address, 0x8039, "L", Error.NO_ERROR)

    def _worker_sort_waveforms(self, skip_id, count, sort_key):
        self.state.sort_waveforms(count, sort_key, skip_id)
        self._device.emulator.finish_async_rpc(self.address, 0x803a, "LL", Error.NO_ERROR, len(self.state.sorted_waveforms))

    async def _application_main(self):
        self.initialized.set()

        while True:
            action, args = await self._work.get()
            if args is None:
                args = tuple()

            try:
                action(*args)
            except:  #pylint:disable=bare-except;This is a background server-style task
                self._logger.exception("Error processing work item %s, args=%s", action, args)

    def load_shocks(self, count=1, max_g=3.5, axis="z", duration=40):
        """Load a fixed number of identical shocks into the tile.

        This scenario will add ``count`` shocks that are all identical and
        have a fixed peak G value on a fixed ``axis`` (defaults to z).
        Each shock has a single bump with the given duration of ``duration``
        samples.
        """

        data = build_waveform(max_g, duration, rise_time=10, axis=axis)

        for _ in range(0, count):
            self.state.add_shock(data)

    def dump_state(self):
        """Dump the current state of this emulated object as a dictionary.

        Returns:
            dict: The current state of the object that could be passed to load_state.
        """

        return self.state.dump()

    def restore_state(self, state):
        """Restore the current state of this emulated object.

        Args:
            state (dict): A previously dumped state produced by dump_state.
        """

        self.state.restore(state)

    @tile_rpc(0x8003, "", "L")
    def count_shocks(self):
        """Count how many shocks we have."""

        return [len(self.state.waveforms)]

    @tile_rpc(0x8004, "xB", "HHLLL")
    def get_shock_info(self, index):
        """Get packed summary information about a stored shock."""

        if index == 1:
            shock = self.state.shock_cache['max_g']
        elif index == 2:
            shock = self.state.shock_cache['delta_v']
        else:
            shock = self.state.shock_cache['last']

        return shock.packed_summary()

    @tile_rpc(0x8006, "", "LLBBBB3h2x")
    def get_status(self):
        """Get the packed status of the accelerometer tile."""

        return self.state.get_status()

    @tile_rpc(0x8030, "", "LLL")
    def flash_info(self):
        """Get information about how much data is stored in flash."""

        return [len(self.state.waveforms), MAX_WAVEFORMS, self.state.erase_count]

    @tile_rpc(0x803c, "H", "HHHH")
    def load_compressed_waveform(self, index):
        """Load a compressed waveform by index."""

        if self.state.mode != TileState.Streaming:
            return [Error.STATE_CHANGE_AT_INVALID_TIME, 0, 0, 0]

        if index >= len(self.state.waveforms):
            return [Error.INVALID_ARRAY_KEY, 0, 0, 0]

        self.state.load_shock(index)
        return [0, 0, len(self.state.loaded_waveform.data), index]

    @tile_rpc(0x8038, "", "L")
    def enter_streaming_mode(self):
        """Put the tile into streaming mode."""

        self._work.put_nowait((self._worker_enter_streaming, None))
        raise AsynchronousRPCResponse()

    @tile_rpc(0x8039, "", "L")
    def leave_streaming_mode(self):
        """Take the tile out of streaming mode."""

        self._work.put_nowait((self._worker_leave_streaming, None))
        raise AsynchronousRPCResponse()

    @tile_rpc(0x8035, "", "L")
    def pause_recording(self):
        """Stop recording data."""

        self.state.control_recording(False)
        return [Error.NO_ERROR]

    @tile_rpc(0x8036, "", "L")
    def resume_recording(self):
        """Start or resume recording data."""

        self.state.control_recording(True)
        return [Error.NO_ERROR]

    @tile_rpc(0x803a, "LHB", "LL")
    def sort_waveforms(self, skip_id, count, sort_key):
        """Sort all stored waveforms."""

        if self.state.mode != TileState.Streaming:
            return [Error.STATE_CHANGE_AT_INVALID_TIME, 0]

        self._work.put_nowait((self._worker_sort_waveforms, (skip_id, count, sort_key)))
        raise AsynchronousRPCResponse()

    @tile_rpc(0x803b, "H", "V")
    def sorted_waveform_indices(self, offset):
        """Download a chunk of the list of sorted waveform indices."""

        if self.state.sorted_waveforms is None or offset >= len(self.state.sorted_waveforms):
            return [b'']

        chunk = self.state.sorted_waveforms[offset: offset + 10]
        return [pack_rpc_payload("%dH" % len(chunk), [x.index for x in chunk])]

    @tile_rpc(0x803d, "", "L")
    def trace_single_waveform(self):
        """Trace at high speed the currently loaded waveform."""

        if self.state.mode != TileState.Streaming:
            return [Error.NO_ERROR]

        if self.state.loaded_waveform is None:
            return [Error.STATE_CHANGE_AT_INVALID_TIME]

        self._work.put_nowait((self._worker_trace_one, None))
        return [Error.NO_ERROR]

    @tile_rpc(0x803e, "", "V")
    def stream_sorted_waveforms(self):
        """Stream sorted waveforms."""

        if self.state.mode != TileState.Streaming:
            return [pack_rpc_payload("L", Error.NO_ERROR)]

        self._work.put_nowait((self._worker_trace_sorted, None))
        raise AsynchronousRPCResponse()

    @tile_rpc(0x8034, "", "L")
    def force_capture_waveform(self):
        """Forcibly capture a single waveform."""

        self.load_shocks(count=1)
        return [Error.NO_ERROR]
