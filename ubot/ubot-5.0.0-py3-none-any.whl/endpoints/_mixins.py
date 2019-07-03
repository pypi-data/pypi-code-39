from ._base import BaseMixin
from ..settings import json_lib as json


def chat_or_inline_message(chat_or_inline_message_id, message_id):
    if message_id is not None:
        return {
            'chat_id': chat_or_inline_message_id,
            'message_id': message_id
        }
    else:
        return {
            'inline_message_id': chat_or_inline_message_id
        }


class Caption(BaseMixin):
    def caption(self, caption):
        assert len(caption) < 1025

        self.args['caption'] = caption
        return self


class ReplyToMessageId(BaseMixin):
    def reply_to_message_id(self, message_id):
        self.args['reply_to_message_id'] = message_id
        return self


class DisableNotification(BaseMixin):
    def disable_notification(self):
        self.args['disable_notification'] = True
        return self


parse_modes = {'Markdown', 'HTML'}


class ParseMode(BaseMixin):
    def parse_mode(self, parse_mode):
        assert parse_mode in parse_modes

        self.args['parse_mode'] = parse_mode
        return self


class ReplyMarkup(BaseMixin):
    def reply_markup(self, reply_markup):
        self.args['reply_markup'] = json.dumps(reply_markup.serialize())
        return self
