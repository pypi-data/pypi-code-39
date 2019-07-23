#****************************************************************************
#                             avg4lac.py
#****************************************************************************

ms=['reg','hhsz','ed','hisp','hoh','ch16']
#ms ='hoh'

for i in ms:
    inp=vars()[str(i)+'pct'+str(per1)].append([vars()[str(i)+'pct'+str(per3)],vars()[str(i)+'pct'+str(per4)],vars()[str(i)+'pct'+str(per2)]])
    opavg4=inp.pivot_table(index=i, columns='date', values='perc').reset_index()
    opavg4['Avg'] = opavg4[[per1,per3,per2,per4]].mean(axis=1)
    wue=pd.concat([opavg4,vars()[str(i)+'ue']],axis=1)
    vars()[str(i)+'inp']=wue.copy(deep=True)
    vars()[str(i)+'inp']=vars()[str(i)+'inp'][['uecat','ue','Avg']]
    vars()[str(i)+'inp']['yes']=np.round(vars()[str(i)+'inp'].Avg*vars()[str(i)+'inp'].ue/100,0).astype(int)
    vars()[str(i)+'inp']['no']=vars()[str(i)+'inp'].ue-vars()[str(i)+'inp'].yes
    vars()[str(i)+'inp1']=vars()[str(i)+'inp'][["yes","no"]]
    vars()[str(i)+'inp1']=np.array(vars()[str(i)+'inp1'])
    vars()[str(i)+'ue1']=vars()[str(i)+'ue']['ue']
    vars()[str(i)+'ue1']=vars()[str(i)+'ue1'].T
    vars()[str(i)+'ue1']=np.array(vars()[str(i)+'ue1'])
    vars()['usinthh'+str(period)+'_1']=vars()['usinthh'+str(period)]['ue']
    vars()['usinthh'+str(period)+'_1']=np.array(vars()['usinthh'+str(period)+'_1'])
    intop2=Lace.Lace.Lace2D(25,vars()['usinthh'+str(period)+'_1'],vars()[str(i)+'ue1'],vars()[str(i)+'inp1'])
    intop2=pd.DataFrame(intop2).astype(int)
    intop2.rename(columns={0:'Y',1:'N'}, inplace=True)
    vars()[str(i)+'interue_'+str(period)]=pd.concat([vars()[str(i)+'ue'].uecat,intop2],axis=1)
    
  
    
ms1=['pers','hisp','ed']

for j in ms1:
    inp=vars()[str(j)+'pctp2p'+str(per1)].append([vars()[str(j)+'pctp2p'+str(per3)],vars()[str(j)+'pctp2p'+str(per4)],vars()[str(j)+'pctp2p'+str(per2)]])
    opavg4=inp.pivot_table(index=j, columns='date', values='perc').reset_index()
    opavg4['Avg'] = opavg4[[per1,per2,per3,per4]].mean(axis=1)
    wue=pd.concat([opavg4,vars()[str(j)+'uep2p']],axis=1)
    vars()[str(j)+'inp']=wue.copy(deep=True)
    vars()[str(j)+'inp']=vars()[str(j)+'inp'][['uecat','ue','Avg']]
    vars()[str(j)+'inp']['yes']=np.round(vars()[str(j)+'inp'].Avg*vars()[str(j)+'inp'].ue/100,0).astype(int)
    vars()[str(j)+'inp']['no']=vars()[str(j)+'inp'].ue-vars()[str(j)+'inp'].yes
    vars()[str(j)+'inp1']=vars()[str(j)+'inp'][["yes","no"]]
    vars()[str(j)+'inp1']=np.array(vars()[str(j)+'inp1'])
    vars()[str(j)+'ue1p2p']=vars()[str(j)+'uep2p']['ue']
    vars()[str(j)+'ue1p2p']=vars()[str(j)+'ue1p2p'].T
    vars()[str(j)+'ue1p2p']=np.array(vars()[str(j)+'ue1p2p'])
    vars()['usintp2p'+str(period)+'_1']=vars()['usintp2p'+str(period)]['ue']
    vars()['usintp2p'+str(period)+'_1']=np.array(vars()['usintp2p'+str(period)+'_1'])
    intop2=Lace.Lace.Lace2D(25,vars()['usintp2p'+str(period)+'_1'],vars()[str(j)+'ue1p2p'],vars()[str(j)+'inp1'])
    intop2=pd.DataFrame(intop2).astype(int)
    intop2.rename(columns={0:'Y',1:'N'}, inplace=True)
    vars()[str(j)+'interuep2p_'+str(period)]=pd.concat([vars()[str(j)+'uep2p'].uecat,intop2],axis=1)
    
#****************************************************************************
#                             avg4lacdma.py
#****************************************************************************

inp=vars()['dmapct'+str(per1)].append([vars()['dmapct'+str(per3)],vars()['dmapct'+str(per4)],vars()['dmapct'+str(per2)]])
opavg4=inp.pivot_table(index='dma', columns='date', values='perc').reset_index()
opavg4['Avg'] = opavg4[[per1,per2,per3,per4]].mean(axis=1)

wue=opavg4.merge(dmaue,on='dma',how='inner')
srtue=dmaue.sort_values('dma')
dmainp=wue.copy(deep=True)
dmainp=dmainp[['dma','uecat','ue','p2p','Avg']]
dmainp['yes']=np.round(dmainp.Avg*dmainp.ue/100,0).astype(int)
dmainp['no']=dmainp.ue-dmainp.yes
vars()['dmahhctl'+str(period)+'_1']=vars()['dmahhctl'+str(period)].copy(deep=True) 
dmainp1=dmainp[["yes","no"]]
dmainp1=np.array(dmainp1)
dmaue1=srtue['ue']
dmaue1=dmaue1.T
dmaue1=np.array(dmaue1)
vars()['dmahhctl'+str(period)+'_1']=vars()['dmahhctl'+str(period)]['ue']
vars()['dmahhctl'+str(period)+'_1']=np.array(vars()['dmahhctl'+str(period)+'_1'])
intop3=Lace.Lace.Lace2D(25,vars()['dmahhctl'+str(period)+'_1'],dmaue1,dmainp1)
intop3=pd.DataFrame(intop3).astype(int)
intop3.rename(columns={0:'Y',1:'N'}, inplace=True)
srtop1=pd.concat([wue.uecat,intop3],axis=1).sort_values('uecat') 


###P2P

inp=vars()['dmapctp2p'+str(per1)].append([vars()['dmapctp2p'+str(per3)],vars()['dmapctp2p'+str(per4)],vars()['dmapctp2p'+str(per2)]])
opavg4=inp.pivot_table(index='dma', columns='date', values='perc').reset_index()
opavg4['Avg'] = opavg4[[per1,per2,per3,per4]].mean(axis=1)
wue=opavg4.merge(dmaue,on='dma',how='inner')
srtue=dmaue.sort_values('dma')
dmainpp2p=wue.copy(deep=True)
dmainpp2p=dmainpp2p[['dma','uecat','ue','p2p','Avg']]
dmainpp2p['yes']=np.round(dmainpp2p.Avg*dmainpp2p.p2p/100,0).astype(int)
dmainpp2p['no']=dmainpp2p.p2p-dmainpp2p.yes
vars()['dmap2pctl'+str(period)+'_1']=vars()['dmap2pctl'+str(period)].copy(deep=True)
dmainpp2p1=dmainpp2p[["yes","no"]]
dmainpp2p1=np.array(dmainpp2p1)
dmauep2p1=srtue['p2p']
dmauep2p1=dmauep2p1.T
dmauep2p1=np.array(dmauep2p1)
vars()['dmap2pctl'+str(period)+'_1']=vars()['dmap2pctl'+str(period)]['ue']
vars()['dmap2pctl'+str(period)+'_1']=np.array(vars()['dmap2pctl'+str(period)+'_1'])
intop4=Lace.Lace.Lace2D(25,vars()['dmap2pctl'+str(period)+'_1'],dmauep2p1,dmainpp2p1)
intop4=pd.DataFrame(intop4).astype(int)
intop4.rename(columns={0:'Y',1:'N'}, inplace=True)
srtop2=pd.concat([wue.uecat,intop4],axis=1).sort_values('uecat') 


