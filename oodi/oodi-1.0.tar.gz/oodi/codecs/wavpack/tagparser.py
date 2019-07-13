
from mutagen.wavpack import WavPack

from ...codecs.base import BaseTagParser, ValueTotalCountTag
from .constants import TAG_FIELDS, INTERNAL_FIELDS, LIST_FIELDS


class WavpackTotalCountTag(ValueTotalCountTag):
    """
    Count / value tags for wavpack
    """

    def get(self):
        """
        Get data from ogg metadata numbering tag
        """
        try:
            data = self.parser.__entry__[self.parser.fields[self.field][0]][0].split('/')
            self.value = int(data[0])
            if len(data) > 1:
                self.total = int(data[1])
        except KeyError:
            self.value = None
            self.total = None

    def save(self):
        """
        Method to save ogg metadata numbering tag
        """
        if self.total is not None:
            self.parser.__entry__[self.parser.fields[self.field][0]] = '{}/{}'.format(
                self.value,
                self.total
            )
        else:
            self.parser.__entry__[self.parser.fields[self.field][0]] = '{}'.format(self.value)
        self.parser.__entry__.save()


class WavpackTrackNumbering(WavpackTotalCountTag):
    """
    Wavpack container track number / total tracks tags
    """
    field = 'track_number'


class WavpackDiskNumbering(WavpackTotalCountTag):
    """
    Wavpack container disk number / total disks tags
    """
    field = 'disk_number'


class TagParser(BaseTagParser):
    """
    Wavpack tag processor
    """

    format = 'wavpack'
    loader = WavPack
    track_numbering_class = WavpackTrackNumbering
    disk_numbering_class = WavpackDiskNumbering
    fields = TAG_FIELDS
    list_fields = LIST_FIELDS
    internal_fields = INTERNAL_FIELDS

    def __getattr__(self, attr):
        value = super().__getattr__(attr)
        if value is not None:
            value = value.value
        return value
