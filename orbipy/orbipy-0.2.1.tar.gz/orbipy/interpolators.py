# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 12:34:13 2019

@author: stasb
"""

import math
import numpy as np
#from scipy.interpolate import interp1d

class base_interpolator:
    '''
    Root class for all interpolators.
    Calculates mapping from [A, B] to [a, b]
    '''
    
    def __init__(self, A=0.0, B=1.0, a=0.0, b=1.0):
        self.A = A
        self.B = B
        self.a = a
        self.b = b
        
    def __call__(self, x):
        pass
    
    def AB(self, n):
        return np.linspace(self.A, self.B, n)
    
    def ab(self, n):
        return self(self.AB(n))
    
class linear_interpolator(base_interpolator):        
    def __init__(self, A=0.0, B=1.0, a=0.0, b=1.0):
        self.d = B-A
        if math.fabs(self.d) < 1e-16:
            raise RuntimeError('A and B are very close, B-A=%f'%self.d)
        super().__init__(A, B, a, b)
        
    def __call__(self, x):
        coef = (x - self.A) / self.d
        return self.a*(1-coef)+self.b*coef
    
class log_interpolator(base_interpolator):
    def __init__(self, A=0.0, B=1.0, a=0.0, b=1.0, N=math.exp(1.0)):
        d = a-b
        if math.fabs(d) < 1e-16:
            raise RuntimeError('a and b are very close, a-b=%f'%d)
        super().__init__(A, B, a, b)
        self.N_ab = N**(a-b)
        self.x0 = (A-self.N_ab*B)/(self.N_ab-1)
        self.logN = math.log(N)
        self.y0 = a - math.log(A+self.x0)/self.logN
        
    def __call__(self, x):
        return np.log(x+self.x0)/self.logN+self.y0

class flipY_interpolator(base_interpolator):
    def __init__(self, intrp):
        if not isinstance(intrp, base_interpolator):
            raise TypeError('This object is not base_interpolator inherited: %r'%intrp)
        self.intrp = intrp
        
    def __getattr__(self, attr):
        return getattr(self.intrp, attr)

    def __call__(self, x):
        return self.a+self.b-self.intrp(x)
    
class flipX_interpolator(base_interpolator):
    def __init__(self, intrp):
        if not isinstance(intrp, base_interpolator):
            raise TypeError('This object is not base_interpolator inherited: %r'%intrp)
        self.intrp = intrp
        
    def __getattr__(self, attr):
        return getattr(self.intrp, attr)
        
    def __call__(self, x):
        return self.intrp(self.B+self.A-x)

class chain_interpolator(base_interpolator):
    def __init__(self, interpolators):
        if len(interpolators) == 0:
            raise ValueError('No one interpolator passed')
        for intrp in interpolators:
            if not isinstance(intrp, base_interpolator):
                raise TypeError('This object is not base_interpolator inherited: %r'%intrp)
        self.interpolators = interpolators
        
    def __getattr__(self, attr):
        return getattr(self.interpolators[0], attr)

    def __call__(self, x):
        r = x
        for intrp in self.interpolators:
            r = intrp(r)
        return r
