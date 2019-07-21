import sys
#sys.path.append('..')

from PyFin.api import *
from PyFin.api.Analysis import DELTA
from PyFin.Math.Accumulators import Log
from PyFin.Math.Accumulators import MovingRank
from PyFin.Math.Accumulators.IAccumulators import Pow
from PyFin.Math.Accumulators.StatefulAccumulators import MovingCorrelation
from PyFin.Analysis.CrossSectionValueHolders import CSRankedSecurityValueHolder
from PyFin.Analysis.SecurityValueHolders import SecurityIIFValueHolder
from PyFin.Analysis.SecurityValueHolders import SecurityDeltaValueHolder
from PyFin.Analysis.SecurityValueHolders import SecurityShiftedValueHolder
from PyFin.Analysis.SecurityValueHolders import SecurityLatestValueHolder
from PyFin.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecurityMinimumValueHolder
from PyFin.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecurityMaximumValueHolder
from PyFin.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecurityExpValueHolder
from PyFin.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecuritySqrtValueHolder
from PyFin.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecuritySignValueHolder
from PyFin.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecurityLogValueHolder
from PyFin.Analysis.TechnicalAnalysis import SecurityMovingAverage
from PyFin.Analysis.TechnicalAnalysis import SecurityMovingSum
from PyFin.Analysis.TechnicalAnalysis import SecurityMovingStandardDeviation
from PyFin.Analysis.TechnicalAnalysis import SecurityMovingRank


import datetime as dt
import numpy as np
import numpy.matlib as matlib
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import select, and_
from PyFin.examples.model import Market

engine = create_engine('postgresql+psycopg2://alpha:alpha@180.166.26.82:8889/alpha')
begin_date = '2018-12-01'
end_date = '2018-12-28'

query = select([Market]).where(
            and_(Market.trade_date >= begin_date, Market.trade_date <= end_date, ))
mkt_df = pd.read_sql(query, engine)
mkt_df.rename(columns={'preClosePrice':'pre_close','openPrice':'openPrice',
                      'highestPrice':'highestPrice','lowestPrice':'lowestPrice',
                      'closePrice':'closePrice','turnoverVol':'turnoverVol',
                      'turnoverValue':'turnover_value','accumAdjFactor':'accum_adj',
                       'vwap':'vwap'}, inplace=True)
mkt_df = mkt_df[[('000000' + str(code))[-6:][0] in '036' for code in mkt_df['code']]]
trade_date_list = list(set(mkt_df.trade_date))
trade_date_list.sort(reverse=True)
mkt_df = mkt_df.set_index(['trade_date', 'code'])
mkt_df = mkt_df[mkt_df['turnoverVol'] > 0]
#计算收益率

df = mkt_df.loc['2018-12-20':'2018-12-28'].reset_index().set_index('trade_date')
#
# #CLOSE-(CLOSE>DELAY(CLOSE,1)
# expression1 = SecurityLatestValueHolder('closePrice') - (
#     SecurityLatestValueHolder('closePrice') > SecurityShiftedValueHolder(1, SecurityLatestValueHolder('closePrice')))
#
# #MIN(LOW,DELAY(CLOSE,1))
# expression2 = SecurityMinimumValueHolder(SecurityLatestValueHolder('closePrice'),
#                                          SecurityShiftedValueHolder(1, SecurityLatestValueHolder('closePrice')))
#
# #MAX(HIGH,DELAY(CLOSE,1)
# expression3 = SecurityMaximumValueHolder(SecurityLatestValueHolder('highestPrice'),
#                                          SecurityShiftedValueHolder(1, SecurityLatestValueHolder('closePrice')))
#
# #DELAY(CLOSE,1)?0:CLOSE-(CLOSE>DELAY(CLOSE,1) -->DELAY(CLOSE,1)?0:expression1
# expression4 = SecurityIIFValueHolder(SecurityShiftedValueHolder(1, SecurityLatestValueHolder('closePrice')), 0, expression1)
#
# #(CLOSE=expression4?expression2:expression3)
# expression5 = SecurityIIFValueHolder(expression4, expression2, expression3)
#
# #SUM(CLOSE,6)
# expression6 = SecurityMovingSum(6, expression5) #缺少windows暴露
# name = 'alpha3'
# df[name] = expression6.transform(df,name=name,category_field='code', dropna=False)[name]
# df.reset_index()[['trade_date','code','closePrice','highestPrice',name]].set_index('code').loc[603999]

exression1 = CSRankedSecurityValueHolder(SecurityLatestValueHolder('turnoverVol'))
exression2 = CSRankedSecurityValueHolder(SecurityLatestValueHolder('vwap'))
exression3 = CSRankedSecurityValueHolder(exression1 > exression2)
exression4 = SecurityMovingRank(5, exression3)
name = 'alpha16'
df = mkt_df.loc['2018-12-19':'2018-12-28'].reset_index().set_index('trade_date')
df = exression4.transform(df, name=name, category_field='code', dropna=False)
print(df)