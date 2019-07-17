# -*- coding: utf-8 -*-
"""
Created on Thu Aug 06 14:38:01 2015

@author: pkiefer
"""
import numpy as np
import math
from scipy.optimize import curve_fit
from random import uniform
from table_operations import update_column_by_dict as _update_col#, split_table_by_columns
###############################################################################################
# USEFUL FUNCTIONS fur curve fitting

def pt1(t, k, T):
    # first order kinetics
    return k*(1-np.exp(-t/T))

def decay(t, k, T):
    return k*np.exp(-t/T)

def logistic(t,T,k, y0):
    # source: http://en.wikipedia.org/wiki/Logistic_function
   return (k*y0*np.exp(t*T))/(k+y0*np.exp(t*T)-y0)

def double_logistic_model (t, y0, ymax, k1,T1, k2,T2):
    return y0+(ymax-y0)*((1+np.exp(-k1*(t-T1)))**(-1) + (1+np.exp(k2*(t-T2)))**(-1)-1)

def dbl_logistic_model (t, y0, ymax, k1,T1, k2,T2):
    return y0+(ymax-y0)*((1+np.exp(-k1*(t-T1)))**(-1) + (1+np.exp(k2*(t-T2)))**(-1)-1)

def double_pt1_model(t,k1, k2, T1,T2, c):
        return k1*(1-np.exp(-t/T1))-k2*(1-np.exp(-t/T2))+c
        
def weibull(t, ym, y0, k, g):
    return ym-(ym-y0)*np.exp(-(k*t)**g)

def linear(t,m, b):
    return m * t + b

def gauss(t, sigma, rt):
    from math import sqrt, exp, pi
    return 1/(sigma*sqrt(2*pi))*exp(-(t-rt)**2/(2*sigma**2))


def emg_exact(rts, h, z, w, s, sqrt_two_pi=math.sqrt(math.pi), sqrt_2=math.sqrt(2.0), exp=np.exp):
        # avoid zero division
        if s * s == 0.0:
            s = 1e-6
        inner = w * w / 2.0 / s / s - (rts - z) / s
        # avoid overflow: may happen if _fun_eval is called with full
        # rtrange (getSmoothed...), and s is small:
        inner[inner > 200] = 200
        nominator = np.exp(inner)
        # avoid zero division
        if w == 0:
            w = 1e-6
        denominator = 1 + exp(-2.4055 / sqrt_2 * ((rts - z) / w - w / s))
        return h * w / s * sqrt_two_pi * nominator / denominator  
    
def savitzky_golay(y, window_size, order, deriv=0, rate=1):
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
    result=np.convolve( m[::-1], y, mode='valid')
    return result.tolist()
        
###############################################################################################
# intial value generators

def generate_initial_pt1(x,y):
    for k in np.linspace(-max(y), max(y),4):
        for T in np.linspace(0,max(x), 4):
            yield k, T

def generate_initial_logistic(x,y):
    for y0 in np.linspace(min(y), max(y), 3):
        for k in np.linspace(max(y), min(y), 3):
            for T in np.linspace(min(x), max(x), 3):
                yield T, k, y0


def generate_initial_double_log(x,y):
    for i  in range(2000):
        k1=uniform(-3*max(y), 20*max(y))
        k2=uniform(-1,3)
        T1=uniform(-1000, max(y)/0.5)
        T2=uniform(0.5,max(y)*3.0)
        yield min(y), max(y),k1,k2,T1,T2


def generate_inital_pt1_pt1(x,y):
    for i  in range(100):
        k1=uniform(-3*max(y), 20*max(y))
        k2=uniform(-1,3)
        T1=uniform(-1000, max(y)/0.5)
        T2=uniform(0.5,max(y)*3.0)
        c=uniform(-2, 100)
        yield k1,k2,T1,T2,c

def generate_initial_weibull(x,y):
   for y0 in np.linspace(min(y), max(y), 3):
       for ym in np.linspace(min(y), max(y), 3):
           for k in np.linspace(0.01, 5, 3):
               for g in np.linspace(0.1, 5, 3):
                   yield ym, y0, k, g
                   
def generate_initial_linear(x,y):
    for m in np.linspace(0.0,1,10):
        for b in np.linspace(0.001 ,1,10):
            yield m, b
################################################################################################
# CURVE FITTING

def calculate_nrmse(x,y, fun, params):
        if params!=None:
            rmse=np.sqrt(sum([(fun(x[i], *params)-y[i])**2 for i in range(len(x))])/len(x))
            return rmse/(max(y)-min(y)) if max(y)!= min(y) else 0.0
            
def fit_curve(x, y, fun, params, remove, sigma=None):
#    import pdb; pdb.set_trace()
    try:
        popt, pcov=curve_fit(fun, np.array(x), np.array(y), p0=params, sigma=sigma, maxfev=10000)
        x,y,crit=remove_outlier(x,y,fun, popt)
        if all(crit) and remove:
            popt, pcov=curve_fit(fun, np.array(x), np.array(y), p0=params, maxfev=10000)
        perr =np.sqrt(np.diag(pcov)).tolist()
        perr=[float(v) for v in perr]
        if remove:
            return popt, perr, crit
        else:            
            return popt, perr, (None, None)
    except:
        return None, None, (None, None) #outlier is x y pair


def remove_outlier(x,y, fun, popt, f=3.0):
    crit=(None, None)
    pos=range(len(x))
    exclude=None
    y_=[fun(v, *popt) for v in x]
    diff=[y[i]-y_[i] for i in pos]
    lower = np.mean(diff) - f*np.std(diff)
    #define outliers
    crit1=[i for i in pos if diff[i]<lower ]
    # values below close to not labeled
    if len(crit1):
        exclude=min(crit1)
        crit= (x[exclude], y[exclude])
#        crit=True
    return [x[i] for i in pos if i != exclude], [y[i] for i in pos if i != exclude], crit
           



def get_fun2generator():
    return {'pt1': generate_initial_pt1,
            'logistic': generate_initial_logistic,
            'dbl_logistic_model': generate_initial_double_log,
            'double_logistic_model': generate_initial_double_log,
            'double_pt1_model': generate_inital_pt1_pt1,
            'weibull': generate_initial_weibull,
            'linear' : generate_initial_linear,
            'decay':generate_initial_pt1}
            


def main_curve_fitting(x, y, fun, params=None, sigma=None, max_nrmse=1e-2, max_iterations=10, 
                       remove_outlier=True):
    """ 
    main_curve_fitting(x, y, fun, **kwargs) determines fitting parameters for iterables
    x and y, with y=fun(x). **kwargs: 
    - params: iterable of initial values for fitting function fun, in case of fittinh functions
      of the fitting module value can ve
      if None, parameters are provided by generator functions  if fitting functions is defined
      in the fiotting moduel (e.g. `pt1`, `logistic`, `dbl_logistic_model`, ...), else AssertionError 
      raises.
    - max_nrmse: fitting  routine will be aborted, if nrmse of fit < mac_nrmse
    - max_iterations: maximum numvber fitting operation, global abortion criteria. If reached 
      before max_nrmse criterium was fullfilled, best fitting results are returned.
    """
#    import pdb
#    pdb.set_trace()
    x=np.array(x)
    y=np.array(y)
    if not params:
        params=get_fun2generator().get(fun.__name__)(x,y)
        assert 'parmeter_generator for function %s is missing. Please choose alternative fitting'\
        'function or provide initial fitting parameters' % fun.__name__
    pairs=[]
    count=0
    while True:
        try:
            param=params.next()
        except:
            if isinstance(params, list):
                if count<len(params):
                    param=params[count]
                else:
                    break
                    
            else:
                break
        ' provided as list or tuple'
        popt, perr, outlier =fit_curve(x, y, fun, param, remove_outlier)
        nrmse=calculate_nrmse(x,y,fun, popt)
        if nrmse>=0:
            pairs.append((list(popt), perr, outlier, nrmse))
            if nrmse<=max_nrmse:
                break
        count +=1
        if max_iterations <= count :
            break
    print 'total number of iterations: ', count
    if len(pairs):
        pairs=tuple(pairs)
        return min(pairs, key=lambda v: v[-1])
    else:
        print 'no fit possible with fun %s' %fun.__name__


def select_best_fit(xy_pairs, funs, params=None, max_nrmse=1e-2, max_iterations=10, 
                    remove_outlier=True):
    """
    """
    x,y =xy_pairs
    dic=dict(max_nrmse=max_nrmse, max_iterations=max_iterations)
    if params:
        assert len(params)==len(funs)
        numbers=range(len(funs))
        result=[(main_curve_fitting(x, y, funs[i], params[i],**dic), funs[i]) for i in numbers]
#        print result
    else:
        result=[(main_curve_fitting(x, y, fun,**dic), fun) for fun in funs]  
#        print result
#    import pdb; pdb.set_trace()
    return _select(result)


def _select(fittings):
    fittings=[v for v in fittings if v[0]]
    for line in fittings:
        if line:
            print 'function: %s, ' %line[1].func_name, 'obtained nrmse: %2.2e' %line[0][-1] 
    try:
        selected=min(fittings, key=lambda v: v[0][-1]) 
        print 'selected fitting function: %s' %selected[1].__name__
        print
        return selected[0][0], selected[0][1], selected[0][2], selected[0][3], selected[1]
    except:
        print 'WARNING no fit possible!'
        print
        return None, None, (None,None), None, None
        
       
#############################################################################################
from _multiprocess import main_parallel

def curve_fitting_from_table(t, funs, fun_params=None, id_cols=('feature_id',), time_col='time', 
                             value_col='mi_fraction', max_nrmse=0.05, max_iterations=10,
                        missing_tp_as_0= False, remove_outlier=False, selected_raws='selected'):
    """
    *In place curve_fitting_from_table(t, funs, fun_params=None, id_cols=('feature_id',), 
    time_col='time', value_col='mi_fraction', max_nrmse=0.05, max_iterations=10,
     missing_tp_as_0= False, remove_outlier=False, selected=False) applies fitting functions funs
     to table and selects function with best fitting result based on nmrse. Columns 'fit_pararms'
     (calculkated parameters of fitting function ),' fit_stds' (standard devieation of fitting 
     function), 'fit_nrmse' (normalized root mean square error), and fit_fun (fitting function) 
     are added. If remove outlier==True, column outlier 
     containing remvoved outlier (x,y) will be add. Attributes:
    - funs: list of functions for fitting 
    - fun_params: initial fitting function parameters. if None, parameters are provided by 
      generator functions in case fitting functions is defined in the fitting moduel 
      (e.g. `pt1`, `logistic`, `dbl_logistic_model`, ...), else AssertionError raises.
    - id_cols: Tuple defining subtable for fitting. It allows combining different columns 
      to define subgroup. Example: To fita all isotpologues of a feature you can combine 
      the two columns as identifier by id_cols=(‘feature_id’, ‘mi’)
    - time_col: Defines column with x- values (time)
    - value_col: Defines y values for plot
    - max_nrmse: Maximal allowed nrmse value to accept a fit
    - max_iterations: number of allowed iterations for nrnmse minimization
    - missing_tp_as_0: replaces None value by zero
    - remove_outlier: Removes (x, y) pair from fit if deviation between fitted and existing values
      exhibits 3 times standard deviation
   
    
    
    """
    postfix_cols=list(id_cols)
    postfix_cols.append(value_col)
    pstfx=t.supportedPostfixes(postfix_cols)
    assert len(pstfx)==1, 'Postfixes of columns %s are not identic !!' %', '.join(postfix_cols)
    pstfx=pstfx[0]
    id_cols_=[t.getColumn(col+pstfx).values for col in id_cols]
    tuples=zip(*id_cols_)
    t.addColumn('splitter', tuples, type_=tuple)
    time_courses=filter_selected(t, filter_col=False)
    time_points=get_all_time_points(t, missing_tp_as_0)
    col_params=[time_col, value_col, id_cols, pstfx, time_points]
    fit_params=[funs, fun_params, max_nrmse, max_iterations, remove_outlier]
    params=[[col_params, fit_params]] # due to unpacking in multi.nested
    pairs=main_parallel(process_fitting, time_courses, args=params)
    id2params={p[0]: p[1] for p in pairs}
    return _add_fitting_results_to_table(t, value_col, pstfx, id2params, remove_outlier)
#    t.dropColumns('splitter', tuples, type_=tuple)
  

def filter_selected(t, filter_col='selected'):
    time_courses=[_filter(v, filter_col) for v  in t.splitBy('splitter')]
    return [v for v  in time_courses if len(v)]


def _filter(t, filter_col):
    if t.hasColumn(filter_col):
        assert all([isinstance(v, bool) for v in t.getColumn(filter_col).values]), 'filter_col'\
                ' values must be of type bool!'
        return t.filter(t.getColumn(filter_col)==True)
    return t
    
    
def process_fitting(time_course, params):
    print 'start fitting...'
    # extract value cols
    time_col, value_col, id_cols, pstfx, time_points=params[0]
    splitter=time_course.splitter.uniqueValue()
    time=time_course.getColumn(time_col).values
    values=time_course.getColumn(value_col+pstfx).values
    xy_pairs=remove_redundance(time, values)
    xy_pairs=add_missing_time_points(xy_pairs, time_points)
    id_=', '.join(id_cols)
    ids_=', '.join([str(v) for v in splitter])
    print 'fitting values from column %s with id cols %s: %s' %(value_col, id_, ids_)
    fit_res=select_best_fit(xy_pairs, *params[1])
    fit_params, fit_std, outlier, nrmse, fun=fit_res
    return splitter, (fit_params, fit_std, outlier, nrmse, (fun,))

  
def remove_redundance(x,y):
    pairs=list(set(zip(x,y)))
    pairs.sort(key=lambda v: v[0])
    return [v[0] for v in pairs], [v[1] for v in pairs]


def get_all_time_points(t, time_col, add_=False):
    return set(t.getColumn(time_col).values) if add_ else []
    

def add_missing_time_points(xy_pairs, time_points):
    for tp in time_points:
        if tp not in [v[0] for v in xy_pairs]:
            xy_pairs.append((tp, 0.0))
    return xy_pairs
            
def _add_fitting_results_to_table(t, value_col, pstfx, id2params, remove_outlier):
#    print id2params
    t=_update_col(t, 'temp', 'splitter', id2params)    
    t.updateColumn( '_'.join([value_col,'fit_params'])+pstfx, t.temp.apply(lambda v: v[0]), 
                   type_=tuple)
    t.updateColumn( '_'.join([value_col,'fit_stds'])+pstfx, t.temp.apply(lambda v: v[1]), 
                   type_=tuple)   
    if remove_outlier:
        t.updateColumn( '_'.join([value_col,'outlier'])+pstfx, t.temp.apply(lambda v: v[2]), 
                       type_=tuple, format_='%s')   
    t.updateColumn( '_'.join([value_col, 'fit_nrmse'])+pstfx, t.temp.apply(lambda v: v[-2]), 
                   type_=float, format_='%2.2e')
    t.updateColumn( '_'.join([value_col,'fit_fun'])+pstfx, t.temp.apply(lambda v: v[-1]), 
                   type_=tuple,
                   format_=None)
    def fun(v):
        try:
            return v[-1][0].__name__
        except:
            return ''
    t.updateColumn( '_'.join([value_col,'fit_fun_name']) + pstfx, t.temp.apply(fun), 
                   type_=str,  format_='%s')
    t.dropColumns('temp', 'splitter')        
    return t

#########################################################
def help_test():
    import pylab as pl
    x=np.linspace(0,10, 50)
    y=[logistic(v+uniform(-0.008,0.08),2, 3.2,0.5) for v in x]
    pl.figure()
    i=0
    for fun in [pt1, logistic, dbl_logistic_model, double_pt1_model]:
        i+=1
        params, nrmse=main_curve_fitting(x,y,fun, max_iterations=100, max_nrmse=8e-3)
        print fun.__name__, params, nrmse
        y_fit=[fun(v, *params) for v in x]
        pl.subplot(4,1,i)
        pl.plot(x,y, '*')
        pl.plot(x,y_fit, 'b')
    pl.show()
        
