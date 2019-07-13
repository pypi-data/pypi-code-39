
from mutagen.mp4 import MP4, MP4Cover, MP4MetadataValueError, MP4StreamInfoError

from oodi.metadata.albumart import AlbumArt
from oodi.codecs.base import BaseTagParser, ValueTotalCountTag, TagError
from oodi.codecs.mp4.constants import TAG_FIELDS, INTERNAL_FIELDS

ALBUMART_TAG = 'covr'
ALBUMART_PIL_FORMAT_MAP = {
    'JPEG':     MP4Cover.FORMAT_JPEG,
    'PNG':      MP4Cover.FORMAT_PNG
}


class MP4ValueTotalTag(ValueTotalCountTag):
    """
    AAC value/total pair tags
    """

    def get(self):
        try:
            self.value, self.total = self.parser.__entry__[self.tag][0]
        except KeyError:
            self.value = None
            self.total = None

    def save(self):
        """
        Save numbering tag value

        If self.total is not set, set it to value
        """
        if self.value is not None and self.total is None:
            self.total = self.value
        self.parser.__entry__[self.tag] = [(self.value, self.total)]
        self.parser.__entry__.save()


class MP4TagParser(BaseTagParser):
    """
    MP4 container tag processor
    """

    supports_album_art = True
    loader = MP4
    fields = TAG_FIELDS
    internal_fields = INTERNAL_FIELDS
    track_numbering_class = MP4ValueTotalTag
    disk_numbering_class = MP4ValueTotalTag
    track_numbering_tag = 'trkn'
    disk_numbering_tag = 'disk'

    def load(self, path):
        """
        Handle stream errors when loading
        """
        try:
            return super().load(path)
        except MP4StreamInfoError as e:
            raise TagError('Error loading {}: {}'.format(path, e))


    def __format_tag__(self, tag, value):
        """
        Format tag to internal tag presentation
        """
        if tag == 'bpm':
            # Format BPM to int list. Strange, yeah
            value = [int(value)]

        return value

    def has_albumart(self):
        """
        Check if albumart tag exists
        """
        return ALBUMART_TAG in self.__entry__

    def get_albumart(self):
        """
        Get data from tag to Albumart object
        """
        if ALBUMART_TAG in self.__entry__:
            albumart = AlbumArt(configuration=self.configuration, path=None)
            albumart.load_data(self.__entry__[ALBUMART_TAG][0])
            return albumart
        else:
            return None

    def set_albumart(self, albumart):
        """
        Imports albumart object to the file tags.

        Sets self.track.modified to True
        """

        file_format = albumart.file_format
        if file_format is not None:
            try:
                img_format = ALBUMART_PIL_FORMAT_MAP[file_format]
            except KeyError:
                raise TagError('Unsupported albumart format {}'.format(file_format))
        else:
            raise TagError('Error getting file format for image {} ({})'.format(
                albumart.mimetype, albumart.__image__.format
            ))

        try:
            tag = MP4Cover(data=albumart.dump(), imageformat=img_format)
        except MP4MetadataValueError as e:
            raise TagError('Error encoding albumart to mp4 tags: {}'.format(e))

        if ALBUMART_TAG in self.__entry__:
            if self.__entry__[ALBUMART_TAG] == [tag]:
                return False
            else:
                del self.__entry__[ALBUMART_TAG]

        self.__entry__[ALBUMART_TAG] = [tag]
        self.__entry__.save()
