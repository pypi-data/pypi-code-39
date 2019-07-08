"""
BROADSOFT XSI-SIP auth plugin for HTTPie.
"""
from httpie.plugins import AuthPlugin
import base64

__version__ = '1.0.0'
__author__ = 'Pietro Bertera'
__licence__ = 'BSD'


class HttpXSISIP:
    def __init__(self, xsi_username, sip_username, sip_password):
        self.xsi_username = xsi_username
        self.sip_username = sip_username
        self.sip_password = sip_password

    def __call__(self, r):
        r.headers['Authorization'] = 'BroadWorksSIP basic="' + \
            base64.b64encode('%s:%s' % (self.xsi_username, self.sip_password)) + \
            '",sipUser="' + base64.b64encode(self.sip_username) + '"'
        return r

class XSISIPAuthPlugin(AuthPlugin):

    name = 'Broadsoft XSI-SIP auth'
    auth_type = 'xsisip'
    description = ''
    auth_parse = False #do not parse user:password
    def get_auth(self):
        (xsi_username, sip_username, sip_password) = self.raw_auth.split(':')
        return HttpXSISIP(xsi_username, sip_username, sip_password)
