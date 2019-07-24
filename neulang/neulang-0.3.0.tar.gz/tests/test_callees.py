"""

"""


import pytest

from neulang.callees import Callee


class TestCallee:

    @pytest.fixture
    def c(self):
        return Callee()

    def test_x_setv(self, c):
        c.x_setv('a', 3)
        assert c.ns['a'] == 3
        return

    def test_x_getv(self, c):
        c.x_setv('b', 29)
        assert c.x_getv('b') == 29
        return

    def test_c_delv(self, c):
        c.x_setv('q', 13)
        c.x_delv('q')
        assert 'q' not in c.ns
        return

    @pytest.mark.parametrize('test, t_body, f_body, ctx, e_retv', [
        (lambda **ctx: True, lambda **ctx: 'test 1', None, {}, 'test 1'),
        (lambda **ctx: False, lambda **ctx: 'test 2 true', lambda **ctx: 'test 2 false', {}, 'test 2 false'),
    ])
    def test_x_if(self, c, test, t_body, f_body, ctx, e_retv):
        # TODO: test expr test and other possible cases
        retv = c.x_if(test, t_body, f_body, **ctx)
        assert retv == e_retv
        return

    @pytest.mark.parametrize('target, iter_, body, orelse, ctx, e_retv', [
        ('idx', range(0, 5), lambda i, **ctx: f'{i} potato', lambda **ctx: 'no potato', {}, 'no potato'),
    ])
    def test_x_for(self, c, target, iter_, body, orelse, ctx, e_retv):
        # TODO: test other possible cases
        retv = c.x_for(target, iter_, body, orelse, **ctx)
        assert retv == e_retv
        return

    @pytest.mark.parametrize('test, body, orelse, ctx, e_retv', [
        ('5 == 3 + 1', lambda ctx: True, None, {}, None),
    ])
    def test_x_while(self, c, test, body, orelse, ctx, e_retv):
        # TODO: more input combos
        retv = c.x_while(test, body, orelse, **ctx)
        assert retv == e_retv
        return

    def test_x_do(self, c):
        from functools import partial
        ctx = {}

        def add(val, **ctx):
            return val + ctx.get('return', 0)
        one = partial(add, 1)
        two = partial(add, 2)
        three = partial(add, 3)
        retv = c.x_do(one, two, three, **ctx)
        assert retv == 6
        return

    def test_x_import(self, c):
        mods = c.x_import('os', 'sys')
        assert mods and isinstance(mods, tuple)
        mod = c.x_import('.callees', packages='neulang')
        assert mod
        return

    def test_x_with(self, c):
        def enter(self):
            return 'entered'
        CM = c.x_class('CM', {'__enter__': enter, '__exit__': lambda s, *a: None})
        retv = c.x_with([CM, 'rv'], lambda rv, **ctx: rv)
        assert retv == 'entered'
        return

    def test_x_class(self, c):
        meth = lambda self: 3
        Cls = c.x_class('MyException', {'meth': meth}, tuple([Exception]))
        cls = Cls()
        assert isinstance(cls, Exception)
        assert cls.meth() == 3
        return

    @pytest.mark.parametrize('body, hans, ore, fin, ctx, e_retv', [
        (lambda c, **ctx: c.x_raise(SyntaxError, 'test'), [[SyntaxError, lambda exc, **ctx: 'syntax error raised']], None, None, {}, 'syntax error raised')
    ])
    def test_x_try(self, c, body, hans, ore, fin, ctx, e_retv):
        # TODO: test other possible cases
        from functools import partial
        retv = c.x_try(partial(body, c), *hans, orelse=ore, finalbody=fin, **ctx)
        assert retv == e_retv
        return

    def test_x_raise(self, c):
        msg = 'test successful'
        try:
            c.x_raise(ValueError, msg)

        except SyntaxError as se:
            assert se.args[0] == 'something broke'

        except ValueError as ve:
            assert ve.args[0] == msg

        except Exception as e:
            assert e.args[0] == 'more breakage'
        return

    def test_to_dict(self, c):
        cd = c.to_dict()
        assert cd and isinstance(cd, dict) and all([k.startswith('x_') for k in cd.keys()]) and all([callable(v) for v in cd.values()])
        return
