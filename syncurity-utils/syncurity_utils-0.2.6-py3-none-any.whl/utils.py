""" syncurity_utils.utils

This module provides static utility functions - these are the functions in the irflow_integrations.utils module in the
current integrations framework, tuned to be used from this module.

:copyright: (c) 2019 Syncurity
:license: Apache 2.0, see LICENSE.txt for more details
"""

import validators
import logging
import sys
import re

logger = logging.getLogger(__name__)

try:
    from urllib.parse import parse_qs, urlparse
    attempt_compat = False
except ImportError:
    if sys.version_info[0] < 3:
        logger.error('This utilities package is intended for python3 only')
        attempt_compat = True


def find_domain(target, only_domain=False, only_hostname=False):
    """ Utility to extract a fully qualified domain from a string that may contain a domain name 
    
    Args:
        target (str): The string that may contain a domain
        only_domain (bool): Optional - return only the domain name of a FQDN
        only_hostname (bool): Optional - return only the hostname in an FQDN
    
    Raises:
        TypeError: If the value past as ``target`` is not of type ``str``
        ValueError: If both ``only_domain`` and ``only_hostname`` are found to be ``True``
        ValueError: If ``only_hostname`` is passed as ``True`` for a target that is not an FQDN  
            e.g. target is an email address
    Returns:
        str: The domain, if found
    """

    def _parse_from_email(email):
        """ Hidden inner function to perform parsing from values determined to be email addresses """
        # only_domain option ignored in email parsing
        if only_hostname:
            raise ValueError('The value provided ({}) was an email address, no hostname can be returned'.format(email))
        return email.split('@')[1]

    def _parse_from_domain(domain):
        """ Hidden inner function to perform parsing from values determined to be existing domains """
        if only_domain:
            return '.'.join(domain.split('.')[-2:])
        if only_hostname:
            # only return hostname if a hostname is present (len('hostname.domain.tld'.split('.')) will return 3)
            if len(domain.split('.')) >= 3:
                return '.'.join(domain.split('.')[:-2])
            else:
                raise ValueError('The domain provided ({}) was not an FQDN'.format(domain))
        return domain

    def _parse_from_url(url):
        """ Hidden inner function to perform parsing from values determined to be URLs """
        fqdn = url.split('://')[1].split('/')[0].split('?')[0]
        if only_domain:
            return '.'.join(fqdn.split('.')[-2:])
        if only_hostname:
            if len(fqdn.split('.')) >= 3:
                return '.'.join(fqdn.split('.')[:-2])
            else:
                raise ValueError('The URL provided ({}) did not contain an FQDN'.format(url))
        return fqdn

    if not isinstance(target, str):
        raise TypeError('Value provided was of type {}, must be of type str'.format(type(target)))
    if only_domain and only_hostname:
        raise ValueError('The \'only_domain\' and \'only_hostname\' optional arguments are mutually exclusive, only one'
                         ' should be evaluated to True')
    if validators.email(target):
        return _parse_from_email(target)
    if validators.domain(target):
        return _parse_from_domain(target)
    if validators.url(target):
        return _parse_from_url(target)

    # No validation succeeded, attempt once more prepended with a protocol and try to parse as url
    #
    # This is useful in the case that someone passes something like google.com/images, which is not a proper domain or
    # url without the protocol
    protocol_target = 'http://{}'.format(target)

    if validators.url(protocol_target):
        logger.info('Provided value appears to be url without protocol - assuming form \'{}\''.format(protocol_target))
        return _parse_from_url(protocol_target)

    raise ValueError('The value provided ({}) was not an email address, domain, fully qualified domain name, '
                     'or URL'.format(target))


class DecodeProofpointURL(object):
    """Decodes Proofpoint rewritten URLs

    Args:
        url(str): Encoded Proofpoint URL

    Attributes:
        self.pplink (str): The endcoded Proofpoint URL
        self.arguments (dict): Parse a query string given as a string argument
            (data of type application/x-www-form-urlencoded)
        self.url (str): The decoded Proofpoint URL
    """

    def __init__(self, url):
        if attempt_compat:
            logger.error('This class\' functionality is python3 only')
        else:
            self.pplink = url
            self.arguments = parse_qs(urlparse(url).query)
            self.url = self._decodeurl()
            self._parse()

    def _decodeurl(self):
        """Private Method to decode URL

        Returns:
            str: If the URL could be decoded, ``None`` otherwise
        """
        try:
            tmp = self.arguments['u'][0].replace("_", "/")
            for x in list(set(re.findall('-[0-9A-F]{2,2}', tmp))):
                tmp = tmp.replace(x, chr(int(x[1:3], 16)))
            return tmp
        # If KeyError then not a rewritten URL
        except KeyError:
            return None

    def _parse(self):
        """Private method to decode ``recipient`` and ``site``

        Attributes:
            self.recipient (str): The ``recipient`` in ``self.arguments``
            self.site (str): The ``site`` in ``self.arguments``
        """
        if 'r' in self.arguments:
            self.recipient = self.arguments['r'][0]
        if 'c' in self.arguments:
            self.site = self.arguments['c'][0]
