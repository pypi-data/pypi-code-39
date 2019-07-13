
from ...codecs.base import GenericAudioFile

from .decoder import Decoder
from .encoder import Encoder
from .tagparser import TagParser


class Audiofile(GenericAudioFile):
    """
    AAC audio file
    """

    decoder_class = Decoder
    encoder_class = Encoder
    tagparser_class = TagParser

    format = 'aac'
    description = 'Advanced Audio Coding'
    extensions = (
        'm4a',
        'mp4',
        'm4b',
        'm4p',
        'm4r',
        'm4v',
        '3gp',
    )
    mimetypes = (
        'audio/aac',
        'audio/aacp',
        'audio/3gpp',
        'audio/3gpp2',
        'audio/mp4',
        'audio/mp4a-latm',
        'audio/mpeg4-generic',
    )
