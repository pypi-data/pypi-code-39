# -*- coding: utf-8 -*-
"""
Created on Tue May 12 12:10:37 2015

@author: pkiefer
"""
import os, glob, sys
import emzed
import in_out as _io
import _multiprocess
#from workflow_toolbox import table_operations as top
import checks_and_settings as _checks
import numpy as np
from time import time
from integrate_smoothed_emg import emg_smoothed

##################################################################################################
def remove_files_from_dir(dir_, type_='*.*', remove_dir=True):
    path=os.path.join(dir_,type_)    
    pathes=glob.glob(path)
    if len(pathes):
        for p in pathes:
            os.remove(p)
    if remove_dir:
        os.rmdir(dir_)


#################################################################################################
def integrate_tables(tables, integratorid='max'):
    integrate=emzed.utils.integrate
    # since multiprocessing is applied n_cpus of integrator must be set to 1
    params={'n_cpus': 1, 'integratorid':'max'}
    return _multiprocess.main_parallel(integrate, tables, kwargs=params)

#################################################################################################
def enhanced_integrate(t, step=1, fwhm=None, max_dev_percent=20, min_area=100, mslevel=1, 
                        n_cpus=None):
    """
    Function 
    enhanced_integrate(t, step=1, fwhm=None, max_dev_percent=20, min_area=100, mslevel=1, 
                        n_cpus=None)
    requires only 1 eic peak per row !; common postfix for all colnames!
    performs emg_exact based peak integration for integration intervals step*fwhm, 0.5/step*fwhm 
    and 2*step*fwhm. if columns fwhm not in table fwhm can be provided and must be float > 0.
    Alternatively, fwhm is calculated as rtmax-rtmin.
    emg_exact integration is accepted if peak area difference between both integration < max_dev_percent
    All peak areas below min_area will be set to None.
    """
    
    assert step>0, 'enhanced integrate requires step >0 !'
    initial_colnames=[n for n in t.getColNames()]
    _prepare_table(t, fwhm)
    max_=max_dev_percent    
    emg1=_special_integrate(t, a=1*step, mslevel=mslevel, n_cpus=n_cpus, max_dev_percent=max_)
    emg2=_special_integrate(t, a=2*step, mslevel=mslevel, n_cpus=n_cpus, max_dev_percent=max_)
    emg3=_special_integrate(t, a=0.5/step, mslevel=mslevel, n_cpus=n_cpus, max_dev_percent=max_)
    emg=merge_tables([emg1, emg2, emg3])
    pstfx=_get_postfix(emg)
    condition=(emg.getColumn('area'+pstfx)>=min_area)&(emg.getColumn('method'+pstfx)=='emg_exact')
    emg=emg.filter(condition)
    score_peaks(emg, max_/100.0)
    selected=select_peaks(emg)
    fids=list(set(t.getColumn('_id'+pstfx).values)-set(selected.getColumn('_id'+pstfx).values))
    remaining=t.filter(t.getColumn('_id'+pstfx).isIn(fids))
    if len(remaining):
        remaining=gauss_integrate(remaining, mslevel=mslevel, n_cpus=n_cpus)
        excluded=get_excluded(t, remaining, min_area, pstfx)
        remaining=remaining.filter(remaining.getColumn('area'+pstfx)>=min_area)
        merged=merge_tables([selected, remaining, excluded])
        _sort(merged, pstfx)
        _cleanup(t, initial_colnames)
        return merged
    _cleanup(t, initial_colnames)
    _sort(selected, pstfx)
    return selected
    
def _prepare_table(t, fwhm):
    _checks.is_integratable_table(t)
    exp=t.getColumn
    pstfx=_get_postfix(t)
    t.addColumn('_id'+pstfx, range(len(t)), type_=int)
    if not t.hasColumn('rt'+pstfx):
            t._addColumnWithoutNameCheck('rt'+pstfx, (exp('rtmin'+pstfx) + exp('rtmax'+pstfx))/2.0, 
                        type_=float)
    if not fwhm:
        if not t.hasColumn('fwhm'+pstfx):
            t._addColumnWithoutNameCheck('fwhm'+pstfx, (exp('rtmax'+pstfx)-exp('rtmin'+pstfx)), 
                        type_=float, insertBefore='rtmin'+pstfx)
    else:
        t._updateColumnWithoutNameCheck('fwhm'+pstfx, fwhm)

   
def _cleanup(t, colnames):
    drop=[n for n in t.getColNames() if n not in colnames]
    t.dropColumns(*drop) 

        
def calc_skewness(params):
    h,z,w,s=params
    l=1/s
    return abs(1-2.0/(w**3 * l**3)*(1+1/(w**2 * l**2))**(-3.0/2))

def area_score(a, min_, max_, max_dev):
    if a<=(1+max_dev)*min_:
        return 0.6
    elif (1+max_dev)*min_<a<(1-max_dev)*max_:
        return 0.3
    else:
        return 0.0

def asymmetry_score(f, min_, max_):
    if abs(f-min_)<1e-6:
        return 0.4
    elif (max_-f)>1e-2:
        return 0.2
    return 0.0
        

def score_peaks(t, max_dev):
    exp=t.getColumn
    pstfx=_get_postfix(t)
    t.addColumn('min_area', exp('area'+pstfx).min.group_by(exp('_id'+pstfx)), type_=float)
    t.addColumn('max_area', exp('area'+pstfx).max.group_by(exp('_id'+pstfx)), type_=float)
    t.addColumn('area_score', 
                t.apply(area_score,(exp('area'+pstfx), t.min_area, t.max_area, max_dev)), 
                type_=float)
    t._updateColumnWithoutNameCheck('asym'+pstfx, exp('params'+pstfx).apply(calc_skewness), type_=float)
    t.addColumn('min_asym', exp('asym'+pstfx).min.group_by(exp('_id'+pstfx)), type_=float)
    t.addColumn('max_asym', exp('asym'+pstfx).max.group_by(exp('_id'+pstfx)), type_=float)
    t.addColumn('asym_score', t.apply(asymmetry_score, (exp('asym'+pstfx), t.min_asym, t.max_asym)), 
                type_=float)
    t._updateColumnWithoutNameCheck('score'+pstfx, t.asym_score + t.area_score, type_=float)
    drop_cols=['min_area', 'max_area', 'min_asym', 'max_asym', 'area_score', 'asym_score']
    t.dropColumns(*drop_cols)

def get_excluded(t, emg, min_area, pstfx):
    excluded=emg.filter(emg.getColumn('area'+pstfx)<min_area)
    ids=excluded.getColumn('_id'+pstfx).values
    excluded=t.filter(t.getColumn('_id'+pstfx).isIn(ids))
    return emzed.utils.integrate(excluded, 'no_integration')
    
    
    
def select_peaks(t):
    pstfx=_get_postfix(t)
    selected=t.copy()
    exp=selected.getColumn
    selected.updateColumn('select', exp('score'+pstfx).max.group_by(exp('_id'+pstfx)), type_=float)
    selected=selected.filter(exp('score'+pstfx)==selected.select)
    t.dropColumns('select')
    return _check_for_double_peaks(selected, pstfx)


def _check_for_double_peaks(t, pstfx):
    t=t.copy()
    doubles=len(t)-len(set(t.getColumn('_id'+pstfx).values))
    if doubles:
        t=_filter_grouped_by(t, 'area'+pstfx, '_id'+pstfx, float)
        doubles=len(t)-len(set(t.getColumn('_id'+pstfx).values))
        if doubles:
            t=_filter_grouped_by(t, 'asym'+pstfx, '_id'+pstfx, float)
            doubles=len(t)-len(set(t.getColumn('_id'+pstfx).values))
            if doubles:
                peaks=t.splitBy('_id'+pstfx)
                for peak in peaks:
                   max_=len(peak)
                   for i in range(1, max_)[::-1]:
                       peak.rows.pop(i)
                t=merge_tables(peaks)                                                    
    return t
                           
                           
def _filter_grouped_by(t, colname, id_col, type_):
    t.addColumn('temp', t.getColumn(colname).min.group_by(t.getColumn(id_col)), type_=type_)
    t=t.filter(t.getColumn(colname)==t.temp)    
    t.dropColumns('temp')
    return t
    
        
def _special_integrate(t, a=1, mslevel=1, n_cpus=None, max_dev_percent=20):
    t1=t.copy()
    exp=t1.getColumn
    pstfx=_get_postfix(t1)
    t1.replaceColumn('rtmin'+pstfx, exp('rt'+pstfx)-a*exp('fwhm'+pstfx), 
                     type_=float, format_="'%.2fm' %(o/60.0)")
    t1.replaceColumn('rtmax'+pstfx, exp('rt'+pstfx)+a*exp('fwhm'+pstfx), 
                     type_=float, format_="'%.2fm' %(o/60.0)") 
    if not n_cpus:
        n_cpus=get_n_cpus(t1)
#    t1 = emzed.utils.integrate(t1, 'emg_exact', n_cpus=n_cpus, msLevel=mslevel)
    return emg_smoothed(t1, n_cpus=n_cpus, max_diff_percent=max_dev_percent, mslevel=mslevel,
                        id_col='_id')
    return t1    


def gauss_integrate(t, times_sigma=1.96, mslevel=1, n_cpus=None):
    """ gauss integration on 95% quantile 
    """
    t1=t.copy()
    pstfx=_get_postfix(t1)
    exp=t1.getColumn
    t1.replaceColumn('rtmin'+pstfx, exp('rt'+pstfx)-times_sigma*exp('fwhm'+pstfx), 
                     type_=float, format_="'%.2fm' %(o/60.0)")
    t1.replaceColumn('rtmax'+pstfx, exp('rt'+pstfx)+times_sigma*exp('fwhm'+pstfx), 
                     type_=float, format_="'%.2fm' %(o/60.0)")
    if not n_cpus:
        n_cpus=get_n_cpus(t)
    return emzed.utils.integrate(t1, 'trapez', n_cpus=n_cpus, msLevel=mslevel)
    

def get_n_cpus(t, max_cpus=4):
   from multiprocessing import cpu_count
   n_cpus=cpu_count()-1 if cpu_count()>1 else cpu_count()
   if n_cpus>max_cpus:
       n_cpus=max_cpus
   estimated=int(np.ceil(np.log((len(t)+1)/500.0 )))
   if estimated<=n_cpus:
       return estimated if estimated>1 else 1
   return n_cpus 


def _get_postfix(t):
    required=['rtmin', 'rtmax', 'mzmin', 'mzmax', 'peakmap']
    postfix=t.supportedPostfixes(required)
    assert len(postfix)==1, 'Function accepts only one integreatable'\
                            ' peak per row not %d.' %len(postfix)
    return postfix.pop()
    
def merge_tables(tables):
    try:
        return emzed.utils.stackTables(tables)
    except:
        return emzed.utils.mergeTables(tables, force_merge=True)

def _sort(t, pstfx):
    t.sortBy('_id'+pstfx)
    t.dropColumns('_id'+pstfx)
    

########################################################
# caching of intermediate workfkow results

def cache_result(fun, params, path, foldername= 'cache'):
    """cache_function_result(fun, path, params) creates  subfolder `cache` in path and 
       saves funtion output in folder. Function arguments params must be list or tuple  with 
       parameter values or a dictionary with function argument keywords  as keys. 
       Inplace operations are not cached
    """
    cache_dir=_get_cache_dir(path, foldername)
    target=_get_cache_path(fun, params, cache_dir)
    if os.path.exists(target):
        return _io.load_pickled_item(target)
    else:
        if isinstance(params, list) or isinstance(params, tuple):
            result=fun(*params)
        elif isinstance(params, dict):
            result=fun(**params)
        else:
            assert False, 'Function arguments params must be list or'\
            ' tuple, or dictionary with argument names as keyy and not %s' %type(params)
        if result is not None: # not an inplace operation
           _io.save_item_as_pickle(result, target)
           return result
           
def _get_cache_dir(path, foldername='cache'):
    cache_dir=os.path.join(path, foldername)
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)
    return cache_dir
               
      
def _get_cache_path(fun, params, cache_dir):
    name='_'.join([fun.func_name, _hash_params(params)])
    name= '.'.join( [name, 'pickled'])
    return os.path.join(cache_dir, name)


def _hash_params(params):
    return str(hash(str(params)))


def remove_cache(path, foldername='cache'):
    """ remove_cache(path) removes subfolder foldername (`cache` by default) and its content in 
    directory specified in argument `path`.
    """
    cache_dir=_get_cache_dir(path, foldername)
    from glob  import glob   
    targets=glob(os.path.join(cache_dir, '*.*'))
    [os.remove(target) for target in targets]
    os.rmdir(cache_dir)
    
#################################################################################################
# determine fwhm
def determine_typical_fwhm(peakmap, mslevel):
    params=_checks.default_ffmetabo_config()
    params['common_noise_threshold_int']
    # BAUSTELLE
    
##############################################################################################
def compare_peaks(t1, t2, mztol=0.003, rttol=5.0, keep_t1=False):
    """ returns a joined table containing peaks present in t1 and t2 based on rt and mz values. 
    If keep_t1=True, all peaks of t1 are kept and only those present in t2 and t1 are kept for t2
    """
    required=['mz', 'rt']
    assert t1.hasColumns(*required), 'columns are missing'
    assert t2.hasColumns(*required), 'columns are missing'
    tables=[]
    t1.sortBy('mz')
    t2.sortBy('mz')
    subtables=_split_table(t1, 1000)
    for sub_1  in subtables:
        try:
            sub_2=t2.filter(t2.mz.inRange(sub_1.mz.min()-mztol, sub_1.mz.max()+mztol))
        except:
            sub_2=t2
        expr=sub_1.mz.equals(sub_2.mz, abs_tol=mztol) & sub_1.rt.equals(sub_2.rt, abs_tol=rttol)
        if keep_t1:
            res=sub_1.leftJoin(sub_2, expr)
        else:
            res=sub_1.join(sub_2, expr)
        if len(res):
            tables.append(res)
    return emzed.utils.stackTables(tables) if len(tables) else [] 

def _split_table(t, length):
    if length>len(t):
        return [t]
    blocks=len(t)/length
    subtables=[]
    for i in range(1, blocks+1):
        start=(i-1)*length
        stop=i*length
        subtables.append(t[start:stop])
    if blocks*length<len(t):
        subtables.append(t[blocks*length:])
    return subtables
    
##################################################################################
    
def process_time(fun, args=None, kwargs=None, in_place=False):
    """ returns process time of function fun with parameters params. if in_place_== True no value 
        will be returned
    """
    args=[] if not args else args
    kwargs= {} if not kwargs else kwargs
    start=time()
    if in_place:
        
        fun(*args, **kwargs)
    else:
        res= fun(*args, **kwargs)
    stop=time()
    print 'runtime of function %s: %ds'%(fun.func_name, stop-start)
    if not in_place:
        return res
    
        
def show_progress_bar(iterable, fun, args=None, kwargs=None, in_place=False, bar_len=20):
    """ shows progress bar while processing iterable items with function fun. if in_place_== True no value 
        will be returned
    """
    
    args=[] if not args else args
    kwargs={} if not kwargs else kwargs
    results=[]
    count=1
    total=len(iterable)
    step=int(round(float(total) / bar_len))
    if step == 0:
        step=int(round(float(bar_len)/total))
    for item in iterable:
        if in_place:
            fun(item, *args, **kwargs)
        else:
            results.append(fun(item, *args, **kwargs))
        if total > bar_len:
            if (float(count)/step)==int(count/step):
                _progress(count, total, bar_len)
        else:
            _progress(count, total, bar_len)
        count+=1
    return None if in_place else results

def _progress(count, total, bar_len=20):
    fraction=int(round(bar_len*count/float(total)))
    bar = '#' * fraction + ' '*(bar_len - fraction)
    sys.stdout.write('>%s<\r' %bar)
    sys.stdout.flush()
    
        
#############################################################################################
# 
def fast_isIn_filter(t, value_col, values, not_in=False):
    t=t.copy()
    d={v:v for v in values}
    def is_in(key, d, not_in=not_in):
        if not_in:
            return not d.has_key(key)
        return d.has_key(key)
    t.updateColumn('is_in_temp', t.apply(is_in,(t.getColumn(value_col), d)), type_=bool)
    t=t.filter(t.is_in_temp==True)
    t.dropColumns('is_in_temp')
    return t
        
def perform_loop(fun, elements):
    return [fun(e) for e in elements]
    
        
    
