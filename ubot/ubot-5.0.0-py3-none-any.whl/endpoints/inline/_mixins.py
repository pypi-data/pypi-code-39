from ._base import InlineQueryResultMixin
from ...settings import json_lib as json


class Description(InlineQueryResultMixin):
    def description(self, description):
        self.args['description'] = description
        return self


class Duration(InlineQueryResultMixin):
    def duration(self, duration):
        key = f'{self.prefix}_duration'
        self.args[key] = duration
        return self


class InputMessageContent(InlineQueryResultMixin):
    def input_message_content(self, input_message_content):
        self.args['input_message_content'] = json.dumps(input_message_content.args)
        return self


class Size(InlineQueryResultMixin):
    def width(self, width):
        key = f'{self.prefix}_width'
        self.args[key] = width
        return self

    def height(self, height):
        key = f'{self.prefix}_height'
        self.args[key] = height
        return self


class Title(InlineQueryResultMixin):
    def title(self, title):
        self.args['title'] = title
        return self


class Thumb(InlineQueryResultMixin):
    def thumb_url(self, thumb_url):
        self.args['thumb_url'] = thumb_url
        return self

    def thumb_width(self, thumb_width):
        self.args['thumb_width'] = thumb_width
        return self

    def thumb_height(self, thumb_height):
        self.args['thumb_height'] = thumb_height
        return self
