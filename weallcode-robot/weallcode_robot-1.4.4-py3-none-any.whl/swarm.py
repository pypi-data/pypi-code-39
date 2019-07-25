from .robot import Robot


class Swarm(Robot):
    def __init__(self, secret=None):
        super(Swarm, self).__init__()
        self.secret = secret

    def _get_headers(self):
        return { "Authorization": "Basic %s" % (self.secret) }

    def _get_url(self):
        return "%s/broadcast" % (self.api_url)
