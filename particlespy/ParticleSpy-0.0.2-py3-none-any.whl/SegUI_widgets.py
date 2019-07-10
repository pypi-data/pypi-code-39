# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 15:11:00 2019

@author: qzo13262
"""

import ipywidgets as widgets
from IPython.display import display

def SegUI():
    w = widgets.IntSlider()
    display(w)
    
if __name__ == '__main__':
    SegUI()