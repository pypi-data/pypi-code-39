from __future__ import absolute_import, division, print_function

from telnyx.api_resources.abstract import UpdateableAPIResource
from telnyx.api_resources.abstract import ListableAPIResource


class MessagingPhoneNumber(ListableAPIResource, UpdateableAPIResource):
    OBJECT_NAME = "messaging_phone_number"
