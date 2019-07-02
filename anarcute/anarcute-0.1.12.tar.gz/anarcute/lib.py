from hy import HyExpression, HyInteger, HyList, HySymbol
from hy.core.language import distinct, rest
from hy.core.shadow import hyx_Xplus_signX, not_in
import os
import csv
import json
import hy
hy.macros.macro('car')(lambda hyx_XampersandXname, arr: HyExpression([] + [
    HySymbol('get')] + [arr] + [HyInteger(0)]))
import hy
hy.macros.macro('cdr')(lambda hyx_XampersandXname, arr: HyExpression([] + [
    HySymbol('get')] + [arr] + [HyExpression([] + [HySymbol('slice')] + [
    HyInteger(1)] + [HySymbol('None')])]))
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


def write_csv(fname, arr, id=None):
    writer = csv.DictWriter(open(fname, 'w+'), fieldnames=fieldnames(arr))
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


import hy
hy.macros.tag('map')(lambda f: HyExpression([] + [HySymbol('fn')] + [HyList
    ([] + [HySymbol('arr')])] + [HyExpression([] + [HySymbol('list')] + [
    HyExpression([] + [HySymbol('map')] + [f] + [HySymbol('arr')])])]))
import hy
hy.macros.tag('filter')(lambda f: HyExpression([] + [HySymbol('fn')] + [
    HyList([] + [HySymbol('arr')])] + [HyExpression([] + [HySymbol('list')] +
    [HyExpression([] + [HySymbol('filter')] + [f] + [HySymbol('arr')])])]))


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


def distinct(arr, f):
    res = {}
    for row in arr:
        res[f(row)] = row
    return res

