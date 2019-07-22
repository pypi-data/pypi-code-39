#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 11:44:05 2019

@author: aguimera
"""

import matplotlib.pyplot as plt
import quantities as pq
import h5py


file = h5py.File('Test.h5', 'r')
data = file['data']
#plt.figure()
#plt.plot(data)
