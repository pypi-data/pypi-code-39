import numpy as np
from numpy import ndarray

import pandas as pd


def _get_z_scores(
    x: pd.DataFrame, 
    window: int,
    min_periods: int,
    reduce_func: str
) -> np.ndarray:

    reduce_mapping = {
        'median': lambda x: x.median(),
        'mean': lambda x: x.mean()
    }

    r = x.rolling(
        window=window,
        center=False,
        min_periods=min_periods
    )
    means = reduce_mapping[reduce_func](r)
    stds = r.std(ddof=0)

    z_scores = (x - means) / (stds + 1e-6)
    return z_scores


def remove_outliers(
    df: pd.DataFrame,
    window_size: int,
    sigma_threshold: int = 3,
    min_periods: int = 1,
    reduce_func: str = 'median',
    return_z_scores: bool = False
) -> pd.DataFrame:
    """
        Remove outliers using z-score.

        Inputs:
        - df: DataFrame with columns where outliers will be removed.
        - window_size: Sliding window size to calculate z-score.
        - sigma_threshold: point will be removed if |z-score| > sigma_threshold.
        - min_periods: Minimum number of observations in window required 
            to have a value (otherwise result is NA).
        - reduce_func: Function to calculate mean. Can be mean or median.
        - return_z_scores: Whether to return z-scores.
    """

    # Get z-scores
    z_scores = _get_z_scores(
        df,
        window_size,
        min_periods,
        reduce_func
    )

    # Filter points where z_score > sigma_threshold
    df_no_outliers = df.mask(
        abs(z_scores) > sigma_threshold,
        np.nan
    )

    if return_z_scores:
        return df_no_outliers, z_scores
    
    return df_no_outliers


def fill_blanks(
    df: pd.DataFrame,
    method: str = 'ff'
) -> pd.DataFrame:
    """
        Fill NA values.

        Inputs:
        - df: DataFrame with columns to fill.
        - method: Filling strategy. 
            ff -> forward fill
            li -> linear interpolation
            zeros -> fill with zeros
    """

    strategy_mapping = {
        'ff': lambda df: df.fillna(method='ffill'),
        'li': lambda df: df.interpolate(),
        'zeros': lambda df: df.fillna(0)
    }

    if method not in strategy_mapping.keys():
        raise ValueError(f'method: {method} unknown')

    return strategy_mapping[method](df)


def _simple_exp_smooth(
    s: pd.Series,
    alpha: float
) -> pd.Series:

    x = np.zeros(len(s))
    x[0] = s[0]
    for i in range(1, len(s)):
        x[i] = alpha * s[i] + (1- alpha)*x[i-1]
    
    return x


def _double_exp_smooth(
    s: pd.Series,
    alpha: float,
    beta: float
) -> pd.Series:

    x = np.zeros(len(s))
    x[0] = s[0]
    b = s[1] - s[0]

    for i in range(1, len(s)):
        x[i] = alpha * s[i] + (1- alpha)*(x[i-1] + b)
        b = beta*(x[i] - x[i-1]) + (1-beta)*b
    
    return x


def smooth_noise(
        s: pd.Series,
        method: str = 'simple_exp',
        alpha: float = 0.95,
        beta: float = 0.3
) -> pd.Series:
    """
        Smooth time series.

        Inputs:
        - s: pandas.Series to smooth.
        - method: Smoothing method. 
            simple_exp -> simple exponential smoothing
            double_exp -> double exponential smoothing
    """

    if method == 'simple_exp':
        return _simple_exp_smooth(s, alpha)
    elif method == 'double_exp':
        return _double_exp_smooth(s, alpha, beta)
    
    raise ValueError(f'method: {method} unknown')