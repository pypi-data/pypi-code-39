# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 12:47:52 2017

@author: pkiefer
"""
import emzed
import hires
import wtbox
import shared_functions as sf
from shared_functions import update_rt
from rt_align_idms import rt_align_idms
import _local_ff_remove_multiple as rm_multi



def detect_features(samples, kwargs):
    config=kwargs['ff_config']
    rtalign=kwargs['rtalign']
    signal2noise=config['common_chrom_peak_snr']
    remove_sholders=kwargs['remove_sholders']
    print 'detecting features...'
    spectral_sn=kwargs['spectral_signal_noise']
    samples, thresholds=run_ff(samples, config, kwargs['determine_noise_level'], spectral_sn)
    kwargs['common_noise_thresholds']=thresholds
    # Instead of using the default hires.remove_shoulder_peaks function which runs feature_finder
    # metabo to detect major peaks we use ff_detection results directly
    #we remove the sholder peaks based on detected peaks. Potential shoulder will
    # be removed if peak_intensity is 50 x noise level.
    samples=remove_shoulder_peaks(samples, remove_sholders, thresholds, signal2noise)
    # remove shoulder _peaks includes an integration step. If remove_shodlder == False the
    # peaks are not integrated and the update_rt function will fail. Therefore we integrate
    # tables in case remove_sholder == False.
    if not remove_sholders:
        samples=sf.integrate_tables(samples)
    # since ff_metabo determines rt =(rtmin + rtmax)/2 and not the value at rt(max_int) we correct
    # for the appex position
    [update_rt(s) for s in samples]
    if kwargs['rtalign']:
         samples=rt_align_idms(samples, samples[-1], rtalign, kwargs['destination'])
    # double peaks might occur if satelites were not completely removed
    samples=[rm_multi.remove_multiple_peaks(s) for s in samples]
    return samples


#####################################################
def remove_shoulder_peaks(tables, remove_sholders, thresholds, signal2noise):
    if remove_sholders:
        remove_shoulders(tables, remove_sholders, thresholds)
        return remove_shoulder_peaks_from_samples(tables, thresholds, signal2noise)


def remove_shoulders(tables, remove_sholders, thresholds):
    print 'removing shoulder peaks from peakmap...'
    for t in tables:
        source=t.source.uniqueValue()
        min_int=thresholds[source]*50
        _remove(t, min_int)
    print 'Done.'

    
def _remove(t, min_int):
    pm=t.peakmap.uniqueValue()
    ntuples=zip(t.rtmin, t.rtmax, t.mzmin, t.mzmax, t.intensity)
    ntuples.sort(key = lambda v: v[-1], reverse=True)
    i=0
    while i<len(ntuples):
        if ntuples[i][-1]>=min_int:
            hires.remove_shoulder_peaks(pm, *ntuples[i][:-1])
        i+=1

def remove_shoulder_peaks_from_samples(samples, thresholds, sn):
    print 'removing sholder peaks from tables ...'
    # samples must be reintegrated to determine changes in area due to peakmap correction
    samples=sf.integrate_tables(samples)
    filtered=[]
    for s in samples:
        source=s.source.uniqueValue()
        min_area=thresholds[source]*sn
        filtered.append(s.filter(s.area>=min_area))
        # reducing the number of peaks might lead to undetermined feature charge states if len==1
        [sf.check_z(f) for f  in filtered]
    print 'done'
    return filtered 
                       
   

def _keep_min_sn_peak_only(sample, thresholds):
    s=sample
    source=s.source.uniqueValue()
    min_int=thresholds[source]
    return s.filter(s.area>min_int)    

def _filter_min_spectra(sample, min_spectra=3):
    def _get_len(params, min_spectra):
        __, ints=params
        return len([i for i in ints if i>0])>=min_spectra
    sample.updateColumn('_keep', sample.apply(_get_len, (sample.params, min_spectra)), type_=bool)
    sample=sample.filter(sample._keep==True)
    sample.dropColumns('_keep')
    return sample
    

def run_ff(pms, config, determine_noise_level=True, sn=3.0):
    """ function run_ff run_ff(pms, config, determine_noise_level=True) runs in parallel
        emzed.ff.runMetaboFeatureFinder. If determine noise_level== True, peakmap noise level
        is determined for each peak,ap and ff_config_parameter `common_noise_threshold_int`
        is replaced by the noise_level value. Return values:  list of tables and dictionary
        peakmap sorce -> noise_level value
    """
    from copy import copy
    configs=[copy(config) for i in range(len(pms))]
    thresholds={}
    for config_, pm in zip(configs, pms):
        if determine_noise_level:
            # we determine baseline and and noise over all spectra of the peakmap
            # and we calcuate the threshold as baseline + 3 sigma of baseline
            threshold=sf.determine_ff_config_intensity_threshold(pm, sn=sn)
            config_['common_noise_threshold_int']=threshold
        else:
            threshold=config_['common_noise_threshold_int']
        thresholds[pm.meta['source']]= threshold
    pairs=zip(pms, configs)
    tables=wtbox._multiprocess.main_parallel(_run_ff, pairs)
    # bug fix: fixed in later emzed version
    [_update_formats(t) for t  in tables]
    return tables, thresholds


def _run_ff(pair):
    pm ,config=pair    
    return emzed.ff.runMetaboFeatureFinder(pm, **config)


def _update_formats(t):  
    # fixes emzed bug  [fixed in higher emzed versions]
    t.setColFormat('mzmin',  '%.5f')
    t.setColFormat('mzmax',  '%.5f')

#################################################################################################