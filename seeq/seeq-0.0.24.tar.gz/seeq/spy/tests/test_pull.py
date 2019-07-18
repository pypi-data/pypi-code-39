import pytest

from seeq import spy

from . import test_common


@pytest.mark.system
def test_pull():
    test_common.login()

    search_results = spy.search({
        'Name': 'Area A_Temperature'
    })

    spy.pull(search_results, start='2019-01-01T00:00:00.000Z', end='2019-06-01T00:00:00.000Z')
