
import os

from mutagen.aiff import AIFF

from ...codecs.base import BaseTagParser, ValueTotalCountTag
from .constants import TAG_FIELDS


class AIFFValueTotalCountTag(ValueTotalCountTag):
    """
    AIFF value total track argument pairs
    """
    field = None
    numbering_tag = None

    def get(self):
        """
        Get AIFF numbering details
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
        Save AIFF numbering details
        """
        if self.total is not None:
            value = '{}/{}'.format(self.value, self.total)
        else:
            value = '{}/{}'.format(self.value, self.value)

        self.parser.__entry__[self.field] = self.parser.__format_tag__(self.numbering_tag, value)
        self.parser.__entry__.save()


class AIFFTrackNumberingTag(AIFFValueTotalCountTag):
    numbering_tag = 'track_number'
    field = 'TRKN'


class AIFFDiskNumberingTag(AIFFValueTotalCountTag):
    numbering_tag = 'disk_number'
    field = 'TPOS'


class AIFFCommentTag:
    """
    AIFF comment with language code 'eng'
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
    AIFF tag processor
    """

    format = 'aif'
    loader = AIFF
    fields = TAG_FIELDS
    track_numbering_class = AIFFTrackNumberingTag
    disk_numbering_class = AIFFDiskNumberingTag

    @property
    def info(self):
        """
        Return information about loaded file
        """
        if self.__path__:
            return vars(self.__entry__.info)
        else:
            return {}

    def __delattr__(self, attr):
        """
        Delete AIFF tags
        """
        if attr == 'comment':
            AIFFCommentTag(self).delete()
        else:
            return super().__delattr__(attr)

    def __getattr__(self, attr):
        """
        Get AIFF tags
        """
        if attr == 'comment':
            return AIFFCommentTag(self).value
        else:
            value = super().__getattr__(attr)
            if value is not None:
                return value.text[0]
        return None

    def __setattr__(self, attr, value):
        """
        Set AIFF tags
        """
        if attr == 'comment':
            AIFFCommentTag(self).value = value
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
        )
