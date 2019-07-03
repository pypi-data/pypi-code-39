#
# Invoke the prototype class pyBPCA and run a simple job
# for one iteration
#

import time as tm
import pandas as pd
import numpy as np
from pyBPCA import pyBPCA

infilename = '/projects/sequence_analysis/vol1/prediction_work/ClimateML/SEA-ICE-rawdata/goddard_nt_seaice_conc_monthly_withll_23Apr2019.dat'

pybpca = pyBPCA(filename = infilename,p=5, maxiter=20,numRandom=1,showTimes=True,scalingMethod=0)
newA,newB,newX = pybpca.runProcess()


