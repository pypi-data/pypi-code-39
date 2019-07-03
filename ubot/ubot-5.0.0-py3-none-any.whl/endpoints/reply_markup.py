from ._base import Endpoint
from ._mixins import ReplyMarkup, chat_or_inline_message

button_types = {
    'url', 'callback_data', 'switch_inline_query', 'switch_inline_query_current_chat', 'callback_game',
    'pay'
}
must_be_first_button_types = {'callback_game', 'pay'}


class InlineKeyboard:
    __slots__ = ['current_row', 'rows']

    def __init__(self):
        self.current_row = None
        self.rows = []

    def serialize(self):
        return {'inline_keyboard': self.rows}

    def add_row(self):
        row = []
        self.rows.append(row)
        self.current_row = row
        return self

    def add_button(self, text, button_type, button_value):
        assert button_type in button_types

        if button_type in must_be_first_button_types:
            assert self.current_row

        self.current_row.append({
            'text': text,
            button_type: button_value
        })
        return self


class ReplyKeyboard:
    __slots__ = ['buttons', 'options']

    def __init__(self):
        self.buttons = []
        self.options = {}

    def serialize(self):
        return {
            'keyboard': self.buttons,
            **self.options
        }

    def resize_keyboard(self):
        self.options['resize_keyboard'] = True
        return self

    def one_time_keyboard(self):
        self.options['one_time_keyboard'] = True
        return self

    def selective(self):
        self.options['selective'] = True
        return self

    def add_button(self, text, request_contact=False, request_location=False):
        button = {
            'text': text
        }

        if request_contact:
            button['request_contact'] = True

        if request_location:
            button['request_location'] = True

        self.buttons.append(button)
        return self


class ReplyKeyboardRemove:
    __slots__ = ['options']

    def __init__(self):
        self.options = {}

    def serialize(self):
        return {
            'remove_keyboard': True,
            **self.options
        }

    def selective(self):
        self.options['selective'] = True
        return self


class ForceReply:
    __slots__ = ['options']

    def __init__(self):
        self.options = {}

    def serialize(self):
        return {
            'force_reply': True,
            **self.options
        }

    def selective(self):
        self.options['selective'] = True
        return self


class AnswerCallbackQuery(Endpoint):
    def __init__(self, callback_query_id):
        super().__init__()
        self.args['callback_query_id'] = callback_query_id

    def text(self, text):
        self.args['text'] = text
        return self

    def show_alert(self):
        self.args['show_alert'] = True
        return self

    def url(self, url):
        self.args['url'] = url
        return self

    def cache_time(self, cache_time):
        self.args['cache_time'] = cache_time
        return self


class EditMessageReplyMarkup(Endpoint, ReplyMarkup):
    def __init__(self, chat_or_inline_message_id, message_id):
        super().__init__()
        self.args.update(args=chat_or_inline_message(chat_or_inline_message_id, message_id))
