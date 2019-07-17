# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 09:54:27 2017

@author: pkiefer
"""
import math   
import emzed
import numpy as np
from scipy.optimize import curve_fit
from fitting import savitzky_golay, emg_exact as emg_exact_


def emg_smoothed(t, window_size=5, n_cpus=1, max_diff_percent=None, mslevel=1):
    """ improved emg_exact integration since emg_fitting is enhanced via providing a 
    savitzky_golay filtered intensity signal.
    
    """
    # each row requires a unique identifyer:
    t.updateColumn('id_', range(len(t)), type_=float)
    id_col='id_'
    #1. perform a std integration to obtain smoothed intensities
    t=emzed.utils.integrate(t, 'trapez',  n_cpus=n_cpus, msLevel=mslevel)
    id2area={id_: area for id_,area in zip(t.getColumn(id_col), t.area)}
    _update_smoothed_label(t)
    #2. perform emg_exact fit of smoothed signals
    colnames=['area', 'rmse', 'params', 'method', 'smoothed_eic']
    coltypes=[t.getColType(n) for n in colnames]
    colformats=[t.getColFormat(n) for n in colnames]
    for pstfx in t.supportedPostfixes(['area', 'rmse', 'params']):
        params_col=''.join(['params', pstfx])
        expr=t.getColumn
        t.updateColumn('temp_', t.apply(integrate_smoothed, (expr(params_col), window_size), 
                                        keep_nones=True), type_=tuple)
        for i in range(len(colnames)):
            name=''.join([colnames[i], pstfx])
            t.updateColumn(name, t.apply(_update_integration, (expr(id_col), expr(name), 
                                t.temp_, i, id2area, max_diff_percent), keep_nones=True), 
                                type_=coltypes[i], format_=colformats[i])
    t.dropColumns('id_', 'temp_')
    return t


def _update_integration(id_, value, values, i, d, max_diff_percent):
    area=values[0]
    if abs(d[id_]-area)/(d[id_]+1.0)*100.0<=max_diff_percent or max_diff_percent==None:
        return values[i]
    return value


def _update_smoothed_label(t):
    for pstfx in t.supportedPostfixes(['area', 'rmse', 'params']):
        smoothed=''.join(['smoothed_eic', pstfx])
        method=''.join(['method', pstfx])
        t.updateColumn(smoothed, False, type_=bool, insertAfter=method)
        

def integrate_smoothed(params, winsize):
    if params:
        rts, ints=params
        try:
            ints_sg=savitzky_golay(np.array(ints), winsize, 2)
            smoothed=True
        except:
            ints_sg=ints
            smoothed=False
        bounds=_determine_peak_param_bounderies(rts, ints_sg)
        try:
            param, pcov = curve_fit(emg_exact_, rts, ints_sg, bounds=bounds)
            y_fit=emg_exact_(rts, *param)
            method='emg_exact'
        except:
            y_fit=ints_sg
            param=np.array([rts,ints_sg])
            method='std' if smoothed else 'trapez'
        rmse = 1 / math.sqrt(len(rts)) * np.linalg.norm(y_fit - ints)
        area=np.trapz(y_fit, rts)
        # since all data must be of type float np.arrays are converted to lists
        return area.tolist(), rmse.tolist(), param, method, smoothed
    return 0.0, 0.0, None, 'max', False 
    



def _determine_peak_param_bounderies(rts, ints):
    pairs=zip(rts,ints)
    # bounfery for rt
    rt, appex=max(pairs, key=lambda v: v[1])
    appex_rts=[p[0] for p in pairs if p[1]>=0.5*appex]
    rt_bounds=(min(appex_rts), max(appex_rts))
    # to estimate the fwhm bounderies we determine the full width at 0.4 *appex and 0.6 * appex
    max_sigma=3*(max(rts)-min(rts))
    min_sigma=0.3
    s_bounds=(min_sigma, max_sigma)
#    print sigma_bounds
    area=np.trapz(ints, rts)
    h_bounds=(max(ints), 1.5 *area)
    w_bounds=(1e-6, max(rts)-min(rts))
    
    return ([h_bounds[0], rt_bounds[0], w_bounds[0], s_bounds[0]], [h_bounds[1], rt_bounds[1], 
                 w_bounds[1], s_bounds[1]])


