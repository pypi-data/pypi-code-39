# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 12:45:59 2017

@author: pkiefer
"""
from detect_features import detect_features
from map_idms_peaks import assign_12c_u13c_features
from idms_feature_grouper import idms_feature_grouper
from build_idms_pair_table import build_idms_pair_table



def main_pair_finder(samples, kwargs, cut=False):
    if cut:
        samples=[pm.extract(mzmin=200, mzmax=500, rtmin=800, rtmax=1640) for pm in samples]
    t_nl, t_ul, t_idms=detect_features(samples, kwargs)
    idms_nl,idms_ul, ref_nl, ref_ul = assign_12c_u13c_features(t_nl, t_ul, t_idms, kwargs)
    nl, ul=idms_feature_grouper(idms_nl, idms_ul, kwargs)
    print
    result=build_idms_pair_table(nl, ul, kwargs, kwargs['mzdiff'])
    result.meta['config']=kwargs
    return result

