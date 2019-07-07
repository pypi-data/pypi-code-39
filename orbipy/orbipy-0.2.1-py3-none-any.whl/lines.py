# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 10:14:44 2019

@author: stasb
"""
import math
import numpy as np
from scipy.interpolate import interp1d
from .interpolators import base_interpolator, linear_interpolator
    
class base_line:
    def __init__(self, interp=None):
        if interp is not None:
            if not isinstance(interp, base_interpolator):
                raise TypeError('This object is not base_interpolator inherited: %r'%intrp)
        self.interp = interp
    
    def __call__(self, l):
        pass

    def get_points(self, n):
        if self.interp is not None:
            return self(self.interp.AB(n))
        return self(np.linspace(0.0, 1.0, n))
        
class line_segment(base_line):
    
    def __init__(self, x0, x1, interp=None):
        super().__init__(interp)
        self.x0 = x0
        self.x1 = x1
        
    def __call__(self, l):
        if self.interp is not None:
            li = self.interp(l)
        else:
            li = l
        
        if isinstance(li, np.ndarray):
            return self.x0*(1.0-li[:,None])+self.x1*li[:,None]
        
        return self.x0*(1.0-li)+self.x1*li    

def heading_2d(x1, x2):
    '''
    Calculate angle from point x1 to point x2.
    '''
    dx = x2 - x1
    return math.degrees(math.atan2(dx[1], dx[0]))

def vector_2d(head):
    '''
    Calculate unit vector in head direction.
    '''    
    if isinstance(head, np.ndarray):
        rad = np.radians(head)
        return np.vstack((np.cos(rad),np.sin(rad))).T

    rad = math.radians(head)
    return np.array([math.cos(rad), math.sin(rad)])

class arc_segment(base_line):
    def __init__(self, center, head, fov, r, interp=None):
        super().__init__(interp)
        self.center = center
        self.head = head
        self.fov = fov
        self.r = r
        self.i1d = linear_interpolator(A=0.0, B=1.0, 
                                       a=self.head-self.fov*0.5, 
                                       b=self.head+self.fov*0.5)

    def __call__(self, l):
        if self.interp is not None:
            li = self.interp(l)
        else:
            li = l
        
        heads = self.i1d(li)

        if isinstance(li, np.ndarray):
            return self.center[None,:] + self.r*vector_2d(heads)

        return self.center + self.r*vector_2d(heads)
    
class spline(base_line):
    
    def __init__(self, pts, kind='linear', interp=None):
        super().__init__(interp)
        self.pts = pts
        self.kind = kind
        self.l = np.concatenate(([0.], np.sum((pts[1:]-pts[:-1])**2,axis=1)**0.5))
        self.l = np.cumsum(self.l)/np.sum(self.l)
        self.i1d = interp1d(self.l, pts, kind=kind, 
                            axis=0, copy=False, fill_value='extrapolate')
        
    def __call__(self, l):
        if self.interp is not None:
            li = self.interp(l)
        else:
            li = l

        return self.i1d(li)
    
    @classmethod
    def linear(cls, pts, interp=None):
        return cls(pts, kind='linear', interp=interp)
    
    @classmethod
    def quad(cls, pts, interp=None):
        return cls(pts, kind='quadratic', interp=interp)

    @classmethod
    def cubic(cls, pts, interp=None):
        return cls(pts, kind='cubic', interp=interp)
    
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from .interpolators import (log_interpolator, 
                                chain_interpolator,
                                flipX_interpolator,
                                flipY_interpolator)

    A, B = 1., 2.
    a, b = 0., 1.
    
    intrp = linear_interpolator(A, B, a, b)
    intrp1 = flipX_interpolator(log_interpolator(A, B, a, b))
    intrp2 = flipY_interpolator(log_interpolator(a, b, A, B))
    
    intrp = chain_interpolator([intrp1, intrp2])
    
    x = np.linspace(A, B, 100)
    y = intrp(x)
    
    plt.figure(figsize=(10,10))
    plt.plot(x, y, '.-')
    
    x0 = np.array([10.,10.])
    x1 = np.array([20.,20.])
    ls = line_segment(x0, x1, log_interpolator(N=10))
    arc = arc_segment(x0, 45., 90., 10., log_interpolator(N=10))
    
    pts = arc.get_points(10)
    #ls.get_points(10)
    #pts[:,1] = -pts[:,1] + np.random.rand(pts.shape[0])*2-1
    
    pwl = spline.linear(pts, flipY_interpolator(log_interpolator(N=10)))
    pts1 = arc.get_points(50)
    
    plt.figure(figsize=(10,10))
    plt.plot(pts[:,0], pts[:,1], '.-')
    plt.plot(pts1[:,0], pts1[:,1], '.r')
    plt.axis('equal')
    
    