#****************************************************************************
#                             remwts.py
#****************************************************************************

vars()['tgb2for'+str(period)]=pd.read_pickle(path+'tgb2for'+str(period)+'.pkl')

wts_rem=pd.read_fwf(inpath+"\\wts.Remainder",header=None,names=['day', 'hhld', 'weight'])
wts_rem['weight']=wts_rem['weight']/28

wts_rem.sort_values(['day', 'hhld'],inplace=True)

match=pd.merge(vars()['tgb2for' +str(period)],wts_rem,on=['day','hhld'],how='inner')
#match.to_csv('match.csv')

nomatch_temp=pd.merge(vars()['tgb2for'+str(period)],wts_rem,on=['hhld','day'],how='outer')
nomatch=nomatch_temp[pd.isnull(nomatch_temp).any(axis=1)]

vars()['wwts' +str(period)+'rem']=match.copy(deep=True)
vars()['wwts' +str(period)+'rem']['wtp2p']=vars()['wwts' +str(period)+'rem']['weight']*vars()['wwts' +str(period)+'rem']['p2p']
vars()['wwts' +str(period)+'rem']=vars()['wwts' +str(period)+'rem'][['day', 'hhld', 'dma', 'weight', 'inter','wtp2p','p2p']]

group=vars()['wwts' +str(period)+'rem'].groupby('inter')

def count_missing(rem):
    return (rem.weight.isnull().values.ravel().sum())
vars()['wwts' +str(period)+'rem_count']=group.weight.count()
vars()['wwts' +str(period)+'rem_miss'] = vars()['wwts' +str(period)+'rem'].groupby('inter').apply(count_missing)
vars()['wwts' +str(period)+'rem_sum']=group.weight.sum()

def count_missing(rem):
    return (rem.wtp2p.isnull().values.ravel().sum())
vars()['wwts' +str(period)+'rem_count_p2p']=group.wtp2p.count()
vars()['wwts' +str(period)+'rem_miss_p2p']=vars()['wwts' +str(period)+'rem'].groupby('inter').apply(count_missing)
vars()['wwts' +str(period)+'rem_sum_p2p']=group.wtp2p.sum()

nomatchrem_count=nomatch['weight'].count()
nomatchrem_mis=nomatch['weight'].isnull().values.ravel().sum()
nomatchrem_sum=nomatch['weight'].sum()

vars()['wwts'+str(period)+'rem'].to_csv(inpath+ 'Avg/wwts'+str(period)+'rem.csv')
vars()['wwts'+str(period)+'rem'].to_pickle(path+'wwts'+str(period)+'rem.pkl')
