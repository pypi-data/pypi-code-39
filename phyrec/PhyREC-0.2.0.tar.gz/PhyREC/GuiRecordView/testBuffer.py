#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 11:14:32 2019

@author: aguimera
"""

import numpy as np
from scipy.signal import welch

class Buffer2D(np.ndarray):
    def __new__(subtype, shape, dtype=float, buffer=None, offset=0,
                strides=None, order=None, info=None):
        # Create the ndarray instance of our type, given the usual
        # ndarray input arguments.  This will call the standard
        # ndarray constructor, but return an object of our type.
        # It also triggers a call to InfoArray.__array_finalize__
        obj = super(Buffer2D, subtype).__new__(subtype, shape, dtype,
                                                buffer, offset, strides,
                                                order)
        # set the new 'info' attribute to the value passed
        obj.bufferind = 0
        # Finally, we must return the newly created object:
        return obj
    def __array_finalize__(self, obj):
        # see InfoArray.__array_finalize__ for comments
        if obj is None: return
        self.ind = getattr(obj, 'bufferind', None)
            
    def __str__(self):
        print('hola', self.bufferind)
        
    def AddData (self, NewData):
        newsize = NewData.shape[0]        
        self[0:-newsize, :] = self[newsize:, :]
        self[-newsize:, :] = NewData
        self.bufferind += newsize            

    def IsFilled(self):
        return self.bufferind >= self.shape[0]
        
test = Buffer2D((2**17, 3))

while not test.IsFilled():
    test.AddData(np.ones((10,3)))
    print(test.bufferind)


ff, psd = welch(test, axis=0)
