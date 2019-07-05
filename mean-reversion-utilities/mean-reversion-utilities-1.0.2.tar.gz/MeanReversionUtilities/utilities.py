# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 11:02:08 2019

@author: Administrator
"""

#@title
#!pip install quandl
#import quandl
# Request: allow HTTP-post API calls
import requests
# Json: to format as json calls to API
import json 
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
import itertools
# Json: to format as json calls to API

#@title
#!pip install johansen
# Request: allow HTTP-post API calls
import requests
# Json: to format as json calls to API
import json 
# Pandas: to plot the timeseries
import pandas as pd
# Datetime: to convert different date formats
import datetime as dt
# Import the Time Series library
import statsmodels.tsa.stattools as ts


import numpy as np
from numpy import cumsum, log, polyfit, sqrt, std, subtract
#@title
from johansen import Johansen

import matplotlib.pyplot as plt
import operator as op



# API_ENDPOINT = "https://markovsimulator.azurewebsites.net/api/MarkovCalibrator_01?code=UFYL9CcFRERnVbZJ3ELdRRY7u59vD3BgONzaGLNEOekTfKf0Ug9Bfw=="
API_ENDPOINT = "https://gmaatest.azurewebsites.net/api/HttpTriggerCSharp1?code=COXmk9ou6Mr8/dUCYj045SaeNm6jCkPzJ3ilU/dCiTvNcFNQax4BMQ=="

QUANDL_API_KEY = "o6YKGjyDcseE3LFKrSK3"

QUAND_FX_prefix = "https://www.quandl.com/api/v3/datasets/"
QUAND_FX_suffix = ".json?api_key="+QUANDL_API_KEY
#@title
# Call Quandl to get all the data
def readQuandlECB(FXid):
  print (QUAND_FX_prefix+FXid+QUAND_FX_suffix)
  q = requests.get(url = QUAND_FX_prefix+FXid+QUAND_FX_suffix)
  
  q_json = q.json() 
  q_data = q_json['dataset']['data']

  # Compute derived series from Quandl Data
  dates = []
  values = []
  q_len = len(q_data)
  column_len = len(q_data[0])
  column = column_len-1
  columns = q_json['dataset']['column_names']
  #print (columns)


  # The following could be easily done using Quandl's
  # python API - but I keep it the 'hard way' to allow
  # compatibility with Google Colaboratory
  df = pd.DataFrame.from_records(q_data, columns = columns)
  df['Date'] = pd.to_datetime(df['Date'])
  df.set_index('Date', inplace=True)
  return df


def MarkovCalibration(df_ts, column_name = None, calType = "MeanReverting"):
    # if no column name is given takes only the first one.
    # to send data to the Azure API we need to:
    # - sort the dates increasing
    # - remove NaNs
    # - put dates in string format readable by Azure
    
    # Time Series seed
    json_ts =  {
       "calType" : "",
        "seriesName" : 'seriesName',
        "colName" : "Value",
      "dates": [],  
      "vals" : []
    }

    panda_ts = df_ts.copy()    
    panda_ts.sort_index(inplace = True)
    panda_ts['dates_'] = panda_ts.index
    panda_ts = panda_ts.dropna()

    json_ts['dates'] = panda_ts['dates_'].apply(lambda x: x.strftime('%Y-%m-%d')).tolist()
    if not column_name:
        json_ts['vals'] = panda_ts[panda_ts.columns[0]].tolist()
    else:
        json_ts['vals'] = panda_ts[column_name].tolist()
    json_ts['calType'] = calType
    r = requests.post(url = API_ENDPOINT, json = json_ts)
    r_json = r.json()
    theta = r_json['calibrationResult']['Lambda']
    half_life = -np.log(0.5) * 365.25 / theta
    r_json['calibrationResult']['HalfLife'] = half_life
    sigma = r_json['calibrationResult']['Sigma']
    r_json['calibrationResult']['Std_band'] = np.sqrt(sigma * sigma / (2 * theta))
    return r_json


def OU_Calibrate_ML(df,delta):
  S = df.values
  from numpy import sum,power,sqrt,log,exp
  n = len(S)-1

  Sx = sum(S[0:-1])
  Sy = sum(S[1: ])
  Sxx = sum(power(S[0:-1],2))
  Sxy = sum( S[0:-1] * S[1: ])
  Syy = sum(power(S[1: ],2))

  mu  = (Sy*Sxx - Sx*Sxy) / ( n*(Sxx - Sxy) - (power(Sx,2) - Sx*Sy) )

  lambda_ = -log( (Sxy - mu*Sx - mu*Sy + n*power(mu,2)) / (Sxx -2*mu*Sx + n*power(mu,2)) ) / delta
  a = exp(-lambda_*delta)
  sigmah2 = (Syy - 2*a*Sxy + power(a,2)*Sxx - 2*mu*(1-a)*(Sy - a*Sx) + n*power(mu,2)*power(1-a,2))/n
  sigma = sqrt(sigmah2*2*lambda_/(1-power(a,2)))

  half_life = -np.log(0.5) * 365.25 / lambda_
  std_band = np.sqrt(sigma * sigma / (2 * lambda_))

  return (mu,sigma,half_life, std_band)   



#
#TimeSeries = cryptos[assets].dropna()
#TimeSeriesTraining = TimeSeries.loc['2014-01-01' : '2018-03-01']
#https://github.com/iisayoo/johansen
#http://qed.econ.queensu.ca/working_papers/papers/qed_wp_1227.pdf
def findMeanRevertingSignals(timeSeries):
    x = timeSeries.as_matrix()
    x_centered = x - np.mean(x, axis=0)

    # model:
    # If set to 2, case 1 will be used. This case should be used if
    #        the input time series have linear trends but the cointegrating
    #        relations are not expected to have linear trends.
    #   significance_level: 0, 90% significance will be used. 
    #                       1, 95% will be used. If set
    #                       2, 99% will be used.
    johansen = Johansen(x_centered, model=2, significance_level=1)
    try:
      eigenvectors, r = johansen.johansen()
      print (r)

      mean_rev = [False]
      for k in r:

          j_ev = eigenvectors[:, k] 


          bb = pd.DataFrame(timeSeries.dot(j_ev))
          
          #r_json = MarkovCalibration(bb)
          #half_life = r_json['calibrationResult']['HalfLife']
          #sigma = r_json['calibrationResult']['Sigma']

          #mu = r_json['calibrationResult']['Mu']
          #theta_ = r_json['calibrationResult']['Lambda']    
          #std_band = r_json['calibrationResult']['Std_band']
          ##cc = bb - mu
          ##dd = TimeSeries * j_ev
          #mean_rev.append([list(timeSeries.columns), j_ev, [mu, sigma, half_life, std_band]]) 
          mu, sigma, half_life, std_band = OU_Calibrate_ML(bb, 1)
          mean_rev.append([list(timeSeries.columns), j_ev, [mu, sigma, half_life, std_band]]) 
          
          #mean_rev.append([list(timeSeries.columns), j_ev]) 
          mean_rev[0] = True
    except:
      print ("Numerical error")
      return [False]

    return mean_rev

def plot_multi(data, cols=None, spacing=.1, **kwargs):

    from pandas import plotting

    # Get default color style from pandas - can be changed to any other color list
    if cols is None: cols = data.columns
    if len(cols) == 0: return
    colors = getattr(getattr(plotting, '_style'), '_get_standard_colors')(num_colors=len(cols))

    # First axis
    ax = data.loc[:, cols[0]].plot(label=cols[0], color=colors[0], **kwargs)
    ax.set_ylabel(ylabel=cols[0])
    lines, labels = ax.get_legend_handles_labels()

    for n in range(1, len(cols)):
        # Multiple y-axes
        ax_new = ax.twinx()
        ax_new.spines['right'].set_position(('axes', 1 + spacing * (n - 1)))
        data.loc[:, cols[n]].plot(ax=ax_new, label=cols[n], color=colors[n % len(colors)])
        ax_new.set_ylabel(ylabel=cols[n])

        # Proper legend position
        line, label = ax_new.get_legend_handles_labels()
        lines += line
        labels += label

    ax.legend(lines, labels, loc=0)
    return ax




def scatterLongShort(TimeSeries, TrainingLen, j_ev, ax):
  #j_short = j_ev * (j_ev <= 0 )
  #j_long = j_ev * (j_ev > 0 )
  if (all(j_ev >=0) or all(j_ev <=0)):
    j_filt = j_ev * 0
    j_filt[0] = 1
    j_filt2 = 1 - j_filt
    j_short = j_ev * (j_filt )
    j_long = j_ev * (j_filt2 )
    print ('All one way')
  else:
    j_short = j_ev * (j_ev <= 0 )
    j_long = j_ev * (j_ev > 0 )
    
  
  #print (j_short, j_long)

  scat = -pd.DataFrame(TimeSeries.dot(j_short))
  scat['long'] = pd.DataFrame(TimeSeries.dot(j_long))
  #print (scat.head())
  #ax = plt.subplot()
  color = ['b'] * (len(TimeSeries) - TrainingLen) + ['r']*(TrainingLen)
  ax.scatter(scat[0], scat['long'], color=color)
  #scat.plot(kind = 'scatter', x = 0, y = 'long' )

  port_usd = TimeSeries * j_short + TimeSeries * j_long
  #plt.show()
  #print (port_usd[-1:])
  
  

def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, xrange(n, n-r, -1), 1)
    denom = reduce(op.mul, xrange(1, r+1), 1)
    return numer//denom

def plotMrBands(ts,LastCalibrationDay,mu,std_band, ax2):
    ts.loc[:LastCalibrationDay].plot(ax = ax2)
    #bb.loc[:'2018-1-1'].plot(ax = ax2)
    ts.loc[LastCalibrationDay:].plot(ax = ax2, color = 'r')
    #mu = item[1][2][0]
    #std_band = item[1][2][3]
    #cc['mu'] = mu / maxEurWeight
    #cc['2p_std'] = cc['mu'] + 2 * std_band / maxEurWeight
    #cc['2m_std'] = cc['mu'] - 2 * std_band / maxEurWeight
    ts['mu'] = mu
    ts['2p_std'] = ts['mu'] + 2 * std_band
    ts['2m_std'] = ts['mu'] - 2 * std_band

    ts[['mu','2p_std', '2m_std']].plot(ax = ax2, style = ['y-.', 'g-.', 'g-.'])

    
    
# useful sites for pip installation:
# https://packaging.python.org/tutorials/packaging-projects/#uploading-your-project-to-pypi
# https://flummox-engineering.blogspot.com/2017/08/pypi-upload-failed-403-invalid-or-non-existent-authentication-information.html
    



