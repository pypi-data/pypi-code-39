from .types import Payload, get_headers


class Search:
    def __init__(self, session, url):
        self._session = session
        self._url = url

    def get(self, query: dict, header: dict) -> Payload:
        url = self._url+'/search'
        return Payload(self._session.get(url, params=query, headers=header).result())
