"""Shared global constants defined in firm_accelerometer."""

LSB = 0.049
SAMPLE_RATE = 3200.0 / 3
MAX_WAVEFORMS = 2047
MAX_SORTED_WAVEFORMS = 100
G_CONST = 9.80665


class TileState(object):
    """Possible tile states."""

    Initializing = 0
    Capturing = 1
    Streaming = 2
