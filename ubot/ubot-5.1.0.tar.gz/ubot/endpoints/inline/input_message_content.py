from ._base import InputMessageContent
from .._mixins import ParseMode
from ..contact import ContactMixin
from ..location import LocationMixin
from ..text import TextMixin
from ..venue import VenueMixin


class Text(InputMessageContent, ParseMode, TextMixin):
    def __init__(self, message_text):
        self.args = {
            'message_text': message_text
        }


class Location(InputMessageContent, LocationMixin):
    def __init__(self, latitude, longitude):
        self.args = {
            'latitude': latitude,
            'longitude': longitude
        }


class Venue(InputMessageContent, VenueMixin):
    def __init__(self, latitude, longitude, title, address):
        self.args = {
            'latitude': latitude,
            'longitude': longitude,
            'title': title,
            'address': address
        }


class Contact(InputMessageContent, ContactMixin):
    def __init__(self, phone_number, first_name):
        self.args = {
            'phone_number': phone_number,
            'first_name': first_name
        }
