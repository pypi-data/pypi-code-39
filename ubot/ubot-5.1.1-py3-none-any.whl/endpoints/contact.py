from ._base import BaseMixin, Endpoint
from ._mixins import DisableNotification, ReplyMarkup, ReplyToMessageId


class ContactMixin(BaseMixin):
    def last_name(self, last_name):
        self.args['last_name'] = last_name
        return self

    def vcard(self, vcard):
        self.args['vcard'] = vcard
        return self


class SendContact(Endpoint, ContactMixin, DisableNotification, ReplyMarkup, ReplyToMessageId):
    def __init__(self, chat_id, phone_number, first_name):
        super().__init__()
        self.args['chat_id'] = chat_id
        self.args['phone_number'] = phone_number
        self.args['first_name'] = first_name
