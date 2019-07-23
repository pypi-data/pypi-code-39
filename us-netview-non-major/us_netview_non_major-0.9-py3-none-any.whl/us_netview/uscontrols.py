#****************************************************************************
#                             uscontrols.py
#****************************************************************************


sumuswts = vars()['sumuswts'+str(period)].copy(deep=True)


sumuswts.reset_index(inplace=True)
sumuswts.rename(columns={'level_0':'NAME OF FORMER VARIABLE'},inplace=True)
ues = pd.concat([ustotue,sumuswts],axis=1)

ues['ueyes'] = round((ues['Y']/ues['T'])* ues['ue'])
ues['ueno'] = ues['ue'] - ues['ueyes']
    
usinthh = ues.iloc[0]
usintp2p = ues.iloc[1]

hhop = usinthh.copy(deep=True)
hhop = hhop[['ueyes','ueno']]
hhop.index = 'internet-yes','internet-no'
hhop = hhop.reset_index()
hhop.columns = [['uecat', 'ue']]
hhop.to_csv('hhop')


p2pop = usintp2p.copy(deep=True)
p2pop = p2pop[['ueyes','ueno']]
p2pop.index = 'internet-yes','internet-no'
p2pop = p2pop.reset_index()
p2pop.columns = [['uecat', 'ue']]
p2pop.to_csv('p2pop')

vars()['usinthh'+str(period)] = hhop

vars()['usintp2p'+str(period)] = p2pop
