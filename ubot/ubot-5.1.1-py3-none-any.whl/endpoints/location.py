from ._base import BaseMixin, Endpoint
from ._mixins import DisableNotification, ReplyMarkup, ReplyToMessageId, chat_or_inline_message


class LocationMixin(BaseMixin):
    def live_period(self, live_period):
        assert 60 <= live_period <= 86400

        self.args['live_period'] = live_period
        return self


class SendLocation(Endpoint, DisableNotification, LocationMixin, ReplyMarkup, ReplyToMessageId):
    def __init__(self, chat_id, latitude, longitude):
        super().__init__()
        self.args['chat_id'] = chat_id
        self.args['latitude'] = latitude
        self.args['longitude'] = longitude


class EditMessageLiveLocation(Endpoint, ReplyMarkup):
    def __init__(self, chat_or_inline_message_id, message_id, latitude, longitude):
        super().__init__()
        self.args['latitude'] = latitude
        self.args['longitude'] = longitude
        self.args.update(chat_or_inline_message(chat_or_inline_message_id, message_id))


class StopMessageLiveLocation(Endpoint, ReplyMarkup):
    def __init__(self, chat_or_inline_message_id, message_id):
        super().__init__()
        self.args.update(chat_or_inline_message(chat_or_inline_message_id, message_id))
