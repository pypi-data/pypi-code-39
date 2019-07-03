from ._base import Endpoint


class GetMe(Endpoint):
    pass


class GetUserProfilePhotos(Endpoint):
    def __init__(self, user_id):
        super().__init__()
        self.args['user_id'] = user_id

    def offset(self, offset):
        self.args['offset'] = offset
        return self

    def limit(self, limit):
        self.args['limit'] = limit
        return self
