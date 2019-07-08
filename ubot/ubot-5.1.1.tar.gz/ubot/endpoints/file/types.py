from ._base import File
from ._mixins import Thumb, ToInputMedia
from .._mixins import Caption, ParseMode


class Photo(File, Caption, ParseMode, ToInputMedia):
    @staticmethod
    def _get_file_id(response):
        return response[-1]


class Audio(File, Caption, ParseMode, Thumb, ToInputMedia):
    def duration(self, duration):
        self.args['duration'] = duration
        return self

    def performer(self, performer):
        self.args['performer'] = performer
        return self

    def title(self, title):
        self.args['title'] = title
        return self


class Document(File, Caption, ParseMode, Thumb, ToInputMedia):
    pass


class Video(File, Caption, ParseMode, Thumb, ToInputMedia):
    def supports_streaming(self):
        self.args['supports_streaming'] = True
        return self

    def duration(self, duration):
        self.args['duration'] = duration
        return self

    def width(self, width):
        self.args['width'] = width
        return self

    def height(self, height):
        self.args['height'] = height
        return self


class Animation(File, Caption, ParseMode, Thumb, ToInputMedia):
    def duration(self, duration):
        self.args['duration'] = duration
        return self

    def width(self, width):
        self.args['width'] = width
        return self

    def height(self, height):
        self.args['height'] = height
        return self


class Voice(File, Caption, ParseMode):
    def duration(self, duration):
        self.args['duration'] = duration
        return self


class VideoNote(File, Thumb):
    def duration(self, duration):
        self.args['duration'] = duration
        return self

    def length(self, length):
        self.args['length'] = length
        return self
