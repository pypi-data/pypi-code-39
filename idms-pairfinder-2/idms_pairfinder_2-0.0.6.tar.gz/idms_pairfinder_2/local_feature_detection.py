# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 17:36:13 2018

@author: pkiefer
"""
import emzed
import wtbox
from wtbox import collect_and_lookup as cl
from shared_functions import  determine_pm_noise_and_baseline, filter_min_specs, savitzky_golay
import shared_functions as sf
import numpy as np
import _local_ff_remove_multiple as rm_multi
from itertools import product
from collections import Counter
################################################################################################

def local_ff_detect(t, kwargs, signal_to_noise=1.0, show_progress=True, mztol=0.003):
    ff_config=kwargs['ff_config']
    min_specs=kwargs['min_specs']
    pm=t.peakmap.uniqueValue()
    baseline, noise=determine_pm_noise_and_baseline(pm)#*signal_to_noise
    threshold=baseline + signal_to_noise*noise
    d={fid:rt for fid, rt in set(zip(t.feature_id, t.rt))}
    t=local_isotopologue_search(t, threshold,ff_config, mztol=mztol, show_progress=show_progress,
                                min_specs=min_specs)
    t=wtbox.table_operations.update_column_by_dict(t, 'rt', 'feature_id', d, type_=float)
    return t


def local_isotopologue_search(t, noise_level, ff_config, id_col='feature_id', min_specs=5, 
                              show_progress=True, mztol=0.003):
    max_id=t.id.max()                              
    counts=Counter(t.getColumn(id_col))
    t=wtbox.table_operations.update_column_by_dict(t, 'counts', id_col, counts, type_=int)
    keep=t.filter(t.counts>1)
    process=t.filter(t.counts==1)
    local_mzspace=_get_local_mz_space()
    enlarged=build_search_space(process, local_mzspace, max_id)
    enlarged=select_enlarged(enlarged, ff_config, noise_level, min_specs, show_info=True)
    enlarged=remove_multiple_peaks_by_enlargement(keep, enlarged, mztol)    
    text='z assigned by local isotopologue search'
    sf.charge_assign_event(enlarged, text)
    result=emzed.utils.stackTables([keep, enlarged])
    emzed.utils.recalculateMzPeaks(result)
    sf.check_z(result, id_col)
    result.dropColumns('counts')
    return result
    

def build_search_space(process, local_mzspace, max_id):
    tables=[]
    for delta_mz, z in local_mzspace:
        t=process.copy()
        ids=range(max_id+1, max_id+len(t)+1)
        t.replaceColumn('mz', t.mz+delta_mz, type_=float)
        t.replaceColumn('mzmin', t.mzmin+delta_mz, type_=float)
        t.replaceColumn('mzmax', t.mzmax+delta_mz, type_=float)
        t.replaceColumn('z', z, type_=int)
        t.replaceColumn('id', ids, type_=int)
        tables.append(t)
        max_id=t.id.max()
    enlarged=emzed.utils.stackTables(tables)
    # mz windos are centered around the mean spectral mz value ...
    _update_mz_windows(t)
    # check for double peaks due to enlargment -> the origin is mainly peaks that were not grouped
    enlarged=rm_multi.remove_multiple_peaks_by_enlargement(process, enlarged, mztol=0.002)
    enlarged=emzed.utils.stackTables([process, enlarged])        
    n_cpus=wtbox.utils.get_n_cpus(enlarged, 4)
    return emzed.utils.integrate(enlarged, 'max', n_cpus=n_cpus)


def _update_mz_windows(t):
    emzed.utils.recalculateMzPeaks(t)
    t.updateColumn('mzmin', t.mz-(t.mzmax-t.mzmin)/2, type_=float)
    t.updateColumn('mzmax', t.mz+(t.mzmax-t.mzmin)/2, type_=float)
    

def _get_local_mz_space():
    local_mzspace=list(product([-1.00335, 1.00335], range(1,4)))
    return [(v[0]/v[1], v[1]) for v in local_mzspace]
    

def select_enlarged(t, ff_config, noise_level, min_specs, show_info=True):
#    from develop_determine_trace_length import filter_min_specs
    # check for peaks fullfilling min intensity criterium
    t=filter_for_area_crit(t, noise_level)
#    assert len(set(removed)-set(t.id))==0
    # check for peaks with rt in expected rttol within feature
    t=check_rt_shift(t)
    t=filter_min_specs(t, ff_config, min_specs)
    t=remove_low_psl_peaks(t)
    features= t.splitBy('feature_id')
    [check_feature_charge_state(f) for f in features]
    return emzed.utils.stackTables(features)
        
    

def filter_for_area_crit(t, noise_level, signal_to_noise=1.0):
    t.updateColumn('areamax', t.area.max.group_by(t.feature_id), type_=float)
    def check_area(area, max_area, noise_level=noise_level, sn=signal_to_noise):
        threshold=noise_level*sn
        min_int=max_area*0.005
        min_int= noise_level if min_int<threshold else min_int
        return area>=min_int
    t.updateColumn('_keep', t.apply(check_area, (t.area, t.areamax)), type_=bool)
    t=t.filter(t._keep==True)
    t.dropColumns('areamax', '_keep')
    return t


def check_rt_shift(f):
    def _get_rt_shift(rt, params):
        rt_, __=max(zip(*params), key=lambda v: v[1])
        return abs(rt-rt_)
    f.updateColumn('rt_shift', f.apply(_get_rt_shift, (f.rt, f.params)), type_=float)
    f=f.filter(f.rt_shift<=f.fwhm/2)
    f.dropColumns('rt_shift')
    return f

  
def check_feature_charge_state(f, show_info=True):
    if len(f)>=2:
        if not _consistent_z(f):
            if show_info:    
                emzed.gui.showInformation('More than one possible charge state was detected. Please select'\
                ' the charge state manually by removing rows with higher charge state than selected')
            emzed.gui.inspect(f)
    if len(f)==1 and f.z.max()>0:
        print 'FEHLER'
        emzed.gui.inspect(f)
    f.replaceColumn('z', f.z.max(), type_=int)
    f.replaceColumn('rt', f.apply(_get_appex, (f.params, )), type_=float)
    

def _get_appex(params, winsize=11):
    rts, ints=params
    try:
        ints_sg=savitzky_golay(np.array(ints), winsize, 2)
    except:
        ints_sg=ints
    pairs=zip(rts, ints_sg)
    return max(pairs, key=lambda v: v[1])[0]


    
def _consistent_z(t):
    """ find the lowest charge state z in zs that explains grouped peaks
    """
    mzs=list(t.mz.values)
    zs=list(t.z.values)
    mzs=sorted(mzs)
    for z in sorted(zs):
        if z:
            deltas=(np.array(mzs[1:])-np.array(mzs[:len(mzs)-1]))*z
            def precision(v, mtol=0.01):
                return abs(int(round(v,2))-v)<=mtol
            if all([precision(v) for v in deltas]):
                t.updateColumn('z', z, type_=int)
                return True
    return False


def remove_multiple_peaks_by_enlargement(keep, enlarged, mztol=0.001):
    rttol=sf.get_typical_fwhm(keep)/2
    key2tol={'mz': mztol, 'rt' : rttol}
    
    # steps 1. build a lookup of enlarged
    lookup=cl.table2lookup(enlarged, key2tol)
    # step 2. find all feautures where peaks are already present in keep
    fids=_get_fids_with_common_peaks(keep, lookup, mztol)
    # remove features in enlarged where peaks are also present in keep
    enlarged=wtbox.utils.fast_isIn_filter(enlarged, 'feature_id', fids, True)
    return enlarged
    
        
    
    
    
def _get_fids_with_common_peaks(keep, lookup, mztol):
    fids=[]
    for ntuple in zip(keep.mz, keep.rt, keep.fwhm):
        fwhm=ntuple[2]
        # determine a peak specific rttolerance for detection
        tols=(mztol, fwhm/2)    
        for key in cl.calculate_keys(ntuple[:2], lookup['bin_tols']):
            fids.extend(readout_lookup(ntuple, key, lookup, tols))
    return fids

                    
def readout_lookup(ntuple, key, lookup, tols):
    fids=[]
    if lookup.has_key(key):
        for row in lookup[key]:
            key_tuple, colname2value=row
            if cl.fullfilled(ntuple, key_tuple, tols):
                fids.append(colname2value['feature_id'])
    return fids

#######################################################################################  


def remove_low_psl_peaks(t):
    t.updateColumn('id_', range(len(t)), type_=int)
    t.updateColumn('psl', t.apply(calc_psl, (t.params,)), type_=float)
    remove=[]
    t1=t.filter(t.psl<1)
    t1.addColumn('width', (t1.rtmax-t1.rtmin).apply(abs), type_=float) # if rtmin and rtmax <0 ....
    t1.replaceColumn('width', t1.width.apply(abs), type_=float)
    t1.replaceColumn('rtmin', t1.rtmin-0.2*t1.width, type_=float)
    t1.replaceColumn('rtmax', t1.rtmax+0.2*t1.width, type_=float)
    t1=emzed.utils.integrate(t1, n_cpus=1, showProgress=False)
    t1.addColumn('psl1', t1.apply(calc_psl, (t1.params,)), type_=float)
    t1=t1.filter(t1.psl1<=1)
    if len(t1):
        remove=t1.id_.values
    t=wtbox.utils.fast_isIn_filter(t, 'id_', remove, not_in=True)
    t.dropColumns('psl', 'id_')
    _check_z(t)
    return t


def _check_z(t):
    """
    if len of feature == 1 set z value to 0
    """
    d=Counter(t.feature_id.values)
    def _replace(fid, z, d):
        return z if d[fid]>1 else 0
    t.replaceColumn('z', t.apply(_replace, (t.feature_id, t.z, d)), type_=int)
    
        

def calc_psl(params, win_size=11):
    rts, ints=params
    try:
        ints_sg=savitzky_golay(np.array(ints), win_size, 2)
    except:
        ints_sg=ints
    return wtbox.feature_analysis.peak_significance_level(ints_sg)