
from mutagen.oggopus import OggOpus

from ..ogg.tagparser import OggTagParser


class TagParser(OggTagParser):
    """
    OPUS tag processor
    """
    format = 'opus'
    loader = OggOpus
