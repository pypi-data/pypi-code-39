# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 10:26:18 2019

@author: Administrator
"""

# importing the requests library 
import requests 
import csv
import urllib.request
import codecs
import pandas as pd
import datetime as dt
#!pip install mean-reversion-utilities
from .utilities import readQuandl
#!pip install python-binance
from binance.client import Client
import pandas as pd
from datetime import datetime




def portReadCryptoData(assets,prefix,suffix,column):
  firstTime = True 
  for asset in assets: 
    url = prefix+asset+suffix
    r = requests.get(url = url, verify = False) 

    text = r.iter_lines()
    reader = csv.reader(codecs.iterdecode(text, 'utf-8'))


    from io import StringIO

    data = StringIO(r.text)

    df = pd.read_csv(data,skiprows = [0], header=0)
    df.set_index('Date', inplace = True)
    
    if firstTime:
      
      timeSeries = pd.DataFrame(df[column])
      timeSeries.columns = [asset]
      firstTime = False
    else:
      timeSeries[asset] = df[column]
      #timeSeries = pd.concat([timeSeries, df[column]], axis = 1, sort=True)
      
  return timeSeries  

def portReadBinance(cryptos,column,timeInterval,start_date,end_date,api_key,api_secret):
  
  client = Client(api_key, api_secret)
  first_time = True
  for crypto in cryptos:

    klines = client.get_historical_klines(crypto, timeInterval, start_date, end_date)

    df = pd.DataFrame(klines)
    try:
      df.columns = ['openTime',crypto,'high','low','close','volume','closeTime','quoteAssetVolume','numberOfTrades','takerbuyBaseAssetVolume','takerBuyQuoteAssetVolume','ignore']
      df['date'] = pd.to_datetime(pd.Series(df['openTime']),unit='ms')
      df.set_index('date', inplace=True)
      df[crypto] = pd.to_numeric(df[crypto])
      #print ('loading '+crypto)
      if first_time:
        cryptos_df = pd.DataFrame(df[crypto])
        first_time = False
      else:
          cryptos_df[crypto] = df[crypto]
          #cryptos_df = pd.concat([cryptos_df, df[crypto]], axis = 1)

    except:
      dummy_line = 0
      #print ('problem with '+crypto)
  return cryptos_df    


def portReadQuandl(assets,Crypto_flag, QUANDL_API_KEY):

  firstAsset = True
  
  if Crypto_flag:
    source = 'BITFINEX'
    column = 'Mid'

  else:
    source = 'ECB'
    column = 'Value'


  for asset in assets:
    q_ticker = source+'/'+asset.upper()

    #print (q_ticker)
    if True:
    #  try:
      #df = quandl.get(q_ticker)
      df = readQuandl(q_ticker, QUANDL_API_KEY)
      df.rename(columns={column:asset.upper()}, inplace=True)
      if firstAsset:
        timeS = df[asset.upper()]
        firstAsset = False
      else:
        timeS = pd.concat([timeS, df[asset.upper()]], axis = 1)

  #  except:
  #    print (asset.upper()+' not in ' + source)

#df.head()
  return timeS 
