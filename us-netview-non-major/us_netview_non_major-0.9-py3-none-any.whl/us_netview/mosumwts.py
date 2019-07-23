#****************************************************************************
#                             mosumwts.py
#****************************************************************************

srted = vars()['agesex'+str(period)].sort_values('inter')
uswts = srted.groupby('inter').sum()[['weight','wtp2p']]
uswts.columns = [['hhus', 'p2pus']]
trans = uswts.T
vars()['sumuswts'+str(period)] = trans.copy(deep=True)
vars()['sumuswts'+str(period)]['T'] = vars()['sumuswts'+str(period)]['N'] + vars()['sumuswts'+str(period)]['Y']
