# -*- coding: utf-8 -*-
"""
Created on Wed Aug 05 11:15:31 2015

@author: pkiefer
"""

import emzed


def adapt_ff_metabo_config(config=None, advanced=False):
    """ provides a GUI to adapt ffMetabo settigs by user. Optional arguments: 
        1) config: dictionary with ffMetabo parameterws as keys, if None a default setup is 
        provided 
        2) advanced: bool  if True all parameters can be edited. Default is False since only a 
        subset which is sufficient for most users
        Config settings are returned
    """
    
   
    width_filter=["off", "auto", "fixed"]    
    # sum==0: advanced off, sum==1: advanced  == on, since multiple choice dialog
    dic=config if config else get_default_ff_metabo()
    criterion=['outlier', 'sample_rate']
    names=['common_noise_threshold_int', 'common_chrom_peak_snr', 'common_chrom_fwhm',
           'mtd_mass_error_ppm', 'mtd_reestimate_mt_sd', 'mtd_trace_termination_criterion',
           'mtd_trace_termination_outliers', 'mtd_min_sample_rate', 'mtd_min_trace_length',
           'mtd_max_trace_length', 'epdet_width_filtering', 'epdet_min_fwhm','epdet_max_fwhm',
           'epdet_masstrace_snr_filtering', 'ffm_local_rt_range', 'ffm_local_mz_range', 
           'ffm_charge_lower_bound', 'ffm_charge_upper_bound', 'ffm_report_summed_ints',
           'ffm_disable_isotope_filtering', 'ffm_use_smoothed_intensities']
    # HELPER Funs
    # openMS uses strg instead of  boolean value:
    def bools_fun(key):
        dic={'true': True, 'false': False}
        return dic[key] if dic.has_key(key) else False
    # inverse fun to bools_fun
    def boolToStr(value):
        return "true" if value else "false"
        
    def get_index(v, liste):
        if v in liste:
            return liste.index(v)
        else:
            return 0
        # GUI        
    if advanced:
        params=emzed.gui.DialogBuilder("Configure Peak Detection")\
        .addFloat(names[0], default=dic[names[0]], min=1.0,
                  help="intensity threshold below which peaks are regarded"\
                  " as noise")\
        .addFloat(names[1], default=dic[names[1]], help="minimum signal-"\
                    "to-noise a mass trace should have")\
        .addFloat(names[2], default=dic[names[2]], min=1.0, max=120.0,
                  help="typical peak width (full width at half maximum)")\
        .addFloat(names[3], default=dic[names[3]], help="allowed mass deviation")\
        .addBool(names[4], default=bools_fun(dic[names[4]]), help="enables dynamic re-"\
                "estimatation of m/z variance during mass trace collection state")\
        .addChoice(names[5], criterion ,default=get_index(dic[names[5]], criterion), 
                   help='Termination criterion for the extension of mass traces.\n In `outlier` mode,'\
                   'trace extension cancels if a predifined number of consecutive outliers are found'\
                   '(see trace_termination_outliers parameter).\n In `sample_rate` mode, trace '\
                   'extension in both direction stops if ratio of found peaks versus visited spectra'
                   'falls below `min_sample_rate` threshold')\
        .addInt(names[6], default=dic[names[6]], help='mass trace extension in one direction'\
                'cancels if set value of consecutive spectra without detected peaks is reached')\
        .addFloat(names[7], default=dic[names[7]], help='minimum fraction of scans along the mass trace'\
                'that must contain a peak')\
        .addFloat(names[8], default=dic[names[8]], min=1.0, help="minimum expected"\
                    " length of a mass trace (in seconds)")\
        .addFloat(names[9], default=dic[names[9]], min=-1.0, help="maximum expected"\
                    " length of a mass trace (in seconds)")\
        .addChoice(names[10], width_filter ,default=get_index(dic[names[10]], width_filter),
                   help="enable filtering of"\
                " unlikely peaks width.\n The fixed setting filters out mass traces"\
                " outside the\n [min_fwhm, max_fwhm] interval (please set parameters"\
                " accordingly!).\n The auto setting filters with the 5% and 95%"\
                "quantiles of the peak width distribution.")\
        .addFloat(names[11], default=dic[names[11]], min=1.0, help="minimum full-width"\
                    "-at-half-maximum of chromatographic peak (in seconds).\n"\
                    "Ignored if parameter epd_width_filtering is off or auto.")\
        .addFloat(names[12], default=dic[names[12]], min=2.0, help="maximum full-width"\
                    "-at-half-maximum of chromatographic peak (in seconds).\n"\
                    "Ignored if parameter epd_width_filtering is off or auto.")\
        .addBool(names[13], default=bools_fun(dic[names[13]]), help="apply post"\
                "-filtering by signal-to-noise ratio after smoothing")\
        .addFloat(names[14], default=dic[names[14]], min=0.0, help='RT range where to look for'\
                            'coeluting mass traces')\
        .addFloat(names[15], default=dic[names[15]], min=1.0, help='MZ range where to look for'\
                            'isotopoic mass traces')\
        .addInt(names[16], default=dic[names[16]], help='lowest charge state to consider')\
        .addInt(names[17], default=dic[names[17]], help='highest charge state to consider')\
        .addBool(names[18], default=bools_fun(dic[names[18]]), help="Set to true for a feature "\
            "intensity summed up over all traces rather than using monoisotopic "\
            'trace intensity alone')\
        .addBool(names[19], default=bools_fun(dic[names[19]]), help="")\
        .addBool(names[20], default=bools_fun(dic[names[20]]), help="Use LOWESS intensities "\
                "instead of raw intensities")\
        .show()
        # replace changed parameters    
        for i,value in enumerate(params):
            if isinstance(value, bool):
                dic[names[i]]=boolToStr(value)
            elif i == 5:
                dic[names[i]]=criterion[value]
            elif i == 10:
                dic[names[i]]=width_filter[value]
            else:
               dic[names[i]]=value
    else:
        #debug
        switch=["off", "auto"]
        params=emzed.gui.DialogBuilder("Configure Peak Detection")\
        .addFloat(names[0], default=dic[names[0]], min=1.0,
                  help="intensity threshold below which peaks are regarded"\
                  " as noise")\
        .addFloat(names[1], default=dic[names[1]], help="minimum signal-"\
                    "to-noise a mass trace should have")\
        .addFloat(names[2], default=dic[names[2]], min=1.0, max=120.0,
                  help="typical peak width (full width at half maximum)")\
        .addFloat(names[3], default=dic[names[3]], help="allowed mass deviation")\
        .addBool(names[4], default=bools_fun(dic[names[4]]), help="enables dynamic re-"\
                "estimatation of m/z variance during mass trace collection state")\
        .addChoice(names[10], switch ,default=get_index(dic[names[10]], 
                   width_filter),   help="enable filtering of"\
                " unlikely peaks width.\n The auto setting filters with the 5% and 95%"\
                "quantiles of the peak width distribution.")\
        .addFloat(names[14], default=dic[names[14]], min=0.0, help='RT range where to look for'\
                            'coeluting mass traces')\
        .addFloat(names[15], default=dic[names[15]], min=1.0, help='MZ range where to look for'\
                            'isotopoic mass traces')\
        .addInt(names[16], default=dic[names[16]], help='lowest charge state to consider')\
        .addInt(names[17], default=dic[names[17]], help='highest charge state to consider')\
        .show()
        # replace changed parameters 
        for i, j in enumerate([0, 1, 2, 3, 4, 10, 14, 15, 16, 17]):
            if j==4:
                dic[names[j]] = boolToStr(params[i])
                print boolToStr(params[i])
            elif j==10:
                dic[names[j]] = width_filter[params[i]]
            else:
                 if i<len(params)-1:
                    dic[names[j]]=params[i]
    return dic

def get_default_ff_metabo():
    """ default setting for TBA ion pairing reversed phase with QExactive intrument
    """
    return dict(common_noise_threshold_int=80000.0,
                common_chrom_peak_snr=3.0,
                common_chrom_fwhm=25.0,
                mtd_mass_error_ppm=15.0,
                mtd_reestimate_mt_sd='true',
                mtd_trace_termination_criterion='outlier',
                mtd_trace_termination_outliers=5,                
                mtd_min_sample_rate=0.5,                
                mtd_min_trace_length=10.0,
                mtd_max_trace_length=-1.0,
                epdet_width_filtering='auto',
                epdet_min_fwhm=3.0,
                epdet_max_fwhm=120.0,
                epdet_masstrace_snr_filtering='false',
                ffm_local_rt_range=5.0,
                ffm_local_mz_range=5.0,
                ffm_charge_lower_bound=0, 
                ffm_charge_upper_bound=3, 
                ffm_report_summed_ints='false',
                ffm_disable_isotope_filtering='true',
                ffm_use_smoothed_intensities='true')

################################################################################################

