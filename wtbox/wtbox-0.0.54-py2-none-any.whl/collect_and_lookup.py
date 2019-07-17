# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 14:57:55 2017

@author: pkiefer
"""
from collections import defaultdict
import itertools
import emzed
from operator import add, div, sub
import numpy as np
from scipy.spatial import distance
from copy import copy
from random import uniform


def table2lookup(t, key2tol, d=None):
    if not d:
        d=defaultdict(list)
        # empty clone allows rebuilding of table keeping column order, formats and types
        d['empty_clone']=t.buildEmptyClone()
    key_cols=sorted(key2tol.keys())
    ntuples=zip(*[t.getColumn(col).values for col in key_cols])
    # rt values are identical within the same feature thus the key tuple might be no longer unique.
    ntuples=unique_tuples(ntuples)
    value_cols=[n for n in t.getColNames()]
    values=zip(*[t.getColumn(col).values for col in value_cols])
    tolerances=[key2tol[key] for key in key_cols]
    # tolerances are added to d to allow key calculation from loopkup object
    d['bin_tols']=tolerances
    for key_tuple, value_tuple in zip(ntuples, values):
        keys=calculate_keys(key_tuple, tolerances)
        for key in keys:
            add_values(d, key, key_tuple, value_cols, value_tuple)
    return d

def unique_tuples(ntuples):
    d={}
    unique_tuples=[]
    for ntuple in ntuples:
        while d.has_key(ntuple):
            # we modify the tuple values below significance
            ntuple=tuple([v+uniform(-1e-10, 1e-10) for v in ntuple])
        d[ntuple]=ntuple
        unique_tuples.append(ntuple)
    return unique_tuples
        
    
####################################################################################
def add_values(d, key, key_values, value_cols, values):
    value=key_values, {v_col: v for v_col, v in zip(value_cols, values)}
    d[key].append(value)


def calculate_keys(ntuple, tolerances):
    key=calculate_key(ntuple, tolerances)
    return get_neighbour_keys(key)


def calculate_key(ntuple, tolerances):
    ntuple=round_tuple_values(ntuple)
    key=tuple(itertools.imap(div, ntuple, tolerances))
    return tuple([int(v) for v in key])    


def round_tuple_values(ntuple):
    """ avoids rounding problems
    """
    if all([v!=None for v in ntuple]):
        return tuple([np.round(v, 6) for v in ntuple])
    return []

def get_neighbour_keys(key):
    modif=itertools.product((-1, 0, 1), repeat=len(key))
    return [add_tuples(key, tuple_) for tuple_ in modif]
    

def add_tuples(tup1, tup2):
    return tuple(itertools.imap(add, tup1, tup2))

def subtract_tuples(tup1, tup2):
    return tuple(itertools.imap(sub, tup1, tup2))    

def fullfilled(tup1, tup2, tols):
    delta=subtract_tuples(tup1, tup2)
    return all([abs(delta[i])<=tols[i] for i  in range(len(delta))])
    

def read_out(key_tuple, tols, lookup):
    keys=calculate_keys(key_tuple, tols)
    tuple2values=dict()
    for k in keys:
        try:
            pairs=lookup[k]
            for tuple_, col2value in pairs:
#                print key_tuple, tuple_, tols
                if fullfilled(key_tuple, tuple_, tols):
                    tuple2values[tuple_]=col2value
        except:
            pass
    return tuple2values
            
def read_out_table(bin_tuple, lookup, leftJoin=True, tols=None):
    rows=set([])
    bintols=lookup['bin_tols']
    if not tols:
        tols=bintols
    keys=calculate_keys(bin_tuple, bintols)
    colname2values=defaultdict(list)
    t=lookup['empty_clone']
    for k in keys:
        pairs=lookup.get(k) if lookup.has_key(k) else []
        for tuple_, col2value in pairs:
           if fullfilled(bin_tuple, tuple_, tols): 
               for colname in t.getColNames():
                    colname2values[colname].append(col2value[colname])
    rows=zip(*[colname2values[colname] for colname in t.getColNames()]) 
    # list is required to allow modifying rows object
    rows=[list(row) for row in rows]
    if not len(rows) and leftJoin:
        rows=[[None]*len(t.getColNames())]
    t.rows=rows
    return t.uniqueRows()

                
def _convert_subtables_to_table(t, colname='_matches'):
    for id_, sub in zip(t.id, t.getColumn(colname)):
        sub.updateColumn('sub_id', id_, type_=int)
    t1=emzed.utils.stackTables(t.getColumn(colname).values)
    t.updateColumn('sub_id', t.id, type_=int)
    t=t.fastJoin(t1, 'sub_id')
    postfixes=t.supportedPostfixes(['sub_id'])
    subs=[''.join(['sub_id', p]) for p in postfixes]
    drop=[colname]
    drop.extend(subs)
    t.dropColumns(*drop)
    return t
    
        
def get_best_match(key_tuple, tols, lookup):
    """ collect criterions if feature contains only a single peak: min deviation
    """
    tuple2values=read_out(key_tuple, tols, lookup)
    if len(tuple2values):
        key=_min_diff(key_tuple, tuple2values.keys())
        return tuple2values[key]
    
def _min_diff(key_tuple, tuples):
    def _euclidean(tuple_, key_tuple=key_tuple):
        return distance.euclidean(tuple_, key_tuple)
    return min(tuples, key=_euclidean)


def unique_value(values):
    assert len(set(values))==1, 'values of column are not unique!'
    return values[0]
    
#################################################################
# operations

def subtract_blank(t1, t2, diff_col='intensity',  key2tol=None, postfix='blank', scaling=3.0):
    assert t1.hasColumn(diff_col) and t2.hasColumn(diff_col), 'column %s is missing ' %diff_col
    if not key2tol:
        key2tol={'mz': 0.003, 'rt': 5.0}
    t1=compare_tables(t1, t2, columns=None, key2tol=key2tol)
    colname='_'.join([diff_col, postfix])
    t1.updateColumn(colname, t1.apply(max_value,(t1._matches, diff_col)), type_=float)
    t1.replaceColumn(colname, t1.getColumn(colname)*scaling, type_=float, format_='%.2e')
    t1.dropColumns('_matches')
    t=t1.filter(t1.getColumn(diff_col)>t1.getColumn(colname))
    t.dropColumns(colname)
    return t
    


def compare_tables(t1, t2, columns=None, key2tol=None, leftJoin=True):
    Table=emzed.core.data_types.Table
    t1=t1.copy()
    if not columns:
        columns=t2.getColNames()
    if not key2tol:
        key2tol={'mz': 0.003, 'rt': 5.0}
    key_cols=sorted(key2tol.keys())
#    tols=[key2tol[key] for key in key_cols]
    lookup=table2lookup(t2, key2tol)
    expr=zip(*[t1.getColumn(col) for col in key_cols])
    t1.addColumn('key', expr, type_=tuple)
    t1.addColumn('_matches', t1.apply(read_out_table, (t1.key, lookup, leftJoin)), 
                 type_=Table, format_='%r')
    t1=_convert_subtables_to_table(t1)
    t1.dropColumns('key')
    return t1
    
    
def max_value(d, diff_col):
    if len(d):
        diffs=[v[diff_col] for v in d.values()]
        return max(diffs)
    return 0.0
    
    
def readColumnValues(t, colnames, postfix='readout'):
    names=copy(colnames)
    names.append(postfix)
    name='_'.join(names)
    t.updateColumn(name, t.apply(_readout,(t.matches, colnames)), type_=tuple)


def _readout(d, colnames):
    matches=d.values()
    return tuple([[match.get(colname) for colname in colnames] for match in matches])
    
################################################################################################¬

def build_consensus_table_from_lookup(lookup, min_hits=1, weight_col='area', source_key='source',
                                      average_cols=['mz', 'rt'], id_cols=None):
    peaks_list=[]
    tolerances=lookup['bin_tols']
    for key in get_sorted_keys(lookup, weight_col):
        gen_values=genuin_values(key, lookup[key], tolerances)
        while len(gen_values):
            ref_values=most_intense(gen_values, weight_col)[0]
            selected=read_out(ref_values, tolerances, lookup)
            selected=source_dependent_best(selected, ref_values, source_key)
            [remove_value_from_dict(lookup, v) for v in selected]
            gen_values=genuin_values(key, lookup[key], tolerances)
            row=summarize_grouped_peaks(selected, min_hits, average_cols, weight_col, source_key, id_cols=id_cols)
            if row:
                peaks_list.append(row)
#    return peaks_list
    return build_consensus_table(peaks_list)
    

def genuin_values(key, values, tolerances):
    genuin=[]
    for entry in values:
        genuin_key=calculate_key(entry[0], tolerances) ## improve: provide calculate key directly
        if genuin_key == key:
           genuin.append(entry)
    return genuin
    

def most_intense(values, weight_col):
    return max(values, key=lambda v: v[-1][weight_col])

    
def get_sorted_keys(d, weight_col='area'):
    bintols=d['bin_tols']
    pairs=[]
    for key in d.keys():
        # since lookup dictionary has also keys assigned to original table
        # linit keys to table rows
        if isinstance(key, tuple):
            values=d[key]
            values=genuin_values(key, values, bintols)
            selected=[entry[1] for entry in values]
            weight=sum([v[weight_col] for v  in selected])
            pairs.append((key,weight))
    pairs.sort(key=lambda v: v[1], reverse=True)
    return [p[0] for p in pairs]


def source_dependent_best(key_val2row, ref_values, source_key):
    d=defaultdict(list)
    selected=[]
    for key_val, rowdict in key_val2row.items():
        source=rowdict[source_key]
        d[source].append((key_val, rowdict))
    for pairs in d.values():
        selected.append(min_euklid(pairs, ref_values))
    return selected

        
def min_euklid(pairs, ref):
    def euklid(v, ref=ref):
        tols, __=v
        return np.linalg.norm(np.array(tols)-np.array(ref))
    return min(pairs, key=euklid)


def remove_value_from_dict(d, v):
    tols=d['bin_tols']
    key=calculate_key(v[0], tols)
    keys=get_neighbour_keys(key)
    for key in keys:
        _remove_value(d, key, v)


def _remove_value(d,key,v):
    if d.has_key(key):
        while True:
            try: 
                d[key].remove(v)
            except:
                break
################################################################################################

def summarize_grouped_peaks(rows, min_hits, average_keys, weight_key, source_key, id_cols=None):
    PeakMap=emzed.core.data_types.PeakMap
    expr= isinstance(id_cols, list) or isinstance(id_cols, tuple)
    id_cols= id_cols if expr else []
    if len(rows)>=min_hits:
        rowsdict=defaultdict(list)
        for __, rowdict in rows:
            for key, value in rowdict.items():
                if not isinstance(value, PeakMap):
                    rowsdict[key].append(value)
        for key in average_keys:
            averaged=weighted_average(zip(rowsdict[key], rowsdict[weight_key]))
            rowsdict[key]=averaged
#        zs=set([v for v  in rowsdict['z'] if v>0])
#        if not len(zs):
#            zs=[0]
#        if len(zs)==1:
#        rowsdict['z']=tuple(zs)
#        else:
#        rowsdict['z']=0
#        for id_col in id_cols:
#            rowsdict[id_col]=zip(rowsdict[id_col], rowsdict[source_key])
        return rowsdict
        

def temporary(t, value_col, weight_col):
    def do_it(values, weights):
        return weighted_average(zip(values, weights), i=0, weight_fun=weight_)
    t.replaceColumn(value_col, t.apply(do_it, (t.getColumn(value_col), t.getColumn(weight_col))), type_=float)

def weight_(w):
    return float(np.log(w)+1)


def weighted_average(ntuples, i=0, weight_fun=weight_):
    if not weight_fun:
        def fun(v):
            return v
    else:
        fun=weight_fun
    values=[p[i] for p in ntuples]
    weights=[fun(p[-1]) for p in ntuples]
    return float(np.average(values, weights=weights))

       
def build_consensus_table(peaks):
    t=emzed.utils.toTable('id', range(len(peaks)), type_=int)
    # since each list entry is a dictionary with the same key()
    colnames=sorted(peaks[0].keys())
    for colname in colnames:
        if colname!='id':
            values, type_=_readout_column(peaks, colname)
            t.addColumn(colname, values, type_=type_)
    return t

def _readout_column(peaks, key):
    values=[]
    for peak in peaks:
        value=peak[key]
        if isinstance(value, list) or isinstance(value,str):
            values.append(tuple(value))
        else:
            values.append(value)
    return values, _get_type(values)


def _get_type(values):
    types=set([type(v) for v in values if v!=None])
    if not len(types):
        return object
    if len(types)==1:
        return types.pop()
    assert False, 'not one unique Type detected!'
    
#################################################################################################
def get_consistent_ids(t, id_cols):
    for id_col in id_cols:
        _get_consistent_ids(t, id_col)

def _get_consistent_ids(t, id_col):
    id2pairs=defaultdict(set)
    pair2ids=defaultdict(set)
    id2ids=defaultdict(set)
    for id_, id_pairs in zip(t.id, t.getColumn(id_col)):
       for pair in id_pairs:
           id2pairs[id_].add(pair)
           pair2ids[pair].add(id_)
    for id_ in t.id:
       pairs=id2pairs[id_]
       for pair in pairs:
           id2ids[id_].update(pair2ids[pair])
    id2group_id={}
    # start with min id
    id2id={id_: id_ for id_ in t.id}
    id_=t.id.min()
    m=0
    while len(id2id):
        print len(id2id)
        id_=min(id2id.keys())
        grouped_ids=set([id_])
        ids=id2ids[id_]
        grouped_ids.update(ids)
        while True:
            additional=_find_additional(grouped_ids, ids, id2ids)
            if len(additional):
                print len(additional)
                grouped_ids.update(additional)
            else:
                break
        [id2group_id.update({id_:m}) for id_ in grouped_ids]
        for id_ in grouped_ids:
            try:
                __=id2id.pop(id_)
            except:
                pass
        m+=1
    def add(v, d):
       return d.get(v)
    t.updateColumn(id_col, t.apply(add, (t.id, id2group_id)), type_=int)
    
             


def _find_additional(grouped, ids, id2ids):
    before=copy(grouped)
    for id_ in before:
        grouped.update(id2ids[id_])
    return grouped - before
    
        
         
     
        
        