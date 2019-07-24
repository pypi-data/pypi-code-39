"""
Tests for core.py
"""


import pytest

from os.path import exists

import neulang.core as core
from neulang.callees import Callee


def neu_samples():
    # TODO: find a way to always locate tests.neu
    tests = """
    * air_say
** air_joined_str
*** air_mul
**** air_div
***** 48
***** 94
**** 100
*** '% of AST nodes implemented'

* print("This is a regular Python expression...")

* air_say '... and this is inline ASTIR (Abstract Syntax Tree Intermediate Representation)...'

* air_setv
** this
** "... which can also be expressed hierarchially"
* air_say this

* air_say
** ["a", 'Python', "list"]
** is also a regular Python expression,
** "but under ASTIR"

* air_say
** 'Now for a lil math: 7+13+9='
** air_add
*** 7
*** 13
*** air_add 6 3

* print(f'15+21={15 + 21} also works of course')

* air_say
** 'Testing random combined math:'
** air_mul
*** 5
*** 31
*** air_div 10 3
*** 7.9
*** air_sub 99.3 100
** with some text after it

* air_say
** Testing unary 'not'; should yield True:
** air_not 0
** and False:
** air_not
*** 13

* air_say
** 'And' table results:
** air_and
*** 0
*** 0
** air_and
*** 0
*** 1
** air_and
*** 1
*** 0
** air_and 1 1

* air_say
** 'Or' table results:
** air_or
*** 0
*** 0
** air_or 0 1
** air_or
*** 1
*** 0
** air_or 1 1

* air_say
** Test comparison 5 == 4+1 == 3+2:
** air_eq
*** 5
*** air_add 4 1
*** air_add
**** 3
**** 2
*** 
** 

* air_call print 'Now we can call functions!'

* air_nop
** Everything in this node is ignored
** air_call
*** air_say
*** This call syntax looks a bit weird...
*** But it'll make sense in time, I hope
** air_call
*** air_say
*** This string has embedded "double quotes" and 'single quotes' in it, and even "a 'nested example'".
** air_while
*** 
** air_return None

* air_import
** os
* air_import random
* air_say 'Imports:' os random

* air_if
** air_eq
*** 5
*** 6
** air_say "They're equal!"
** air_say "They aren't equal..."

* air_for
** idx
** air_call range 1 5
** air_say idx "potato"

* air_def
** hello
** args
*** name
** body
*** air_say 'Hi there' name '!'
** decorators
** returns
* hello('Drew')

* air_class
** my_life
** body
*** air_setv fav_num 13
*** air_setv
**** now_playing
**** "Chat Wars"
** 
* print(f"Favorite number is {my_life.fav_num}")
* air_say
** Current obsession:
** air_call
*** getattr
*** my_life
*** 'now_playing'
* air_delete my_life

* air_assert True 'Some random message that never shows'

* air_try
** body
*** air_say 'Testing exceptions'
*** air_raise
**** air_call
***** Exception
***** Some random reason
** handlers
*** air_except_handler
**** Exception
**** e
**** body
***** air_say 
****** "Raising for:"
****** air_call str e

* air_say
** air_dict
*** 145
**** 'one quatro go'
*** 'a string'
**** 'says blah'
*** True
**** 13

* air_def
** arg_ts
** args
*** a
*** air_kwd
**** e
**** 27
*** air_starred
**** b
*** air_kwd
**** c
**** None
*** air_kwd
**** d
** body
*** air_say a b c d e
* air_call
** arg_ts
** 29
** air_starred
*** air_list
**** 'a disassociated list' 
**** 'of strings'
** air_kwd
*** c
*** True
** air_kwd
*** air_dict
**** 'x'
***** 'ekans'
**** 'y'
***** 'Yugioh'
**** 'z'
***** 'Zabuza'

* air_say
** 'Testing'
** air_list 'list' 'of' 'elements'

* air_say
** 'Result of slicing a list: '
** air_slice
*** air_list 1 2 3
*** -1

* air_with
** items
*** fo
**** open('file.txt', 'w')
** body
*** fo.write('Some random text')

* air_say 'Goodbye ASTIR'

* print("=============================")

* say Hello natural language programming
** add_adapt_handler
*** intent_parts
**** 'say (?P<req_text>.+)'
*** body
**** air_say text
* say The above sub definition is visible beyond!
"""
    src = open('tests/tests.neu').read() if exists('tests/tests.neu') else tests
    samps = [e for e in src.split('\n\n') if e.startswith('* ')] if '\n\n' in src else list(map(lambda l: f'* {l}', '\n'.join(list(filter(lambda l: l[:1] == '*', src.split('\n')))).split('\n* ')))
    return samps

@pytest.fixture(scope="module")
def Neu():
    neu = core.Neulang
    return neu

@pytest.fixture(scope="function")
def neu(Neu):
    neu = Neu()
    c = Callee()
    neu.update_namespace(**c.to_dict())
    return neu


class TestNeulang:

    @pytest.mark.parametrize("expr,retv", [("* 1 + 5", 6)])
    def test_eval_py_expr(self, neu, expr, retv):
        neu.loads(expr)
        assert neu.eval(mode="eval") == retv
        return

    @pytest.mark.parametrize("expr, fun, mode", [
        ("* air_setv\n** a\n** 3", lambda ns: ns['a'] == 3, 'exec'),
        ("* air_slice\n** air_list 1 2 3\n** -1", lambda ns: ns['_'] == 3, 'eval'),
        ('* air_call\n** print\n** Weird call syntax', lambda ns: True, 'exec'),
        ("""* air_setv
** string
** 'This is a string'
* add_adapt_handler
** intent_parts
*** 'replace (?P<req_txt>.+) with (?P<req_rep>.+) in (?P<req_var>\w+)'
** body
*** air_setv
**** globals()[var]
**** globals()[var].replace(txt, rep)
* replace string with modified string in string""", lambda ns: ns['string'] == 'This is a modified string', 'exec'),
        ("""
* x_setv('b', 7)
* air_setv
** q
** x_getv('b') * 12""", lambda ns: ns['q'] == 84, 'exec'),
        ("""
* find average of 3 and 5
** add_adapt_handler
*** intent_parts
**** 'find average of (?P<req_num1>\d+) and (?P<req_num2>\d+)'
*** body
**** x_setv('num1', num1)
** get and sum the numbers
*** add_adapt_handler
**** intent_parts
***** 'get and sum the numbers'
**** body
#***** print(x_setv('num1'), num1)
***** x_setv('num_sum', int(num1) + int(num2))
** divide by 2
*** add_adapt_handler
**** intent_parts
***** 'divide by (?P<req_amount>\d+)'
**** body
***** x_setv('num_ave', x_getv('num_sum') / int(amount))
** output result
*** add_adapt_handler
**** intent_parts
***** 'output result'
**** body
***** air_setv
****** num_ave
****** x_getv("num_ave")
***** print(f'Average of {num1} and {num2} is {num_ave}')""", lambda ns: ns['num_ave'] == 4, 'exec')
    ])
    def test_eval_astir(self, neu, mocker, monkeypatch, expr, fun, mode):
        neu.loads(expr)
        neu.eval(mode=mode)
        assert fun(neu._ns)
        return

    @pytest.mark.parametrize("samp", [s for s in neu_samples()])
    def test_samples(self, neu, samp, capsys):
        # Run the samples in tests.neu
        # NB: doesn't really validate anything it seems
        neu.loads(samp)
        neu.eval()
        captured = capsys.readouterr()
        assert captured and not 'Error' in captured
        captured = None
        return

    def test_update_namespace(self, neu):
        ad = {'a': 23, 'z': False}
        rl = ['z']
        neu.update_namespace(**ad)
        assert neu.ns['a'] == 23 and neu.ns['z'] is False
        neu.update_namespace(*rl)
        assert 'z' not in neu.ns
        return

    def test_to_py(self, neu):
        n_s = neu_samples()
        n_code = n_s[0]
        neu.loads(n_code)
        py = neu.to_py()
        assert 'print' in py and 'AST nodes' in py
        return

    @pytest.mark.parametrize('name, pkg, code, e_path, e_res_t', [
        ('script', None, '* neu code', './script.neu', str),
        ('foo.bar', None, '* neu code', './foo/bar/__init__.neu', str),
        ('foo.bar.bad', None, 'bad\nneu\ncode', './foo/bar/bad.neu', ImportError),
        ('fer.ben', None, '* invalid package/module format', None, ModuleNotFoundError),
        ('foo.bar.baz', None, '* neu code', './foo/bar/baz.neu', str)
    ])
    def test_load_module(self, neu, mocker, monkeypatch, name, pkg, code, e_path, e_res_t):
        m_paths = [
            './foo',
            './foo/__init__.neu',
            './foo/bar',
            './foo/bar/__init__.neu',
            './foo/bar/bad.neu',
            './fer',
            './fer/ben.neu',
            './script.neu',
            './foo/bar/baz.neu',
        ]

        def ope(p):
            return True if p in m_paths else False
        ope_mock = mocker.Mock(side_effect=ope)
        opi_mock = mocker.Mock(side_effect=lambda p: True if p.endswith('.neu') else False)

        def n_eval(*a, **k):
            neu.loads(code)
            return True #neu.eval(*a, **k)  # RecursionError
        l_mock = mocker.Mock(side_effect=lambda m, sf='blah': code)
        monkeypatch.setattr(neu, 'load', l_mock)
        monkeypatch.setattr(core, 'op_exists', ope_mock)
        monkeypatch.setattr(core, 'op_isfile', opi_mock)
        monkeypatch.setattr(neu, 'eval', n_eval)

        try:
            res = neu.load_module(name, pkg)
            l_mock.assert_called_with(e_path)

        except Exception as e:
            res = e
        assert isinstance(res, e_res_t)
        return
