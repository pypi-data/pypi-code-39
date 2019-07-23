#****************************************************************************
#                             sumwts.py
#****************************************************************************

#ftp = ftplib.FTP(server)
#ftp.login(user, password)
#downloadFiles(source1, destination, list(['agesex'+str(per2) + '.sas7bdat']))
#vars()['agesex'+str(per2)]=pd.read_sas(inpath + 'agesex'+str(per2)+'.sas7bdat',encoding='utf-8')

## Code has been changed from period to per2 as its required to be older period (code changed by ALex)

oldper = TAM_sync

srted = vars()['agesex'+str(oldper)].sort_values('inter')
uswts = srted.groupby('inter').sum()[['weight','wtp2p']]
uswts.columns = [['hhus', 'p2pus']]
trans = uswts.T
vars()['sumuswts'+str(oldper)] = trans.copy(deep=True)
vars()['sumuswts'+str(oldper)]['T'] = vars()['sumuswts'+str(oldper)]['N'] + vars()['sumuswts'+str(oldper)]['Y']

work1 = vars()['wwts'+str(oldper)+'rem']
srted = work1.sort_values('inter')
remwts = srted.groupby('inter').sum()[['weight','wtp2p']]
remwts.columns = [['hhrem', 'p2prem']]

apmm = uswts.copy(deep=True)
apmm.sort_values('inter',ascending= False)


rem = remwts.copy(deep=True)
rem.sort_values('inter',ascending= False)


outp = pd.concat([apmm,rem],axis=1)

out1 = outp.copy(deep=True).reset_index()
out1['hhmm'] = out1['hhus'].values - out1['hhrem'].values
out1 = out1[['inter','hhmm', 'hhrem']]


vars()['hhinpapvrm'+str(oldper)] = out1.T.reset_index()

vars()['hhinpapvrm'+str(oldper)].columns = vars()['hhinpapvrm'+str(oldper)].iloc[0]
vars()['hhinpapvrm'+str(oldper)] = vars()['hhinpapvrm'+str(oldper)][['inter','Y','N']]
vars()['hhinpapvrm'+str(oldper)].drop(0, inplace=True)

print(" Sum of HH wts (total-rem) vs rem hhinpapvrm %s" %oldper )


out2 = outp.copy(deep=True).reset_index()
out2['p2pmm'] = out2['p2pus'].values - out2['p2prem'].values
out2 = out2[['inter','p2pmm', 'p2prem']]

vars()['p2pinpapvrm'+str(oldper)] = out2.T.reset_index()

vars()['p2pinpapvrm'+str(oldper)].columns = vars()['p2pinpapvrm'+str(oldper)].iloc[0]
vars()['p2pinpapvrm'+str(oldper)] = vars()['p2pinpapvrm'+str(oldper)][['inter','Y','N']]
vars()['p2pinpapvrm'+str(oldper)].drop(0, inplace=True)

print(" Sum wted p2p (total-rem) vs rem p2pinpapvrm  %s" %oldper )

