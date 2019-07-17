# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 13:45:24 2017

@author: pkiefer
Algorithm:
1) idms sample defines the isotopologue features. Features will be detected with isotopologue
grouper and max_c_gap is set to maximal number of allowed carbon atoms for idms and set to 0 for
all other samples to include other common peaks of the tables


"""
import numpy as np
from hires import feature_regrouper
from _rt_align import rtAlign
import shared_functions as sf
import  wtbox.collect_and_lookup as cl


def rt_align_idms(tables, t_idms, kwargs, destination, max_c=30, idms_tables=False):
    # extract parameters
    max_rt_diff=kwargs['maxRtDifference']
    mz_pair_tol=kwargs['maxMzDifferencePairfinder']
    if idms_tables:
        ref=t_idms.extractColumns('mz', 'rt', 'peakmap')   
        [t.updateColumn('intensity', t.area, type_=float) for t in tables]
        samples=[prepare_alignment_table(t) for t in tables]
#        ref=None
    else:
        rttol=round(np.median(t_idms.fwhm.values))+0.001
        tols=(mz_pair_tol, max_rt_diff)
        ref=prepare_ref_table(t_idms, rttol, max_c)
        collection, mapping=build_ref_collection(ref, (mz_pair_tol, max_rt_diff))
        samples=[build_alignment_table(t, collection, mapping, tols) for t in tables]
    aligned=rt_align(samples, tables,  ref, kwargs, destination)
    aligned=_sort_aligned_by_tables(aligned, tables)
    # update rts of parameters since peaks were shifted by alignment 
    [update_rt_params(a) for a in aligned]
    return aligned


def prepare_ref_table(t, rttol, max_c):
    t=t.copy()
    colnames=[n for n in t.getColNames()]
    colnames.append('mz0')
    t=feature_regrouper(t, rt_tolerance=rttol, max_c_gap=max_c)
    t.replaceColumn('feature_id', t.isotope_cluster_id, type_=int)
    t.addColumn('mz0', t.mz.min.group_by(t.feature_id), type_=float)
    t.replaceColumn('rt', t.rt.median.group_by(t.feature_id), type_=float)
    t=get_top_n_peaks(t)
    return t.extractColumns(*colnames)

    
def get_top_n_peaks(t, percentile=50):
    t.addColumn('summed_int', t.intensity.sum.group_by(t.intensity))
    min_int=np.percentile(t.summed_int.values, percentile)
    t=t.filter(t.summed_int>min_int)
    t.dropColumns('summed_int') 
    return t


def build_ref_collection(t, tols):
    collection={}
    mapping={}
    for mz, rt, z, mz0 in zip(t.mz, t.rt, t.z, t.mz0):
        ntuple=(mz, rt)
        key=cl.calculate_key(ntuple, tols)
        # use only unique hits
        keys=cl.get_neighbour_keys(key)
        if not any([collection.has_key(k) for k in keys]):
            for k in keys:
                collection[k]=(mz, rt, z)
                mapping[k]=mz0
        else:
            for k in keys:
                try:
                    __=collection.pop(k)
                    __=mapping.pop(k)
                except:
                    pass
    return collection, mapping
        

def build_alignment_table(t, collection, mapping, tols):
    t=t.copy()
    t=get_top_n_peaks(t)
    rttol=round(np.median(t.fwhm.values))+0.001
    t=feature_regrouper(t, rt_tolerance=rttol, max_c_gap=0)
    t.replaceColumn('feature_id', t.isotope_cluster_id)    
    sf.add_representing_mz(t, id_col='feature_id', value_col='area')
    t=t.filter(t.mz.approxEqual(t.mz_rep, 0.0001))
    # since rtAlign excepts no columns origination from emzed.utils.integration
    # we remove those colummns after feature_regrouper 
    t=_remove_integration_columns(t)
    t.addColumn('key', t.apply(_calculate_key, (t.mz, t.rt, tols)), type_=tuple)
    t.addColumn('mz0', t.apply(read_out, (t.key, t.mz, t.rt, collection, mapping, tols)), 
                type_=float)
    selected=t.filter(t.mz0.isNotNone())
    selected.replaceColumn('mz', selected.mz0, type_=float)
    selected.dropColumns('key')
    return selected


def prepare_alignment_table(t):
    t.updateColumn('intensity', t.area, type_=float)
    t.updateColumn('quality', 0.1, type_=float)
    required=['id', 'feature_id', 'mz', 'mzmin', 'mzmax', 'rt', 'rtmin', 
              'rtmax', 'intensity', 'quality', 'fwhm', 'z', 'peakmap', 'source']
    t_align=t.extractColumns(*required)
    t.dropColumns('intensity', 'quality')
    return t_align
    

def _remove_integration_columns(t):
    colnames=set(t.getColNames())-set(('method', 'area', 'baseline', 'rmse', 'params'))
    return t.extractColumns(*colnames)
    
    
def _calculate_key(mz, rt, tols):
        return cl.calculate_key((mz, rt), tols)
        
        
def read_out(key, mz, rt, collection, mapping, tols):
        matches=[]
        mztol, rttol=tols
        for k in cl.get_neighbour_keys(key):
            if collection.has_key(k):
                mz_, rt_=collection[k][:2]
                expr=abs(mz-mz_)<=mztol and abs(rt-rt_)<=rttol
                if expr:
                    diff=sf.calc_nsse((mz, rt), (mz_, rt_))
                    matches.append((diff, mapping[k]))
        return min(matches, key=lambda v: v[0])[1] if len(matches) else None

                
def rt_align(samples, tables, ref, kwargs, destination):
    kwargs['destination']= destination
    aligned=rtAlign(samples, tables, refTable=ref, **kwargs)    
    return aligned


def _remove_integration(t):
    colnames=[n for n in t.getColNames() if n not in ('method', 'area', 'baseline', 'rmse', 'params')]
    t.meta['integrated']=(False, '\n')
    return t.extractColumns(*colnames)


def _sort_aligned_by_tables(aligned, tables):
    sources=[t.source.uniqueValue() for t in tables]
    source2index={t.source.uniqueValue():i for i,t in enumerate(aligned)}    
    ordered=[]
    for source in sources:
        i=source2index[source]
        ordered.append(aligned[i])
    return ordered


def update_rt_params(t):
    def _update(method, params, rt_):
        fun=int_method2replace_function(method)
        return fun(params, rt_)
    type_=t.getColType('params')
    format_=t.getColFormat('params')
    t.updateColumn('params', t.apply(_update,(t.method, t.params, t.rt)), type_=type_, 
                   format_=format_)

def _update_rts(params, rt):
    rts, ints=params
    pairs=zip(*params)
    rt_=max(pairs, key=lambda v: v[1])[0]
    delta=rt - rt_
    rts=rts+delta
    return (rts, ints)
    
    
def int_method2replace_function(method):
    d={}
    names=['std', 'max', 'trapez', 'trapez_with_baseline']
    for name in names:
        d[name]=_update_rts
    def fun_emg(params, rt):
        params[1]=rt
        return params
    def fun_asym_gauss(params, rt):
        params[-1]=rt
        return params
    d['emg']=fun_emg
    d['emg_with_baseline']=fun_emg
    d['asym_gauss']=fun_asym_gauss
    return d[method]
    
############################################################################
import math


def get_ref_table_and_max_rtdiff(idms_tables, mztol):
    min_hits=len(idms_tables)-1
    lookup=sf.collect_unique_peaks(idms_tables, mztol, only_labeled=False, id_col='feature_id')
    consensus=cl.build_consensus_table_from_lookup(lookup, min_hits=min_hits, weight_col='area', 
                                                  source_key='source', average_cols=[], id_cols=[])
    ref_table= _find_best_reference(consensus, idms_tables)
    max_rt_diff=_estimate_max_rt_diff(ref_table, consensus)
    return ref_table, max_rt_diff


def _find_best_reference(consensus, tables):
    d=_get_id_source2bool(consensus)
    selected=_select_unique_peaks(tables, d)
    source=_find_best_table_by_scoring(selected)
    pairs={t.source.uniqueValue(): t  for t in tables}
    return pairs[source]


def _get_id_source2bool(consensus):
    d={}
    for id_, sources in zip(consensus.id, consensus.source):
        for source in sources:
            d[(id_, source)]=True
    return d


def _select_unique_peaks(tables, d):
    def _select(id_, source, d):
        return d.get((id_, source))
    [t.updateColumn('keep', t.apply(_select, (t.id, t.source, d)), type_=bool) for t in tables]
    selected=[t.filter(t.keep==True) for t  in tables]
    [t.dropColumns('keep') for t in tables]
    return selected
  
  
def _find_best_table_by_scoring(selected, id_col='id'):
    res=emzed.utils.mergeTables(selected)
    res.addColumn('rtmean', res.rt.mean.group_by(res.getColumn(id_col)), type_=float)          
    res.addColumn('areamax', res.area.max.group_by(res.getColumn(id_col)), type_=float)
    # to avoid zero division
    res.updateColumn('areamax', (res.area.max==0).thenElse(1.0, res.areamax), type_=float)
    res.addColumn('rt_score', res.apply(_rt_score, (res.rt, res.rtmean)), type_=float)
    res.addColumn('rel_area', res.area/res.areamax, type_=float)
    res.addColumn('summed_rt_score', res.rt_score.sum.group_by(res.source), type_=float)
    res.addColumn('summed_rel_area', res.rel_area.sum.group_by(res.source), type_=float)
    res.addColumn('score', 0.7*res.summed_rt_score/len(res)+0.3*res.summed_rel_area/len(res), type_=float)
    pairs=list(set(zip(res.score, res.source)))
    source=max(pairs, key=lambda v: v[0])[1]
    return source

def _rt_score(v, mean):
    return 1- math.sqrt((v-mean)**2)/mean



def _estimate_max_rt_diff(ref_table, consensus):
    source=ref_table.source.uniqueValue()
    rtdiffs=[]
    for sources, rts in zip(consensus.source, consensus.rt):
        try:
            idx=sources.index(source)
            rtdiff=max([abs(rt-rts[idx]) for rt  in rts])
            rtdiffs.append(rtdiff)
        except:
            pass
    assert len(rtdiffs)>0, 'no common unique features found! Please check if idms_pair tables are'\
        ' fitting together!!!!'
    return np.percentile(rtdiffs, 90)





#####################################################################
def align_idms_pairfinder_result_tables(tables, kwargs, destination):
    align_tables=_build_align_tables(tables)
    kwargs['forceAlign']=True
    return rt_align(align_tables, tables, None, kwargs, destination)
    
    
def _build_align_tables(tables):
    align_tables=[]
    colnames=colnames=['id', 'feature_id', 'rt', 'rtmin', 'rtmax', 'fwhm', 'mz', 
                       'mzmin', 'mzmax', 'z', 'area', 'peakmap']
    for t in tables:
        t=t.extractColumns(*colnames)
        t.updateColumn('source', t.peakmap.values[0].meta['source'], type_=str)
        t.renameColumn('area', 'intensity')
        align_tables.append(t)
    return align_tables


import emzed
import os        
def save_aligned_tables(tables):
    for t in tables:
        path=t.meta['loaded_from']
        dir_, name=os.path.split(path)
        name, ending=name.split('.')
        name='_'.join([name, 'rt_aligned'])
        name='.'.join([name, ending])
        path=os.path.join(dir_, name)
        emzed.io.storeTable(t, path)
        
        