# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 15:06:22 2018

@author: pkiefer
"""
from wtbox.collect_and_lookup import calculate_keys
import emzed
import shared_functions as sf
from collections import defaultdict
from evaluate_idms_features import get_final_idms_features, final_evaluate


def build_idms_pair_table(nl, ul, kwargs, mztol=0.0009, mi_min=1, mi_max=40):
    # steps
    # reduce to representing peaks
    nl=extract_representing_peaks(nl)
    ul=extract_representing_peaks(ul)
    # match representing peaks -> idms_groups
    t_idms=match_representing_peaks(nl, ul, mztol, mi_min, mi_max)
    # select idms pairs
    t_idms=get_final_idms_features(t_idms)
    t_idms=final_evaluate(t_idms)
    edit_table(t_idms)
    return t_idms
    


#############################################################
def extract_representing_peaks(t):
    return t.filter(t.mz.approxEqual(t.mz_rep, 1e-5)==True )


def match_representing_peaks(nl, ul, mztol, mi_min=2, mi_max=30, mzcol='mz_rep'):
    
    nl=nl.filter(nl.getColumn(mzcol).approxEqual(nl.mz, 1e-5)) # to avoid rounding problems
    ul=ul.filter(ul.getColumn(mzcol).approxEqual(ul.mz, 1e-5)) # to avoid rounding problems
    rttol=sf.get_typical_fwhm(nl)
    lookup=build_idms_istopologue_dict(nl, mi_min=mi_min, mi_max=mi_max, mztol=mztol, rttol=rttol)
    nl.addColumn('idms_id', nl.apply(lambda v: tuple([v]), (nl.id,)), type_=tuple)
    ul.addColumn('idms_id', ul.apply(lookup_u13c,(lookup, ul.getColumn(mzcol), ul.rt, ul.z, ul.fwhm,
                                                  mztol, rttol)), type_=tuple)
    return emzed.utils.stackTables([nl, ul])    

def build_idms_istopologue_dict(t, mi_min=2, mi_max=40, mztol=0.001, rttol=5):
    d=defaultdict(list)
    delta=emzed.mass.C13-emzed.mass.C
    for mz0, z, rt, fwhm, id_ in zip(t.mz_rep, t.z, t.rt, t.fwhm, t.id):
        z_range=range(z, z+1) if z else range(1, 4)
        mi_range=range(mi_min, mi_max+1)
        _add_values_to_dict(mz0, rt, fwhm, id_, delta, mi_range, z_range, mztol, rttol, d)
    return d


def _add_values_to_dict(mz_ref, rt, fwhm, id_, delta, mi_range, z_range, mztol, rttol, d):
    for z in z_range:
        for mi in mi_range:
            mz=mz_ref+mi*delta/z
            keys=calculate_keys((mz,rt), (mztol, rttol))
            for k in keys:
                d[k].append((mz, z, rt, fwhm, id_))
    return d


def lookup_u13c(lookup_dict, mz, rt, z, fwhm, mztol, rttol):
    """ bin by rt; 
        extract representing nl. (m/z, z);
        calculate allowed isotopologues 
        extract representing ul pair (mz/z)
    """
    keys=calculate_keys((mz,rt), (mztol, rttol))
    values=[]
    [values.extend(lookup_dict[k]) for k in keys]
    return _readout(values, mz, rt, z, mztol, fwhm)    


def _readout(values, mz, rt, z, mztol, fwhm):
    ids=[]
    for mz_, z_, rt_, fwhm_, id_ in set(values):
        tol=min(fwhm, fwhm_)
        req1=abs(mz-mz_)<=mztol
        # this paramerter is very critical in positive mode with narrow peaks!!
        # we choose fwhm /2 wich allows more false positive for larger peaks. 
        req2=abs(rt-rt_)<=tol/2.0
#        req3= z==z_ or (z==0 or z_==0)
#        if all([req1, req2, req3]):
        if all([req1, req2]):    
            ids.append(id_)
    return tuple(ids)

##################################################################################################                                         

def edit_table(t):
    t.dropColumns('fid_ref', 'idms_id')