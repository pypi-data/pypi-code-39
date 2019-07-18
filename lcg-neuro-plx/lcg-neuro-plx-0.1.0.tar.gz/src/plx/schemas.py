"""Marshmallow_ schemas for the parts of a PLX file.

.. todo:: It would be great to have automatic schemas generated from the record parsing library!
"""

from marshmallow_patch.marshmallow import Schema, fields


class Counts(Schema):
    timestamps = fields.NumpyArray(without_dtype=True)
    waveforms = fields.NumpyArray(without_dtype=True)
    events = fields.NumpyArray(without_dtype=True)

    class Meta:
        ordered = True
        strict = True


class Event(Schema):
    Timestamp = fields.Integer(attribute="timestamp")
    Channel = fields.Integer(attribute="channel")
    Unit = fields.Integer(attribute="unit")
    Padding = fields.String(attribute="padding")

    class Meta:
        ordered = True
        strict = True


class EventHeader(Schema):
    Name = fields.String(attribute="name")
    Channel = fields.Integer(attribute="channel")
    Comment = fields.String(attribute="comment")

    class Meta:
        ordered = True
        strict = True


class EventData(Schema):
    headers = fields.Nested(EventHeader(many=True))
    events = fields.Nested(Event(many=True))

    class Meta:
        ordered = True
        strict = True


class Header(Schema):
    MagicNumber = fields.Integer(attribute="magic_number")
    Version = fields.Integer(attribute="version")
    Comment = fields.String(attribute="comment")
    ADFrequency = fields.Integer()
    NumDSPChannels = fields.Integer(attribute="num_dsp_channels")
    NumEventChannels = fields.Integer(attribute="num_event_channels")
    NumSlowChannels = fields.Integer(attribute="num_slow_channels")
    NumPointsWave = fields.Integer(attribute="num_points_wave")
    NumPointsPreThr = fields.Integer(attribute="num_points_pre_thr")
    Year = fields.Integer()
    Month = fields.Integer()
    Day = fields.Integer()
    Hour = fields.Integer()
    Minute = fields.Integer()
    Second = fields.Integer()
    FastRead = fields.Integer()
    WaveformFreq = fields.Integer()
    LastTimestamp = fields.Float()
    Trodalness = fields.Integer(attribute="trodalness")
    DataTrodalness = fields.Integer(attribute="data_trodalness")
    BitsPerSpikeSample = fields.Integer(attribute="bits_per_spike_sample")
    BitsPerSlowSample = fields.Integer(attribute="bits_per_slow_sample")
    SpikeMaxMagnitudeMV = fields.Integer()
    SlowMaxMagnitudeMV = fields.Integer()
    SpikePreAmpGain = fields.Integer(attribute="spike_pream_gain")

    class Meta:
        ordered = True
        strict = True


class SlowHeader(Schema):
    Name = fields.String(attribute="name")
    Channel = fields.Integer(attribute="channel")
    ADFreq = fields.Integer()
    Gain = fields.Integer(attribute="gain")
    Enabled = fields.Integer()
    PreAmpGain = fields.Integer(attribute="pre_amp_gain")
    SpikeChannel = fields.Integer(attribute="spike_channel")
    Comment = fields.String(attribute="comment")

    class Meta:
        ordered = True
        strict = True


class SlowChannel(Schema):
    header = fields.Nested(SlowHeader)
    data = fields.NumpyArray()

    class Meta:
        ordered = True
        strict = True


class SpikeHeader(Schema):
    Name = fields.String(attribute="name")
    SIGName = fields.String(attribute="sig_name")
    Channel = fields.Integer(attribute="channel")
    WFRate = fields.Integer()
    SIG = fields.Integer(attribute="sig")
    Ref = fields.Integer(attribute="ref")
    Gain = fields.Integer(attribute="gain")
    Filter = fields.Integer()
    Threshold = fields.Integer(attribute="threshold")
    Method = fields.Integer()
    NUnits = fields.Integer(attribute="no_units")
    Template = fields.NumpyArray()
    Fit = fields.NumpyArray()
    SortWidth = fields.Integer()
    Boxes = fields.NumpyArray()
    SortBeg = fields.Integer()
    Comment = fields.String(attribute="comment")

    class Meta:
        ordered = True
        strict = True


class SpikeData(Schema):
    Timestamp = fields.Integer(attribute="timestamp")
    Unit = fields.Integer(attribute="unit")
    Waveform = fields.NumpyArray(attribute="waveform")
    Padding = fields.String(attribute="padding")

    class Meta:
        ordered = True
        strict = True


class SpikeChannel(Schema):
    header = fields.Nested(SpikeHeader)
    data = fields.Nested(SpikeData(many=True))

    class Meta:
        ordered = True
        strict = True


class PlxFile(Schema):
    header = fields.Nested(Header)
    counts = fields.Nested(Counts)
    spike_headers = fields.Nested(SpikeHeader(many=True))
    event_headers = fields.Nested(EventHeader(many=True))
    slow_headers = fields.Nested(SlowHeader(many=True))
