from ._base import BaseMixin, Endpoint
from ._mixins import DisableNotification, ReplyMarkup, ReplyToMessageId


class VenueMixin(BaseMixin):
    def foursquare_id(self, foursquare_id):
        self.args['foursquare_id'] = foursquare_id
        return self

    def foursquare_type(self, foursquare_type):
        self.args['foursquare_type'] = foursquare_type
        return self


class SendVenue(Endpoint, DisableNotification, ReplyMarkup, ReplyToMessageId, VenueMixin):
    def __init__(self, chat_id, latitude, longitude, title, address):
        super().__init__()
        self.args['chat_id'] = chat_id
        self.args['latitude'] = latitude
        self.args['longitude'] = longitude
        self.args['title'] = title
        self.args['address'] = address
