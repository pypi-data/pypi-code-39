from .group import Group
from .membership import Membership
from .search import Search
from typing import List, Iterable
from .types import get_headers, Payload, MemberLookup
import concurrent.futures as cf
from requests_futures.sessions import FuturesSession


class Client:
    def __init__(self, client_cert: str, client_key: str, url: str):
        session = FuturesSession()
        session.cert = (client_cert, client_key)
        session.verify = True

        self._session = session
        self._url = url



    def get_group(self, group_id: str, if_none_match: str = None) -> Payload:
        header = get_headers(**{'If-None-Match': if_none_match})
        group = Group(self._session, self._url)
        return group.get_one(group_id, header)

    def get_groups(self, group_ids: Iterable[str], if_none_match: str = None) -> List[Payload]:
        header = get_headers(**{'If-None-Match': if_none_match})
        group = Group(self._session, self._url)
        return group.get_many(group_ids, header)



    def get_membership(self, group_id: str) -> Payload:
        header = get_headers()
        membership = Membership(self._session, self._url)
        return membership.membership(group_id, header)
    
    def get_memberships(self, group_ids: Iterable[str]) -> Payload:
        header = get_headers()
        membership = Membership(self._session, self._url)
        return membership.memberships(group_ids, header)



    def get_membership_count(self, group_id: str) -> Payload:
        header = get_headers()
        membership = Membership(self._session, self._url)
        return membership.count(group_id, header)
    
    def get_membership_counts(self, group_ids: Iterable[str]) -> List[Payload]:
        header = get_headers()
        membership = Membership(self._session, self._url)
        return membership.counts(group_ids, header)



    def find_member(self, lookup: MemberLookup) -> Payload:
        header = get_headers()
        membership = Membership(self._session, self._url)
        return membership.find_member(lookup, header)
    
    def find_members(self, lookups: Iterable[MemberLookup]) -> List[Payload]:
        header = get_headers()
        membership = Membership(self._session, self._url)
        return membership.find_members(lookups, header)



    def get_effective_membership(self, group_id: str) -> Payload:
        header = get_headers()
        membership = Membership(self._session, self._url)
        return membership.effective_membership(group_id, header)
    
    def get_effective_memberships(self, group_ids: Iterable[str]) -> List[Payload]:
        header = get_headers()
        membership = Membership(self._session, self._url)
        return membership.effective_memberships(group_ids, header)



    def get_effective_membership_count(self, group_id: str) -> Payload:
        header = get_headers()
        membership = Membership(self._session, self._url)
        return membership.effective_count(group_id, header)

    def get_effective_membership_counts(self, group_ids: Iterable[str]) -> List[Payload]:
        header = get_headers()
        membership = Membership(self._session, self._url)
        return membership.effective_counts(group_ids, header)



    def find_effective_member(self, lookup: MemberLookup) -> Payload:
        header = get_headers()
        membership = Membership(self._session, self._url)
        return membership.find_effective_member(lookup, header)
    
    def find_effective_members(self, lookups: Iterable[MemberLookup]) -> List[Payload]:
        header = get_headers()
        membership = Membership(self._session, self._url)
        return membership.find_effective_members(lookups, header)


    def search(self,
            name: str = None,
            stem: str = None,
            scope: str = None,
            member: str = None,
            ty: str = None,
            owner: str = None,
            affiliate: str = None,
            instructor: str = None) -> Payload:
        query = {
            "name": name,
            "stem": stem,
            "scope": scope,
            "member": member,
            "type": ty,
            "owner": owner,
            "affiliate": affiliate,
            "instructor": instructor,
            "source=registry": 'registry'
        }
        header = get_headers()
        search = Search(self._session, self._url)
        return search.get(query, header)
