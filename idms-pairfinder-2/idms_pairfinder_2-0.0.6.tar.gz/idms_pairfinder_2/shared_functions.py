# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 12:58:04 2017

@author: pkiefer
"""
import emzed
from emzed.utils import toTable, stackTables
import numpy as np
from collections import defaultdict, Counter
import pyopenms
import wtbox


def estimate_rttol(tables, mztol, min_hits, only_labeled=True, id_col='idms_pid', mintol=1.0):
    assert min_hits<=len(tables), 'not enough tables or you have to reduce '\
        'the number of hits'
    print 'estimating rt_shift over all tables ...'
    # we take only peaks into account that occur unique within the same runtime
    collected=collect_unique_peaks(tables, mztol, only_labeled, id_col)
    rttol=_estmimate_rttol(collected, mztol, min_hits)
    rttol= rttol if rttol>0 else mintol
    print 'Done.'
    return rttol

def _estmimate_rttol(collected, mztol, min_hits):
    delta_rts=[]
    for key,values in collected.items():
        # collect and lookup adds the key bin_tol and empty_clone to simplify table_reconstruction
        # those keys have to be removed
        if isinstance(key, tuple):
            rts=[]
            values=wtbox.collect_and_lookup.genuin_values(key, values, (mztol,))
            for pair in values:
                __, value=pair
                rts.append(value['rt'])
            if len(rts)>=min_hits:    
                delta=max(rts)-min(rts)
                delta_rts.append(delta)
    assert len(delta_rts)>0, 'no common unique features found! Please check if idms_pair tables'\
        ' are fitting together!!!!'
    return np.median(delta_rts)*2
    
###################################################################################################    

def update_rt(t, id_col='feature_id'):
    """ ff_metabo sets rt to (rtmin+rtmax)/2 assuming gaussian peak shapes. In many cases peak rt
        shape is not symmetric and rt is shifted. We therefore replace rt value by 
        rt at max_intensity. Function requires integration with 'max' integration algorithm prior
        to execution
    """
    d={}
    assert t.method.uniqueValue() in ['max', 'trapez', 'std']
    t.updateColumn('max_area', t.area.max.group_by(t.getColumn(id_col)), type_=float)
    sub=t.filter(t.area==t.max_area)
    t.dropColumns('max_area')
    for fid, params, rt in zip(sub.getColumn(id_col), sub.params, sub.rt):
#        rt_values=_get_rt(params, rt)
        d[fid]=_get_rt(params, rt)
    def _update(fid, d):
        return d.get(fid)
    t.replaceColumn('rt', t.apply(_update,(t.getColumn(id_col), d)), type_=float)


def _get_rt(params, rt_, threshold=0.01):
    if params ==None:
        return rt_
    else:
        pairs=zip(*params)
    rt, inten= max(pairs, key=lambda v: v[1])
    # the window size should not be changed!!
#    rtmin_pairs=[p for p in pairs if p[0]<rt and p[1]<threshold*inten]
#    rtmax_pairs=[p for p in pairs if p[0]>rt and p[1]<threshold*inten]
#    if len(rtmin_pairs)>1:
#        rtmin=max(rtmin_pairs, key=lambda v: v[0])[0]
#    else:
#        rtmin=min(pairs, key=lambda v: v[0])[0]
#    if len(rtmax_pairs)>1:
#        rtmax=min(rtmax_pairs, key=lambda v: v[0])[0]
#    else:
#        rtmax=max(pairs, key=lambda v: v[0])[0]
    return rt


#############################################################################################
def update_rts_params(t):
    t.updateColumn('params', t.apply(_update_rts,(t.params, t.rtmin)), type_=object)

def _update_rts(params, rtmin):
    rts, ints=params
    delta=rtmin - min(rts)
    rts=rts+delta
    return (rts, ints)
##############################################################################

def check_z(t, id_col='feature_id'):
    """
    if len of feature == 1 set z value to 0
    """
    d=Counter(t.getColumn(id_col).values)
    def _replace(fid, z, d):
        return z if d[fid]>1 else 0
    t.replaceColumn('z', t.apply(_replace, (t.getColumn(id_col), t.z, d)), type_=int)

########################################################################

def build_fid2values(t):
    d={}
    d['colnames']=[n for n in t.getColNames()]
    d['coltypes']=_get_name2type(t)
    d['colformats']=_get_name2format(t)
    d['features']={}
    _add_fid2values(d['features'], t)
    return d


def _get_name2type(t):
    colnames=[n for n in t.getColNames()]
    types=[n for n in t.getColTypes()]
    return {name:type_ for name, type_ in zip(colnames, types)}
    
    
def _get_name2format(t):
    colnames=[n for n in t.getColNames()]
    formats=[n for n in t.getColFormats()]
    return {name:format_ for name, format_ in zip(colnames, formats)}


def _add_fid2values(d, t):
    colnames=[n for n in t.getColNames()]
    for row in t.rows:
        i=colnames.index('feature_id')
        fid=row[i]
        if not d.has_key(fid):
            d[fid]=defaultdict(list)
        for j in range(len(colnames)):
            d[fid][colnames[j]].append(row[j])
    
############################################################################

def build_table_from_fid2values(d, fids=None):
    keys=d['colnames']
    tables=[]
    values=[d['features'][fid] for fid in fids] if fids else d['features'].values()
    for colname2value in values:
        key=keys[0]
        t=toTable(key, colname2value[key], type_=d['coltypes'][key], format_=d['colformats'][key])
        for key in keys[1:]:
            t.addColumn(key, colname2value[key], type_=d['coltypes'][key], 
                        format_=d['colformats'][key])
        tables.append(t)
    return stackTables(tables)
###################################################################################################

def build_selection_table(t, ref_features):
    m=0
    for f in ref_features:
        rt=np.median(f['rt'])
        mzs=t.mz.values
        areas=t.area.values
        fwhm=np.median(f['fwhm'])
        pm=build_peakmap_from_feature(mzs, areas, rt, fwhm)
        pstfx=str(m)
        for v, name in zip([-0.00001, 0.00001], ['mzmin', 'mzmax']):
            colname='_'.join([name, pstfx])
            t.addColumn(colname, t.mz+v, type_=float)
        rtmin, rtmax = pm.rtRange()
        t.addColumn('_'.join(['rtmin', pstfx]), rtmin, type_=float)
        t.addColumn('_'.join(['rtmax', pstfx]), rtmax, type_=float)
        t.addColumn('_'.join(['peakmap', pstfx]), pm, type_=emzed.core.data_types.PeakMap)
        m+=1


def build_peakmap_from_feature(mzs, areas, rt, fwhm):
    intensities=[v/fwhm for v in areas]
    spectras=[]
    rts=get_rts(rt, fwhm)
    for rt_ in rts:
        peaks=make_fwhm_spec(mzs, rt_, rt, fwhm, intensities)
        spec=emzed.core.data_types.Spectrum(peaks, rt_, 1, '-' )
        spectras.append(spec)
    return emzed.core.data_types.PeakMap(spectras, {})


def get_rts(rt, fwhm):
    rtmin=rt-4*fwhm
    rtmin= rtmin if rtmin>=0 else 0
    rtmax=rt+4*fwhm
    return np.linspace(rtmin, rtmax, (rtmax-rtmin)*2)


def make_fwhm_spec(mzs, time, rt, fwhm, intensities):
    intensities= [i if rt-fwhm/2<=time <=rt+fwhm/2 else 0 for i  in intensities]
#    ints=[intensity]*len(mzs) 
    return np.array(zip(mzs, intensities))


def undo_build_selection_table(t):
    names=['mzmin', 'mzmax', 'rtmin', 'rtmax', 'peakmap']
    for pstfx in t.supportedPostfixes(names):
        if len(pstfx):
            colnames=[''.join([n, pstfx]) for  n  in names]
            t.dropColumns(*colnames)
#################################################################################################

def get_typical_fwhm(t):
    return float(np.percentile(t.fwhm.values, 70))

##################################################################################################

def add_representing_mz(t, id_col='feature_id', value_col='intensity'):
    expr=t.getColumn
    t.addColumn('max_', expr(value_col).max.group_by(expr(id_col)), type_=float)
    t.updateColumn('mz_rep', (expr(value_col)==t.max_).thenElse(t.mz, 0.0), type_=float, 
                   format_='%.5f')
    t.replaceColumn('mz_rep', t.mz_rep.max.group_by(expr(id_col)), type_=float)
    t.dropColumns('max_')
###################################################################################################
from wtbox.collect_and_lookup import subtract_tuples, add_tuples

def calc_nsse(a,b):
    diff=subtract_tuples(a,b)
    added=add_tuples(a,b)
    numerator= squared_sum(diff)**2
    denominator=squared_sum(added)**2
    return numerator/denominator


def squared_sum(vec):
    return sum([v**2 for v in vec])
    
##############################################################################################
def integrate_tables(tables, integratorid='max'):
    integrate=emzed.utils.integrate
    # since multiprocessing is applied n_cpus of integrator must be set to 1
    params={'n_cpus': 1, 'integratorid':'max'}
    return wtbox._multiprocess.main_parallel(integrate, tables, kwargs=params)
###############################################################################################




def determine_ff_config_intensity_threshold(pm, sn=3):
    """
        Determines what is the minimal peak_intensity below a spectral peak is ignored. 
        The function determines baseline and noise level assuming that the baseline should contain
        the highest point density (J Ams Soc Mass Spectrom 2000, 11, 320-332).
        To this end we build a histogramm of all intensities over all spectra, the bin width of
        the histogramm is deteremined by the rule of Freedman und Diaconis. the mean intensity
        of the bin with highest abundance is said to be the baseline value and the fwhm of the
        histogramm is said to be the noise (more precisely : fwhm/2.5438 = sigma, sigma * 3=noise).
        
    """
    baseline, noise=determine_pm_noise_and_baseline(pm)
    return baseline+ sn*noise/2.3548 # fwhm/sigma = 2.3548
    

def determine_pm_noise_and_baseline(pm):
    intensities=_get_intensities(pm)
    return determine_noise(intensities)



def determine_noise(intensities):
    binwidth=get_binwidth(intensities)
    x,y=bin_sum(intensities, binwidth)
    return  _determine_noise_params(x,y)


#################################################################
def median_spectral_intensities(pm):
    field=[]
    for spec in pm.spectra:
        intensities=sorted(spec.peaks[:,1])
        field.append(intensities)
    field=zip(*field)
    return np.median(field, axis=0)
    


def mean_spectral_intensities(pm):
    field=[]
    for spec in pm.spectra:
        intensities=sorted(spec.peaks[:,1])
        field.append(intensities)
    field=zip(*field)
    return np.median(field, axis=0)
#####################################################################

    
def get_binwidth(intensities):
    # Regel nach Freedman und Diaconis
    # David Freedman, Persi Diaconis: n the histogram as a density estimator: 
    # L 2 {\displaystyle L_{2}} L_2 theory. 
    # In: Zeitschrift für Wahrscheinlichkeitstheorie und verwandte Gebiete. 
    # Band 57, Nr. 4, 1981, S. 453–476, doi:10.1007/BF01025868
    nominator=(2*(np.percentile(intensities,75)-np.percentile(intensities,25)))
    denominator=len(intensities)**(1/3.0)
    return int(round(nominator/denominator))



def _get_intensities(pm):
    intensities=[]
    for spec in pm.spectra:
        intensities.extend(spec.peaks[:,1])
    return sorted([v for v in intensities if v>0])

    

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
        

#def determine_general_noise(lookup_pm, mz, rt, bin_tols=(20.0, 1.0), rtwidth=300.0, mzwidth=25.0, 
#                            upper_noise=None):
#    intensities=read_out_intensities(lookup_pm, mz, rt, bin_tols, rtwidth, mzwidth, upper=upper_noise)
#    return determine_noise(intensities, binwidth=1000.0)


#def peak2noiselevel(pm, mz, rtmin, rtmax, binwidth=100.0):
#    intensities=[]
#    for spec in pm.spectra:
#        if rtmin <= spec.rt <=rtmax:
#            for mz_, intensity in spec.peaks:
#                if mz-binwidth<=mz_<=mz+binwidth:
#                    intensities.append(intensity)
#        if spec.rt>rtmax:
#                break
#    return intensities
#

def bin_sum(intensities, width=500):
    d=defaultdict(list)
    x_values=[]
    counts=[]
    for i in intensities:
        d[int(i/width)].append(i)
#    total=0
    for group in sorted(d.keys()):
        x_values.append(np.mean(d[group]))
#        total+=len(d[group])
#        counts.append(total)
        counts.append(len(d[group]))
    return x_values, counts


#def _get_pm_intensities(pm):
#    intensities=[]
#    for spec in pm.spectra[::4]:
#        [intensities.append(peak[-1]) for peak in spec.peaks if peak[-1]>0]
#    return intensities
#
#def _logbin_intensities(values):
#    import math
#    d1=defaultdict(int)
#    d2=defaultdict(list)
#    for value in values:
##        key=int(math.log(value,2))
#        key=int(value/100)
#        d1[key]+=1
#        d2[key].append(value)
#    return d1, d2

def _get_main_group(key2count, key2values):
    pairs=[(k, key2count[k]) for k in key2count.keys()]
    max_key=max(pairs, key=lambda v: v[1])[0]
    keys=[k for k  in key2count.keys() if k<=max_key]
    values=[]
    [values.extend(key2values[key]) for key in keys]
    return values


############################################################################
def collect_unique_peaks(tables, mztol, only_labeled=True, id_col='idms_pid'):
    collected=defaultdict(list)
    key2tol={'mz': mztol}
    for t in tables:
        delta_rt=t.rtmax.max()/5.0
        # we select only fully labeled species
        if only_labeled:
            t=t.filter(t.is_nl==False)
        __, uniques=wtbox._shift_rt_windows.find_overlapping_peaks(t, delta_rt, id_col)
        t=wtbox.utils.fast_isIn_filter(t, id_col, uniques)
        collected=wtbox.collect_and_lookup.table2lookup(t, key2tol,d=collected)
    return collected



############################################################################

def filter_min_specs(t, ff_config, min_specs):
    """ function filter_min_specs(t, ff_config, min_specs) determines number of spectra
        in longest mass trace within rtmin rtmax where the trace determination criterium 
        is defined by the ff_metabo config parameters. If the number of 
        spectra < min_spectra, the peak will be removed.
    """
    
    
    t=t.copy()
#    ff_config=kwargs['ff_config']
#    t.updateColumn('trace_length', t.apply(determine_peak_trace_length, (t.params, ff_config)), 
#                   type_=float)
    t.updateColumn('num_spectra', t.apply(determine_num_spectra_in_trace, (t.params, ff_config)),
                   type_=int)
    t=t.filter(t.num_spectra>=min_specs)               
    t.dropColumns('num_spectra')
    return t

def determine_num_spectra_in_trace(params, ff_config):
    pairs=zip(*params)
    intensities=params[1]
    min_frequency, max_outliers=get_args(ff_config)
    indices=_determine_peak_trace_bounderies(pairs, max_outliers, min_frequency)
    return max_number_of_specs(indices, intensities)


def get_args(ff_config):
    mode=ff_config['mtd_trace_termination_criterion']
    if mode=='outlier':
        return None, ff_config['mtd_trace_termination_outliers']
    if mode=='sample_rate':
        return ff_config['mtd_min_sample_rate'], None
    assert False, 'mtd_trace_termination_criterion must be outlier or sample_rate and not %s' %mode


def _determine_peak_trace_bounderies(pairs, max_outliers, min_frequency):
    index=_get_start_index(pairs)
    sections=[(index, index)]
    while index<len(pairs):
        if max_outliers:
            bounds=_determine_bounderies_outlier(pairs, index, max_outliers)
        elif min_frequency:
            bounds=_determine_bounderies_frequency(pairs, index, min_frequency)
        sections.append(bounds)
        index=bounds[1]
        if index<len(pairs):
            index=_get_start_index(pairs, index)
    return sections


def _determine_bounderies_outlier(pairs, index, max_outliers):
    counter=0
    start=index
    index
    while index<len(pairs):
        if pairs[index][1]==0:
            counter+=1
        else:
            counter=0
        index+=1
        if counter==max_outliers:
            break
    return start, index


def _determine_bounderies_frequency(pairs, index, min_frequency):
    counter=0
    start=index
    num_spectra=1.0
    while index<len(pairs):
        if pairs[index][1]>0:
            counter+=1
        index+=1
        if float(counter)/num_spectra<min_frequency:
            break
#        length=pairs[index][0]-pairs[start][0]
        num_spectra+=1.0
    return start, index
    

def _get_start_index(pairs, i=0):
    while i<len(pairs)-1:
        __, intensity=pairs[i]
        if intensity:
            return i
        if len(pairs)==i-1:
            return i
        i+=1
    return i+1
    

def max_number_of_specs(indices, intensities):
    return max([_number_of_specs(intensities, bounds) for bounds in indices])


def _number_of_specs(intensities, bounds):
    start, stop=bounds
    return len(np.argwhere(intensities[start:stop]>0))
    
#def filter_min_specs(f, min_specs=3):
#    def num_specs(params):
#        __, ints=params
#        return len(set(ints))-1
#    f.updateColumn('min_specs', f.apply(num_conseq_specs,(f.params, min_specs)), type_=bool)
#    f1=f.filter(f.min_specs==True)
#    f.dropColumns('min_specs')
#    f1.dropColumns('mins_specs')
#    return f1
#
#def num_conseq_specs(params, min_specs=3):
#    __, ints=params
#    counts=0
#    for v in ints:
#        if v>0:
#            counts+=1
#        else:
#            counts=0
#        if counts>= min_specs:
#            return True
#    return False
    

################################################################################

    
def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    y=_savitzky_golay(y, window_size, order, deriv=0, rate=1)
    pos=np.argwhere(y<0)
    np.put(y, pos, 0.0)
    return y

def _savitzky_golay(y, window_size, order, deriv=0, rate=1):
    r"""Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
    The Savitzky-Golay filter removes high frequency noise from data.
    It has the advantage of preserving the original shape and
    features of the signal better than other types of filtering
    approaches, such as moving averages techniques.
    Parameters
    ----------
    y : array_like, shape (N,)
        the values of the time history of the signal.
    window_size : int
        the length of the window. Must be an odd integer number.
    order : int
        the order of the polynomial used in the filtering.
        Must be less then `window_size` - 1.
    deriv: int
        the order of the derivative to compute (default = 0 means only smoothing)
    Returns
    -------
    ys : ndarray, shape (N)
        the smoothed signal (or it's n-th derivative).
    Notes
    -----
    The Savitzky-Golay is a type of low-pass filter, particularly
    suited for smoothing noisy data. The main idea behind this
    approach is to make for each point a least-square fit with a
    polynomial of high order over a odd-sized window centered at
    the point.
    Examples
    --------
    t = np.linspace(-4, 4, 500)
    y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
    ysg = savitzky_golay(y, window_size=31, order=4)
    import matplotlib.pyplot as plt
    plt.plot(t, y, label='Noisy signal')
    plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
    plt.plot(t, ysg, 'r', label='Filtered signal')
    plt.legend()
    plt.show()
    References
    ----------
    .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
       Data by Simplified Least Squares Procedures. Analytical
       Chemistry, 1964, 36 (8), pp 1627-1639.
    .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
       W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
       Cambridge University Press ISBN-13: 9780521880688
    """
    import numpy as np
    from math import factorial

    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError, msg:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m[::-1], y, mode='valid')





def fast_in_range(values, lower, upper, key=None, depth=10, sorted_=True):
    if not sorted_:
        values.sort(key=key)
    start=_get_index(values, lower, True, depth)
    end=_get_index(values, upper, False, depth)
    return [v for v in values[start:end+1]]

def _get_index(values, value, lower=True, depth=3):
    i=0
    loop=0
    low=0
    up=len(values)-1
#    _values=copy(values)
    assert values[0]<=value<=values[up]
    while True:
        i=(up+low)/2
        if values[i]<value:
            low=i
        if values[i] >value:
            up=i
        elif values[i]==value:
            return i
        if loop<depth:
            loop+=1
        if loop==depth:
            return low if lower else up
#############################################################################################
from pylab import plot, figure, show, title
from itertools import product


    
import wtbox.collect_and_lookup as cl
import wtbox.utils as ut

def pm_intensity2lookup(pm, rtwidth, mzwidth, upper_limit=1e5):
    print 'converting peakmap to lookup ...'
    d=defaultdict(list)
    tols=(rtwidth, mzwidth)
    ut.show_progress_bar(pm.spectra, _readout_spectrum, args=(d, tols, upper_limit), in_place=True)
    return d


def _readout_spectrum(spectrum,  d, tols, upper):
    rt=spectrum.rt
    for mz, intensity in spectrum.peaks:
        if intensity<upper:
           key=cl.calculate_key((rt, mz), tols)
           d[key].append(intensity)



def read_out_intensities(lookup, mz, rt, bin_tols, rttol, mztol, upper=None):
    intensities=[]
    lower_key=cl.calculate_key((rt-rttol, mz-mztol), bin_tols)
    upper_key=cl.calculate_key((rt+rttol, mz+mztol), bin_tols)
    lower_rt, lower_mz=lower_key
    upper_rt, upper_mz=upper_key
    rt_range=range(lower_rt, upper_rt+1)
    mz_range=range(lower_mz, upper_mz+1)
    for key in list(product(rt_range, mz_range)):
        if lookup.has_key(key):
            if not upper:
                intensities.extend(lookup.get(key))
            else:
                intensities.extend([v[-1] for v in lookup.get(key) if v[-1]<=upper])
    return intensities

def _readout(d, key, rt, mz, tols):
    readout=[]
    for rt_, mz_, int_ in d.get(key):
        if cl.fullfilled((rt, mz), (rt_, mz_), tols):
            readout.append(int_)
    return set(readout)
        
        
def test_noise_profile(d, bin_width=(5.0, 50.0), rttol= 20.0, mztol=125.0, mz_key=3):
    keys=sorted(d.keys(), key=lambda v: v[0])  
    keys=sorted(keys, key=lambda v: v[1])
    rts=[]
    drt, dmz=bin_width
#    pairs=[]
    noises=[]
    for rt_key, mz_key in [k for k in keys if k[1]==mz_key]:
        try:
            mz=mz_key*dmz
            rt=rt_key*drt
            noises.append(determine_noise(d, mz, rt, bin_width, rttol, mztol, None)[1])
            rts.append(rt/60.0)
        except:
            pass
    rtrange=int(rttol/drt)*drt
    mzrange=(int((mz-mztol)/dmz)*dmz, int(((mz+mztol)/dmz)+1)*dmz)
    header='mzrange = %r, rtwidth= %.1f s' %(mzrange, rtrange)
    figure()
    title(header)
    plot(rts, noises)
    plot(rts, noises, '*')
    show()
    
    
def calculate_signal_to_noise(t, lookup, bin_tols=(5.0, 300.0), size=21):
    def _calculate_sn(mz, rt, params, d=lookup, bin_tols=bin_tols):
        baseline, noise= determine_general_noise(d, mz, rt, bin_tols, rtwidth=60.0, mzwidth=0.0)
        rts, intensities=params
        if len(intensities)<=size:
            delta=size-len(intensities)
            delta=delta if delta/3.0==int(delta/3.0) else delta + 1
            size_=size-delta
        else:
            size_=size
        smoothed=savitzky_golay(intensities, size_, 2)
        int_signal=max(smoothed)
        return (int_signal - baseline)/noise
    t.updateColumn('S_N_ratio', t.apply(_calculate_sn, (t.mz, t.rt, t.params)), type_=float)




#########
import itertools

def rt_consistency(t, group_id='isotope_cluster_id', width_col='fwhm', denominator=4.0):
    """
    Function calculates peakwise rt tolerances for grouped peaks based on their individual 
    rt tolerances (fwhm/denominator) and ungroups peaks for which rt_tolercance criterium 
    is not fullfilled 
    """
    # sort by intensity
    t.sortBy('area', ascending=False)
    id_=t.getColumn(group_id).max()
    t.updateColumn('limit', t.getColumn(width_col)/denominator, type_=float)
    groups=[]
    for group in t.splitBy(group_id):
        i=0
        current_id=group.getColumn(group_id).uniqueValue()
        while len(group):
            group.replaceColumn(group_id, current_id, type_=int)
            pairs=zip(group.rt, group.limit)
            combs=itertools.product(pairs[:i+1], pairs[i:])
            combs=check_combs(combs)
            group.updateColumn('keep', combs, type_=bool)
            group.sortBy('keep')
            try:
                group, checked=group.splitBy('keep')
                groups.append(checked)
            except:
                assert all(group.keep.values), 'This is an error that should not occur.'\
                ' Code is sh.t !!'
                groups.append(group)
                # end while loop
                group=[]
            current_id=id_+1
    
    return emzed.utils.stackTables(groups)
            
            
def check_combs(combs):
    return [_check(comb) for comb in combs]
    

def _check(comb):
    return abs(comb[0][0]-comb[1][0])<= min(comb, key=lambda v: v[1])[1]
     

############################################################################################
#################################################################################################

def c13_count(t):
    t.updateColumn('mz0', t.mz.min.group_by(t.idms_pid), type_=float)
    t.updateColumn('mzul', t.mz.max.group_by(t.idms_pid), type_=float)
    t.updateColumn('num_c', t.apply(count_carbons, (t.mz0, t.mzul, t.z)), type_=tuple)
    t.dropColumns('mz0', 'mzul')


def count_carbons(mz0, mzul, z):
    delta_c=emzed.mass.C13-emzed.mass.C
    num_cs=[]
    zs=[z] if z else [1,2,3]
    for z_ in zs:
        num_c=int(round((mzul-mz0)*z_/delta_c, 1))
        num_cs.append(num_c)
    return tuple(num_cs)

################################################################################################

def charge_assign_event(t, text, colname='charge_assigned_by'):
    id2text={id_:text for id_, z in zip(t.id, t.z) if z}
    update_event(t, id2text, 'id', colname)

def update_event(t, id2text, id_col, target_col, insertAfter=None):
    expr=t.getColumn
    if not t.hasColumn(target_col):
        t.addColumn(target_col, '', type_=str, insertAfter=insertAfter)
    t.updateColumn(target_col, 
                   t.apply(_add_event, (expr(id_col), id2text, expr(target_col))), type_=str)


def _add_event(id_, id2text, event):
    assert isinstance(event, str)
    text=id2text.get(id_)
    if text:    
        events=[event] if len(event) else []
        events.append(text)
        return '; '.join(events)
    return event


##########################################################################################
# Functions to  handle openms tranformation objects
def save_transformation(trafo, path):
    t_file=pyopenms.TransformationXMLFile()
    t_file.store(path, trafo)


def load_transformation(path):
    t_file=pyopenms.TransformationXMLFile()
    trafo=pyopenms.TransformationDescription()
    t_file.load(path, trafo, True) # True is a flag that got lost while code wrapping
    return trafo
    

def transform_peakmap_rt(peakmap, transformation):
    """
    """
    for spec in peakmap.spectra:
        spec.rt=transformation.apply(spec.rt)
    peakmap.meta['aligned']=True
    return peakmap

     