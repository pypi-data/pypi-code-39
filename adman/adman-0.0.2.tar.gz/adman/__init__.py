import ldap
import logging
from pprint import pformat

from .ldapfilter import Filter
from .locate import get_domain_ldap_servers
from .types import SID
from .util import single_or

from ldap.filter import escape_filter_chars
from ldap.modlist import modifyModlist


logger = logging.getLogger(__name__)


USER_SEARCH_BASE_RDN = None
USER_SEARCH_FILTER = Filter('objectClass=user') & Filter('objectCategory=Person') & ~Filter('sAMAccountName=krbtgt*')

GROUP_SEARCH_BASE_RDN = None
GROUP_SEARCH_FILTER = Filter('objectClass=group')

def format_modlist(modlist):
    opnames = {
        ldap.MOD_ADD:       'MOD_ADD',
        ldap.MOD_DELETE:    'MOD_DELETE',
        ldap.MOD_REPLACE:   'MOD_REPLACE',
        ldap.MOD_INCREMENT: 'MOD_INCREMENT',
    }

    newlist = []
    for op, atype, val in modlist:
        opname = opnames[op]
        newlist.append((opname, atype, val))

    return pformat(newlist)


def get_dc_info(l):
    attrs = ['defaultNamingContext', 'dnsHostName']
    r = l.search_s('', ldap.SCOPE_BASE, None, attrs)[0]
    dn, attr_vals = r
    return {k: v[0].decode() for k, v in attr_vals.items()}


def ldap_initialize(domain, proto=None):
    uri = ' '.join(get_domain_ldap_servers(domain, proto=proto))

    logger.debug("ldap.initialize(uri={!r})".format(uri))
    return ldap.initialize(uri)


def ldap_connect_gssapi(domain):
    l = ldap_initialize(domain)

    # https://github.com/python-ldap/python-ldap/issues/275
    l.set_option(ldap.OPT_REFERRALS, 0)


    # Perform an anonymous bind first to get server info
    l.simple_bind_s()
    info = get_dc_info(l)

    # Perform a GSSAPI (Kerberos) secure SASL bind
    l.sasl_gssapi_bind_s()

    return l, info


class AdPosixUserManager:
    def __init__(self, dnsdomain, ldapconn, base=None):
        self.dnsdomain = dnsdomain
        self.ldapconn = ldapconn
        self.base = base


    @classmethod
    def connect(cls, dnsdomain):
        ldapconn, ldapinfo = ldap_connect_gssapi(dnsdomain)
        logger.info("Connected to {dnsHostName} ({defaultNamingContext})".format(**ldapinfo))

        ad = cls(
                dnsdomain = dnsdomain,
                ldapconn = ldapconn,
                base = ldapinfo['defaultNamingContext'],
            )

        return ad


    def _search(self, base_rdn=None, filt=None, attrs=None, scope=ldap.SCOPE_SUBTREE):
        base = self.base
        if base_rdn is not None:
            base = base_rdn + ',' + base
        logger.debug("Search base: %s", base)
        logger.debug("Search filter: %s", filt)

        results = self.ldapconn.search_s(base, scope, str(filt), attrs)

        for dn, attrs in results:
            if dn is None:
                # Filter out referrals
                # https://mail.python.org/pipermail/python-ldap/2014q1/003350.html
                uri = attrs
                logger.debug("Received referral: %s", uri)
                continue
            yield dn, attrs


    def _modify(self, dn, modlist):
        rc = self.ldapconn.modify_s(dn, modlist)
        logger.debug("modify_s({!r}, {!r}) returned {}".format(
            dn, modlist, rc))


    def get_users(self, filt=None, attrs=None):
        if attrs is None:
            attrs = ['sAMAccountName', 'uidNumber', 'gidNumber']

        f = USER_SEARCH_FILTER
        if filt is not None:    # Append caller filter
            f = f & filt

        userlist = self._search(USER_SEARCH_BASE_RDN, f, attrs)
        for dn, attrvals in userlist:
            yield AdUser(self, dn, **attrvals)


    def get_user_by_uid(self, uid, attrs=None):
        filt = Filter('uidNumber={}'.format(uid))
        return single_or(self.get_users(filt, attrs), None)


    def get_groups(self, filt=None, attrs=None):
        if attrs is None:
            attrs = ['name', 'gidNumber']

        f = GROUP_SEARCH_FILTER
        if filt is not None:    # Append caller filter
            f = f & filt

        grouplist = self._search(GROUP_SEARCH_BASE_RDN, f, attrs)
        for dn, attrvals in grouplist:
            yield AdGroup(self, dn, **attrvals)


    def get_group_by_gid(self, gid, attrs=None):
        filt = Filter('gidNumber={}'.format(gid))
        return single_or(self.get_groups(filt, attrs), None)

    def get_group_by_sid(self, sid, attrs=None):
        filt = Filter('objectSid={}'.format(escape_filter_chars(str(sid), 1)))
        return single_or(self.get_groups(filt, attrs), None)




class LdapChangeTrackObject:

    @property
    def _known_attrs2(self):
        def get():
            # Name => (Type, Read-only, [LdapAttr])
            for attr, data in self._known_attrs.items():
                type_, ro = data[0:2]
                try:
                    ldap_attr = data[2]
                except IndexError:
                    ldap_attr = attr
                yield attr, (type_, ro, ldap_attr)
        return dict(get())


    def __init__(self, ad, dn, **attrs):
        super().__setattr__('_data', {})
        super().__setattr__('_ad', ad)
        super().__setattr__('_dn', dn)
        super().__setattr__('_pending_changes', {})

        for attr, (type_, ro, ldap_attr) in self._known_attrs2.items():
            val = attrs.get(ldap_attr)
            if val is not None:
                # python-ldap always returns attributes as strings in a list
                assert isinstance(val, list)
                val = type_(val[0])

            self._data[attr] = val

    @property
    def dn(self):
        return self._dn

    def __str__(self):
        s = self.dn

        for attr, (type_, ro, ldap_attr) in self._known_attrs2.items():
            val = getattr(self, attr, None)
            if val is not None:
                s += ', {}={}'.format(attr, val)

        return s


    def __getattr__(self, name):
        # This is only called when normal method raises AttributeError which
        # makes our internal implementation easier

        # First see if it's in the pending changes
        try:
            return self._pending_changes[name]
        except KeyError:
            pass

        # Then try to get it from the normal data store
        try:
            return self._data[name]
        except KeyError:
            raise AttributeError("'{}' object has no attribute '{}'".format(type(self), name))


    def __setattr__(self, name, value):
        try:
            type_, ro, ldap_attr = self._known_attrs2[name]
        except KeyError:
            # No creation of unknown attributes allowed
            raise AttributeError("'{}' object does not allow attribute '{}' to be set".format(type(self), name))

        if ro:
            raise AttributeError("'{}' object attribute '{}' is read-only".format(type(self), name))

        # Convert the type accordingly
        if value is not None:
            value = type_(value)

        # Store the pending change
        logger.debug("Storing pending change: {} => {}".format(name, value))
        self._pending_changes[name] = value


    def _prepare_dict(self, d):
        """Prepare a dictionary for python-ldap modlist
        """
        result = {}
        for k, values in d.items():
            # Keys are Python attributes; map them to ldap attributes
            _, _, ldap_attr = self._known_attrs2[k]

            # Values are always lists with python-ldap
            if not isinstance(values, list):
                values = [values]

            # And each value must be a bytes string, ugh.
            for i in range(len(values)):
                v = values[i]

                if v is None:
                    pass
                elif isinstance(v, bytes):
                    pass
                elif isinstance(v, (str, int)):
                    # TODO: Is this safe and correct in all cases?
                    v = str(v).encode()
                else:
                    raise Exception("Not sure what to do with value of type {}".format(type(v)))
                values[i] = v

            result[ldap_attr] = values

        return result



    def commit(self):
        old = {k:v for k, v in self._data.items() if k in self._pending_changes}

        old = self._prepare_dict(old)
        new = self._prepare_dict(self._pending_changes)

        logger.debug("Building modlist:\n  old: {}\n  new: {}".format(
            pformat(old), pformat(new)))

        modlist = modifyModlist(old, new)
        if modlist:
            logger.debug("Ready to modify {} with changelist:\n{}".format(
                self.dn, format_modlist(modlist)))
            self._ad._modify(self.dn, modlist)
        else:
            logger.debug("Nothing to modify in {}".format(self.dn))

        # Move everything from _pending_changes to _data
        self._data.update(self._pending_changes)
        self._pending_changes.clear()



class AdUser(LdapChangeTrackObject):
    _known_attrs = {
        # Name => (Type, Read-only)
        'uidNumber':        (int, False),
        'gidNumber':        (int, False),
        'primaryGroupID':   (int, True),
        'objectSid':        (SID.from_bytes, True),
    }


class AdGroup(AdUser):
    pass
