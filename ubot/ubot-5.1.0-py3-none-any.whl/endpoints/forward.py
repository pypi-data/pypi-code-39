from ._base import Endpoint
from ._mixins import DisableNotification


class ForwardMessage(Endpoint, DisableNotification):
    def __init__(self, chat_id, from_chat_id, message_id):
        super().__init__()
        self.args['chat_id'] = chat_id
        self.args['from_chat_id'] = from_chat_id
        self.args['message_id'] = message_id
