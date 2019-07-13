
from mutagen.oggvorbis import OggVorbis

from ..ogg.tagparser import OggTagParser


class TagParser(OggTagParser):
    """
    Vorbis tag processor
    """
    format = 'vorbis'
    loader = OggVorbis
