from ._base import BaseMixin, Endpoint
from ._mixins import DisableNotification, ParseMode, ReplyToMessageId, chat_or_inline_message
from .reply_markup import ReplyMarkup


class TextMixin(BaseMixin):
    def disable_web_page_overview(self):
        self.args['disable_web_page_overview'] = True
        return self


class SendMessage(Endpoint, DisableNotification, ParseMode, ReplyMarkup, ReplyToMessageId, TextMixin):
    def __init__(self, chat_id, text):
        super().__init__()
        self.args['chat_id'] = chat_id
        self.args['text'] = text


class EditMessageText(Endpoint, ParseMode, ReplyMarkup, TextMixin):
    def __init__(self, chat_or_inline_message_id, message_id, text):
        super().__init__()
        self.args['text'] = text
        self.args.update(chat_or_inline_message(chat_or_inline_message_id, message_id))
