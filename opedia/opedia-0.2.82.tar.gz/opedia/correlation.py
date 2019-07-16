"""
Author: Mohammad Dehghani Ashkezari <mdehghan@uw.edu>

Date: 2019-06-17

Function: Compute and plot correlation between a dataframe variables.
"""

from docopt import docopt
import sys
import os
sys.path.append(os.path.dirname(__file__))
import numpy as np
import pandas as pd
import warnings
import db
import subset
import common as com
from opedia import colocalize as COL
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns
from matplotlib import cm as cm
import scipy.cluster.hierarchy as sch

import jupyterInline as jup
if jup.jupytered():
    from tqdm import tqdm_notebook as tqdm
else:
    from tqdm import tqdm





def heatmap(df):

    # X = df.corr().values
    # d = sch.distance.pdist(X)   
    # L = sch.linkage(d, method='complete')
    # ind = sch.fcluster(L, 0.5*d.max(), 'distance')
    # columns = [df.columns.tolist()[i] for i in list((np.argsort(ind)))]
    # df = df.reindex_axis(columns, axis=1)

    plt.clf()
    method = 'spearman'      # options: pearson, kendall, spearman 
    print(df.columns)
    corr = df.corr(method=method)
    sns.heatmap(
        corr, 
        xticklabels=corr.columns, 
        yticklabels=corr.columns, 
        annot=True, 
        annot_kws={"size": 6}, 
        cmap= 'coolwarm'
        )
    plt.tight_layout()
    dirPath = 'embed/'
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)        
    plt.savefig(dirPath + 'corr.png', dpi=300)
    plt.show()
    return




# inline = jup.inline()   # check if jupyter is calling this script

