# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 10:28:36 2017

@author: pkiefer
"""
import emzed
import hires
import utils as ut
import table_operations as top
import numpy as np
import peakmap_operations
from _ff_metabo_config import adapt_ff_metabo_config
from collections import defaultdict
from copy import deepcopy
from collect_and_lookup import compare_tables

################################################################################################
# based on ff_metabo
################################################################################################

def local_ff_metabo(t, c13=False, ff_config=None, max_c_gap=0, min_abundance=0.01, elements=('C',)):
    assert len(set(t.peakmap.values))==1, 'Only 1 peakmap per table allowed.'
    
    if not ff_config:
        ff_config = adapt_ff_metabo_config(advanced=True)
    ff_config=adapt_config_parameters(t, ff_config)
    pm=extract_local_peakmap_environment(t, c13=c13)
    local=emzed.ff.runMetaboFeatureFinder(pm, **ff_config)
    local=emzed.utils.integrate(local, 'max', n_cpus=1)
    if c13:
        rttol=float(np.percentile(local.fwhm.values, 60))/2
        local=hires.feature_regrouper(local, min_abundance=min_abundance, elements=elements, 
                                max_c_gap=max_c_gap, rt_tolerance=rttol)
        local.replaceColumn('feature_id', local.isotope_cluster_id, type_=int, format_='%d')
        local.dropColumns('isotope_cluster_id', 'carbon_isotope_shift', 'unlabeled_isotope_shift',
                          'mass_corr')
    local.setColFormat('mzmin', '%.5f')
    local.setColFormat('mzmax', '%.5f')
    return complement_t(t, local)
    #

    
def adapt_config_parameters(t, ff_config):
    ff_config=deepcopy(ff_config)
    pm=t.peakmap.uniqueValue()
    ff_config['common_chrom_peak_snr']= 1.0 
    ff_config['mtd_trace_termination_outliers']= 25
    ff_config['mtd_min_trace_length']= 0.2
    ff_config['epdet_min_fwhm']= 0.5
    ff_config['ffm_use_smoothed_intensities']='true'
    ff_config['mtd_reestimate_mt_sd']='true'
    determine_noise_intensity_threshold(ff_config, pm, signal_to_noise=0.5)
    return ff_config

def determine_noise_intensity_threshold(ff_config, pm, signal_to_noise=3.0):
    intensities=get_pm_intensities(pm)
    key2count, key2values=logbin_intensities(intensities)
    noise_level=float(np.median(get_main_group(key2count, key2values)))
    print '%.1f times noise level %.f' %(signal_to_noise, noise_level)
    ff_config['common_noise_threshold_int']=round(signal_to_noise*noise_level,0)

def get_pm_intensities(pm):
    intensities=[]
    for spec in pm.spectra[::4]:
        for peak in spec.peaks:
            intensities.append(peak[-1])
    return intensities

def logbin_intensities(values):
    import math
    d1=defaultdict(int)
    d2=defaultdict(list)
    for value in values:
        key=int(math.log(value))
        d1[key]+=1
        d2[key].append(value)
    return d1, d2
    

def get_main_group(key2count, key2values):
    pairs=[(k, key2count[k]) for k in key2count.keys()]
    key=max(pairs, key=lambda v: v[1])[0]
    return key2values[key]

###################################################################################################
    
def extract_local_peakmap_environment(t, c13=False, delta_mz=1.5):
    print 'extracting local feature_environment ...'
    subset=t.filter(t.z==0)
    local_pms=[]
    for mz, rtmin, rtmax, pm in zip(subset.mz, subset.rtmin, subset.rtmax, subset.peakmap):
        mzmin=mz-delta_mz
        mzmax=mz+delta_mz
        local=peakmap_operations.cut_peakmap(pm, rtmin, rtmax, mzmin, mzmax, mslevel=1)
        local_pms.append(local)
    pm=peakmap_operations._merge_peakmaps(local_pms)
    print 'done'
    return pm


def complement_t(t, local):
#    import pdb; pdb.set_trace()
    PeakMap=emzed.core.data_types.PeakMap
    colnames=[n for n  in local.getColNames()]
    uncharged=t.filter(t.z==0)
    key2tol={'mz':0.0001, 'rt':1.0}
    local=compare_tables(local, uncharged, key2tol=key2tol)
#    print len(local)
    # get postfix of compare tables
#    postfix=''.join(['__', str(local.maxPostfix())])
#    d=_local2original(local)
#    local.replaceColumn('feature_id', local.apply(_replace,(local.feature_id, d)), type_=int)
    colname='__'.join(['feature_id', str(local.maxPostfix())])
    local.replaceColumn('feature_id', local.getColumn(colname), type_=int)
    local=local.filter(local.feature_id.isNotNone())
    print len(local)
#    local.replaceColumn('feature_id', local.apply(_get_fid, (local.feature_id, local.matches)), 
#                        type_=int)
    local=local.extractColumns(*colnames)
    local.replaceColumn('peakmap', t.peakmap.uniqueValue(), type_=PeakMap, format_=t.getColFormat('peakmap'))
    sub=ut.fast_isIn_filter(t, 'feature_id', set(local.feature_id.values), True)
    return emzed.utils.stackTables([sub,local])

#################################################################################################
