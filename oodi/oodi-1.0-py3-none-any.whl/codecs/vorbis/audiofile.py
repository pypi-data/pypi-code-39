
from ...codecs.base import GenericAudioFile

from .decoder import Decoder
from .encoder import Encoder
from .tagparser import TagParser


class Audiofile(GenericAudioFile):
    """
    Ogg Vorbis audio file
    """

    decoder_class = Decoder
    encoder_class = Encoder
    tagparser_class = TagParser

    format = 'vorbis'
    description = 'Ogg Vorbis'
    extensions = (
        'ogg',
        'vorbis',
    )
    mimetypes = (
        'application/ogg',
        'audio/ogg',
        'audio/vorbis',
        'audio/vorbis-config'
    )
