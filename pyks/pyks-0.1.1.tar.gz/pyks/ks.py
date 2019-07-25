'''Calculation KS statistic for a model.'''

import pandas as pd
import numpy as np

def summary(df, n_group = 10):
    '''Calculation KS statistic
    Inspired by one WenSui Liu's blog at 
    https://statcompute.wordpress.com/2012/11/18/calculating-k-s-statistic-with-python/

    Parmaters
    ---------
    df: pandas.DataFrame
        with M x N size.
        M length is the number of bins.
        N measures the number of metrics related to KS.
    n_group: float
             The number of cutted groups.

    Returns
    -------
    agg2  : The DataFrame return with KS and related metrics.'''

    df["bad"] = 1 - df.good
    df['bucket'] = pd.qcut(df.score, n_group, duplicates = 'drop')

    grouped = df.groupby('bucket', as_index = False)

    agg1 = pd.DataFrame()
    agg1['min_scr'] = grouped.min().score
    agg1['max_scr'] = grouped.max().score
    agg1['bads'] = grouped.sum().bad
    agg1['goods'] = grouped.sum().good
    agg1['total'] = agg1.bads + agg1.goods

    agg2 = (agg1.sort_values(by = 'min_scr')).reset_index(drop = True)
    agg2['odds'] = (agg2.goods / agg2.bads).apply('{0:.2f}'.format)
    agg2['bad_rate'] = (agg2.bads / agg2.total).apply('{0:.2%}'.format)
    agg2['ks'] = np.round(((agg2.bads / df.bad.sum()).cumsum() - (agg2.goods / df.good.sum()).cumsum()), 4) * 100
    flag = lambda x: '<----' if x == agg2.ks.max() else ''
    agg2['max_ks'] = agg2.ks.apply(flag)
    
    return agg2
