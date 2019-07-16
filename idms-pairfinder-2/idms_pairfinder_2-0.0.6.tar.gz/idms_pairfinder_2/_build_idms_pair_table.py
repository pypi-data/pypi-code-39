# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 10:36:33 2018

@author: pkiefer
"""

import emzed, wtbox
import numpy as np
import shared_function as sf
from collections import defaultdict
from wtbox.collect_and_lookup import calculate_keys

########################################################################################
# MAIN FUNCTION
###########################################################################################

def build_idms_table(nl, ul, mztol=0.0009, mi_min=2, mi_max=40):
    nl=sf.build_table_from_fid2values(nl)
    ul=sf.build_table_from_fid2values(ul)
    # take only peaks with mapped in references -> unmapped peaks will be removed
    nl=nl.filter(nl.total_score.isNotNone())
    ul=ul.filter(ul.total_score.isNotNone())
    idms_table=match_representing_peaks(nl, ul, mztol, mi_min, mi_max)
    idms_table=get_final_idms_features(idms_table)
    _update_charge(idms_table)
    idms_table=verify_charge_state(idms_table, min_z=1, max_z=4, id_col='idms_pid')
    temporary=['fid_ref', 'idms_id']
    idms_table.dropColumns(*temporary)
    return idms_table


def _update_charge(t):
    d=defaultdict(list)
    for id_, z in zip(t.idms_pid, t.z):
        d[id_].append(z)
    t.replaceColumn('z', t.apply(_update,(t.idms_pid, d)), type_=int, format_='%d')

    
def _update(id_, d):
    zs=d.get(id_)
    assert len(zs)==2, ' BUG: there is wrong pairing for idms_pid %d!!' %id_ 
    if min(zs)==0 and max(zs)>0:
        return max(zs)
    elif min(zs)==max(zs):
        return max(zs)
    else:
        return 0


def _update_fid(ul, fid):
    fid+=1
    def increase(fid, add=fid):
        return fid+add
    ul.updateColumn('feature_id', ul.apply(increase,(ul.feature_id, )), type_=int)


def match_representing_peaks(nl, ul, mztol, mi_min=2, mi_max=30, mzcol='mz_rep'):
    
    nl=nl.filter(nl.getColumn(mzcol).approxEqual(nl.mz, 1e-5)) # to avoid rounding problems
    print len(nl)
    ul=ul.filter(ul.getColumn(mzcol).approxEqual(ul.mz, 1e-5)) # to avoid rounding problems
    print len(ul)
    rttol=sf.get_typical_fwhm(nl)
    print rttol
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
        _add_values_to_dict(mz0, rt, fwhm, id_, delta, (mi_min, mi_max+1), z_range, mztol, rttol, d)
    return d


def _add_values_to_dict(mz_ref, rt, fwhm, id_, delta, mi_range, z_range, mztol, rttol, d):
    for z in z_range:
        for mi in range(*mi_range):
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

def verify_charge_state(t, min_z=1, max_z=4, id_col='idms_pid'):
    update=wtbox.table_operations.update_column_by_dict
    assert min_z>=1
    colnames=[id_col, 'mz', 'mzmin', 'mzmax', 'rt','rtmin', 'rtmax', 'fwhm', 'is_nl', 'z']
    new=_get_empty_subtable(t, colnames)
    ntuples=[t.getColumn(n) for n in colnames]
    ntuples.append( [1]*len(t))
    ntuples=zip(*ntuples)
    sol_space=np.ones((max_z-min_z+1, len(colnames)+1))
    rows=_build_z_space(ntuples, sol_space, min_z, max_z)
    new.rows=rows
    new.addColumn('peakmap', t.peakmap.uniqueValue(), type_=emzed.core.data_types.PeakMap)
    new.replaceColumn('rtmin', ((new.rt-new.fwhm/2)<0).thenElse(0.0, new.rt-new.fwhm/2), type_=float)
    new.replaceColumn('rtmax', new.rt+new.fwhm/2, type_=float)
    n_cpus=wtbox.utils.get_n_cpus(new)
    test=emzed.utils.integrate(new, 'max', n_cpus=n_cpus)
    id2charge = _verify_z(test, id_col)
    return  update(t, 'z', 'idms_pid', id2charge, type_=int)
    
    
    
def _get_empty_subtable(t, colnames):
    new=t.extractColumns(*colnames)
    new =new.buildEmptyClone()
    new.addColumn('z_', None, type_=int, format_='%d')
    return new


def _build_z_space(ntuples, sol_space, min_z, max_z):
    rows=[]
    delta=1.00335/np.arange(float(min_z),max_z+1.)
    for row in ntuples:
        ssp=row*sol_space
        ssp[:,-1]=range(1,5) # setting z values
        # update values mz, mzmin, mzmax
        for i in range(1,4):
            if row[-3]:
                ssp[:,i]+=delta
            else:
                ssp[:,i]-=delta
        rows.extend(ssp.tolist())
    return rows

    
def _verify_z(t, id_col):
    # introduce m0 for inspection only
    t.addColumn('max_isotope_area', t.area.max.group_by(t.getColumn(id_col), t.is_nl), type_=float)
    colnames=[id_col, 'area', 'max_isotope_area', 'z', 'z_', 'is_nl']
    expr=[t.getColumn(name) for name in colnames]    
    d=defaultdict(set)
    for id_, area, max_area, z, z_, is_nl in zip(*expr):
        if max_area==0:
            d[id_].add(z)
        elif area and area==max_area:
             if z>0:
                 d[id_].add(z_)
             else:
                 d[id_].add(z)
                 

    def _read_z(id_col, z, d):
        zs=d[id_col]
        if len(zs)==1 and z in zs:
            return False
        if len(zs-set([0]))==1 and z in zs:
            return False
        return True
    id2charge=dict(zip(t.getColumn(id_col), t.z))
    t.updateColumn('_verify', t.apply(_read_z, (t.getColumn(id_col), t.z, d)), type_=bool)
    check=t.filter(t._verify==True)
    check=_add_main_peaks(check, id_col)
    check=check.filter(check.area>0)
    consistent_mi(check, id_col, id2charge)
    return id2charge
    
    

def _add_main_peaks(t, id_col):
    t.updateColumn('min_', t.mz.min.group_by(t.getColumn(id_col)), type_=float)
    t.updateColumn('max_', t.mz.max.group_by(t.getColumn(id_col)), type_=float)
    sub=t.filter((t.mz==t.min_) | (t.mz==t.max_))
    t.dropColumns('min_', 'max_')
    def _replace(mz, mzmin, mzmax, z_, min_, max_):
        if mz==min_:
            delta= - 1.00335/z_
        if mz==max_:
            delta=1.00335/z_
        return mz+delta, mzmin+delta, mzmax+delta
    expr=(sub.mz, sub.mzmin, sub.mzmax, sub.z_, sub.min_, sub.max_)
    sub.updateColumn('temp', sub.apply(_replace, expr), type_=float)
    sub.replaceColumn('mz', sub.temp.apply(lambda v: v[0]), type_=float)
    sub.replaceColumn('mzmin', sub.temp.apply(lambda v: v[1]), type_=float)
    sub.replaceColumn('mzmax', sub.temp.apply(lambda v: v[2]), type_=float)
    sub.replaceColumn('z_', 0.0, type_=int)
    sub.dropColumns('min_', 'max_', 'temp')        
    sub=emzed.utils.integrate(sub, 'max', n_cpus=1)
    return emzed.utils.stackTables([sub, t])    


def consistent_mi(t, id_col, id2charge):
    m=1
    while len(t):
        print m
        t.updateColumn('max_z', t.z_.max.group_by(t.getColumn(id_col), t.is_nl), type_=int)
        t.updateColumn('min_', t.mz.min.group_by(t.getColumn(id_col)), type_=float)
        t.updateColumn('max_', t.mz.max.group_by(t.getColumn(id_col)), type_=float)
        t.updateColumn('mi', t.apply(_add_mi, (t.is_nl, t.mz, t.min_, t.max_, t.max_z)))
        t=_consistent_mi(t, id_col)
        corrected=t.filter(t.consistent_mi==True)
        id2charge.update(dict(zip(corrected.getColumn(id_col), corrected.max_z)))
        t=t.filter(t.consistent_mi==False)
        t.updateColumn('max_z', t.z_.max.group_by(t.getColumn(id_col)), type_=int)
        t=t.filter(t.z_<t.max_z)
        m+=1
    
    
    
def _add_mi(is_nl, mz, min_, max_, max_z):
    delta=1.00335
    if is_nl:
        mi_=round((mz-min_)*max_z/delta, 2)
    else:
        mi_=round((mz-max_)*max_z/delta, 2)
    return mi_
    
    
def _consistent_mi(t, id_col):
    d=defaultdict(list)
    id2z={}
    id2check={}
    for id_, mi, max_z, is_nl  in zip(t.getColumn(id_col), t.mi, t.max_z, t.is_nl):
        d[id_].append(mi)
        id2z[(id_, is_nl)]=max_z
    for key, values in d.items():
        id2check[key]=_compare_values(values, id2z, key)
    return wtbox.table_operations.update_column_by_dict(t, 'consistent_mi', 'idms_pid', 
                                                        id2check, bool)
    
def _compare_values(values, id2z, id_):
#    import pdb;pdb.set_trace()
    # same max_z for nl and ul
    if not id2z[(id_, True)]==id2z[(id_, False)]:
        return False
    pattern=_get_z2pattern()[id2z[(id_, True)]]
    values.sort()
    i=values.index(0)
    ul=values[:i+1]
    # since ul values are neg :
    ul=ul[::-1]
    checks=[]
    for i in range(len(ul)):
        try:
            checks.append(abs(pattern[i]+ul[i])<0.01)
        except:
            checks.append(False)
    nl=values[i+1:]
    for i in range(len(nl)):
        try:
            checks.append(abs(nl[i]-pattern[i])<0.01)
        except:
            checks.append(False)
    return all(checks)


def _get_z2pattern():
    d={0 : (0,),
       1 : (0, 1),
       2 : (0, 1, 2),
       3 : (0, 1, 3),
       4 : (0, 1, 2, 4)}
    return d
       
def remove_max_z(t):
    return t.filter(t.z<t.max_z)
##################################################################################################
def remove_isotope_pattern_splits(t, mztol=0.002):
    # separate nl and ul peaks
    # local workaround if z is of type float
    t.replaceColumn('z', t.z.apply(int), type_=int)
    
    nl=t.filter(t.is_nl==True)
    nl.sortBy('area', ascending=False)
    ul=t.filter(t.is_nl==False)
    ul.sortBy('area', ascending=False)
    iso_nl, rttol=build_isotopologue_dict(nl, mztol)
    tols=(mztol, rttol)
    _remove_pattern(nl, iso_nl, tols)
    iso_ul, rttol=build_isotopologue_dict(ul, mztol)
    tols=(mztol, rttol)
    _remove_pattern(ul, iso_ul, tols)
    t=emzed.utils.stackTables([nl, ul])
    return create_best_match(t)
    
    

def build_isotopologue_dict(t, mztol):
    delta=emzed.mass.C13-emzed.mass.C
    d=defaultdict(list)
    mi_range=range(-3, 0)
    mi_range.extend(range(1, 5))
    rttol=sf.get_typical_fwhm(t)
    for mz, z, rt, fwhm, id_ in zip(t.mz, t.z, t.rt, t.fwhm, t.idms_pid):
        z_range=range(z, z+1) if z else range(1, 5)
        _add_values_to_dict(mz, rt, fwhm, id_, delta, mi_range, z_range, mztol, rttol, d)
    return d, rttol  
    
    
def _remove_pattern(t, d, tols):
    id2ids={}
    for mz, rt, fwhm, z, id_ in zip(t.mz, t.rt, t.fwhm, t.z, t.idms_pid):
        ids= _find_matches(mz, rt, fwhm, z, d, tols)
        id2ids[id_]=ids
    def _is_in(key, d):
        if d.get(key):
            values=[key]
            values.extend(d.get(key))
            return values
    t.updateColumn('match_ids', t.apply(_is_in,(t.idms_pid, id2ids)), type_=tuple)
    
    

def _find_matches(mz, rt, fwhm, z, d, tols):
    keys=calculate_keys((mz,rt), tols)
    values=[]
    [values.extend(d[k]) for k in keys]
    mztol, __ =tols
    return _readout(values, mz, rt, z, mztol, fwhm)



def create_best_match(t):
    # during testing
#    import pdb; pdb.set_trace()
    t=t.copy()
    d=defaultdict(list)
    idms2idms=_get_idms2idms(t)
    # assign common idms_pid value to grouped idms_pairs
    def _assign(idms_pid, idms2idms):
        return idms2idms[idms_pid] if idms2idms.has_key(idms_pid) else idms_pid
    t.replaceColumn('idms_pid', t.apply(_assign, (t.idms_pid, idms2idms)), type_=int)
    idms_pids=idms2idms.values()
    t_=wtbox.utils.fast_isIn_filter(t, 'idms_pid', idms_pids)
    expr=[t_.getColumn(n) for n in ['idms_pid', 'id', 'is_nl', 'area']]    
    for idms_pid, id_, is_nl, area in zip(*expr):
        d[idms_pid, is_nl].append((id_, area))
    remove=[]
    for pairs in d.values():
        max_=max(pairs, key=lambda v: v[1])[0]
        remove.extend([pair[0] for pair in pairs if pair[0]!=max_])
    return wtbox.utils.fast_isIn_filter(t, 'id', remove, True)
    
    
def _get_idms2idms(t):
    idms_pairs=[sorted(v) for v in t.match_ids.values if v]
    d={}
    for pair in idms_pairs:
        value=pair[0]
        for key in pair[1:]:
            d[key]=value
    t.dropColumns('match_ids')
    return d