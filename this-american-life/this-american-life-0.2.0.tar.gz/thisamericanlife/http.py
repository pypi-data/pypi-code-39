
import requests
from functools import lru_cache
import thisamericanlife.endpoints as tal_endpoints


class HttpClient(object):

    @lru_cache(maxsize=64)
    def get(self, endpoint, **kwargs):
        resp = requests.get(endpoint.format(**kwargs))
        resp.raise_for_status()
        return resp
