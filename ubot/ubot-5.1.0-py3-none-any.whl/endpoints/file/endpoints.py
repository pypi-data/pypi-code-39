from .._base import Endpoint
from .._mixins import Caption, DisableNotification, ParseMode, ReplyToMessageId, chat_or_inline_message
from ..reply_markup import ReplyMarkup
from ..._utils.multipart_encoder import MultipartEncoder
from ...settings import json_lib as json


class SendMedia(Endpoint, DisableNotification, ReplyMarkup, ReplyToMessageId):
    def __init__(self, file, chat_id):
        super().__init__()
        self.endpoint = f'send{file.__class__.__name__}'
        self.args['chat_id'] = chat_id
        self.args.update(file.args)
        self.args.update(file.attributes)

        if file.is_data:
            self.method = 'POST'
            multipart_encoder = MultipartEncoder()
            multipart_encoder.files = file.value
            boundary, self.data = multipart_encoder.encode()
            self.headers['content-type'] = f'multipart/form-data; boundary={boundary}'
        else:
            self.args[file.file_type] = file.value


class SendMediaGroup(Endpoint, DisableNotification, ReplyToMessageId):
    media_types = ['photo', 'video']

    def __init__(self, chat_id, files):
        super().__init__()

        self.__multipart_encoder = None
        self.method = 'GET'
        media = []

        for file in files:
            assert file.file_type in self.media_types

            serialized, files = file.to_input_media()
            media.append(serialized)
            if files is not None:
                self.method = 'POST'
                self.multipart_encoder.files.extend(files)

        self.args['chat_id'] = chat_id
        self.args['media'] = json.dumps(media)

        if self.method == 'POST':
            boundary, self.data = self.multipart_encoder.encode()
            self.headers['content-type'] = f'multipart/form-data; boundary={boundary}'

    @property
    def multipart_encoder(self):
        if self.__multipart_encoder is None:
            self.__multipart_encoder = MultipartEncoder()
        return self.__multipart_encoder


class GetFile(Endpoint):
    # https://api.telegram.org/file/bot<token>/<file_path>
    def __init__(self, file_id):
        super().__init__()
        self.args['file_id'] = file_id


class EditMessageCaption(Endpoint, Caption, ParseMode, ReplyMarkup):
    def __init__(self, chat_or_inline_message_id, message_id):
        super().__init__()
        self.args.update(chat_or_inline_message(chat_or_inline_message_id, message_id))


class EditMessageMedia(Endpoint, ReplyMarkup):
    def __init__(self, chat_or_inline_message_id, message_id, media):
        super().__init__()
        self.args['media'] = media.to_input_media()
        self.args.update(chat_or_inline_message(chat_or_inline_message_id, message_id))
