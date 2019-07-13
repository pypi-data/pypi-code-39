
from ...codecs.base import GenericAudioFile

from .decoder import Decoder
from .encoder import Encoder
from .tagparser import TagParser


class Audiofile(GenericAudioFile):
    """
    Wavpack audio file
    """

    decoder_class = Decoder
    encoder_class = Encoder
    tagparser_class = TagParser

    format = 'wavpack'
    description = 'Wavpack files'
    extensions = (
        'wv',
        'wavpack',
    )
    mimetypes = (
    )
