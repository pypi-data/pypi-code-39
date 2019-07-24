"""

"""


import pytest

from neulang.pubsub import PubSub


class TestPubSub:

    @pytest.fixture
    def ps(self):
        return PubSub()

    def test_pub(self, ps):
        t = 'namespace.default'
        c = 'my content'
        ps.pub(t, c)
        hub = ps._hub
        assert t in hub and hub[t].get('content_list') == [c]
        return

    def test_sub(self, ps, mocker):
        t = 'namespace.default'
        self.test_pub(ps)
        c = mocker.Mock()
        nsl = ps.sub()
        assert nsl == [t]
        ps.sub(topic=t, callback=c)
        c.assert_called_with('my content')
        return
