"""

"""


import pytest

from neulang.omp import OMP
from neulang.resolvers import PyExprResolver

from neulang.adapt_resolver import AdaptResolver


class TestAdaptResolver:

    @pytest.fixture
    def otree(self):
        def otree(text):
            ompo = OMP()
            ompo.loads(text, None)
            return ompo.tree
        return otree

    @pytest.fixture
    def ar(self):
        return AdaptResolver()

    @pytest.mark.xfail(reason='TBD')
    def test_resolve(self):
        assert 0
        return

    @pytest.mark.xfail(reason='TBD')
    def test_add_handler(self, otree, ar, mocker, monkeypatch):
        t_rx = 'get (?P<req_var>\w+)'
        d = f'* add_adapt_handler\n** intent_parts\n*** {t_rx}'
        rre_mock = mocker.Mock(side_effect=ar._eng.register_regex_entity)
        monkeypatch.setattr(ar._eng, 'register_regex_entity', rre_mock)

        try:
            res = ar.add_handler(otree(d)[0])

        except Exception as e:
            res = e
        assert res is None
        rre_mock.assert_called_with(t_rx)
        return

    @pytest.mark.xfail(reason='TBD')
    def test_nl_call(self):
        assert 0
        return
