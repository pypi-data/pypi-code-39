from contextlib import contextmanager
import json
import logging

from . import LdapChangeTrackObject
from .ldapfilter import Filter
from .util import single

logger = logging.getLogger(__name__)


class DomainState(LdapChangeTrackObject):
    _known_attrs = {
        # Name => (Type, Read-only, [LdapAttr])
        'next_uid':             (int, False, 'msSFU30MaxUidNumber'),
        'next_gid':             (int, False, 'msSFU30MaxGidNumber'),
    }

    @classmethod
    def get(cls, ad):
        # We can't easily know the SFU30 domain name, so for now we'll just assume there's only one.
        rdn = 'CN=ypservers,CN=ypServ30,CN=RpcServices,CN=System'
        f = Filter('objectClass=msSFU30DomainInfo')
        attrs = ['msSFU30MaxUidNumber', 'msSFU30MaxGidNumber']

        dn, attrvals = single(ad._search(rdn, f, attrs))
        return cls(ad, dn, **attrvals)

    def __str__(self):
        return 'Next uidNumber: {}\nNext gidNumber: {}'.format(
                self.next_uid, self.next_gid)

    @property
    def complete(self):
        return None not in (self.next_uid, self.next_gid)
