"""Random number generators as Python generator functions."""

import numpy as np
import scipy.stats as stats

__all__ = ['expon', 'gamma', 'norm', 'truncnorm']

batch_size = 100

def expon(mean, seed):
    '''Returns a generator function for an i.i.d random variate from an
    exponential distribution with the given mean.'''
    rv = stats.expon(scale=mean)
    rv.random_state = np.random.RandomState(seed)
    while True:
        for x in rv.rvs(batch_size):
            yield x

def gamma(a, scale, seed):
    '''Returns a generator function for an i.i.d. random variate from a
    gamma distribution, where a is the shape parameter (when a is an
    integer, gamma reduces to the Erlang distribution; and when a = 1
    to the exponential distribution).'''
    rv = stats.gamma(a, scale)
    rv.random_state = np.random.RandomState(seed)
    while True:
        for x in rv.rvs(batch_size):
            yield x

def norm(mean, stdev, seed):
    '''Returns a generator function for an i.i.d. random variate from a
    normal distribution with teh given mean and standard deviation.'''
    rv = stats.norm(loc=mean, scale=stdev)
    rv.random_state = np.random.RandomState(seed)
    while True:
        for x in rv.rvs(batch_size):
            yield x
            
def truncnorm(a, b, seed):
    '''Returns a generator function for an i.i.d. random variate from a
    normal distribution truncated to the range between a and b.'''
    rv = stats.truncnorm(a, b)
    rv.random_state = np.random.RandomState(seed)
    while True:
        for x in rv.rvs(batch_size):
            yield x
