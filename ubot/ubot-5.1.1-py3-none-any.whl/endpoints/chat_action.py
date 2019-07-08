from ._base import Endpoint

actions = {'typing', 'upload_photo', 'record_video', 'upload_video', 'record_audio', 'upload_audio',
           'upload_document', 'find_location', 'record_video_note', 'upload_video_note'}


class SendChatAction(Endpoint):
    def __init__(self, chat_id, action):
        assert action in actions

        super().__init__()
        self.args['chat_id'] = chat_id
        self.args['action'] = action
