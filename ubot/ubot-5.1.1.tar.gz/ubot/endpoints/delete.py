from ._base import Endpoint


class DeleteMessage(Endpoint):
    def __init__(self, chat_id, message_id):
        super().__init__()
        self.args['chat_id'] = chat_id
        self.args['message_id'] = message_id
