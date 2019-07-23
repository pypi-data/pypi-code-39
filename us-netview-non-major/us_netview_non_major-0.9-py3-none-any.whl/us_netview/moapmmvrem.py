#****************************************************************************
#                             moapmmvrem.py
#****************************************************************************

oldper = TAM_sync

hhinpapvrm1=vars()['hhinpapvrm'+str(oldper)].ix[:,1:]
hhinpapvrm1=np.array(hhinpapvrm1)
apmmvremue1=apmmvremue['ue']
apmmvremue1=apmmvremue1.T
apmmvremue1=np.array(apmmvremue1)

vars()['usinthh'+str(period)+'_1']=vars()['usinthh'+str(period)]['ue']
vars()['usinthh'+str(period)+'_1']=np.array(vars()['usinthh'+str(period)+'_1'])
intop=Lace.Lace.Lace2D(25,vars()['usinthh'+str(period)+'_1'],apmmvremue1,hhinpapvrm1)
intop=pd.DataFrame(intop)
intop.rename(columns={0:'Y',1:'N'}, inplace=True)
                                                      

apvrmint=pd.concat([intop,apmmvremue],axis=1)

yesno=['internet-yes','internet-no']
dmainthh=apvrmint.head(1)
dmainthh=[dmainthh.ix[0,'Y'],dmainthh.ix[0,'N']]
vars()['dmahhctl'+str(period)]= pd.DataFrame({'uecat': yesno,'ue': dmainthh})

reminterue = apvrmint.tail(1)
reminterue = reminterue[['uecat','Y','N']]


p2pinpapvrm=out2.T
p2pinpapvrm.rename(columns={0:'N',1:'Y'}, inplace=True)
p2pinpapvrm.reset_index(inplace=True)
p2pinpapvrm.drop(p2pinpapvrm.index[:1], inplace=True)
p2pinpapvrm.sort_values('level_0',inplace=True)   

p2pinpapvrm = p2pinpapvrm[['level_0','Y','N']]
  
p2pinpapvrm1=p2pinpapvrm.drop('level_0',axis=1)
p2pinpapvrm1=np.array(p2pinpapvrm1)
apmmvremuep2p1=apmmvremuep2p['ue']
apmmvremuep2p1=apmmvremuep2p1.T
apmmvremuep2p1=np.array(apmmvremuep2p1)
vars()['usintp2p'+str(period)+'_1']=vars()['usintp2p'+str(period)]['ue']
vars()['usintp2p'+str(period)+'_1']=np.array(vars()['usintp2p'+str(period)+'_1'])
intop1=Lace.Lace.Lace2D(25,vars()['usintp2p'+str(period)+'_1'],apmmvremuep2p1,p2pinpapvrm1)
intop1=pd.DataFrame(intop1)
intop1.rename(columns={0:'Y',1:'N'}, inplace=True)

apvrmintp2p=pd.concat([intop1,apmmvremuep2p],axis=1)
dmaintp2p=apvrmintp2p.head(1)
dmaintp2p=[dmaintp2p.ix[0,'Y'],dmaintp2p.ix[0,'N']]
vars()['dmap2pctl'+str(period)]=pd.DataFrame({'uecat': yesno,'ue': dmaintp2p})

reminteruep2p = apvrmintp2p.tail(1)
reminteruep2p = reminteruep2p[['uecat','Y','N']]

                                        
