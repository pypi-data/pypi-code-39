
import os


def detect_file_codec(path):
    """
    Try to detect codec for file
    """

    if not os.path.isfile(path):
        return None

    name, extension = os.path.splitext(path)

    if extension in ('.m4a', 'caf'):
        from mutagen.mp4 import MP4
        try:
            codec = MP4(path).info.codec
            if codec == 'alac':
                return codec
            elif codec[:4] == 'mp4a':
                return 'aac'
        except Exception as e:
            raise ValueError('Error detecting file {} codec: {}'.format(path, e))

    if extension == '.aif':
        from mutagen.aiff import AIFF
        try:
            AIFF(path).info
            return 'aif'
        except Exception as e:
            raise ValueError('Error opening {} as aif: {}'.format(path, e))

    if extension == '.flac':
        from mutagen.flac import FLAC
        try:
            FLAC(path).info
            return 'flac'
        except Exception as e:
            raise ValueError('Error opening {} as flac: {}'.format(path, e))

    if extension == '.mp3':
        from mutagen.mp3 import MP3
        try:
            MP3(path).info
            return 'mp3'
        except Exception as e:
            raise ValueError('Error opening {} as mp3: {}'.format(path, e))

    if extension == '.opus':
        from mutagen.oggopus import OggOpus
        try:
            OggOpus(path).info
            return 'opus'
        except Exception as e:
            raise ValueError('Error opening {} as mp3: {}'.format(path, e))

    if extension == '.ogg':
        from mutagen.oggvorbis import OggVorbis
        try:
            OggVorbis(path).info
            return 'vorbis'
        except Exception as e:
            raise ValueError('Error opening {} as ogg vorbis: {}'.format(path, e))

    if extension == '.wv':
        from mutagen.wavpack import WavPack
        try:
            WavPack(path).info
            return 'wavpack'
        except Exception as e:
            raise ValueError('Error opening {} as wavpack: {}'.format(path, e))

    return None
