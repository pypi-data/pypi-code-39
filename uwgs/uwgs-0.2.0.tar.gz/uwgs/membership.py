from .types import Payload, get_headers, MemberLookup
from typing import List, Iterable, Tuple
import concurrent.futures as cf


class Membership:
    def __init__(self, session, url):
        self._session = session
        self._url = url

    def get_url(self, group_id: str) -> str:
        return self._url+'/group/{}/member'.format(group_id)

    def get_effective_url(self, group_id: str) -> str:
        return self._url+'/group/{}/effective_member'.format(group_id)


    def membership(self, group_id: str, header: dict) -> Payload:
        url = self.get_url(group_id)
        query = {'source=registry': 'registry'}
        return Payload(self._session.get(url, params=query, headers=header).result())

    def memberships(self, group_ids: Iterable[str], header: dict) -> List[Payload]:
        urls = map(self.get_url, group_ids)
        fs = [self._session.get(u, headers=header) for u in urls]
        return [Payload(r.result()) for r in cf.as_completed(fs)]



    def count(self, group_id: str, header: dict) -> Payload:
        url = self.get_url(group_id)
        query = {
            'view': 'count',
            'source=registry': 'registry'
        }
        return Payload(self._session.get(url, params=query, headers=header).result())
    
    def counts(self, group_ids: Iterable[str], header: dict) -> List[Payload]:
        urls = map(self.get_url, group_ids)
        query = {
            'view': 'count',
            'source=registry': 'registry'
        }
        fs = [self._session.get(u, params=query, headers=header) for u in urls]
        return [Payload(r.result()) for r in cf.as_completed(fs)]



    def find_member(self, lookup: MemberLookup, header: dict) -> Payload:
        url = self._url+'/group/{}/member/{}'.format(lookup.group_id, lookup.member_id)
        query = {'source=registry': 'registry'}
        return Payload(self._session.get(url, params=query, headers=header).result())
    
    def find_members(self, lookups: Iterable[MemberLookup], header: dict) -> List[Payload]:
        urls = [self._url+'/group/{}/member/{}'.format(l.group_id, l.member_id) for l in lookups]
        query = {'source=registry': 'registry'}
        fs = [self._session.get(u, params=query, headers=header) for u in urls]
        return [Payload(r.result()) for r in cf.as_completed(fs)]



    def effective_membership(self, group_id: str, header: dict) -> Payload:
        url = self.get_effective_url(group_id)
        return Payload(self._session.get(url, headers=header).result())
    
    def effective_memberships(self, group_ids: Iterable[str], header: dict) -> List[Payload]:
        urls = map(self.get_effective_url, group_ids)
        fs = [self._session.get(u, headers=header) for u in urls]
        return [Payload(r.result()) for r in cf.as_completed(fs)]



    def effective_count(self, group_id: str, header: dict) -> Payload:
        url = self.get_effective_url(group_id)
        query = {
            'view': 'count',
            'source=registry': 'registry'
        }
        return Payload(self._session.get(url, params=query, headers=header).result())

    def effective_counts(self, group_ids: Iterable[str], header: dict) -> List[Payload]:
        urls = map(self.get_effective_url, group_ids)
        query = {
            'view': 'count',
            'source=registry': 'registry'
        }
        fs = [self._session.get(u, params=query, headers=header) for u in urls]
        return [Payload(r.result()) for r in cf.as_completed(fs)]



    def find_effective_member(self, lookup: MemberLookup, header: dict) -> Payload:
        url = self._url+'/group/{}/effective_member/{}'.format(
            lookup.group_id, lookup.member_id)
        query = {'source=registry': 'registry'}
        return Payload(self._session.get(url, params=query, headers=header).result())
    
    def find_effective_members(self, lookups: Iterable[MemberLookup], header: dict) -> List[Payload]:
        urls = [self._url+'/group/{}/effective_member/{}'.format(
            lookup.group_id, lookup.member_id) for lookup in lookups]
        query = {'source=registry': 'registry'}
        fs = [self._session.get(u, params=query, headers=header) for u in urls]
        return [Payload(r.result()) for r in cf.as_completed(fs)]
