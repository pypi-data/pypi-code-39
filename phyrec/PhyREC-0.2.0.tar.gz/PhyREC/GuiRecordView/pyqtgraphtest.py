#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 13:05:48 2019

@author: aguimera
"""

import numpy as np
import pyqtgraph as pg


win = pg.GraphicsWindow()
win.setWindowTitle('pyqtgraph example: Scrolling Plots')

p1 = win.addPlot()
p2 = win.addPlot()
data1 = np.random.normal(size=300)
data01 = np.random.normal(size=300)
curve1 = p1.plot(data1)
curve1 = p1.plot(data01)
curve2 = p2.plot(data1)

win.nextRow()
p3 = win.addPlot()
p4 = win.addPlot()
# Use automatic downsampling and clipping to reduce the drawing load
p3.setDownsampling(mode='peak')
p4.setDownsampling(mode='peak')
p3.setClipToView(False)
p4.setClipToView(False)
p3.setRange(xRange=[-100, 0])
p3.setLimits(xMax=0)
curve3 = p3.plot(data1)
curve4 = p4.plot(data1)

win.nextRow()
p5 = win.addPlot(colspan=2)




