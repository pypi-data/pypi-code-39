from eppzy.rfc5910_dnssec import DnsSec, DsData, RemoveAll
from eppzy.util import Rem, Add
from util import data_file_contents, mocked_session


def test_dnssec_info():
    with mocked_session(
            lambda _: data_file_contents('rfc5910/info.xml'),
            [DnsSec.base], [DnsSec]) as s:
        r = s['domain'].info('impa.la')
    assert r.data['dnssec'] == [DsData(
        key_tag=12345, algorithm=3, digest_type=1,
        digest='49FD46E6C4B45C55D4AC')]
    assert r.data['ns']


def test_dnssec_create():
    def checks(body):
        assert b'create' in body
        assert b'321' in body
        return data_file_contents('rfc5731/create_example.xml')
    with mocked_session(checks, [DnsSec.base], [DnsSec]) as s:
        s['domain'].create('impa.la', dnssec=[
            DsData(321, 3, 1, '49FD46E6C4B45C55D4AC')])


def test_dnssec_update_del_all():
    def checks(body):
        assert b'update' in body
        assert b'impa' in body
        assert b'<secDNS:all>' in body
        return data_file_contents('rfc5731/update_example.xml')
    with mocked_session(checks, [DnsSec.base], [DnsSec]) as s:
        s['domain'].update('impa.la', dnssec=RemoveAll)


def test_dnssec_update_change():
    def checks(body):
        assert b'update' in body
        assert b'impa' in body
        assert b'counting' in body
        assert b'up' in body
        return data_file_contents('rfc5731/update_example.xml')
    with mocked_session(checks, [DnsSec.base], [DnsSec]) as s:
        s['domain'].update('impa.la', dnssec=[
            Add(DsData(1, 2, 3, 'counting')),
            Rem(DsData(4, 5, 6, 'up'))])
