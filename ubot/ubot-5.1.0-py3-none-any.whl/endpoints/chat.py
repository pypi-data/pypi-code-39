from ._base import Endpoint
from ._mixins import DisableNotification
from .._utils.multipart_encoder import MultipartEncoder


class ExportChatInviteLink(Endpoint):
    def __init__(self, chat_id):
        super().__init__()
        self.args['chat_id'] = chat_id


class SetChatPhoto(Endpoint):
    def __init__(self, chat_id, photo):
        super().__init__()
        self.method = 'POST'
        self.args['chat_id'] = chat_id

        self.multipart_encoder = MultipartEncoder()
        self.multipart_encoder.add_file('photo', photo)
        boundary, self.data = self.multipart_encoder.encode()
        self.headers['content-type'] = f'multipart/form-data; boundary={boundary}'


class DeleteChatPhoto(Endpoint):
    def __init__(self, chat_id):
        super().__init__()
        self.args['chat_id'] = chat_id


class SetChatTitle(Endpoint):
    def __init__(self, chat_id, title):
        super().__init__()
        self.args['chat_id'] = chat_id
        self.args['title'] = title


class SetChatDescription(Endpoint):
    def __init__(self, chat_id, description):
        super().__init__()
        self.args['chat_id'] = chat_id
        self.args['description'] = description


class PinChatMessage(Endpoint, DisableNotification):
    def __init__(self, chat_id, message_id):
        super().__init__()
        self.args['chat_id'] = chat_id
        self.args['message_id'] = message_id


class UnpinChatMessage(Endpoint):
    def __init__(self, chat_id):
        super().__init__()
        self.args['chat_id'] = chat_id


class LeaveChat(Endpoint):
    def __init__(self, chat_id):
        super().__init__()
        self.args['chat_id'] = chat_id


class GetChat(Endpoint):
    def __init__(self, chat_id):
        super().__init__()
        self.args['chat_id'] = chat_id


class GetChatAdministrators(Endpoint):
    def __init__(self, chat_id):
        super().__init__()
        self.args['chat_id'] = chat_id


class GetChatMemberCount(Endpoint):
    def __init__(self, chat_id):
        super().__init__()
        self.args['chat_id'] = chat_id


class GetChatMember(Endpoint):
    def __init__(self, chat_id, user_id):
        super().__init__()
        self.args['chat_id'] = chat_id
        self.args['user_id'] = user_id


class SetChatStickerSet(Endpoint):
    def __init__(self, chat_id, sticker_set_name):
        super().__init__()
        self.args['chat_id'] = chat_id
        self.args['sticker_set_name'] = sticker_set_name


class DeleteChatStickerSet(Endpoint):
    def __init__(self, chat_id):
        super().__init__()
        self.args['chat_id'] = chat_id
