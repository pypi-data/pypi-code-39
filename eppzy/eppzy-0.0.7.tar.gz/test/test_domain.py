from datetime import datetime, date

from eppzy.rfc5731_domain import Domain
from eppzy.util import Add, Rem
from util import mocked_session, data_file_contents


def test_minimal_domain_info():
    d = Domain(None)
    xml, pr = d.info('dname')
    assert xml.find('command/info') is not None
    resp = d._parse_response(
        data_file_contents('rfc5731/domain_info_example.xml'))
    r = pr(resp.data)
    assert r['name'] == 'example.com'


def test_full_domain_info():
    def checks(body):
        assert b'dname' in body
        assert b'domain-1.0' in body
        return data_file_contents('rfc5731/domain_info_full_example.xml')
    with mocked_session(checks, [Domain]) as s:
        r = s['domain'].info('dname')
    assert r.data['name'] == 'example.com'
    assert r.data['host'] == ['ns1.example.com', 'ns2.example.com']
    assert r.data['registrant'] == 'jd1234'
    assert r.data['ns'] == ['ns1.example.com', 'ns1.example.net']


def test_check():
    def checks(body):
        assert b'check' in body
        assert b'panda.io' in body
        assert b'yoho.ho' in body
        return data_file_contents('rfc5731/check_example.xml')
    with mocked_session(checks, [Domain]) as s:
        r = s['domain'].check(['panda.io', 'yoho.ho'])
    assert r.data['checks'] == {
        'example.com': True,
        'example.net': False,
        'example.org': True
    }


def test_renew():
    def checks(body):
        assert b'renew' in body
        assert b'panda.io' in body
        return data_file_contents('rfc5731/renew_example.xml')
    with mocked_session(checks, [Domain]) as s:
        r = s['domain'].renew('panda.io', date.today())
    assert r.data['name'] == 'example.com'
    assert r.data['new_expiry_date'] == datetime(2005, 4, 3, 22, 0)


def test_create():
    def checks(body):
        assert b'create' in body
        assert b'panda.io' in body
        return data_file_contents('rfc5731/create_example.xml')
    with mocked_session(checks, [Domain]) as s:
        r = s['domain'].create('panda.io')
    assert r.data['name'] == 'example.com'


def test_update():
    def checks(body):
        assert b'update' in body
        assert b'panda.oi' in body
        assert b'turtle' in body
        assert b'Resolvulated' in body
        assert b'choo.choo' in body
        return data_file_contents('rfc5731/update_example.xml')
    with mocked_session(checks, [Domain]) as s:
        s['domain'].update(
            'panda.oi',
            ns=[Add('choo.choo'), Rem('woo.hoo')],
            contacts={'tech': Add('some1'), 'pet': Rem('turtle')},
            status={'bad': Rem(''), 'good': Add('Resolvulated')})


def test_delete():
    def checks(body):
        assert b'delete' in body
        assert b'panda.io' in body
        return data_file_contents('rfc5731/delete_example.xml')
    with mocked_session(checks, [Domain]) as s:
        s['domain'].delete('panda.io')
