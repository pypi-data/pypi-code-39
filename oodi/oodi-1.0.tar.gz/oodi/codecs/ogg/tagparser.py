
from ...codecs.base import BaseTagParser, ValueTotalCountTag

from .constants import TAG_FIELDS, INTERNAL_FIELDS, LIST_FIELDS


class OggNumberingTag(ValueTotalCountTag):
    """
    Ogg numbering tag.

    Stores value as value/total string
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


class OggTrackNumbering(OggNumberingTag):
    """
    OGG container track number / total tracks tags
    """
    field = 'track_number'


class OggDiskNumbering(OggNumberingTag):
    """
    OGG container disk number / total disks tags
    """
    field = 'disk_number'


class OggTagParser(BaseTagParser):
    supports_album_art = True
    fields = TAG_FIELDS
    list_fields = LIST_FIELDS
    internal_fields = INTERNAL_FIELDS
    track_numbering_class = OggTrackNumbering
    disk_numbering_class = OggDiskNumbering
