# -*- coding: utf-8 -*-
"""
Created on Tue Apr 04 13:21:26 2017

@author: pkiefer
"""
import itertools
import numpy as np
from collections import defaultdict
from operator import add, div, sub


def subtract_table(t1, t2, diff_col='intensity', key2tol=None, postfix='blank', scaling=3.0,
                   lower_bound=1e2):
    t1=t1.copy()                 
    assert t1.hasColumn(diff_col) and t2.hasColumn(diff_col), 'column %s is missing ' %diff_col
    if not key2tol:
        key2tol={'mz': 0.003, 'rt': 60.0}
    compare_peaks(t1, t2, columns=None, key2tol=key2tol, postfix=postfix)
    colname='_'.join([diff_col, postfix])
    t1.updateColumn(colname, t1.apply(max_value,(t1.matches, diff_col, lower_bound)), type_=float)
    t1.replaceColumn(colname, t1.getColumn(colname)*scaling, type_=float, format_='%.2e')
    t1.dropColumns('matches')
    t=t1.filter(t1.getColumn(diff_col)>t1.getColumn(colname))
    t.dropColumns(colname)
    return t


def max_value(d, diff_col, min_value):
    if len(d):
        diffs=[v[diff_col] for v in d.values()]
        return max(diffs) if max(diffs)>min_value else 0.0
    return 0.0


def compare_peaks(t1, t2, columns=None, key2tol=None, postfix='blank'):
    if not columns:
        columns=t2.getColNames()
    if not key2tol:
        key2tol={'mz': 0.003, 'rt': 5.0}
    key_cols=sorted(key2tol.keys())
    tols=[key2tol[key] for key in key_cols]
    lookup=table2lookup(t2, key_cols, key2tol)
    expr=zip(*[t1.getColumn(col) for col in key_cols])
    t1.addColumn('key', expr, type_=tuple)
    t1.addColumn('matches', t1.apply(read_out, (t1.key, tols, lookup)), type_=dict)
    t1.dropColumns('key')


def table2lookup(t, key_cols, key2tol, d=None):
    if not d:
        d=defaultdict(list)
    ntuples=zip(*[t.getColumn(col).values for col in key_cols])
    value_cols=[n for n in t.getColNames()]
    values=zip(*[t.getColumn(col).values for col in value_cols])
    tolerances=[key2tol[key] for key in key_cols]
    for key_tuple, value_tuple in zip(ntuples, values):
        key=calculate_key(key_tuple, tolerances)
        keys=get_neighbour_keys(key)
        for key in keys:
            add_values(d, key, key_tuple, value_cols, value_tuple)
    return d


def calculate_key(ntuple, tolerances):
    _round_tuple_values(ntuple)
    key=tuple(itertools.imap(div, ntuple, tolerances))
    return tuple([int(v) for v in key])    


def _round_tuple_values(ntuple):
    """ avoids rounding problems
    """
    return tuple([np.round(v, 6) for v in ntuple])


def get_neighbour_keys(key):
    modif=itertools.product((-1, 0, 1), repeat=len(key))
    return [add_tuples(key, tuple_) for tuple_ in modif]

    
def add_tuples(tup1, tup2):
    return tuple(itertools.imap(add, tup1, tup2))


def add_values(d, key, key_values, value_cols, values):
    value=key_values, {v_col: v for v_col, v in zip(value_cols, values)}
    d[key].append(value)


def read_out(key_tuple, tols, lookup):
    key=calculate_key(key_tuple, tols)
    keys=get_neighbour_keys(key)
    tuple2values=dict()
    for k in keys:
        try:
            pairs=lookup[k]
            for tuple_, col2value in pairs:
                if fullfilled(key_tuple, tuple_, tols):
                    tuple2values[tuple_]=col2value
        except:
            pass
    return tuple2values


def fullfilled(tup1, tup2, tols):
    delta=subtract_tuples(tup1, tup2)
    return all([abs(delta[i])<=tols[i] for i  in range(len(delta))])


def subtract_tuples(tup1, tup2):
    return tuple(itertools.imap(sub, tup1, tup2))    
