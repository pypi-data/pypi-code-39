
from mutagen.flac import FLAC

from ..ogg.tagparser import OggTagParser


class TagParser(OggTagParser):
    """
    FLAC tag processor
    """
    format = 'flac'
    loader = FLAC
