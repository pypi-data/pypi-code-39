# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 13:39:05 2017

@author: pkiefer
strategy:

"""
import emzed
import wtbox
import shared_functions as sf
from wtbox.subtract_peak_tables import subtract_table
from shared_functions import estimate_rttol


###########################################################################################
# MAIN FUNCTION 1
##########################################################################################

def assign_12c_u13c_features(t_nl, t_ul, t_idms, kwargs, min_area=1e3):
    # we avoid in place modifications
    t_nl=t_nl.copy()
    t_ul=t_ul.copy()
    t_idms=t_idms.copy()
    t_nl=get_unique_features(t_nl, t_ul, kwargs)
    t_ul=get_unique_features(t_ul, t_nl, kwargs)
    t_nl=t_nl.filter(t_nl.area>min_area)
    t_ul=t_ul.filter(t_ul.area>min_area)
    idms_nl=map_peaks(t_idms, t_nl, kwargs, nl=True)
    idms_ul=map_peaks(t_idms, t_ul, kwargs, nl=False)
    idms_ul.replaceColumn('id', idms_ul.id+len(idms_nl), type_=int)
    fid_shift=t_nl.feature_id.max()+1
    idms_ul.replaceColumn('feature_id', idms_ul.feature_id +fid_shift, type_=int)
    return idms_nl, idms_ul, t_nl, t_ul


#############################################################################################

def get_unique_features(t, ref, kwargs):
    rttol=estimate_rttol([t, ref] , kwargs['mztol'], 2, False, id_col='feature_id')
    kwargs['rttol']=rttol
    kwargs['subtract_blank']['key2tol']={'rt': rttol, 'mz': kwargs['mztol']}
    return subtract_table(t, ref, **kwargs['subtract_blank'])
    return t


    
def _map_peaks(t, ref, kwargs, nl=True):
    colnames=['feature_id', 'mz', 'mzmin', 'mzmax', 'rt', 'rtmin', 'rtmax', 'z', 'fwhm']
    pm=t.peakmap.uniqueValue()
    mapping=ref.extractColumns(*colnames)
    mapping.replaceColumn('mzmin', mapping.mz-kwargs['mztol']/2.0, type_=float)
    mapping.replaceColumn('mzmax', mapping.mz+kwargs['mztol']/2.0, type_=float)
    mapping.addColumn('peakmap', pm, type_=emzed.core.data_types.PeakMap)
    n_cpus=wtbox.utils.get_n_cpus(mapping, 4)
    mapping=emzed.utils.integrate(mapping, 'max', n_cpus=n_cpus)
    mapping=_select_peaks(mapping)
    sf.update_rt(mapping)
    emzed.utils.recalculateMzPeaks(mapping)
#    add_representing_mz(mapping, value_col='area')
    mapping.addColumn('is_nl', nl, type_=bool)
    mapping.addColumn('fid_ref', mapping.feature_id, type_=int)
    mapping.addEnumeration()
    return mapping


def map_peaks(t, ref, kwargs, nl=True):
    colnames=['feature_id', 'mz', 'mzmin', 'mzmax', 'rt', 'rtmin', 'rtmax', 'z', 'fwhm', 'peakmap', 
              'area', 'rmse', 'method', 'params']
    pm=t.peakmap.uniqueValue()
    delta_rt=estimate_rttol([t, ref] , 0.003, 2, False, id_col='feature_id')
    delta_rt = delta_rt if delta_rt<=60.0 else 60.0
    mapping=ref.extractColumns(*colnames)
    mapping.replaceColumn('mzmin', mapping.mz-kwargs['mztol']/2.0, type_=float)
    mapping.replaceColumn('mzmax', mapping.mz+kwargs['mztol']/2.0, type_=float)
    print 'smart feature extraction ...'
    mapping=_extract_peaks(pm, mapping, kwargs, delta_rt=delta_rt)
    print 'done'
    mapping=_select_peaks(mapping)
    emzed.utils.recalculateMzPeaks(mapping)
    mapping.addColumn('is_nl', nl, type_=bool)
    mapping.addColumn('fid_ref', mapping.feature_id, type_=int)
    mapping.addEnumeration()
    return mapping


def _extract_peaks(pm, mapping, kwargs, delta_rt=10.0):
    n_cpus=wtbox.utils.get_n_cpus(mapping, max_cpus=4)
    t=wtbox._shift_rt_windows.shift_rt_windows(pm, mapping, id_col='feature_id', delta_rt=delta_rt)
    # it is necessary to update the params_values for filtering by integration
    t=emzed.utils.integrate(t, 'max', n_cpus=n_cpus)
    sf.update_rt(t)
    return sf.filter_min_specs(t, kwargs['ff_config'], kwargs['min_specs'])
    

def _select_peaks(t):
    threshold=sf.determine_ff_config_intensity_threshold(t.peakmap.uniqueValue())
    # take only into account peaks fullfilling the signal definition on spectral level
    t.addColumn('max_area', t.area.max.group_by(t.feature_id), type_=float)
    def _filter(area, max_area, noise=threshold):
        threshold=0.01*max_area
        min_area=threshold if threshold>noise else noise
        return True if area>min_area else False
    t.addColumn('keep', t.apply(_filter,(t.area, t.max_area)), type_=bool)
    t=t.filter(t.keep==True)
    t.dropColumns('max_area', 'keep')
    return t
    

 

            
        
    
    
    