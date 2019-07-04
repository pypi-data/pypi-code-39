from flask import jsonify
import python_freeipa
from .config import config

IPA_HOST = config.IPA_HOST
IPA_USER = config.PRINCIPAL
IPA_PASSWORD = config.PASSWORD


class Host(object):
    """The Instance object holds EC2 information.

    Args:
        hostname (str): FQDN
        ip (unicode str): Private IP Address

    Attributes:
        hostname (str): FQDN
        ip (unicode str): Private IP Address
        otp (str): One-time password generated for host registration
        connection (): FreeIPA session
        exists (bool): Does host exists in FreeIPA

    """

    def __init__(self, hostname, ip):
        self.hostname = hostname
        self.ip = None
        self.otp = None
        self.connection = None
        self.exists = False

    def connect(self):
        """Connect to FreeIPA."""
        self.connection = python_freeipa.Client(
            IPA_HOST, verify_ssl=False, version='2.215')
        self.connection.login(IPA_USER, IPA_PASSWORD)

    def register(self):
        """Register host with FreeIPA."""
        host = self.connection.host_add(
            self.hostname, random=True, ip_address=self.ip)
        self.otp = host.get('randompassword')

    def deregister(self):
        """Deregister host."""
        self.connection.host_del(self.hostname, updatedns=True)

    def check(self):
        """Check if host exists."""
        if self.connection.host_find(criteria=self.hostname,
                                     fqdn=self.hostname):
            self.exists = True
        else:
            self.exists = False
