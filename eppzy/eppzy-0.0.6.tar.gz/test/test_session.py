from mock import Mock, patch

from eppzy.rfc5730_epp import EPP
from eppzy.rfc5733_contact import Contact
from eppzy.nominet import NContact
from eppzy.session import session
from eppzy.mock_session import mock_connection
from util import data_file_contents


def test_session():
    responses = [
        (b'login', data_file_contents('rfc5730/login_example.xml')),
        (b'logout', data_file_contents('rfc5730/logout_example.xml'))
    ]
    def checks(body):
        should_contain, response = responses.pop(0)
        assert should_contain in body
        return response
    greeting = data_file_contents('nominet/greeting_example.xml')
    with patch('eppzy.session.connection', return_value=mock_connection(checks, greeting)):
        s = session([Contact], [NContact], 'h', 12, 'someone', 'somepass')
        with s as objs:
            assert 'contact' in objs
            assert type(objs['contact']._wrapee).__name__ == 'NomContact'
