from ._base import InlineQueryResult, InlineQueryResultCachedFile, InlineQueryResultFile
from ._mixins import Description, Duration, InputMessageContent, Size, Thumb, Title
from .._mixins import Caption, ParseMode
from ..contact import ContactMixin
from ..location import LocationMixin
from ..venue import VenueMixin


class Article(InlineQueryResult, Description, ParseMode, Thumb):
    def __init__(self, title, input_message_content):
        super().__init__()
        self.args['title'] = title
        self.args['input_message_content'] = input_message_content

    def url(self, url):
        self.args['url'] = url
        return self

    def hide_url(self):
        self.args['hide_url'] = True
        return self


#
class _Photo(Caption, Description, InputMessageContent, ParseMode, Title):
    pass


class Photo(InlineQueryResultFile, _Photo, Size):
    pass


class CachedPhoto(InlineQueryResultCachedFile, _Photo):
    pass


#
class _Gif(Caption, InputMessageContent, ParseMode, Title):
    pass


class Gif(InlineQueryResultFile, _Gif, Duration, Size):
    pass


class CachedGif(InlineQueryResultCachedFile, _Gif):
    pass


#
class _Mpeg4Gif(Caption, InputMessageContent, ParseMode, Title):
    pass


class Mpeg4Gif(InlineQueryResultFile, _Mpeg4Gif, Duration, Size):
    def __init__(self, url, thumb_url):
        super().__init__(url, thumb_url)
        self.prefix = 'mpeg4'


class CachedMpeg4Gif(InlineQueryResultCachedFile, _Mpeg4Gif):
    def __init__(self, file_id):
        super().__init__(file_id)
        self.prefix = 'mpeg4'


#
video_mime_types = {'text/html', 'video/mp4'}


class _Video(Caption, Description, InputMessageContent, ParseMode):
    pass


class Video(InlineQueryResult, _Video, Size):
    def __init__(self, url, mime_type, thumb_url, title):
        assert mime_type in video_mime_types

        super().__init__()
        self.args['video_url'] = url
        self.args['mime_type'] = mime_type
        self.args['thumb_url'] = thumb_url
        self.args['title'] = title


class CachedVideo(InlineQueryResult, _Video):
    def __init__(self, file_id, title):
        super().__init__()
        self.args['video_file_id'] = file_id
        self.args['title'] = title


#
class _Audio(Caption, InputMessageContent, ParseMode):
    pass


class Audio(InlineQueryResultFile, _Audio, Duration):
    def performer(self, performer):
        self.args['performer'] = performer
        return self


class CachedAudio(InlineQueryResultCachedFile):
    pass


#
class _Voice(Caption, InputMessageContent, ParseMode):
    pass


class Voice(InlineQueryResult, _Voice):
    def __init__(self, voice_url, title):
        super().__init__()
        self.args['voice_url'] = voice_url
        self.args['title'] = title

    def voice_duration(self, voice_duration):
        self.args['voice_duration'] = voice_duration
        return self


class CachedVoice(InlineQueryResult, _Voice):
    def __init__(self, file_id, title):
        super().__init__()
        self.args['voice_file_id'] = file_id
        self.args['title'] = title


#
document_mime_types = {'application/pdf', 'application/zip'}


class _Document(Caption, Description, InputMessageContent, ParseMode):
    pass


class Document(InlineQueryResult, _Document, Thumb):
    def __init__(self, title, document_url, mime_type):
        assert mime_type in document_mime_types

        super().__init__()
        self.args['title'] = title
        self.args['document_url'] = document_url
        self.args['mime_type'] = mime_type


class CachedDocument(InlineQueryResult, _Document):
    def __init__(self, title, file_id):
        super().__init__()
        self.args['title'] = title
        self.args['document_file_id'] = file_id


#
class Location(InlineQueryResult, InputMessageContent, LocationMixin, Thumb):
    def __init__(self, latitude, longitude, title):
        super().__init__()
        self.args['latitude'] = latitude
        self.args['longitude'] = longitude
        self.args['title'] = title


class Venue(InlineQueryResult, InputMessageContent, VenueMixin, Thumb):
    def __init__(self, latitude, longitude, title, address):
        super().__init__()
        self.args['latitude'] = latitude
        self.args['longitude'] = longitude
        self.args['title'] = title
        self.args['address'] = address


class Contact(InlineQueryResult, ContactMixin, InputMessageContent, Thumb):
    def __init__(self, phone_number, first_name):
        super().__init__()
        self.args['phone_number'] = phone_number
        self.args['first_name'] = first_name


class Game(InlineQueryResult):
    def __init__(self, game_short_name):
        super().__init__()
        self.args['game_short_name'] = game_short_name


class CachedSticker(InlineQueryResult, InputMessageContent):
    def __init__(self, file_id):
        super().__init__()
        self.args['sticker_file_id'] = file_id
