# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 16:12:57 2018

@author: pkiefer
"""
import emzed
import wtbox
import numpy as np
from collections import defaultdict
from wtbox.collect_and_lookup import calculate_keys
import shared_functions as sf
#################################################################################################
# Main function: automatic and intaractive selection of idms_pairs
#
def get_final_idms_features(t):
    print 'building idms_id table'
    selected=[]
    idms_ids=set([])
    def fun_(v1, v2):
        return True if v1 in v2 else False
    for tuple_ in t.idms_id.values:
        idms_ids.update(tuple_)
    for id_ in idms_ids:
        print id_,
        t.updateColumn('select_', t.apply(fun_, (id_, t.idms_id)), type_=bool)
        sub=t.filter(t.select_==True)
        print 'filter done',
        sub.dropColumns('select_')
        sub.addColumn('idms_pid', id_, type_=int, insertBefore='feature_id')
        sub=auto_remove(sub)
        if len(sub)==2:
            selected.append(sub)
        elif len(sub)>2:
            emzed.gui.showInformation('remove wrong peak(s)')
            emzed.gui.inspect(sub)
            if len(sub)==2:
                selected.append(sub)
    x=emzed.utils.stackTables(selected)
    return _find_and_filter_multiple(x)
    
    

def _find_and_filter_multiple(t):
    d=defaultdict(list)
    remove=set([])
    for key, value in set(zip(t.feature_id, t.idms_pid)):
        d[key].append(value)
    doubles =[k for k in d.keys() if len(d[k])>1]
    first =True
    for double in doubles:
        check=_get_multiple(t, d, double)
        ids=set(check.idms_pid.values)
#        check=auto_select(check)
        if len(check)>2:
            if first:
              emzed.gui.showInformation('select the correct idms_pid by removing the wrong pairing')
              first=False
            emzed.gui.inspect(check)
        rem=set(check.idms_pid.values)
        remove.update(ids-rem)
    return t.filter(~t.idms_pid.isIn(remove))


def _get_multiple(t, d, double):
    dic={v:v for v in d[double]}
    def fun(key,d):
        return True if d.has_key(key) else False
    t.updateColumn('double', t.apply(fun, (t.idms_pid, dic)), type_=bool)
    t1=t.filter(t.double==True)
    t.dropColumns('double')
    t1.dropColumns('double')
    return t1

def auto_select(t):
    if len(t)>2:
        d=defaultdict(int)
        check=auto_remove(t)
        for id_ in check.idms_pid:
            d[id_]+=1
        def fun(key, d=d):
            return True if d.get(key)==2 else False
        check.addColumn('keep', check.apply(fun, (check.idms_pid,)), type_=bool)
        if len(set(check.id.values))==2:
            check=check.filter(check.keep==True)
        check.dropColumns('keep')
        return check
    return t
    

    
def auto_remove(t, mzdiff=0.001, id_col='id'):            
    """ removes m1 or mul-1 peaks that were not correctly grouped with m0 or mul
    """
    if len(t)>2:
        pairs=zip(t.mz.values, t.area.values)
        min_pair=min(pairs, key=lambda v: v[0])
        max_pair=max(pairs, key=lambda v: v[0])
        zs=[z for z  in t.z.values if z>0]
        zs=set(zs)-set([0])
        if len(zs)==1: 
            pass
        else:
            zs=range(1,4)
        tmin=_remove(t, min_pair, zs, mzdiff, id_col=id_col)
        return _remove(tmin, max_pair, zs, mzdiff, id_col=id_col, min_=False)
    return t
    

def _remove(t, pair, zs, mzdiff, scaling=3.0, id_col='feature_id', min_=True):
    delta_c13=emzed.mass.C13-emzed.mass.C
    mzs=[pair[0]+delta_c13/z for z  in zs] if min_ else [pair[0]-delta_c13/z for z  in zs]
    mzs.sort()
    key2mz=lookup_mz(mzs, mzdiff)
    t.addColumn('_remove', t.apply(_has_peak,(t.mz, key2mz, mzdiff)), type_=bool)
    t1=t.filter(t._remove==False)
    t.dropColumns('_remove')
    t1.dropColumns('_remove')
    return t1

def _has_peak(mz, key2mz, mztol):
    keys=calculate_keys((mz,), (mztol,))
    for key in keys:
        try:
            mz_=key2mz[key]
            diff=abs(mz_ -mz)
            return True if diff <= mztol else False
        except:
            pass
    return False

def lookup_mz(mzs, mztol):
    d={}
    for mz in mzs:
        for k in calculate_keys((mz,), (mztol,)):
            d[k]=mz
    return d
    
#############################################################################################

###################################################################################################
# main_function 2

def final_evaluate(t):
    t=verify_charge_state(t, min_z=1, max_z=4, id_col='idms_pid')
    sf.c13_count(t)
    t=classify_idms_pairs(t)
    return remove_unlikely_pairs(t)
    
    
    

#################################################################################################

def verify_charge_state(t, min_z=1, max_z=4, id_col='idms_pid'):
    update=wtbox.table_operations.update_column_by_dict
    _update_charge(t)
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
    t= update(t, 'z', 'idms_pid', id2charge, type_=int)
    t.replaceColumn('z', t.z.apply(int), type_=int)
    return t
   
   
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


def classify_idms_pairs(t):
    d=dict()
    pid2ratio={}
    for idms_pid, is_nl, area in zip(t.idms_pid, t.is_nl, t.area):
        if not d.has_key(idms_pid):
            d[idms_pid]={}
        if is_nl:
            d[idms_pid]['nl']=area 
        else:
            d[idms_pid]['ul']=area
    for idms_pid in d.keys():
        pid2ratio[idms_pid]= d[idms_pid]['nl']/d[idms_pid]['ul']
    t=wtbox.table_operations.update_column_by_dict(t, 'idms_ratio', 'idms_pid', pid2ratio, type_=float)
    lower=np.percentile(t.idms_ratio.values, 10)
    upper=np.percentile(t.idms_ratio.values, 90)
    t.updateColumn('critical_ratio', (t.idms_ratio.inRange(lower, upper).thenElse(False, True)),
                    insertBefore='id', type_=bool)
    return t


def remove_unlikely_pairs(t):
    # 1. num_c >1
    def _min(v):
        return min(v)>=2
    t.updateColumn('keep_', t.apply(_min, (t.num_c,)), type_=bool)
    # 2. 
    def _in_range(keep, ratio):
        return 0.1<=ratio<=10 if keep else keep
    t.updateColumn('keep_', t.apply(_in_range,(t.keep_, t.idms_ratio)), type_=bool)
    t=t.filter(t.keep_==True)
    t.dropColumns('keep_')
    return t
 