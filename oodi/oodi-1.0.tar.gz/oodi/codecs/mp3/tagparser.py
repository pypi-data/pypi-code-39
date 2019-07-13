
import os

from mutagen.mp3 import MP3
from mutagen.id3 import ID3

from ...codecs.base import BaseTagParser, ValueTotalCountTag
from .constants import TAG_FIELDS


class Mp3ValueTotalTag(ValueTotalCountTag):
    """
    MP3 value total track argument pairs
    """
    field = None

    def get(self):
        """
        Get MP3 numbering details
        """
        try:
            data = self.parser.__entry__[self.field].text[0].split('/')
            self.value = int(data[0])
            self.total = int(data[1])
        except KeyError:
            self.value = None
            self.total = None

    def save(self):
        """
        Save MP3 numbering details
        """
        if self.total is not None:
            value = '{}/{}'.format(self.value, self.total)
        else:
            value = '{}/{}'.format(self.value, self.value)

        self.parser.__entry__[self.field] = self.parser.__format_tag__(self.numbering_tag, value)
        self.parser.__entry__.save()


class MP3TrackNumberingTag(Mp3ValueTotalTag):
    numbering_tag = 'track_number'
    field = 'TRKN'


class MP3DiskNumberingTag(Mp3ValueTotalTag):
    numbering_tag = 'disk_number'
    field = 'TPOS'


class MP3CommentTag:
    """
    MP3 comment with language code 'eng'
    """
    def __init__(self, parser, lang='eng'):
        self.parser = parser
        self.lang = lang
        self.__tag__ = 'COMM::{}'.format(self.lang)

    @property
    def value(self):
        try:
            return self.parser.__entry__[self.__tag__].text[0]
        except KeyError:
            return None

    @value.setter
    def value(self, value):
        from mutagen.id3._specs import Encoding
        from mutagen.id3 import COMM
        self.parser.__entry__[self.__tag__] = COMM(
            encoding=Encoding.UTF8,
            lang=self.lang,
            text=value
        )
        self.parser.__entry__.save()

    def delete(self):
        """
        Delete comment tag from file if defined
        """
        if self.value:
            del self.parser.__entry__[self.__tag__]
            self.parser.__entry__.save()


class TagParser(BaseTagParser):
    """
    MP3 tag processor
    """
    format = 'mp3'
    loader = MP3
    fields = TAG_FIELDS
    track_numbering_class = MP3TrackNumberingTag
    disk_numbering_class = MP3DiskNumberingTag

    def __delattr__(self, attr):
        """
        Delete AIFF tags
        """
        if attr == 'comment':
            MP3CommentTag(self).delete()
        else:
            return super().__delattr__(attr)

    def __getattr__(self, attr):
        if attr == 'comment':
            return MP3CommentTag(self).value
        else:
            value = super().__getattr__(attr)
            if value is not None:
                return value.text[0]
        return None

    def __setattr__(self, attr, value):
        """
        Set MP3 tags
        """
        if attr == 'comment':
            MP3CommentTag(self).value = value
        else:
            super().__setattr__(attr, value)

    def __format_tag__(self, tag, value):
        """
        Format tag as MP3 frame for saving
        """
        from mutagen.id3._specs import Encoding

        if not isinstance(value, list):
            value = [value]

        try:
            field = self.fields[tag][0]
            m = __import__('mutagen.id3', globals(), {}, tag)
            frame = getattr(m, field)
            if frame is None:
                raise AttributeError
            return frame(encoding=Encoding.UTF8, text=value)
        except AttributeError as e:
            raise ValueError('Error importing ID3 frame {}: {}'.format(tag, e))

    def items(self):
        """
        Return tag items
        """
        items = super().items()
        comment = self.comment
        if comment is not None:
            items['comment'] = comment
        return items

    def load(self, path):
        self.__path__ = path
        self.__entry__ = self.loader(
            os.path.expandvars(os.path.expanduser(path)),
            ID3=ID3
        )
