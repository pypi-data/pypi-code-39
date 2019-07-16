# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 12:50:37 2018

@author: pkiefer
"""
from wtbox.table_operations import update_column_by_dict
import wtbox.collect_and_lookup  as cl
from wtbox.collect_and_lookup import calculate_keys, fullfilled
from wtbox.utils import fast_isIn_filter as is_in
from wtbox.utils import show_progress_bar
import shared_functions as sf
import numpy as np
from collections import defaultdict, Counter
from local_feature_detection import local_ff_detect
import emzed
from copy import copy




def idms_feature_grouper(nl, ul, kwargs, mi_min=2, mi_max=40, mztol=0.001, id_col='feature_id', 
                         remove_unmatched=True):
    print 'Grouping features  via idms matching ...'
    rttol=sf.get_typical_fwhm(nl)/2
    lookup_nl=build_idms_istopologue_dict(nl, mi_min=mi_min, mi_max=mi_max, mztol=mztol, rttol=rttol)
    lookup_ul=build_idms_istopologue_dict(ul, mi_min=mi_min, mi_max=mi_max, mztol=mztol, 
                                          rttol=rttol, map_nl=False)
    groups_nl=get_feature_groups(lookup_nl, ul, mztol, rttol)
    groups_ul=get_feature_groups(lookup_ul, nl, mztol, rttol)
    t_nl=regroup_features(nl, groups_nl)
    t_nl=label_isotopologue_artefacts(t_nl, rttol)
    text='z assigned by feature_grouping'
    sf.charge_assign_event(t_nl, text)
    t_ul=regroup_features(ul, groups_ul)
    t_ul=label_isotopologue_artefacts(t_ul, rttol)
    sf.charge_assign_event(t_ul, text)
    print 'Done.'
    print 
    if remove_unmatched:
        t_nl=t_nl.filter(t_nl.z_.isNotNone())
        t_ul=t_ul.filter(t_ul.z_.isNotNone())
    print 'local isotopologue search to determine charge state of ungrouped peaks...'
    t_nl=local_ff_detect(t_nl, kwargs, mztol=kwargs['mztol'])
    t_ul=local_ff_detect(t_ul, kwargs, mztol=kwargs['mztol'])
    print 'Done.'
    print 'verfying plausability of natural labeled patterns ...'
    t_nl=check_groups_by_feature_plausability(t_nl, id_col)
    print 'Done.'
    print    
    print 'verfying plausability of U13C labeled patterns ...'
    t_ul=check_groups_by_feature_plausability(t_ul, id_col)
    print 'Done.'
    return t_nl, t_ul
    

def get_feature_groups(lookup, t, mztol, rttol):
    d=defaultdict(set)
    id2ids=defaultdict(set)
    for id_, mz, rt, fwhm in zip(t.id, t.mz, t.rt, t.fwhm):
        ids=read_lookup(lookup, mz, rt, fwhm, mztol, rttol)
        d[id_].update(ids)
    for ids in d.values():
        for id_ in ids:
            if id2ids.has_key(id_):
                id2ids[id_]=id2ids[id_].union(ids)
                for _id in id2ids[id_]:
                    id2ids[_id]=id2ids[id_]
            else:
                id2ids[id_]=ids
    return _unique_groups(id2ids)


def _unique_groups(id2ids):
    def _trafo(values):
        # tranform set into a tuple with sorted values as key
        return tuple(sorted(list(values))) 
    return {_trafo(ids):_trafo(ids) for ids in id2ids.values()}
    

def build_idms_istopologue_dict(t, mi_min=2, mi_max=40, mztol=0.001, rttol=5, map_nl=True):
    print 'building idms_isotopologue_dict ...'
    d=defaultdict(list)
    delta=emzed.mass.C13-emzed.mass.C if map_nl else emzed.mass.C-emzed.mass.C13
    iterable=zip(t.mz, t.z, t.rt, t.fwhm, t.id)
    args=(mi_min, mi_max, mztol, rttol, delta, d)
    show_progress_bar(iterable, add_values, args=args, in_place=True)
    return d

def add_values(values, mi_min, mi_max, mztol, rttol, delta, d):
    mz0, z, rt, fwhm, id_=values
    z_range=range(z, z+1) if z else range(1, 4)
    mi_range=range(mi_min, mi_max+1)
    _add_values_to_dict(mz0, rt, fwhm, id_, delta, mi_range, z_range, mztol, rttol, d)

def _add_values_to_dict(mz_ref, rt, fwhm, id_, delta, mi_range, z_range, mztol, rttol, d):
    for z in z_range:
        for mi in mi_range:
            mz=mz_ref+mi*delta/z
            keys=calculate_keys((mz,rt), (mztol, rttol))
            for k in keys:
                d[k].append((mz, z, rt, fwhm, id_))
    return d


def read_lookup(lookup_dict, mz, rt, fwhm, mztol, rttol):
    """
    bin by rt; 
        calculate allowed isotopologues 
    """
    keys=calculate_keys((mz,rt), (mztol, rttol))
    values=[]
    [values.extend(lookup_dict[k]) for k in keys]
    return _readout(values, mz, rt, mztol, fwhm)  
 
   
def _readout(values, mz, rt, mztol, fwhm):
    ids=[]
    for mz_, __,rt_, fwhm_, id_ in set(values):
        tol=min(fwhm, fwhm_)
        req1=abs(mz-mz_)<=mztol
        # this paramerter is very critical in positive mode with narrow peaks!!
        # we choose fwhm /2 wich as a conseqeunce allows more false positive for larger peaks. 
        req2=abs(rt-rt_)<=tol/2.0
        if all([req1, req2]):    
            ids.append(id_)
    return tuple(ids)   


def regroup_features(t, ids2ids):
    nl=t.is_nl.uniqueValue()
    groups=t.extractColumns('id', 'mz', 'area')
    grouped_tables=[]
    for ids in ids2ids.keys():
        group=is_in(groups, 'id', ids)
        grouped_tables.append(group)
    id2z={}
    id2fid={}
    for group in grouped_tables:
        id2peaks=dict(zip(group.id, group.rows))
        while len(id2peaks):
            _id2z={}
            _id2z=determine_charge_states(id2peaks.values(), nl, mztol=0.001)
            _update(id2fid, _id2z.keys())
            _remove_ids(id2peaks, _id2z)
            id2z.update(_id2z)
    t.updateColumn('fid', t.id, type_=int, insertAfter='feature_id')
    t.updateColumn('z_', None, type_=int, insertAfter='z')
    t=update_column_by_dict(t, 'z_', 'id', id2z, type_=int)
    t= update_column_by_dict(t, 'fid', 'id', id2fid, type_=int)    
    t.replaceColumn('feature_id', t.fid, type_=int)
    return  t


def _update(d, keys):
    value=min(keys)
    [d.update({key: value}) for key in keys]    


def _remove_ids(id2peaks, id2z):
    for _id in id2z.keys():
        try: 
            id2peaks.pop(_id)
        except:
            pass
    

def determine_charge_states(rows, nl, mztol=0.001):
    representing=max(rows, key=lambda v: v[-1])
    d=build_isotopologue_dict(representing[1], mztol, nl)
    hits=defaultdict(list)
    for z in d.keys():
        for row in rows:
            for key in calculate_keys((row[1],), (mztol,)):
                id_=row[0]
                rows_=d[z][key]
                rows_=copy(rows_)
                for row_ in rows_:
                    if len(d[z][key]) and fullfilled((row_[0],), (row[1],), (mztol,) ):
                        row_=list(row_)
                        row_.append(id_)
                        hits[z].append(tuple(row_))
    z2counts=[_count_matches(hits, z, nl) for z in hits.keys()]
    z, matches, counts=max(z2counts, key=lambda v: v[-1])
    # only 1 hit means no isotopologues detected
    if counts==1:
        z=0
    return {int(id_): z for id_ in matches[:,-1]}


def _count_matches(matches, z, nl):
    matched=_extract_matches(matches, z)
    matched=np.array(matched)
    allowed_patterns=matches_allowed_patterns(matched[:, -2], nl)
    counts=max([Counter(matched[:, -2]==allowed)[True] for allowed in allowed_patterns])
    return z, matched, counts


def _extract_matches(matches, z):
    matches=set(matches[z])
    # transform to list
    matches=[v for v in matches]
    return sorted(matches, key=lambda v: v[-2])
    
    
def matches_allowed_patterns(pattern, nl):
    length=len(pattern)
    if nl:
        # for longer patterns the probability of high c compunds increase
        # therefore:
        allowed=[(range(length))]
        min_=(length-1)/2
        if min_>=2:
            _additional=range(-1, length-1)
            allowed.append(_additional)
    else:
        allowed=[range(-length+1, 1)]
        min_=(length-1)/2 
        if min_: # min length >=3 !!
            min_=2 if min_>2 else min_
            _additional=range(-length+min_+1, min_+1)
            allowed.append(_additional)
    return allowed
        

def build_isotopologue_dict(mz, mztol, is_nl):
    delta=emzed.mass.C13-emzed.mass.C 
    d=defaultdict(dict)
    mi_range=range(-4, 5)
    z_range=range(1, 4)
    _add_values(mz, delta, mi_range, z_range, mztol, d)
    return d


def _add_values(mz_ref,  delta, mi_range, z_range, mztol, d):
    for z in z_range:
        d[z]=defaultdict(list)
        for mi in mi_range:
            mz=mz_ref + mi*delta/z
            keys=calculate_keys((mz,), (mztol,))
            for k in keys:
                d[z][k].append((mz, z, mi))    
        
        
################################################################################################
def label_isotopologue_artefacts(t, rttol, mztol=0.0009, id_col='fid'):
    """ Function that removes features which can be explained by isotopologue
        differences others than carbon. Mainly fixes feature_regrouper bug for 
        O16->O18
    """
    t.updateColumn('id_', t.id, type_=int)
    excluded={}
    iso2diff=_get_isotopologue_diffs()
    key2tol={'rt': rttol}
    lookup=cl.table2lookup(t, key2tol)
    # source_key must be set to id to obtain grouping by rttol only !!
    c=cl.build_consensus_table_from_lookup(lookup, average_cols=[], source_key='id',
                                                    id_cols=None)
    c.updateColumn('exclude', c.apply(get_isotopologue_id, 
                    (c.id_, c.mz, c.z, c.area, mztol, iso2diff, excluded)), 
                    type_=dict, format_=None)
    d={key:_get_info(*excluded[key]) for key in excluded.keys()}
    t= update_column_by_dict(t, 'non_carbon_isotopologue', 'id', d, type_=str)
    t.dropColumns('id_')
    return regrouped_ids(t, excluded, id_col) 
    
    
def _get_isotopologue_diffs():
    mass=emzed.mass
    dO18=mass.O18 -mass.O
    dN15=mass.N15 - mass.N
    return {'O18' : dO18, 'dN15': dN15, }


def get_isotopologue_id(ids, mzs, zs, areas, mztol, isotop2diff, excluded):
    if len(ids)>1:
        pairs=zip(ids, mzs, zs, areas)
        pairs.sort(key=lambda v: v[1])
        max_delta_isotop=max(isotop2diff.values())
        n_cols=_get_max_i(mzs, zs, max_delta_isotop)
        for i in range(1, n_cols+1):
            for p1, p2 in zip(pairs, pairs[i:]):
                for isotope, mzdiff in isotop2diff.items():
                    diff=p2[1]-p1[1]
                    # for checked isotopologues we expect that the abundance of 
                    # isotopologues O18 and N15 is significantly smaller than the those
                    # than correspondin O16 and N14 isotopologue peaks (lower mz value -> p1)
                    # therefore:
                    area_ratio=p1[-1]/p2[-1]
                    z_s=[p1[-2]]  if p1[-2]>0 else [1,2,3]
                    #○ BAUSTELLE CHECK THIS LINE
                    if any([abs(diff*z-mzdiff)<=mztol and area_ratio >2 for z  in z_s]):
                        excluded[p2[0]]=(p1[0], p2[0], isotope, 'id')
        return excluded


def _get_max_i(mzs, zs, max_delta):
    values=_get_masses(mzs, zs)
    values.sort()
    i=1
    while True:
        min_delta=_get_min_delta(values, i)
        if min_delta >= max_delta:
            return i
        i+=1
        if i>= len(values):
            return i
          
          
def _get_masses(mzs, zs):
    """ helper function to estimate the mass of corresponding mz value. THe idea is only to 
        determine a limit for zipping
    """
    def fun(z):
        return z if z else 1
    zs=[fun(z) for z in zs]
    return [a*b for a, b in zip(mzs, zs)]


def _get_min_delta(values, i):
    x=np.array(values[:len(values)-i])
    y=np.array(values[i:])
    return min(y-x)


def _get_info(p1, p2, key, id_col):
    start='_'.join([id_col, str(p1)])
    end='_'.join([id_col, str(p2)])
    group='-->'.join([start, end])
    return ': '.join([key, group])
        
    
def regrouped_ids(t, excluded, id_col):
    id2fid=dict(zip(t.id, t.getColumn(id_col)))
    fid2z=dict(zip(t.getColumn(id_col), t.z_))
    fid2ids=defaultdict(set)
    for id_, fid in zip(t.id, t.getColumn(id_col)):
        fid2ids[fid].add(id_)
    # key of excluded represents grouped by non C isotopologue
    # value v[0] and v[1] represent grouping and grouped peak
    # all keys of excluded are grouped peaks
    for grouped in excluded.keys():
        # grouped fid:
        old_fid=id2fid[grouped]    
        # get all ids of old fid
        ids=fid2ids[old_fid]
        grouping=excluded[grouped][0]
        new_fid=id2fid[grouping]
        for id_ in ids:
            id2fid[id_]=new_fid
            fid2ids[new_fid]=fid2ids[new_fid].union(fid2ids[old_fid])
    t = update_column_by_dict(t, 'feature_id', 'id', id2fid, type_=int)
    t.updateColumn('z', t.z_, type_=int, insertAfter='z')
    return update_column_by_dict(t, 'z', 'feature_id', fid2z, type_=int)

##################################################################################################
    
def check_groups_by_feature_plausability(t, id_col):
    add_representing_mz(t, id_col=id_col, value_col='area')
    t.updateColumn('_min_mz', t.mz.min.group_by(t.getColumn(id_col)), type_=float)
    t.updateColumn('_max_mz', t.mz.max.group_by(t.getColumn(id_col)), type_=float)
    t.updateColumn('critical', t.apply(_select_critical,(t._min_mz, t._max_mz, t.mz_rep, t.is_nl)))
    t.dropColumns('_min_mz', '_max_mz')
    keeps=[t.filter(t.critical==False)]
    critical=t.filter(t.critical==True)
    if len(critical):
        emzed.gui.showInformation('check whether the feature_grouping is correct. In case of'\
        ' wrong grouping you can split features by selecting a value from the column fid for all'\
        'peaks that belong to a different group')
        features =critical.splitBy(id_col)
        for f in features:
                # ul peaks:
            if not f.is_nl.uniqueValue():    
                ul_check=[]
                for mz, mz_rep, iso in zip(f.mz, f.mz_rep, f.non_carbon_isotopologue):
                    if mz>mz_rep:
                        ul_check.append(isinstance(iso, str))
                ul_check=all(ul_check)
            else:
                ul_check=False
            if not ul_check:    
                emzed.gui.inspect(f)
                _remove_isotope_label(f)
            keeps.append(f)
    t=emzed.utils.stackTables(keeps)
    t.dropColumns('critical', 'fid', 'z_')
    sf.check_z(t, id_col)    
    # after splitting representing mz hast to be updated
    add_representing_mz(t, 'feature_id')
    # manual inspection might lead to feature_ids with  more than 1 mz_rep
    return t
            

def _select_critical(min_mz, max_mz, mz_rep, is_nl, ):
    if is_nl:
        return abs(min_mz-mz_rep)>1e-8
    return  abs(max_mz-mz_rep)>1e-8

    
def _remove_isotope_label(f):
    id2fid=dict(zip(f.id, f.feature_id))    
    f.replaceColumn('non_carbon_isotopologue', 
                    f.apply(_read_label,(f.non_carbon_isotopologue, id2fid)), type_=str)
    

def _read_label(label, id2fid):
    fields=label.split('_')
    grouping=int(fields[1].split('-->')[0])
    grouped=int(fields[-1])
    return label if  id2fid[grouped]==id2fid[grouping] else None
    
        
def add_representing_mz(t, id_col='fid', value_col='area'):
    expr=t.getColumn
    t.addColumn('max_', expr(value_col).max.group_by(expr(id_col)), type_=float)
    t.updateColumn('mz_rep', (expr(value_col)==t.max_).thenElse(t.mz, 0.0), type_=float, 
                   format_='%.5f', insertAfter='mz')
    t.replaceColumn('mz_rep', t.mz_rep.max.group_by(expr(id_col)), type_=float)
    t.dropColumns('max_')    
    
###################################################################################################
# inverstigation function:
    
def data_reduction_by_feature_grouping(nl, ul, kwargs, mi_min=2, mi_max=40, mztol=0.001, id_col='feature_id', 
                         remove_unmatched=True):
    rttol=sf.get_typical_fwhm(nl)/2
    lookup_nl=build_idms_istopologue_dict(nl, mi_min=mi_min, mi_max=mi_max, mztol=mztol, rttol=rttol)
    lookup_ul=build_idms_istopologue_dict(ul, mi_min=mi_min, mi_max=mi_max, mztol=mztol, 
                                          rttol=rttol, map_nl=False)
    groups_nl=get_feature_groups(lookup_nl, ul, mztol, rttol)
    groups_ul=get_feature_groups(lookup_ul, nl, mztol, rttol)
    t_nl=regroup_features(nl, groups_nl)
    t_nl=label_isotopologue_artefacts(t_nl, rttol)
    text='z assigned by feature_grouping'
    sf.charge_assign_event(t_nl, text)
    t_ul=regroup_features(ul, groups_ul)
    t_ul=label_isotopologue_artefacts(t_ul, rttol)
    sf.charge_assign_event(t_ul, text)
    print 'Done.'
    print 
    if remove_unmatched:
        t_nl=t_nl.filter(t_nl.z_.isNotNone())
        t_ul=t_ul.filter(t_ul.z_.isNotNone())
    return t_nl, t_ul                        