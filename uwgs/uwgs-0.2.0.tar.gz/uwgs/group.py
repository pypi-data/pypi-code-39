from .types import Payload, get_headers
from datetime import datetime
from typing import List, Iterable
import concurrent.futures as cf


class Group:
    def __init__(self, session, url):
        self._session = session
        self._url = url

    def get_url(self, group_id: str) -> str:
        return self._url + '/group/{}'.format(group_id)

    def get_one(self, group_id: str, header: dict) -> Payload:
        url = self.get_url(group_id)
        return Payload(self._session.get(url, headers=header).result())
    
    def get_many(self, group_ids: Iterable[str], header: dict) -> List[Payload]:
        urls = map(self.get_url, group_ids)
        fs = [self._session.get(u, headers=header) for u in urls]
        return [Payload(r.result()) for r in cf.as_completed(fs)]
