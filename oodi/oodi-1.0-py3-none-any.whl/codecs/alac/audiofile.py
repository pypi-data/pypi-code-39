
from ...codecs.base import GenericAudioFile

from .decoder import Decoder
from .encoder import Encoder
from .tagparser import TagParser


class Audiofile(GenericAudioFile):
    """
    ALAC audio file
    """

    decoder_class = Decoder
    encoder_class = Encoder
    tagparser_class = TagParser

    format = 'alac'
    description = ' Apple Lossless Audio Codec'
    extensions = (
        'm4a',
        'alac',
    )
    mimetypes = (
    )
