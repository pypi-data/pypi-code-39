from eppzy.rfc5730_epp import EPP
from eppzy.session import RequestWrapper
from eppzy.connection import LengthPrefixed
from util import data_file_contents, MockTransport


def test_login():
    def checks(body):
        assert b'login' in body
        assert b'bobby' in body
        assert b'passable' in body
        return data_file_contents('rfc5730/login_example.xml')
    mt = MockTransport(checks)
    e = RequestWrapper(EPP(LengthPrefixed(mt)))
    e.login(['oidy'], ['eidy'], 'bobby', 'passable')


def test_logout():
    def checks(body):
        assert b'logout' in body
        return data_file_contents('rfc5730/logout_example.xml')
    mt = MockTransport(checks)
    e = RequestWrapper(EPP(LengthPrefixed(mt)))
    e.logout()
