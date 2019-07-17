# -*- coding: utf-8 -*-
"""
Created on Tue May 19 11:11:25 2015

@author: pkiefer
"""

from emzed.core.data_types import PeakMap, Spectrum
from collections import defaultdict
import numpy as np


def determine_spectral_baseline_and_noise(peakmap):
    """
    Function determine_spectral_baseline_and_noise(pm) determines baseline and noise level assuming 
    that the baseline contains the highest point denity 
    (J Ams Soc Mass Spectrom 2000, 11, 320-3332). To this end, we build a histogramm of all 
    intensities over all spectra, and the bin width of the histogramm is determined by the 
    rule of Freedman und Diaconis. the mean intensity of the bin with highest abundance is 
    said to be the baseline value and the fwhm of the histogramm is said to 
    be the noise.
    """
    intensities=_get_intensities(peakmap)
    return _determine_spectral_noise_and_baseline(intensities)


def _get_intensities(pm):
    intensities=[]
    for spec in pm.spectra:
        intensities.extend(spec.peaks[:,1])
    return sorted([v for v in intensities if v>0])


def _determine_spectral_noise_and_baseline(intensities):
    binwidth=get_binwidth(intensities)
    intensities, counts=_bin_sum(intensities, binwidth)
    return  _determine_noise_params(intensities, counts)


def get_binwidth(intensities):
    # rule of Freedman und Diaconis
    # David Freedman, Persi Diaconis: n the histogram as a density estimator: 
    # L 2 {\displaystyle L_{2}} L_2 theory. 
    # In: Zeitschrift für Wahrscheinlichkeitstheorie und verwandte Gebiete. 
    # Band 57, Nr. 4, 1981, S. 453–476, doi:10.1007/BF01025868
    nominator=(2*(np.percentile(intensities,75)-np.percentile(intensities,25)))
    denominator=len(intensities)**(1/3.0)
    return int(round(nominator/denominator))


def _bin_sum(intensities, width=500):
    d=defaultdict(list)
    x_values=[]
    counts=[]
    for i in intensities:
        d[int(i/width)].append(i)
    for group in sorted(d.keys()):
        x_values.append(np.mean(d[group]))
        counts.append(len(d[group]))
    return x_values, counts


def _determine_noise_params(x,y):
    pairs=zip(x,y)
    _handle_start_value_problem(pairs)
    baseline, appex=max(pairs, key=lambda v: v[1])
    lower=[(p[0], abs(p[1]-appex/2)) for p in pairs if p[0]<baseline]
    upper=[(p[0], abs(p[1]-appex/2)) for p in pairs if p[0]>baseline]
    fwhm1=min(lower, key=lambda v: v[1])[0]
    fwhm2=min(upper, key=lambda v: v[1])[0]
    return baseline, fwhm2-fwhm1


def _handle_start_value_problem(pairs):
    """ Q Ex data have a maximum in the initial bin which leads to wrong estimation
    """
    while not pairs.index(max(pairs, key=lambda v: v[1])):
        index=pairs.index(max(pairs, key=lambda v: v[1]))
        __=pairs.pop(index)
        if not len(pairs):
            assert False, 'Peakmap intinsity distribution is not in line with assumption'\
            'the baseline should contain the highest point denity and the the distribution is'\
            ' Gaussian like.'
            
            
##################################################################################################
def _cut_peakmap(pm, rtmin, rtmax, mzmin, mzmax, mslevel=1):
    sub=pm.extract(rtmin=rtmin, rtmax=rtmax, mzmin=mzmin, mzmax=mzmax)
    sub.spectra=[spec for spec in sub.spectra if spec.msLevel==mslevel]
    return sub
    

    
    
###################################################################################################    
def _merge_peakmaps(peakmaps):
    specs=defaultdict(list)
    for pm in peakmaps:
        for spec in pm.spectra:
            specs[(spec.rt, spec.msLevel)].append(spec)
    for key in specs.keys():
        specs[key]=_merge_specs(specs[key])
    spectra_=specs.values()
    spectra_.sort(key=lambda v: v.rt)
    return PeakMap(spectra_, {})


def check_origine(peakmaps):
    """
    """
    assert len(set([pm.meta['full_source'] for pm in peakmaps]))==1, 'merging only allowed for'\
            'sub peakmaps originating from same peakmap'

def _merge_specs(specs):
    peaks=[]
    [peaks.extend(s.peaks) for s in specs]    
    peaks=set([tuple(peak) for peak in peaks])
    peaks=list(peaks)
    peaks.sort(key=lambda v: v[0])
    spectrum=specs[0]
    spectrum.peaks=np.array(peaks)
    return spectrum



def extract_peakmap_region(pm, rtmin, rtmax, mzmin, mzmax):
    selected=[]
    specs=pm.spectra
    def rtfilter(spec, rtmin=rtmin, rtmax=rtmax):
        return rtmin<=spec.rt<=rtmax
    specs=filter(rtfilter, specs)
    def mzfilter(peak, mzmin=mzmin, mzmax=mzmax):
        return mzmin<=peak[0]<=mzmax
    for spec in specs:
        peaks=spec.peaks
        peaks=filter(mzfilter, peaks)
        spec.peaks=peaks
        if len(peaks):
            selected.append(spectrum2dic(spec))
    return selected
#    return specs

def spectrum2dic(spec, peaks):
    d={}
    d['rt']=round(spec.rt, 5) #  to avoid numeric problems by grouping
    d['polarity']=spec.polarity
    d['ms_level']=spec.msLevel
    d['precursors']=spec.precursors
    d['peaks']=[tuple(peak) for peak in spec.peaks]
    return d
        
def build_peakmap_from_spectrum_dics(spectrum_as_dicts):
    spectra=[]
    rt2peaks=defaultdict(set)
    polarity=set([])
    ms_level=set([])
    for spec in spectrum_as_dicts:
        for peak in spec['peaks']:
            rt2peaks[spec['rt']].add(peak)
        polarity.add(spec['polarity'])
        ms_level.add(spec['ms_level'])
        assert spec['precursors']==None
    assert len(polarity)==1
    assert len(ms_level)==1
    ms_level=ms_level.pop()
    polarity=polarity.pop()
    for rt in sorted(rt2peaks.keys()):
        peaks=np.array(rt2peaks[rt])
        spectra.append(Spectrum(peaks, rt, ms_level, polarity))
    return PeakMap(spectra)
        
from in_out import _convert       

def db_spectrum2peaks(data):
#    import pdb; pdb.set_trace()
    peaks=[]
    data=_convert(data)
    for peak in data.split(' '):
            peaks.append([float(v) for v in peak.split(':')])
    return np.array(peaks)
    
        
            
        
            
    
    
