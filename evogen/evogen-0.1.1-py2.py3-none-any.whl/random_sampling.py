import math
import numpy as np
from scipy.stats import binom

def binomial_prob_func(n, r, p, explicit=False):
    """ The explicit version of the probability mass function for bionomial 
    random variables. """
    if explicit:
        if isinstance(r, (list, np.ndarray)):
            raise TypeError('Wrong type of "r" parameter. If you wish to input '\
                'array-like type of "r" parameter, please set False to "explicit".')

        return nCr(n, r) * p ** r * (1-p) ** (n-r)
    else:
        if isinstance(r, (list, np.ndarray)):
            assert len(r) == n+1, f'Wrong array length: {len(r)}. Expected {n+1}.'
            assert max(r) == n, f'Wrong maximum of # success: {max(r)}, '\
                'Expected less than "n": {n}.'

        return binom.pmf(r, n, p)

def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)
