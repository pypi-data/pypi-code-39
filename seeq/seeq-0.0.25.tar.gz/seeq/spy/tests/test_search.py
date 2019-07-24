import pytest

from seeq import spy

from . import test_common


@pytest.mark.system
def test_search():
    #test_common.login()
    spy.login(url='https://shell.seeq.site', username='agent_api_key', password='iH8IlgQo9jflC7c5JOxDGw', auth_provider='Seeq')

    spy.search({
        'Name': 'CGH.FI364'
    })
