from eppzy.nominet import NContact, NDomain, RegStatus
from eppzy.session import RequestWrapper
from util import data_file_contents, mocked_session


def test_ncontact_create():
    def checks(body):
        assert b'traddie' in body
        return data_file_contents('rfc5733/contact_create_example.xml')
    with mocked_session(checks, [NContact.base], [NContact]) as s:
        s['contact'].create(
            'cid', 'nam', 'org', ['street'], 'city', 'sop', 'RC32 NFQ', 'GB',
            '+44.382919', 'fax', 'bob@bob.bob', '', trad_name='traddie')


def test_ncontact_info():
    def checks(body):
        assert b'info' in body
        assert b'mrbill' in body
        return data_file_contents('nominet/contact_info_example.xml')
    with mocked_session(checks, [NContact.base], [NContact]) as s:
        r = s['contact'].info('mrbill', 'passy')
    assert r.data['trad_name'] == 'Big enterprises'
    assert r.data['org'] == 'Company.'


def test_ndomain_create():
    def checks(body):
        assert b'create' in body
        assert b'datp.music' in body
        assert b'auto-bill' in body
        return data_file_contents('rfc5731/create_example.xml')
    with mocked_session(checks, [NDomain.base], [NDomain]) as s:
        s['domain'].create('datp.music', auto_bill=3)


def test_ndomain_update():
    def checks(body):
        assert b'update' in body
        assert b'renew-not-required' in body
        return data_file_contents('rfc5731/update_example.xml')
    with mocked_session(checks, [NDomain.base], [NDomain]) as s:
        s['domain'].update('a.gg', renew_required=False)


def test_ndomain_info():
    def checks(body):
        assert b'ban.ana' in body
        return data_file_contents('nominet/domain_info_example.xml')
    with mocked_session(checks, [NDomain.base], [NDomain]) as s:
        r = s['domain'].info('ban.ana')
    assert 'renew_required' in r.data
    assert r.data['status'] == RegStatus.REGISTERED


def test_ndomain_list():
    def checks(body):
        assert b'list' in body
        assert b'2018-03' in body
        return data_file_contents('nominet/list_example.xml')
    with mocked_session(checks, [NDomain.base], [NDomain]) as s:
        r = s['domain'].list(2018, 3)
    assert ['example.com', 'example-2.com'] == r.data
