from Bio.SeqRecord import SeqRecord
from Bio.SeqFeature import SeqFeature, CompoundLocation
from functools import wraps
from .region import Context, Region
from .SeqUtils import make_circular_location, is_circular


def region_to_feature_location(region):
    """Convert a Region to a FeatureLocation or CompoundLocation if appropriate."""
    return make_circular_location(
        region.lp, region.rp + 1, region.context_length, region.direction
    )


def feature_locations_to_regions(locations, context):
    """Convert locations to a list of regions."""
    regions = []
    for location in locations:
        for part in location.parts:
            start = part.start
            end = part.end - 1
            strand = part.strand
            regions.append(Region(start, end, context, strand))
    return regions


def bind_feature_to_context(feature, context, start=None, end=None, strand=None):
    """
    Validates a SeqFeature against sequence topology and size. Modifies location features
    to match the context. If location is a Compound

    :param feature:
    :type feature: SeqFeature
    :param context:
    :type context: Context
    :param start: inclusive start position
    :type start: int
    :param end: exclusive end position of the feature.
    :type end: int
    :param strand: direction (1 or -1)
    :type strand: int
    :return:
    :rtype: SeqFeature
    """
    locations = []
    if not all((start, end, strand)):
        regions = feature_locations_to_regions(feature.location.parts, context)
        locations += [region_to_feature_location(r) for r in regions]
    else:
        region = Region(start, end - 1, context, strand)
        locations.append(region_to_feature_location(region))
    if len(locations) > 1:
        feature.location = CompoundLocation(locations)
    elif locations:
        feature.location = locations[0]
    else:
        raise Exception("No locations.")
    return feature


class ImmutableException(Exception):
    @classmethod
    def do_raise(cls, instance, property, msg=""):
        errmsg = "Cannot set immutable property '{}'. {} is immutable.".format(
            property, instance.__class__
        )
        if msg:
            errmsg += " " + msg
        return cls(errmsg)


class ImmutableSeqFeature(SeqFeature):
    @wraps(SeqFeature.__init__)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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


class ImmutableSeqRecord(SeqRecord):
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
        self._context = Context(
            length=len(self), circular=self.circular, start_index=0, strict=True
        )
        for f in self.features:
            bind_feature_to_context(f)

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

    @features.setter
    def features(self, featurelist):
        for f in featurelist:
            self.add_feature(f)

    def add_feature(self, feature, start=None, end=None, strand=None):
        bind_feature_to_context(feature, self.context, start, end, strand)
        self._features.append(feature)

    @property
    def context(self):
        return self._context

    @property
    def seq(self):
        return super().seq

    @seq.setter
    def seq(self, s):
        if self.seq:
            raise ImmutableException.do_raise(self, "seq")
        else:
            super().seq = s
