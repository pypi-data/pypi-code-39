import hy.macros
from hy import HyExpression, HyInteger, HyList, HyString, HySymbol
from hy.core.language import butlast, distinct, last, rest
from hy.core.shadow import hyx_Xplus_signX, not_in
import os
import csv
import json
import time
hy.macros.require('hy.extra.anaphoric', None, assignments='ALL', prefix='')
import hy
hy.macros.macro('car')(lambda hyx_XampersandXname, arr: HyExpression([] + [
    HySymbol('get')] + [arr] + [HyInteger(0)]))
import hy
hy.macros.macro('cdr')(lambda hyx_XampersandXname, arr: HyExpression([] + [
    HySymbol('get')] + [arr] + [HyExpression([] + [HySymbol('slice')] + [
    HyInteger(1)] + [HySymbol('None')])]))
import hy
hy.macros.tag('map')(lambda f: HyExpression([] + [HySymbol('fn')] + [HyList
    ([] + [HySymbol('arr')])] + [HyExpression([] + [HySymbol('list')] + [
    HyExpression([] + [HySymbol('map')] + [f] + [HySymbol('arr')])])]))
import hy
hy.macros.tag('filter')(lambda f: HyExpression([] + [HySymbol('fn')] + [
    HyList([] + [HySymbol('arr')])] + [HyExpression([] + [HySymbol('list')] +
    [HyExpression([] + [HySymbol('filter')] + [f] + [HySymbol('arr')])])]))
import hy
hy.macros.tag('r')(lambda f: HyExpression([] + [HySymbol('fn')] + [HyList([
    ] + [HySymbol('&rest')] + [HySymbol('rest')] + [HySymbol('&kwargs')] +
    [HySymbol('kwargs')])] + [HyExpression([] + [f] + [HyExpression([] + [
    HySymbol('unpack-iterable')] + [HyExpression([] + [HySymbol('reversed')
    ] + [HySymbol('rest')])])] + [HyExpression([] + [HySymbol(
    'unpack-mapping')] + [HySymbol('kwargs')])])]))


def load_csv(fname, key=None):
    arr = list((lambda *rest, **kwargs: map(*reversed(rest), **kwargs))(
        list(csv.DictReader(open(fname, 'r+'))), dict)) if os.path.isfile(fname
        ) else []
    if key:
        obj = {}
        for row in arr:
            obj[row[key]] = row
        _hy_anon_var_1 = obj
    else:
        _hy_anon_var_1 = arr
    return _hy_anon_var_1


def fieldnames(arr):
    return list(set(hyx_Xplus_signX([], *list(map(lambda row: list(row.keys
        ()), arr)))))


hyx_XasteriskXfieldnamesXasteriskX = fieldnames


def write_csv(fname, arr, id=None, fieldnames=None):
    writer = csv.DictWriter(open(fname, 'w+'), fieldnames=fieldnames if
        fieldnames else hyx_XasteriskXfieldnamesXasteriskX(arr))
    writer.writeheader()
    for row in arr:
        writer.writerow(row)


def write_csv_add(fname, arr, **kwargs):
    it = fname
    it = load_csv(it)
    it = list(it) + list(arr)
    it = write_csv(fname, it, **kwargs)
    return it


def thru(x):
    return x


def unique(arr, key=None):
    if key:
        obj = {}
        for elem in arr:
            obj[key(elem)] = elem
        _hy_anon_var_7 = obj.values()
    else:
        _hy_anon_var_7 = list(set(arr))
    return _hy_anon_var_7


def apply_to_chunks(f, arr, size, process=thru):
    """rework it - [[] []]"""
    buffer = []
    results = []
    while arr:
        buffer.append(arr.pop())
        if len(buffer) >= size or not arr:
            results.append(f(buffer))
            buffer = []
            _hy_anon_var_9 = None
        else:
            _hy_anon_var_9 = None
    return process(results)


def not_in(what, where):
    return list(filter(lambda x: not x in where, what))


def select(arr, fields):
    return list(map(lambda obj: get_mass(obj, fields), arr))


def replace(s, obj):
    for k, v in obj.items():
        s = s.replace(k, v)
    return s


def json_quotes_single_to_double(j):
    return replace(j, {"{'": '{"', "':": '":', ", '": ', "', ": '": ': "',
        "'}": '"}'})


def first_that(arr, f):
    for elem in arr:
        if f(elem):
            return elem
            _hy_anon_var_15 = None
        else:
            _hy_anon_var_15 = None
    return None


import hy
hy.macros.macro('last-that')(lambda hyx_XampersandXname, arr, f:
    HyExpression([] + [HySymbol('first-that')] + [HyExpression([] + [
    HySymbol('reversed')] + [arr])] + [f]))


def distinct(arr, f):
    res = {}
    for row in arr:
        res[f(row)] = row
    return res


def get_as(what, structure):
    i = 1
    obj = {}
    for k, v in structure.items():
        obj[k] = what[v]
    return obj


def trim(s):
    s = s.replace('\r\n', '\n').replace('\n', ' ')
    while s.endswith(' '):
        s = s[slice(0, -1)]
    while s.startswith(' '):
        s = s[slice(1, None)]
    while '  ' in s:
        s = s.replace('  ', ' ')
    return s


def ascii(s, mode='replace'):
    return s.encode('ascii', mode).decode('ascii')


def leave_only(s, approved):
    res = ''
    for c in s:
        if c in approved:
            res = res + c
            _hy_anon_var_21 = None
        else:
            _hy_anon_var_21 = None
    return res


def dehydrate(s):
    return leave_only(ascii(trim(s)).lower(), 'qwertyuiopasdfghjklzxcvbnm')


def sum_by(arr, key):
    sum = 0
    for row in arr:
        sum += key(row)
    return sum


def pareto(data, coeff, key):
    data = sorted(data, key=key, reverse=True)
    total = sum_by(data, key)
    for i in range(1, len(data)):
        sub_data = data[slice(0, i)]
        sub_total = sum_by(sub_data, key)
        if sub_total > coeff * total:
            return sub_data
            _hy_anon_var_25 = None
        else:
            _hy_anon_var_25 = None


def escape(s):
    return (lambda hyx_Xpercent_signX1: '"{}"'.format() if '"' in
        hyx_Xpercent_signX1 else hyx_Xpercent_signX1)(s.replace('"', '\\"'))


def only_pcze(s):
    permitted = '1234567890 qwertyuiopasdfghjklzxcvbnm.:/-\\?!'
    permitted = permitted + 'ąćęłńóśźż'
    permitted = permitted + permitted.upper()
    it = s
    it = list(it)
    it = filter(lambda c: c in permitted, it)
    it = list(it)
    it = ''.join(it)
    return it


def remove_control(s):
    return re.sub("r'\\p{C}'", '', s)


def photo_finish_fn(f):
    start = time.time()
    res = f()
    return time.time() - res,


import hy
hy.macros.macro('photo-finish')(lambda hyx_XampersandXname, *args:
    HyExpression([] + [HySymbol('do')] + [HyExpression([] + [HySymbol(
    'setv')] + [HySymbol('start')] + [HyExpression([] + [HySymbol(
    'time.time')])])] + list(args or []) + [HyExpression([] + [HySymbol('-'
    )] + [HyExpression([] + [HySymbol('time.time')])] + [HySymbol('start')])]))
import hy
hy.macros.macro('do-not-faster-than')(lambda hyx_XampersandXname, t, *args:
    HyExpression([] + [HySymbol('do')] + [HyExpression([] + [HySymbol(
    'setv')] + [HySymbol('start')] + [HyExpression([] + [HySymbol(
    'time.time')])])] + list(args or []) + [HyExpression([] + [HySymbol(
    'setv')] + [HySymbol('delta')] + [HyExpression([] + [HySymbol('-')] + [
    HyExpression([] + [HySymbol('time.time')])] + [HySymbol('start')])])] +
    [HyExpression([] + [HySymbol('if')] + [HyExpression([] + [HySymbol('<')
    ] + [HyInteger(0)] + [HySymbol('delta')])] + [HyExpression([] + [
    HySymbol('time.sleep')] + [HyExpression([] + [HySymbol('min')] + [
    HySymbol('delta')] + [t])])])]))


def jsonl_json(jstr):
    it = jstr
    it = it.split('\n')
    it = (lambda arr: list(filter(thru, arr)))(it)
    it = ','.join(it)
    it = '[{}]'.format(it)
    return it


def jsonl_loads(jstr):
    return json.loads(jsonl_json(jstr))


def jsonl_load(f):
    return jsonl_loads(f.read())


def jsonl_dumps(arr):
    return '\n'.join(list(map(json.dumps, arr)))


def jsonl_add(fname, item):
    return open(fname, 'a+').write('{}\n'.format(json.dumps(item)))


def list_dict(arr, key):
    return dict(zip(list(map(lambda x: x[key], arr)), arr))


import hy
hy.macros.macro('get-o')(lambda hyx_XampersandXname, *args: HyExpression([] +
    [HySymbol('try')] + [HyExpression([] + [HySymbol('get')] + list(butlast
    (args) or []))] + [HyExpression([] + [HySymbol('except')] + [HyList([] +
    [HySymbol('Exception')])] + [last(args)])]))
import hy
hy.macros.tag('try')(lambda expr: HyExpression([] + [HySymbol('try')] + [
    expr] + [HyExpression([] + [HySymbol('except')] + [HyList([] + [
    HySymbol('Exception')])] + [HyString('')])]))

