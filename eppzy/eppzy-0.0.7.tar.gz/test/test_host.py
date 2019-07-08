from eppzy.rfc5732_host import Host
from eppzy.util import Add, Rem
from util import mocked_session, data_file_contents


def test_check():
    def checks(body):
        assert b'check' in body
        assert b'ns1.panda.io' in body
        assert b'ns2.yo.ho' in body
        return data_file_contents('rfc5732/check.xml')
    with mocked_session(checks, [Host]) as s:
        r = s['host'].check(['ns1.panda.io', 'ns2.yo.ho'])
    assert r.data['checks'] == {
        'ns1.example.com': True,
        'ns2.example2.com': False,
        'ns3.example3.com': True
    }


def test_info():
    def checks(body):
        assert b'info' in body
        assert b'cheeky' in body
        return data_file_contents('rfc5732/info.xml')
    with mocked_session(checks, [Host]) as s:
        r = s['host'].info('cheeky')
    assert r.data == {
        'name': 'ns1.example.com',
        'roid': 'NS1_EXAMPLE1-REP',
        'IPv4': {'192.0.2.2', '192.0.2.29'},
        'IPv6': {'1080:0:0:0:8:800:200C:417A'}
    }


def test_create():
    def checks(body):
        assert b'create' in body
        assert b'nom' in body
        assert b'4.4.4.4' in body
        assert b'::6' in body
        return data_file_contents('rfc5732/create.xml')
    with mocked_session(checks, [Host]) as s:
        r = s['host'].create('nom', v4s={'4.4.4.4'}, v6s={'::6'})
    assert r.data['name'] == 'ns1.example.com'


def test_delete():
    def checks(body):
        assert b'delete' in body
        assert b'flange' in body
        return data_file_contents('rfc5731/delete_example.xml')
    with mocked_session(checks, [Host]) as s:
        s['host'].delete('flange')


def test_update():
    def checks(body):
        assert b'update' in body
        assert b'bob.cob' in body
        assert b'bob.rob' in body
        return data_file_contents('rfc5731/create_example.xml')
    with mocked_session(checks, [Host]) as s:
        s['host'].update(
            'bob.cob', new_name='bob.rob',
            IPv4=[Add('127.0.0.1'), Rem('127.0.0.2')],
            IPv6=[Add('::1'), Rem('::2')])
