from requests.adapters import HTTPAdapter


class TimeoutAdapter(HTTPAdapter):
    """HTTP adapter that adds timeout to each query."""
    def __init__(self, timeout=None, *args, **kwargs):
        self.timeout = timeout
        super(TimeoutAdapter, self).__init__(*args, **kwargs)

    def send(self, *args, **kwargs):
        kwargs['timeout'] = self.timeout
        return super(TimeoutAdapter, self).send(*args, **kwargs)
