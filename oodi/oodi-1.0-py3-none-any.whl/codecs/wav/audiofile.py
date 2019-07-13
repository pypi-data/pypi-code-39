
from ...codecs.base import GenericAudioFile

from .decoder import Decoder
from .encoder import Encoder


class Audiofile(GenericAudioFile):
    """
    Wav audio file
    """

    decoder_class = Decoder
    encoder_class = Encoder
    tagparser_class = None

    format = 'wav'
    description = 'Waveform Audio File Format'
    extensions = (
        'wav',
        'wave',
    )
    mimetypes = (
        'audio/wav',
        'audio/vnd.wave',
        'audio/wave',
        'audio/x-wav'
    )
