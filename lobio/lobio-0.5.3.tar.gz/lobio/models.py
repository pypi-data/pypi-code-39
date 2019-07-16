from abc import ABC

from Bio.SeqRecord import SeqRecord
from Bio.SeqFeature import SeqFeature, CompoundLocation
from functools import wraps
from .region import Region
from .SeqUtils import make_circular_location, is_circular
from copy import deepcopy
from .exceptions import StrictFeatureError


def region_to_feature_location(region):
    """Convert a Region to a FeatureLocation or CompoundLocation if appropriate."""
    return make_circular_location(
        region.a, region.b, region.context_length, region.direction
    )


def feature_locations_to_regions(locations, length, cyclic):
    """Convert locations to a list of regions."""
    regions = []
    for location in locations:
        for part in location.parts:
            strand = part.strand
            regions.append(
                Region(part.start, part.end, length, cyclic=cyclic, direction=strand)
            )
    return regions


def bind_feature_to_context(feature, length, cyclic, start=None, end=None, strand=None):
    """
    Validates a SeqFeature against sequence topology and size. Modifies location features
    to match the context. If location is a Compound
    """
    locations = []
    if None in [start, end, strand]:
        if not all(x is None for x in [start, end, strand]):
            raise ValueError(
                "Arguments 'start', 'end', 'and' strand must either all be None or all be ints."
            )
        if feature.location:
            regions = feature_locations_to_regions(
                feature.location.parts, length, cyclic
            )
            locations += [region_to_feature_location(r) for r in regions]
    else:
        region = Region(start, end, length, cyclic=cyclic, direction=strand)
        locations.append(region_to_feature_location(region))
    if len(locations) > 1:
        feature.location = CompoundLocation(locations)
    elif locations:
        feature.location = locations[0]
    else:
        raise StrictFeatureError("Cannot create feature. No locations were found.")
    return feature


class ImmutableException(Exception):
    @classmethod
    def do_raise(cls, instance, prop, msg=""):
        errmsg = "Cannot set immutable property '{}'. {} is immutable.".format(
            prop, instance.__class__
        )
        if msg:
            errmsg += " " + msg
        return cls(errmsg)


class ImmutableSeqFeature(SeqFeature):
    @wraps(SeqFeature.__init__)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_seq_feature(self):
        pass

    @property
    def location(self):
        return super().location

    @location.setter
    def location(self, l):
        if self.location:
            raise ImmutableException.do_raise(self, "location")
        else:
            super().location = l


class Constants(object):

    TOPOLOGY = "topology"
    CIRCULAR = "circular"
    LINEAR = "linear"


class ImmutableSeqRecord(SeqRecord, ABC):
    """
    A SeqRecord object with strict requirements for locations of SeqFeatures.

    Features:
        1. feature locations are validated against topology and size of sequence
        2. Seq instance cannot be changed
    """

    @wraps(SeqRecord.__init__)
    def __init__(self, *args, circular=False, **kwargs):
        self._features = []
        super().__init__(*args, **kwargs)
        self.circular = circular
        for f in self.features:
            bind_feature_to_context(f)

    def _init(self):
        for f in self.features:
            bind_feature_to_context(f)

    @classmethod
    def from_seq_record(cls, record):
        return cls(
            seq=record.seq,
            id=record.id,
            name=record.name,
            description=record.description,
            dbxrefs=deepcopy(record.dbxrefs),
            features=deepcopy(record.features),
            annotations=deepcopy(record.annotations),
            letter_annotations=deepcopy(record.letter_annotations),
        )

    def to_seq_record(self):
        return SeqRecord(
            seq=self.seq,
            id=self.id,
            name=self.name,
            description=self.description,
            dbxrefs=deepcopy(self.dbxrefs),
            features=list(deepcopy(self.features)),
            annotations=deepcopy(self.annotations),
            letter_annotations=deepcopy(self.letter_annotations),
        )

    @property
    def circular(self):
        return is_circular(self)

    @circular.setter
    def circular(self, b):
        if b:
            self.annotations[Constants.TOPOLOGY] = Constants.CIRCULAR
        else:
            self.annotations[Constants.TOPOLOGY] = Constants.LINEAR

    @property
    def features(self):
        return tuple(self._features)

    def __add__(self, other):
        return self.from_seq_record(self.to_seq_record() + other.to_seq_record())

    @features.setter
    def features(self, featurelist):
        for f in featurelist:
            self.add_feature(f)

    def add_feature(self, feature, start=None, end=None, strand=None):
        bind_feature_to_context(feature, len(self), self.circular, start, end, strand)
        self._features.append(feature)

    @property
    def context(self):
        return len(self), self.circular

    @property
    def seq(self):
        return super().seq

    @seq.setter
    def seq(self, s):
        if self.seq:
            raise ImmutableException.do_raise(self, "seq")
        else:
            super().seq = s
