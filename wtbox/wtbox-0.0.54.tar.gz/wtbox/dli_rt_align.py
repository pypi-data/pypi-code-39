# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 15:41:33 2016

@author: pkiefer



"""
import emzed
import os
from collections import defaultdict
from scipy.interpolate import splrep, splev
from hires import feature_regrouper
from copy import deepcopy
import numpy as np
from pylab import plot
import pylab
import table_operations
import in_out
from _lowess import lowess
from _multiprocess import main_parallel



def dli_rt_align(peakmaps, pm_idms,  ff_metabo=None, destination=None, max_c_gap=30, params=None):
    ref, tables=get_alignment_tables(peakmaps, pm_idms, max_rt_diff=100.0, ff_metabo=ff_metabo, 
                         max_c_gap=max_c_gap)
    return default_rt_align(tables, ref, destination, params=params)
    
    

                     
def get_alignment_tables(peakmaps=None, pm_idms=None, max_rt_diff=100.0, ff_metabo=None, 
                         max_c_gap=30):
    if peakmaps is None:
        peakmaps=in_out.load_peakmaps()
    if not pm_idms:
        path=emzed.gui.askForSingleFile(caption='select idms sample', extensions=['mzML', 'mzXML'])
        pm_idms=emzed.io.loadPeakMap(path)
    # 1. get_peaks table from idms peakmap
    peaks, ref=get_idms_features(pm_idms, ff_metabo=ff_metabo, max_c_gap=max_c_gap)
    # 2. targeted extract_peaks from peakmaps
#    import pdb; pdb.set_trace()
    
    tables=extract_peaks_from_sample(peakmaps, peaks, max_rt_diff) 
    [reset_integration(t) for t in tables]
    tables=[collapse_table_to_monoisotopic(t) for t in tables]
    ref=collapse_table_to_monoisotopic(ref, group='feature_id')
    return ref, tables


def get_idms_features(pm, ff_metabo=None, max_c_gap=30):
    if isinstance(ff_metabo, dict):
        t=emzed.ff.runMetaboFeatureFinder(pm, **ff_metabo)
    else:
        t=emzed.ff.runMetaboFeatureFinder(pm)
    t.addColumn('area', t.intensity, type_=float)
    rttol=np.percentile(t.fwhm.values, 50)
#    t=t.filter((t.fwhm<=rttol))
    t=feature_regrouper(t,max_c_gap=max_c_gap, elements=('C',), min_abundance=0.01, 
                        rt_tolerance=rttol)    
    expr=((t.intensity>=np.percentile(t.intensity.values, 70)) & \
                    (t.quality>=np.percentile(t.quality.values, 50)))
    t=t.filter(((t.z>0) | expr))
    t=t.filter(t.fwhm<=np.percentile(t.fwhm.values, 50))
    return edit_table(t)

###
def edit_table(t):
    t.updateColumn('mz0', t.mz.min.group_by(t.isotope_cluster_id), type_=float)
    t=_remove_not_c13_isotopes(t)
    replace_value_by_weighted_mean(t, 'rt', 'area') 
    replace_value_by_weighted_mean(t, 'fwhm', 'area') 
    t.updateColumn('mi', t.apply(calc_mi,(t.mz0, t.mz, t.z)), type_=int, format_='%d')
    t.replaceColumn('feature_id', t.isotope_cluster_id, type_=int, format_='%d')
    t.replaceColumn('fwhm', t.fwhm.max, type_=float)
    # set all rtmin-rtmax to unique value this is necessary for max diff parameter
    t.replaceColumn('rtmax', t.rt + t.fwhm.max(), type_=float)  
    t.replaceColumn('rtmin', (t.rt-t.fwhm.max()>0).thenElse(t.rt-t.fwhm.max(), 0.0), type_=float)
    t.dropColumns('area')
    peaks=t.extractColumns('feature_id', 'mz0', 'mz', 'mzmin', 'mzmax', 'z', 'mi', 'rt', 
                            'rtmin', 'rtmax', 'fwhm' )
    peaks=update_isotopologues(peaks)
    return peaks, t

def _remove_not_c13_isotopes(t):
    t.updateColumn('select', ((t.mz==t.mz0)|t.carbon_isotope_shift.isNotNone()).thenElse(True, False))
    t_=t.filter(t.select==True)
    t.dropColumns('select')
    t_.dropColumns('select')
    return t_

def calc_mi(mz0, mz, z):
        return int(round((mz-mz0)*z,0))
    

def update_isotopologues(t):
    to_stack=[]
    for f in t.splitBy('feature_id'):
        if f.z.uniqueValue():
            sub=_update_isotopologues(f)
            to_stack.append(sub)
        else:
            to_stack.append(f)
    return emzed.utils.stackTables(to_stack)

def _update_isotopologues(f, mztol=0.001):
    delta=emzed.mass.C13-emzed.mass.C
    num_c=f.mi.max()
    fid=f.feature_id.uniqueValue()
    mi=range(num_c+1)
    z=f.z.uniqueValue()
    mz0=f.mz0.uniqueValue()
    t=emzed.utils.toTable('feature_id', [fid]*(num_c+1), type_=int)
    t.addColumn('mi', mi, type_=int)
    t.addColumn('mz0', mz0, type_=float, insertBefore='mi')
    t.addColumn('mz', mz0+(t.mi*delta)/z, type_=float, insertBefore='mi')
    t.addColumn('mzmin', t.mz-mztol, type_=float, insertBefore='mi')
    t.addColumn('mzmax', t.mz+mztol, type_=float, insertBefore='mi')
    t.addColumn('z', z, type_=float, insertBefore='mi')
    t.addColumn('rt', f.rt.median(), type_=float)
    t.addColumn('rtmin', t.rt-f.fwhm.median(), type_=float)
    t.addColumn('rtmax', t.rt+f.fwhm.median(), type_=float)
    t.addColumn('fwhm', f.fwhm.median(), type_=float)
    for name in f.getColNames():
        t.setColType(name, f.getColType(name))
        t.setColFormat(name, f.getColFormat(name))
    return t
###


def extract_peaks_from_sample(peakmaps, peaks, max_rt_diff=100):
    step=max_rt_diff/peaks.fwhm.uniqueValue() 
    args=[peaks]
    kwargs={'step': step, 'n_cpus':1}
    fun=wt.feature_extraction.targeted_peaks_ms
    tables=main_parallel(fun, peakmaps, args=args, kwargs=kwargs)
    edited=[]
    for t in tables:
#    t=(pm, peaks, step=step, n_cpus=None)
#        import pdb; pdb.set_trace()
        t=t.filter((t.area>=1e4)&(t.method=='emg_exact')) # remove all peaks not gaussian peaks
        set_rt_appex(t)
        t=replace_value_by_weighted_mean(t, 'rt', 'area') 
        t=replace_value_by_weighted_mean(t, 'fwhm', 'area')    
        edited.append(t)
#    t.addColumn('intensity', t.area, type_=float)
    return edited


def set_rt_appex(t):
    def replace(method, params):
        if method=='asym_gauss':
            return params[-1]
        elif method=='emg_exact' or method=='emg_exact_with_baseline':
            return params[1]
        elif method=='no_integration':
            return
        else:
            pairs=zip(*params)
            return max(pairs, key=lambda v: v[1])[0] # retruns rt of spec with max intensity
    t.replaceColumn('rt', t.apply(replace, (t.method, t.params)), type_=float)


def replace_value_by_weighted_mean(t, value_col, weight_col, group_col='feature_id'):
    t.addColumn('sum_', t.getColumn(weight_col).sum.group_by(t.getColumn(group_col)),
                 type_=float)
    t.addColumn('weight', t.getColumn(weight_col)/t.sum_, type_=float)
    tuples=zip(t.getColumn(group_col), t.getColumn(value_col), t.weight)
    t.dropColumns('sum_', 'weight')
    key2value=defaultdict(float)
    for fid, value, weight in tuples:
        key2value[fid]+=value*weight
    t=table_operations.update_column_by_dict(t, value_col, group_col, key2value)
    return t
    
    

def collapse_table_to_monoisotopic(t_, group='feature_id'):
    t=t_.copy()
    t.updateColumn('intensity', t.intensity.sum.group_by(t.getColumn(group)), type_=float)
#    t.replaceColumn('area', t.intensity, type_=float)
#    t.dropColumns('sum_')
    t.updateColumn('_diff', t.mz-t.mz0, type_=float)
    t.updateColumn('_select', t._diff.min.group_by(t.getColumn(group)), type_=float)
    reduced=t.filter(t._diff==t._select)
    reduced.replaceColumn('mz', reduced.mz-reduced._diff, type_=float)
    reduced.replaceColumn('mzmin', reduced.mzmin-reduced._diff, type_=float)
    reduced.replaceColumn('mzmax', reduced.mzmax-reduced._diff, type_=float)
    reduced.dropColumns('_diff', '_select')
    return reduced


def reset_integration(t, group='feature_id'):
    integration_columns = ("method", "area", "params", "rmse")
    t.updateColumn('intensity', t.area, type_=float)
    t.dropColumns(*integration_columns)
    
##########################################################

def rt_align_lowess(tables, t_ref, destination, max_diff=100.0):
    aligned=[]
    for t in tables:
#        import pdb; pdb.set_trace()
        fid2area, fid2rt=summarize_features(t)
        __,  ref_fid2rt=summarize_features(t_ref)
        rts, drts, weights=get_diff_pair(fid2rt, fid2area, ref_fid2rt, max_diff=max_diff)
        fit = lowess_spline_interpolation(rts,drts)
        fit_range=min(rts), max(rts)
#        return fit
        path=_get_path(destination, t)
        plot_and_save_fit(rts, drts, fit, path)
        pm_aligned=transform(t, fit, fit_range)
        aligned.append(pm_aligned)    
    return aligned

def summarize_features(t):
    fid2area=defaultdict(float)
    fid2rt_=defaultdict(list)
    fid2rt=defaultdict(float)
    tuples=zip(t.feature_id, t.intensity, t.rt)
    for fid, area, rt in tuples:
        fid2area[fid]+=area
        fid2rt_[fid].append((rt, area))
    # rt of each isotopologue ion is weighted by area fraction of mid:
    for key in fid2rt_.keys():
        pairs=fid2rt_[key]
        fid2rt[key]=sum([p[0]/fid2area[key]*p[1] for p in pairs])
    return fid2area, fid2rt


def get_diff_pair(fid2rt, fid2area, ref_fid2rt, max_diff):
    rts=[]
    drts=[]
    weights=[]
    total_area=sum(fid2area.values())
    for fid in ref_fid2rt.keys():
        if fid2rt.has_key(fid):
            rt=fid2rt[fid]
            drt=ref_fid2rt[fid]-rt
            if abs(drt)<=max_diff:
                area_frac=fid2area[fid]/total_area
                weight=(area_frac)**2
                rts.append(ref_fid2rt[fid])
                drts.append(drt)
                weights.append(weight)
    return _sort_by_rt(rts, drts, weights)


def _sort_by_rt(rts, drts, weights):
    pairs=zip(rts, drts, weights)
    pairs.sort(key=lambda v: v[0])
    return [[p[i] for p in pairs] for  i in range(3)]


def lowess_spline_interpolation(x,y):
    # 1. eystimeate y using lowess
    yest=lowess(np.array(x),np.array(y))
    # 2. cubic spline interpolation of x vs. yest to build transformation function
    return splrep(np.array(x), np.array(yest), s=0.01, k=5)
    
def _get_path(dir_, t, ending='png'):
    source=t.source.uniqueValue()
    fields=source.split('.')
    fields=fields[:-1]
    fields.append('rt_aligned')
    name='_'.join(fields)
    name='.'.join([name, ending])
    return os.path.join(dir_, name)

def plot_and_save_fit(x, y, fun, path):
    x_fit=np.linspace(min(x), max(x), num=100)
    y_fit=splev(x_fit, fun, der=0)
    plot(x_fit, y_fit, 'r', linewidth=2)
    pylab.xlabel("time sec", fontsize=18)
    pylab.ylabel('delta t sec', fontsize=18)
    pylab.plot(x, y, "bo", markersize=3)
    pylab.savefig(path)
    pylab.close()
    

def transform(t, trans, fit_range):
    def _align(rt, trans, rtrange=fit_range):
        # since the rtrange of peaks detected is in general smaller than the
        # rt range of the peakmap we apply the shift of minrt to all rts in peakmap
        # < minrt and shift of maxrt to all rts > maxrt
        minrt, maxrt=rtrange
        if minrt<=rt<=maxrt:
            delta=float(splev([rt], trans)[0])
        elif rt<minrt:
            delta=float(splev([minrt], trans)[0])
        else:
            delta=float(splev([maxrt], trans)[0])
        return rt + delta
    pm=t.peakmap.uniqueValue()
    pm=deepcopy(pm)
    pm.meta["rt_aligned"] = True
    for spec in pm.spectra:
        spec.rt = _align(spec.rt, trans)
    return pm

########################################################################

def default_rt_align(tables, ref, destination, params=None):
    if not params:
        params={'maxRtDifference' : 100.0, 'resetIntegration' : True, 
                'maxMzDifferencePairfinder': 0.008, 'maxMzDifference' : 0.005 }
    aligned=emzed.align.rtAlign(tables, ref, destination=destination, forceAlign=True, **params)
    return [t.peakmap.uniqueValue() for t in aligned]

########################################################################################


###################################################################################################
   
def test_dli_rt_align():
    peakmaps=['Z:\\pkiefer\\orbitrap_data\\Dynamet_publication_E_coli\\data_set_2\\PEAKMAPS\\20150815_134_JH_exp15-08-04_fast_label_rep2_nLC_QEx_s1_0sec.mzML',
              'Z:\\pkiefer\\orbitrap_data\\Dynamet_publication_E_coli\\data_set_2\\PEAKMAPS\\20150815_138_JH_exp15-08-04_fast_label_rep2_nLC_QEx_s4_2sec.mzML',
              'Z:\\pkiefer\\orbitrap_data\\Dynamet_publication_E_coli\\data_set_2\\PEAKMAPS\\20150815_140_JH_exp15-08-04_fast_label_rep2_nLC_QEx_s5_5sec.mzML',
              'Z:\\pkiefer\\orbitrap_data\\Dynamet_publication_E_coli\\data_set_2\\PEAKMAPS\\20150815_142_JH_exp15-08-04_fast_label_rep2_nLC_QEx_s6_10sec.mzML']
    peakmaps=[emzed.io.loadPeakMap(n) for n in peakmaps]
    pm_idms=emzed.io.loadPeakMap('Z:\\pkiefer\\temp\\B_methanolicus_set_1\\PEAKMAPS\\20131204_072_JM_BM_poolsize_mz1+mz2_131018_S1.mzML'
    )
    ff_metabo=wt.in_out.load_dict('Z:\\emzed2\\compound_libraries\\ff_metabo.json')
#    destination=r'Z:\pkiefer\temp\_temp'
    return get_alignment_tables(peakmaps, pm_idms, max_rt_diff=100.0, ff_metabo=ff_metabo, 
                         max_c_gap=30)
#    return dli_rt_align(peakmaps, pm_idms, ff_metabo=ff_metabo, destination=destination)
  




#################################################################################################
# older and development
def helper(t):
    to_stack=[]
    for f in t.splitBy('feature_id'):
        sub=get_isotopologues(f.num_c_.uniqueValue(), f.mz0_.uniqueValue(), f.z_.uniqueValue())
        f=f.join(sub, True)
        f.removePostfixes()
        to_stack.append(f)
    return emzed.utils.stackTables(to_stack)

def get_isotopologues(num_c, mz0, z, mztol=0.003):
    delta=emzed.mass.C13-emzed.mass.C
    mi=range(num_c+1)
    t=emzed.utils.toTable('mi', mi, type_=int)
    t.addColumn('mz', mz0+(t.mi*delta)/z, type_=float)
    t.addColumn('mzmin', t.mz-mztol, type_=float)
    t.addColumn('mzmax', t.mz+mztol, type_=float)
    return t

def help_test(t, t_ref, max_diff=100):
    fid2area, fid2rt=summarize_features(t)
    __,  ref_fid2rt=summarize_features(t_ref)
    rts, drts, weights=get_diff_pair(fid2rt, fid2area, ref_fid2rt)
    pairs=zip(rts, drts, weights)
    min_w=np.percentile(weights, 50)
    pairs=[p for p in pairs if abs(p[1])<max_diff and not np.isnan(p[1]) and p[-1]>=min_w]
    return [[p[i] for p in pairs] for i in range(3)]
#    return spline_fitting_curve(rts, drts, weights)


def fuse_(cal, univ):
    colnames=['feature_id', 'name', 'mz', 'mzmin', 'mzmax', 'mi', 'rt', 'rtmin', 'rtmax']
#    rename={'rt_': 'rt', 'z_': 'z'}
#    univ.renameColumns(**rename)
#    cal.renameColumn('mz_hypot', 'mz')
    fused=emzed.utils.stackTables([cal.extractColumns(*colnames), univ.extractColumns(*colnames)])
    names=list(set(fused.name.values))
    d={v[0]: v[1] for v in zip(names,range(len(names)))}
    table_operations.update_column_by_dict(fused, 'feature_id', 'name', d, type_=int)
    return fused
#selected=[0, 2, 4, 7, 9, 26, 27, 42, 45, 46, 68, 122, 266, 2138]
#################################################################################################

def summed_peaks(pm):
    summarized=[]
    for spec in pm.spectra:
        summarized.extend(list(spec.peaks))
    return summarized

def remove_the_demons(t_idms):  
    check=t_idms.filter(t_idms.idms_id.apply(len)>0)
    check.replaceColumn('idms_id', check.idms_id.apply(set), type_=set)
    check.replaceColumn('idms_id', check.apply(lambda v: list(v)[0], (check.idms_id,)), type_=int)
    items=[sub for sub in check.splitBy('idms_id') if len(sub)==2]
    return emzed.utils.stackTables(items)
    
      