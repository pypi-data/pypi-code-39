'''Calculation KS statistic for a model by ROC curve.'''

import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt

def plot(data):
    '''Calculation KS statistic
    Inspired by one Christoforos Anagnostopoulos's tutorial at 
    https://www.datacamp.com/courses/designing-machine-learning-workflows-in-python

    Parmaters
    ---------
    data: pandas.DataFrame
          with y and yhat.
          y is  target.
          yhat is prediction.'''

    fpr, tpr, thres = roc_curve(data.y, data.yhat)
    ks = tpr - fpr
    ks_max = np.max(ks)
    print(ks_max)
    
    plt.plot(thres, ks)
    plt.plot(thres, tpr)
    plt.plot(thres, fpr)
    plt.xlabel('Cutoff')
    plt.ylabel('KS')
    plt.title(str(ks_max))
    plt.xlim(0,1)
    plt.show()
    plt.clf()
    
    return ks_max
