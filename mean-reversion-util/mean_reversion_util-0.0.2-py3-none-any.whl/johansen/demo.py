#!pip install quandl
#import quandl
# Request: allow HTTP-post API calls
import requests
# Json: to format as json calls to API
import json 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
import itertools
# Json: to format as json calls to API
import json 
import utilities
# Currencies publicly available:

assets_ecb = ['EURMXN','EURUSD','EURGBP','EURJPY','EURAUD','EURBRL','EURTRY','EURCNY','EURCHF','EURCZK','EURDKK','EURHRK',
          'EURHUF','EURHKD', 'EURINR', 'EURILS', 'EURIDR', 'EURISK', 'EURKRW', 'EURLTL', 'EURMYR', 'EURNOK', 'EURNZD', 'EURPLN', 
          'EURPHP', 'EURRUB', 'EURRON', 'EURTHB', 'EURZAR', 'EURCAD' ]

# Pegged currencies and bad data:
assets_pegged = ['EURCNY', 'EURDKK','EURHRK','EURHKD','EURNOK', 'EURISK']
assets = list(set(assets_ecb).difference(set(assets_pegged)))

# Arbitrary list of currencies:
assets = ['EURMXN','EURUSD','EURGBP','EURJPY',
          'EURAUD', 'EURNZD', 'EURBRL','EURTRY', 
          'EURILS', 'EURINR', 'EURPLN', 'EURIDR',
          'EURRUB', 'EURZAR', 'EURHUF', 'EURCHF']

# G-10 currencies
# https://en.wikipedia.org/wiki/G10_currencies
assets = ['EURUSD','EURGBP','EURJPY',
          'EURAUD', 'EURNZD', 'EURCAD','EURCHF', 
          'EURNOK', 'EURSEK'] 


assets = ['EURUSD','EURGBP','EURJPY',
          'EURAUD', 'EURNZD', 'EURCAD','EURCHF', 
          'EURMXN', 'EURBRL', 'EURTRY', 
          'EURHUF', 'EURPLN', 'EURILS',
          'EURKRW', 'EURIDR', 'EURCZK'] 

print (assets)

firstAsset = True


source = 'ECB'
column = 'Value'
for asset in assets:
  q_ticker = source+'/'+asset.upper()
  
  print (q_ticker)
  #if True:
  try:
    #df = quandl.get(q_ticker)
    df = readQuandl(q_ticker)
    df.rename(columns={column:asset.upper()}, inplace=True)
    if firstAsset:
      timeS = df[asset.upper()]
      firstAsset = False
    else:
      timeS = pd.concat([timeS, df[asset.upper()]], axis = 1)

  except:
    print (asset.upper()+' not in ' + source)

print (timeS.tail())    


all_assets = timeS.columns

ccyEur = 1 / timeS
ccyEur.plot(figsize = (16,8))
#plot_multi(ccyEur, figsize=(10, 5))

print (ccyEur.tail())



List = []
#Combos = [1,2,3,4,5,6]
#Combos = [1,2]
Combos = [1, 2, 3]
#
TotalCombos = 0
TotalMR = 0


for L in Combos:
  for tuple in itertools.combinations(all_assets, L):
    #print ('-----------------------------------------------------------')
    #print(pairs)
    assets = list(tuple)
    TotalCombos += 1
    TimeSeries = ccyEur[assets].dropna()
    TimeSeriesTraining = TimeSeries.loc[: '2018-01-01']
    #print (assets)
    #TimeSeriesTraining.plot()
    # Assumption: we are testing with 1% confidence interval
    mRev = findMeanRevertingSignals(TimeSeriesTraining)
    if mRev[0]:
      #print (mRev)
      #TimeSeries.plot()
      #plot_multi(TimeSeriesTraining, figsize=(10, 5))
    
      for vector in mRev[1:]:
        print (vector)
        List.append(mRev)
        TotalMR +=1




