# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 14:07:05 2017

@author: pkiefer
"""
from wtbox.collect_and_lookup import compare_tables
#import wtbox.collect_and_lookup as cl
#from wtbox import table_operations as to
from wtbox.utils import fast_isIn_filter
import shared_functions as sf
#from collections import defaultdict



def remove_multiple_peaks(t, quantity_col='area', rttol=None, mztol=0.002):
    t1=t.copy()
    rttol=sf.get_typical_fwhm(t)/4.0
    key2tol={'mz': mztol, 'rt': rttol}
    comp=compare_tables(t1, t, key2tol=key2tol)
    comp.addColumn('keep', (comp.id==comp.id__0).thenElse(False, True), type_=bool)
    doubles=comp.filter(comp.keep==True)
    doubles.sortBy('area', ascending=False)
    # most intense peak is on top
    remove={}
    for id_, id_0 in zip(doubles.id, doubles.id__0):
        if not remove.has_key(id_):
#            keep[id_]=id_
            remove[id_0]=id_0
    return fast_isIn_filter(t, 'id', remove.keys(), True)
    


def remove_multiple_peaks_by_enlargement(t, result, rttol=None,  mztol=0.001):
    # t is the table prior to enlargement, result is the table after enlargement
    # multiple peaks by enlargment have a different id, but same mz and rt_values
    rttol=sf.get_typical_fwhm(t)/4.0
    key2tol={'mz': mztol, 'rt': rttol}
    ids=t.id.values
    new=fast_isIn_filter(result, 'id', ids, not_in=True)
    comp=compare_tables(t, new, key2tol=key2tol, leftJoin=False)
    multiples=comp.id__0.values
    return fast_isIn_filter(result, 'id', multiples, not_in=True)
    





def _remove_multiple_peaks(t, id_col='feature_id', key2tol=None, quantity_col='area'):
    t=t.uniqueRows()
    t1=t.copy()
    t1.sortBy(id_col)
    if not key2tol:
        key2tol={'mz': 0.001, 'rt': 5.0}
    t1=compare_tables(t1,t, key2tol=key2tol)
    pstfx=_get_postfix(t1)
    id__0=''.join(['id', pstfx])
    id_col__0=''.join([id_col, pstfx])
    area__0=''.join([quantity_col, pstfx])
    doubles=set([])
    fid_pairs=set([])
    gc=t1.getColumn
    for id_, id_0, area, area_0, fid, fid_0 in zip(t1.id, gc(id__0), 
            gc(quantity_col), gc(area__0), gc(id_col), gc(id_col__0)):
        if id_ != id_0:
            pairs=sorted([(id_, area), (id_0, area_0)], key=lambda v: v[0])
            remove=min(pairs, key=lambda v: v[1])[0]
            doubles.add(remove)
            fid_pairs.add(tuple(sorted([fid, fid_0])))
    t=fast_isIn_filter(t, 'id', doubles, not_in=True)
    _fuse_fids(t, fid_pairs)
    fid2z=_get_fid2z(t, id_col)
    t.updateColumn('z', t.apply(_update_charge,(t.feature_id, fid2z)), type_=int)
    return t

def _get_postfix(t):
    pstfx=str(t.maxPostfix())
    return ''.join(['__', pstfx])

def _collect_ids(d):
    selected=set([])
    [selected.update(set_) for set_ in d.values()]        
    return selected        

def _get_fid2z(t, id_col):
    fid2z=defaultdict(list)
    for fid, z in zip(t.getColumn(id_col), t.z):
        fid2z[fid].append(z)
    for fid in fid2z.keys():
        if len(fid2z[fid])>1:
            fid2z[fid]=max(fid2z[fid])
        else:
            fid2z[fid]=0
    return fid2z


def _fuse_fids(t, fid_pairs):
    d={fid1: fid2 for fid1, fid2  in fid_pairs}
    def _replace(fid, d=d):
        return d[fid] if d.has_key(fid) else fid
    t.replaceColumn('feature_id', t.apply(_replace, (t.feature_id,)), type_=int, format_='%d')

def _update_charge(fid, fid2z):
    return fid2z[fid]    

#
#import emzed
#import numpy as np
#def remove_multiple_peaks_ff_metabo(t, mztol=0.003, quan_col='area'):
#    selected=[]
#    id2checked={}
##    t1=t.copy()
#    key2tol={'mz': mztol}
#    lookup=cl.table2lookup(t, key2tol)
#    for id_, mz, quan in zip(t.id, t.mz, t.getColumn(quan_col)):
#        if not id2checked.get(id_):
#            grouped=cl.read_out_table((mz,), lookup)
#            while len(grouped):
#                select=apply_similar_rules(grouped)
#                _update_id2checked(id2checked, select)
#                select=select_major_peak(select)
#                selected.append(select)
#                grouped=fast_isIn_filter(grouped, 'id', id2checked.keys(), not_in=True)
#            
#    return emzed.utils.stackTables(selected)
#
#
#def _update_id2checked(d, t):
#    for id_ in t.id.values:
#        d[id_]=id_
#
#
#def apply_similar_rules(t):
##   import pdb; pdb.set_trace()
#   ref_values=max(zip(t.rtmin, t.rtmax, t.fwhm, t.params, t.area), key=lambda v: v[-1])[:-1]
#   rtmin, rtmax, fwhm, params =ref_values                             
#   limits=rtmin-fwhm/2, rtmax+fwhm/2              
#   t.updateColumn('overlap', t.apply(_filter_similar, (t.rtmin, t.rtmax, limits)), type_=bool)
#   t=t.filter(t.overlap==True)
#   t.updateColumn('similar', t.apply(rule_out, (t.params, params)), type_=bool)
#   # remove peaks <
#   t=t.filter(t.similar==True)
#   t.dropColumns('overlap', 'similar')
#   return t
#
#def _filter_similar(rtmin, rtmax, limits):
#    lower, upper=limits
#    return lower <=rtmin<=upper or lower<=rtmax<=upper
#
#def rule_out(params, ref_params):
##    import pdb; pdb.set_trace()
#    shared=shared_spectra(params, ref_params)
#    ref_area=np.trapz(ref_params[1], x=ref_params[0])
#    area=np.trapz(params[1], x=params[0])
#    area_shared=np.trapz(shared[1], x=shared[0])
#    #☺ rule 1: major peak area orginates from ref
#    if 0.5*ref_area<=area_shared:
##        print 'rule 1'
#        return True
#    #@ rule 2: total area < 0.5% of ref_area
#    if 0.005*ref_area>=area:
##        print 'rule 2'
#        return True
#    #- rule_3: max of peak in ref_peak
#    appex=max(zip(*params), key=lambda v: v[1])[0]
#    rtmin=min(ref_params[0])
#    rtmax=max(ref_params[0])
##    print 'rule 3 %s' %(rtmin<=appex<=rtmax) 
#    return True if rtmin<=appex<=rtmax else False
#
#
#def shared_spectra(params, ref):
#    rts, intensities=params
#    ref_rts, ref_intensities=ref
#    ref_rts=_rounded(ref_rts)
#    rts=_rounded(rts)
#    common_rts=set(ref_rts).intersection(set(rts))
#    common_rts=sorted(list(common_rts))
#    rt2rt={v:v for v in common_rts}
#    common_ints=[int_ for rt, int_ in zip(rts, intensities) if rt2rt.has_key(rt)]
#    return  common_rts, common_ints
#
#def _rounded(values):
#    return [round(v,5) for v in values]
#
#
#def select_major_peak(t):
#    return t.filter(t.area==t.area.max())