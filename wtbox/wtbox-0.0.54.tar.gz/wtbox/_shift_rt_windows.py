# -*- coding: utf-8 -*-
"""
Created on Mon Oct 09 11:59:41 2017

@author: pkiefer

Comments and to do:
    
1) Comments

2) to do:
    - missing peaks lead to minimal error this will cause 
"""
import numpy as np
import emzed
import utils
from copy import copy
from collections import defaultdict
import wtbox 


def shift_rt_windows(pm, ref, id_col='feature_id', delta_rt=20.0, multiprocess=True):
    """
    """
    'print find peaks that might overlap within time window ...'
    id2overlaps, uniques=find_overlapping_peaks(ref, delta_rt, id_col)
    print 'finished.'
    t=enlarge_window(pm, ref, delta_rt)
    # find overlapping peaks
    # split tables into unique and overlapping peaks
    single, merged=separate_overlapping_from_unique(t, uniques, id_col)
    single_ref, merged_ref=separate_overlapping_from_unique(ref, uniques, id_col)
    # process unique peaks
    id_col2drt=get_id2drt(single, single_ref, delta_rt, id_col, multiprocess=multiprocess)
    # process overlapping peaks
    id_col2drt_=get_id2rt_from_overlapping(merged, merged_ref, id2overlaps, id_col, delta_rt)
    id_col2drt.update(id_col2drt_)
    reset_enlarge_window(t, delta_rt)
    return shift_rtwindow(t, id_col2drt, id_col)

######
# step 1
def find_overlapping_peaks(ref, delta_rt, id_col='feature_id'):
    # determine mztol from average mz window width
    if ref.hasColumn('id'):
        ref.renameColumn('id', 'id_')
    ref.addEnumeration()
    mztol=sum(np.array(ref.mzmax)-np.array(ref.mzmin))/len(ref)
    t=ref.copy()
    t.replaceColumn('rtmin', t.rtmin-delta_rt, type_=float)
    t.replaceColumn('rtmax', t.rtmax+delta_rt, type_=float)
    
    comp=wtbox.collect_and_lookup.compare_tables(ref, t, ('mz',), {'mz':mztol}, False)
    comp.updateColumn('overlap', comp.apply(_select,(comp.id, comp.id__0, comp.rtmin, comp.rtmax, 
                                                     comp.rtmin__0, comp.rtmax__0)), type_=bool)
    overlaps=defaultdict(set)
    not_unique=set([])
    id_0='__'.join([id_col, '0'])
    for id1, id2, overlap in zip(comp.getColumn(id_col), comp.getColumn(id_0), comp.overlap):
        if overlap:
            ids=sorted([id1, id2])
            overlaps[min(ids)].update(set(ids))
            not_unique.update(set(ids))
    _merge_overlaps(overlaps)  
    uniques=set(t.getColumn(id_col).values)-not_unique
    ref.dropColumns('id')
    if ref.hasColumn('id_'):
        ref.renameColumn('id_', 'id')
    return overlaps, uniques


def _select(id1, id2, rtmin1, rtmax1, rtmin2, rtmax2):
    if id1!=id2:
        lower=max(rtmin1, rtmin2)
        upper=min(rtmax1, rtmax2)
        return lower<=upper
    return False


def _merge_overlaps(d):
    keys=sorted(d.keys())
    while len(keys):
        key=keys.pop(0)
        if d.has_key(key):
            collect_keys(d, key)


def collect_keys(d, key):
    """ 
    Graph like Function to collect elements of a path where all connected values are assigned to starting 
    value 'key';  d=defaultdict(set). d[key] contains a 
    set of values. For all values that are also keys of d, d[key] is collected and 
    checked whether they are keys until only non key values remain.
    """
    processed_keys=set([key])
    keys=copy(d[key])-processed_keys
    while len(keys):
        key_=keys.pop()
        processed_keys.add(key_)
        d[key].add(key_)
        if d.has_key(key_):
            values=d.pop(key_)
            keys.update(values)


#####################################
# step 2
def enlarge_window(pm, ref, delta_rt):
    t=ref.copy()
    # to stay in the rtRange of the peakmap:
    rtrange=pm.rtRange()
    t.title=pm.meta['source']
    t.replaceColumn('peakmap', pm, type_=emzed.core.data_types.PeakMap)
    t.updateColumn('source', pm.meta['source'], type_=str)
    t.updateColumn('_limits', t.apply(_get_drt, (rtrange, t.rtmin, t.rtmax)), type_=float)
    t.replaceColumn('rtmin', 
       t.apply(_enlarge_window,(t._limits, delta_rt, t.rtmin, None), keep_nones=True), type_=float)
    t.replaceColumn('rtmax',
       t.apply(_enlarge_window,(t._limits, delta_rt, None, t.rtmax), keep_nones=True), type_=float)
    t.dropColumns('_limits')
    return t


def _get_drt(rtrange, rtmin, rtmax):
    # stay in rt range of peakmap
    min_, max_=rtrange
    lower=rtmin-min_
    upper=max_-rtmax
    limits=tuple([lower, upper])
    return limits
#    return drt if drt<=limit else limit

def _enlarge_window(limits, delta_rt, rtmin, rtmax):
    limit=min(limits)
    index=limits.index(limit)
    drt=limit if limit <delta_rt else delta_rt
    if index:
        if rtmax!=None:
            return rtmax+drt
        if rtmin!=None:
            drt=max([abs(drt), delta_rt])
            return rtmin-drt
    if rtmax!=None:
        drt=max([abs(drt), delta_rt])
        return rtmax+drt
    return rtmin-drt
    
def reset_enlarge_window(t, delta_rt):
    if t.hasColumn('rt'):
        t.replaceColumn('rt', t.rt-delta_rt, type_=float)
    t.replaceColumn('rtmin', t.rtmin+delta_rt, type_=float)
    t.replaceColumn('rtmax', t.rtmax-delta_rt, type_=float)
    
##########################################################
# step 3: split tables in overlapping and none-overlapping peaks

def separate_overlapping_from_unique(t, uniques, id_col):
    unique=wtbox.utils.fast_isIn_filter(t,  id_col, uniques)
    overlapping=wtbox.utils.fast_isIn_filter(t, id_col,  uniques, not_in=True)
    return unique, overlapping


################################################################################
# step 4: determine rt shift id-wise

def get_id2drt(t, ref, window_size, id_col='feature_id', id2rtmins=None, multiprocess=True):
    if not id2rtmins:
        id2rtmins=defaultdict(list)
    t, ref=_fastest_integration(t, ref, multiprocess)
    id2ref=_get_dominating_peak(ref, id_col)
    id2t=_get_dominating_peak(t, id_col)
    keys=id2ref.keys()
    id2drt={}
    for key in keys:
        rtmins=[]
        if id2rtmins.has_key(key):
            rtmins=id2rtmins[key]
        elif id2ref[key]  is not None:
            rtmins=[min(id2ref[key][0])]
        if len(rtmins):
            id2drt[key]=_determine_rt_shift(id2t[key], id2ref[key], window_size, rtmins)
        else:
            id2drt[key]=0.0
    return id2drt

def _fastest_integration(t, ref, multiprocess):
    ref_cpus=utils.get_n_cpus(ref)
    t_cpus=utils.get_n_cpus(t)
    if t_cpus+ref_cpus<=3 or not multiprocess:
        return [emzed.utils.integrate(v, 'trapez') for v in [t, ref]]
    else:
        n_cpus=utils.get_n_cpus(t)
        t=emzed.utils.integrate(t, 'trapez', n_cpus=n_cpus)
        n_cpus=utils.get_n_cpus(ref)
        ref=emzed.utils.integrate(ref, 'trapez', n_cpus=n_cpus)
        return t, ref

def _get_dominating_peak(t, id_col='feature_id'):
    d={}
    for sub in t.splitBy(id_col):
        d[sub.getColumn(id_col).uniqueValue()]=_max_peak(sub.params.values, sub.area.values)
    return d
        

def _max_peak(params, area):
    return max(zip(params, area), key=lambda v: v[1])[0]
    
    
def _determine_rt_shift(params, ref_params, window_size, rtmins):
    ref_rts, ref_ints=ref_params
    rts, ints=params
    limits=get_limits(ref_rts, rtmins)
    ref_rts, ref_norm=normalize_intensities(ref_params, ref_rts, limits)
    norm_ints=build_norm_ints_array(params, window_size, ref_rts, limits)
    norm_ints=np.nan_to_num(norm_ints) # replaces numpy nan by zero values
    # if the peak was not detected keep the original peak parameters:
    if np.sum(norm_ints)==0:
        return 0.0
    deltas=((norm_ints-ref_norm)**2).dot(np.ones(np.size(ref_ints)))
    # since rows of norm_ints corrspond to rts, the min delta corrsponds
    # to the best starting point of rts
    rtmin=min(zip(rts, deltas), key=lambda v: v[1])[0]
    #since rts was enlarged by window_size
    delta_rt=rtmin-min(ref_rts) # or: min(rts)+winsize whih equals min(ref_rts)
    return float(delta_rt)


def build_norm_ints_array(params, window_size, ref_rts, limits):
    """ the rows correspond to the rt vector, the columns to ref_rts
    """
    ints_array=[]
    rts, __=params
    rt_range=np.argmin((2*window_size- rts+min(rts))**2)
    for i in range(rt_range):
        params_=(params[0][i:], params[1][i:])
        rts_, norm_=normalize_intensities(params_, ref_rts, limits)
        ints_array.append(norm_)
    return ints_array
        
        
def normalize_intensities(params, ref_rts, limits):
    rts, ints=synchronize_params(params, ref_rts)
    norm_areas=[]
    for low,  high  in limits:
        area=[np.trapz(ints[low:high], rts[low:high])]*(high-low)
        # to avoid zero division:
        if sum(area)==0:
            area=[1.0]*(high-low)
        norm_areas.extend(area)
    return rts, ints/np.array(norm_areas)
    
    
def get_limits(ref_rts, rtmins):
    bounds=[]
    bounds.extend(rtmins)
    bounds.append(max(ref_rts)) 
    bounds.sort()
    bounds=np.searchsorted(ref_rts, bounds)
    bounds[-1]+=1 # since last value has to be included
    return zip(bounds, bounds[1:])    
    

def synchronize_params(params, ref_rts):
    rts, ints=params
    ref_rts= _build_ref_rts(ref_rts, min(rts))
    size=(len(ref_rts),len(rts))
    dims=np.ones(size)
    squared_error=(dims*rts-np.transpose(np.transpose(dims)*ref_rts))**2
    # determine the positions of minimal distance along the short axis
    pos = np.argmin(squared_error, axis=1)
    return np.take(rts, pos), np.take(ints, pos)
#    return np.take(rts, pos)


def _build_ref_rts(rts, rtmin):
    return rts-min(rts)+rtmin    

###############################################
# 
#####################################
# special processing for overlapping peaks

def get_id2rt_from_overlapping(t, ref, id2overlaps, id_col, delta_rt):
    ref=_integrate_ref(ref)
    id2rtmins=get_id2rtmins(ref, id2overlaps, id_col)
    merged=merge_overlapping_peaks(t, id2overlaps, id_col)
    merged_ref=merge_overlapping_peaks(ref, id2overlaps, id_col)
    id2drt=get_id2drt(merged, merged_ref, delta_rt, id_col, id2rtmins)
    return _get_id2rt_from_overlapping(id2drt, id2overlaps)


def _integrate_ref(t):
    try:
        wtbox.checks_and_settings.is_integrated_table(t)
        return t
    except:
        return emzed.utils.integrate(t, 'trapez')
        

def get_id2rtmins(t, overlaps, id_col, select_col='area'):
    d={}
    id2rtmins=defaultdict(list)
    t.updateColumn('max_area', t.getColumn(select_col).max.group_by(t.getColumn(id_col)), 
                   type_=float)
    columns=zip(t.getColumn(id_col), t.rtmin, t.getColumn(select_col), t.max_area)
    for id_, rtmin, area, max_area in columns:
        if area==max_area:
            d[id_]=rtmin
    for key in overlaps.keys():
        for id_ in overlaps[key]:
            id2rtmins[key].append(d[id_])
    return id2rtmins


def merge_overlapping_peaks(t, overlaps, id_col, select_col='area'):
    t.updateColumn('max_area', t.getColumn(select_col).max.group_by(t.getColumn(id_col)), 
                   type_=float)
    columns=zip(t.getColumn(id_col), t.area, t.max_area, t.rtmin, t.rtmax)
    id2pairs={}
    id2rtmin_rtmax=defaultdict(list)
    for id_, area, max_area, rtmin, rtmax in columns:
        if area==max_area:
            id2pairs[id_]=(rtmin, rtmax)
    for key in overlaps.keys():
        for id_ in overlaps[key]:
            id2rtmin_rtmax[key].append(id2pairs[id_])
    selected=wtbox.utils.fast_isIn_filter(t, id_col, overlaps.keys())
    selected.updateColumn('rtmin', selected.apply(min_max, (selected.getColumn(id_col), 
                                                 id2rtmin_rtmax, False)), type_=float)
    selected.updateColumn('rtmax', selected.apply(min_max, (selected.getColumn(id_col), 
                                                         id2rtmin_rtmax)), type_=float)
    return selected


def min_max(id_, id2pairs, max_=True):
    i=1 if max_ else 0
    def _filter(pairs, i=i):
        values=[p[i] for p in pairs]
        return max(values) if i else min(values)
    return _filter(id2pairs[id_]) 


def _get_id2rt_from_overlapping(id2drt, id2overlaps):
    id2rtshift={}
    for id_ in id2drt.keys():
        delta_rt=id2drt[id_]
        keys=id2overlaps[id_]
        for key in keys:
            id2rtshift[key]=delta_rt
    return id2rtshift
    
    
    
############################################
# step 6 final processing

def shift_rtwindow(t, id_col2drt, id_col):
    id_=t.getColumn
    t.replaceColumn('rtmin', t.apply(_update_, (id_(id_col), id_col2drt, t.rtmin)), type_=float)
    t.replaceColumn('rtmax', t.apply(_update_, (id_(id_col), id_col2drt, t.rtmax)), type_=float)
    if t.hasColumn('rt'):
        t.replaceColumn('rt', t.apply(_update_, (id_(id_col), id_col2drt, t.rt)), type_=float)
    return t


def _update_(key, d, rt):
    delta_rt=d.get(key)
    return rt+delta_rt if delta_rt else rt
    
##############################################################################################


# test
def quicky(t, winsize=60.0):
    PeakMap=emzed.core.data_types.PeakMap
    pms=wtbox.in_out.load_peakmaps(startAt=r'Z:\pkiefer\temp\hartlj\idms_untargeted')
    'peakmaps loaded.'
    ref_params=t.params.values[0]
    rtmins=[t.rtmin.values[-1]]
    results=[]
    for pm in pms:
        check=t.copy()
        check.replaceColumn('peakmap', pm, type_=PeakMap)
        check.replaceColumn('rtmin', check.rtmin-winsize, type_=float)
        check.replaceColumn('rtmax', check.rtmax+winsize, type_=float)
        check=emzed.utils.integrate(check)
        params=check.params.values[0]
        delta_rt=calculate_delta_rt(params, ref_params, winsize, rtmins)
        check=t.copy()
        check.replaceColumn('peakmap', pm, type_=PeakMap)
        check.replaceColumn('rtmin', check.rtmin+delta_rt, type_=float)
        check.replaceColumn('rtmax', check.rtmax+delta_rt, type_=float)
        check=emzed.utils.integrate(check)
        results.append(check)
    return results
        
    
    