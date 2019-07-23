
#****************************************************************************
#                             tgb2.py
#****************************************************************************


# Read the input file 

EFF=[]
for i in range(0,35):
    EFF.append("EFF"+ str(i+1))

x = list(range(77,112))
y = list(range(78,113))
colEFF=list(zip(x,y))

cols1=[(1,11),(17,18),(20, 23),(48,49),(306,307),(140,142),(142,144),(152,154),
       (238,241),(223,224),(164,167),(170,172),(175,176),(273,275),(67,69),
       (340,342),(342,344),(344,346),(310,311)]
colspecs1 = cols1+colEFF
names1=['hhld','npm','dma','lpm','vgame','FEMALES','WW','MALES','nsys',
        'inter','ahoh','edu','spn','hhsz','state','pcycl','connx','prizm',
        'meterType']
fname1 = names1+EFF

#****************************************************************************
#                             SECTION 1
#****************************************************************************

tgb1=pd.read_fwf(inpath+infile1,colspecs=colspecs1, names=fname1,
                 converters={'state':int, 'FEMALES':int, 'MALES':int,
                             'nsys':int, 'WW':int}) 
tgb1.drop(tgb1.index[:1], inplace=True)
tgb1=tgb1.reset_index(drop='index')

start_end=pd.read_fwf(inpath+infile1,header=None,nrows=1)
start_end=str(start_end.ix[0,0])
startdate=start_end[1:6]
enddate=start_end[7:12]

tgb1['startdate']=startdate
tgb1['enddate']=enddate
tgb1['day1']=day1
tgb1['bday']=bday1
tgb1['eday']=eday1

tgb1['STARTER'] = tgb1.nsys*7 + 391
tgb1['npm']=np.where((tgb1.dma==517)&(tgb1.lpm=='Y'),'Y',tgb1.npm)

tgb1['ed']=np.where(tgb1.edu<12,1,np.where(tgb1.edu==12,2,np.where((tgb1.edu>12)&(tgb1.edu<16),3,np.where(tgb1.edu>15,4,0))))
tgb1['hisp']=np.where(tgb1.spn==1,2,1)
tgb1['hhsz']=np.where(tgb1.hhsz>5,5,tgb1.hhsz)
tgb1['ahoh']=np.where(tgb1.ahoh>100,100,tgb1.ahoh)

codreg = [3,4,3,4,4,1,3,3,3,3,4,2,2,2,2,3,3,1,3,1,2,2,3,2,4,2,4,1,1,4,1,3,2,2,3,4,1,1,3,2,3,3,4,1,3,4,3,2,4,4,4]
codreg1 = pd.DataFrame({'codreg': codreg})
codreg1.index = range(1,len(codreg1)+1)
codreg1['state'] = codreg1.index
tgb1.state = tgb1.state.astype(int)
tgb11 = pd.merge(tgb1, codreg1, how='left', on=['state'])

def func(x):
    if 1 <= x <= 24:
        return '1'
    elif 25 <= x <= 34:
        return '2'
    elif 35 <= x <= 44:
        return '3'
    elif 45 <= x <= 54:
        return '4'
    elif 55 <= x <= 64:
        return '5'
    return '6'

tgb11['hoh'] = tgb11['ahoh'].apply(func)
tgb11['Index'] = tgb11.index
tgb11['p2p']=0


for x in range(1, 16):
    tgb11['posF'+str(x)]=0
    tgb11['posM'+str(x)]=0 

tgb11['posF1']=np.where(tgb11.FEMALES>0,tgb11.STARTER,0)
tgb11['posM1']=np.where(tgb11.MALES>0,tgb11.STARTER+(3*tgb11.FEMALES)+(3*tgb11.WW),0)
for i in range(2,16):
    tgb11['posF'+str(i)]=np.where(tgb11.FEMALES>(i-1),tgb11['posF'+str(i-1)]+3,0)
    tgb11['posM'+str(i)]=np.where(tgb11.MALES>(i-1),tgb11['posM'+str(i-1)]+3,0)

lines1 = open(inpath+infile1).read().splitlines()
lines1 = pd.DataFrame({'col': lines1})
lines1.drop(lines1.index[:1], inplace=True)
lines1=lines1.reset_index(drop='index')
tgb11=tgb11.join(lines1)


for f in range(1,16):
    pos=tgb11['posF'+str(f)]
    ln=[]
    for row,i in zip(tgb11['col'],range(0,len(lines1.col))):
        ln.append(row[pos[i]-1:pos[i]+2])
    ln = pd.DataFrame({'femage'+str(f): ln})
    ln[['femage'+str(f)]] = ln[['femage'+str(f)]].apply(pd.to_numeric)
    ln['Index'] = ln.index
    tgb11 = pd.merge(tgb11, ln, how='left', on=['Index'])
    
for m in range(1,16):
    pos=tgb11['posM'+str(m)]
    ln=[]
    for row,i in zip(tgb11['col'],range(0,len(lines1.col))):
        ln.append(row[pos[i]-1:pos[i]+2])
    ln = pd.DataFrame({'malage'+str(m): ln})
    ln[['malage'+str(m)]] = ln[['malage'+str(m)]].apply(pd.to_numeric)
    ln['Index'] = ln.index
    tgb11 = pd.merge(tgb11, ln, how='left', on=['Index'])

a=['col']
for x in range(1, 16):
    a.append('posF'+str(x))
    a.append('posM'+str(x))
tgb11 = tgb11.drop(a, axis=1)

for x in range(1, 16):
    tgb11['malage'+str(x)].fillna(-1, inplace=True)
    tgb11['femage'+str(x)].fillna(-1, inplace=True)
    
for x in range(1, 16):
    tgb11['malage'+str(x)]=np.where(tgb11['malage'+str(x)]==0,1,tgb11['malage'+str(x)])
    tgb11['femage'+str(x)]=np.where(tgb11['femage'+str(x)]==0,1,tgb11['femage'+str(x)])
    tgb11['malage'+str(x)]=np.where(tgb11['malage'+str(x)]>64,65,tgb11['malage'+str(x)])
    tgb11['femage'+str(x)]=np.where(tgb11['femage'+str(x)]>64,65,tgb11['femage'+str(x)])

age_cnt=[]
tgb11['p2p']=0
for x in range(1,16):
    tgb11['FEMALES_cnt'+str(x)]=np.where(tgb11['femage'+str(x)]>1,1,0)
    tgb11['MALES_cnt'+str(x)]=np.where(tgb11['malage'+str(x)]>1,1,0)
    age_cnt.append('FEMALES_cnt'+str(x))
    age_cnt.append('MALES_cnt'+str(x))
    tgb11['p2p']=tgb11['p2p']+tgb11['FEMALES_cnt'+str(x)]+tgb11['MALES_cnt'+str(x)]

coun=[]
for x in range(bday1,eday1+1):
    coun.append('EFF'+str(x))
tgb11['coun']=tgb11[coun].apply(lambda s: (s != 2).sum(), axis=1)


for i in range(bday1,eday1+1):
## Code chnaged by Alex : whenever there is a  year change need to use the if Statement, change the julian date accordingly 
#    if (tgb11['day1']+1+(i-bday1))[0] >= 18366:
#        tgb11['day1'] = 18999
    tgb11['Counter'+str(i)]=np.where(tgb11['EFF'+str(i)] !=2,tgb11['day1']+1+(i-bday1),0)


tgb12 = tgb11[[col for col in list(tgb11) if col.startswith('Counter') or col.startswith('Index')]]

df_unpivot = pd.melt(tgb12,id_vars=['Index'],var_name=['Counter'])
df_unpivot = df_unpivot[df_unpivot.value != 0]
df_unpivot = df_unpivot.drop_duplicates()
df_unpivot = df_unpivot.rename(columns={'value':'day'})
del df_unpivot['Counter']
df_unpivot = df_unpivot.sort_values(['Index','day'],ascending=[1,1])

tgb11 = tgb11.loc[np.repeat(tgb11.index.values,tgb11.coun)]
tgb11 = tgb11.reset_index()
df_unpivot = df_unpivot.reset_index()

tgb11 = pd.concat([tgb11,df_unpivot],axis=1)

Counter=[]
for i in range(bday1,eday1+1):
    Counter.append("Counter"+ str(i))
tgb11 = tgb11.drop(Counter, axis=1)
tgb11 = tgb11.drop(EFF, axis=1)
tgb11 = tgb11.drop(age_cnt, axis=1)
tgb11 = tgb11.drop(['ahoh', 'bday', 'coun', 'eday', 'edu', 'enddate',
                    'Index', 'lpm', 'meterType', 'npm', 'nsys', 'spn',
                    'startdate', 'STARTER', 'state', 'vgame', 'WW','day1'],axis=1)



#****************************************************************************
#                             SECTION 2
#****************************************************************************

tgb2=pd.read_fwf(inpath+infile2,colspecs=colspecs1, names=fname1,
                 converters={'state':int, 'FEMALES':int, 'MALES':int,
                             'nsys':int, 'WW':int}) 
tgb2.drop(tgb2.index[:1], inplace=True)
tgb2=tgb2.reset_index(drop='index')

start_end=pd.read_fwf(inpath+infile1,header=None,nrows=1)
start_end=str(start_end.ix[0,0])
startdate=start_end[1:6]
enddate=start_end[7:12]

tgb2['startdate']=startdate
tgb2['enddate']=enddate
tgb2['day2']=day2
tgb2['bday']=bday2
tgb2['eday']=eday2

tgb2['STARTER'] = tgb2.nsys*7 + 391
tgb2['npm']=np.where((tgb2.dma==517)&(tgb2.lpm=='Y'),'Y',tgb2.npm)

tgb2['ed']=np.where(tgb2.edu<12,1,np.where(tgb2.edu==12,2,np.where((tgb2.edu>12)&(tgb2.edu<16),3,np.where(tgb2.edu>15,4,0))))
tgb2['hisp']=np.where(tgb2.spn==1,2,1)
tgb2['hhsz']=np.where(tgb2.hhsz>5,5,tgb2.hhsz)
tgb2['ahoh']=np.where(tgb2.ahoh>100,100,tgb2.ahoh)

codreg = [3,4,3,4,4,1,3,3,3,3,4,2,2,2,2,3,3,1,3,1,2,2,3,2,4,2,4,1,1,4,1,3,2,2,3,4,1,1,3,2,3,3,4,1,3,4,3,2,4,4,4]
codreg2 = pd.DataFrame({'codreg': codreg})
codreg2.index = range(1,len(codreg2)+1)
codreg2['state'] = codreg2.index
tgb2.state = tgb2.state.astype(int)
tgb22 = pd.merge(tgb2, codreg2, how='left', on=['state'])

def func(x):
    if 1 <= x <= 24:
        return '1'
    elif 25 <= x <= 34:
        return '2'
    elif 35 <= x <= 44:
        return '3'
    elif 45 <= x <= 54:
        return '4'
    elif 55 <= x <= 64:
        return '5'
    return '6'

tgb22['hoh'] = tgb22['ahoh'].apply(func)
tgb22['Index'] = tgb22.index
tgb22['p2p']=0


for x in range(1, 16):
    tgb22['posF'+str(x)]=0
    tgb22['posM'+str(x)]=0 


tgb22['posF1']=np.where(tgb22.FEMALES>0,tgb22.STARTER,0)
tgb22['posM1']=np.where(tgb22.MALES>0,tgb22.STARTER+(3*tgb22.FEMALES)+(3*tgb22.WW),0)
for i in range(2,16):
    tgb22['posF'+str(i)]=np.where(tgb22.FEMALES>(i-1),tgb22['posF'+str(i-1)]+3,0)
    tgb22['posM'+str(i)]=np.where(tgb22.MALES>(i-1),tgb22['posM'+str(i-1)]+3,0)


lines2 = open(inpath+infile2).read().splitlines()
lines2 = pd.DataFrame({'col': lines2})
lines2.drop(lines2.index[:1], inplace=True)
lines2=lines2.reset_index(drop='index')
tgb22=tgb22.join(lines2)


for f in range(1,16):
    pos=tgb22['posF'+str(f)]
    ln=[]
    for row,i in zip(tgb22['col'],range(0,len(lines2.col))):
        ln.append(row[pos[i]-1:pos[i]+2])
    ln = pd.DataFrame({'femage'+str(f): ln})
    ln[['femage'+str(f)]] = ln[['femage'+str(f)]].apply(pd.to_numeric)
    ln['Index'] = ln.index
    tgb22 = pd.merge(tgb22, ln, how='left', on=['Index'])
    
for m in range(1,16):
    pos=tgb22['posM'+str(m)]
    ln=[]
    for row,i in zip(tgb22['col'],range(0,len(lines2.col))):
        ln.append(row[pos[i]-1:pos[i]+2])
    ln = pd.DataFrame({'malage'+str(m): ln})
    ln[['malage'+str(m)]] = ln[['malage'+str(m)]].apply(pd.to_numeric)
    ln['Index'] = ln.index
    tgb22 = pd.merge(tgb22, ln, how='left', on=['Index'])

a=['col']
for x in range(1, 16):
    a.append('posF'+str(x))
    a.append('posM'+str(x))
tgb22 = tgb22.drop(a, axis=1)

for x in range(1, 16):
    tgb22['malage'+str(x)].fillna(-1, inplace=True)
    tgb22['femage'+str(x)].fillna(-1, inplace=True)
    
for x in range(1, 16):
    tgb22['malage'+str(x)]=np.where(tgb22['malage'+str(x)]==0,1,tgb22['malage'+str(x)])
    tgb22['femage'+str(x)]=np.where(tgb22['femage'+str(x)]==0,1,tgb22['femage'+str(x)])
    tgb22['malage'+str(x)]=np.where(tgb22['malage'+str(x)]>64,65,tgb22['malage'+str(x)])
    tgb22['femage'+str(x)]=np.where(tgb22['femage'+str(x)]>64,65,tgb22['femage'+str(x)])

age_cnt=[]
tgb22['p2p']=0
for x in range(1,16):
    tgb22['FEMALES_cnt'+str(x)]=np.where(tgb22['femage'+str(x)]>1,1,0)
    tgb22['MALES_cnt'+str(x)]=np.where(tgb22['malage'+str(x)]>1,1,0)
    age_cnt.append('FEMALES_cnt'+str(x))
    age_cnt.append('MALES_cnt'+str(x))
    tgb22['p2p']=tgb22['p2p']+tgb22['FEMALES_cnt'+str(x)]+tgb22['MALES_cnt'+str(x)]


coun=[]
for x in range(bday2,eday2+1):
    coun.append('EFF'+str(x))
tgb22['coun']=tgb22[coun].apply(lambda s: (s != 2).sum(), axis=1)

for i in range(bday2,eday2+1):
    tgb22['Counter'+str(i)]=np.where(tgb22['EFF'+str(i)] !=2,tgb22['day2']+1+(i-bday2),0)        
    
tgb23 = tgb22[[col for col in list(tgb22) if col.startswith('Counter') or col.startswith('Index')]]

df_unpivot = pd.melt(tgb23,id_vars=['Index'],var_name=['Counter'])
df_unpivot = df_unpivot[df_unpivot.value != 0]
df_unpivot = df_unpivot.drop_duplicates()
df_unpivot = df_unpivot.rename(columns={'value':'day'})
del df_unpivot['Counter']
df_unpivot = df_unpivot.sort_values(['Index','day'],ascending=[1,1])

tgb22 = tgb22.loc[np.repeat(tgb22.index.values,tgb22.coun)]
tgb22 = tgb22.reset_index()
df_unpivot = df_unpivot.reset_index()

tgb22 = pd.concat([tgb22,df_unpivot],axis=1)

tgb22['day']=np.where(tgb22.day==16367,17001,tgb22.day)
Counter=[]
for i in range(bday2,eday2+1):
    Counter.append("Counter"+ str(i))
tgb22 = tgb22.drop(Counter, axis=1)
tgb22 = tgb22.drop(age_cnt, axis=1)
tgb22 = tgb22.drop(EFF, axis=1)
tgb22 = tgb22.drop(['ahoh', 'bday', 'coun', 'eday', 'edu', 'enddate',
                    'Index', 'lpm', 'meterType', 'npm', 'nsys', 'spn',
                    'startdate', 'STARTER', 'state', 'vgame', 'WW','day2'],axis=1)

#****************************************************************************
vars()['tgb2for' +str(period)] = tgb11.append(tgb22, ignore_index=True)
vars()['tgb2for' +str(period)].to_pickle(path+'tgb2for'+str(period)+'.pkl')
#****************************************************************************


#****************************************************************************
#                        wts.national
#****************************************************************************
try:
    infile3 = 'wts.natl.' + period  #wtffile3
    colspecs3 = [(13,24),(0,6),(25, 33)]
    fname3 = ['hhld','day','weight']
    wts=pd.read_fwf(inpath+infile3,colspecs=colspecs3, names=fname3, converters={'weight':int}) 
    wts['weight'] = wts['weight']/28

except:
    infile3 = 'wts.national'  #wtffile3
    colspecs3 = [(13,24),(0,6),(25, 33)]
    fname3 = ['hhld','day','weight']
    wts=pd.read_fwf(inpath+infile3,colspecs=colspecs3, names=fname3, converters={'weight':int}) 
    wts['weight'] = wts['weight']/28
#****************************************************************************

vars()['wwts'+str(period)]=pd.merge(vars()['tgb2for'+str(period)],wts,on=['hhld','day'],how='inner')

nomatch_temp=pd.merge(vars()['tgb2for'+str(period)],wts,on=['hhld','day'],how='outer')
nomatch=nomatch_temp[pd.isnull(nomatch_temp).any(axis=1)]


Match_count=vars()['wwts'+str(period)]['weight'].count()
Match_mis=vars()['wwts'+str(period)]['weight'].isnull().values.ravel().sum() 
Match_sum=vars()['wwts'+str(period)]['weight'].sum()

nomatch_count=nomatch['weight'].count()
nomatch_mis=nomatch['weight'].isnull().values.ravel().sum() 
nomatch_sum=nomatch['weight'].sum()

Output_num_head = ['Match_count','Match_mis','Match_sum','nomatch_count','nomatch_mis','nomatch_sum']
Output_num = [Match_count,Match_mis,Match_sum,nomatch_count,nomatch_mis,nomatch_sum]

Output_num = pd.DataFrame({'Description':Output_num_head,'Values':Output_num})

writer = pd.ExcelWriter(path+'Tgb2_Output_num.xlsx')
Output_num.to_excel(writer,'Output_num')
writer.save()

#****************************************************************************
tstchd = vars()['wwts'+str(period)].copy(deep=True)

tstchd['CondF1']=0
tstchd['CondM1']=0
for i in range(1,5):
    tstchd['CondM'+str(i)]=0
    tstchd['CondF'+str(i)]=0

fage=[]
mage=[]
temp=[]
for i in range(1,16):
    fage.append('femage'+str(i))
    mage.append('malage'+str(i))
    temp.append('CondFtemp'+str(i))
    temp.append('CondMtemp'+str(i))
    tstchd['CondFtemp'+str(i)]=np.where((tstchd['femage'+str(i)]>11)&(tstchd['femage'+str(i)]<18),1,0)    
    tstchd['CondMtemp'+str(i)]=np.where((tstchd['malage'+str(i)]>11)&(tstchd['malage'+str(i)]<18),1,0)    
    tstchd['CondF1']=tstchd['CondF1']+tstchd['CondFtemp'+str(i)]
    tstchd['CondM1']=tstchd['CondM1']+tstchd['CondMtemp'+str(i)]

for i in range(1,16):
    tstchd['CondFtemp'+str(i)]=np.where((tstchd['femage'+str(i)]>5)&(tstchd['femage'+str(i)]<=11),1,0)    
    tstchd['CondMtemp'+str(i)]=np.where((tstchd['malage'+str(i)]>5)&(tstchd['malage'+str(i)]<=11),1,0)    
    tstchd['CondF2']=tstchd['CondF2']+tstchd['CondFtemp'+str(i)]
    tstchd['CondM2']=tstchd['CondM2']+tstchd['CondMtemp'+str(i)]


for i in range(1,16):
    tstchd['CondFtemp'+str(i)]=np.where((tstchd['femage'+str(i)]>1)&(tstchd['femage'+str(i)]<=5),1,0)    
    tstchd['CondMtemp'+str(i)]=np.where((tstchd['malage'+str(i)]>1)&(tstchd['malage'+str(i)]<=5),1,0)    
    tstchd['CondF3']=tstchd['CondF3']+tstchd['CondFtemp'+str(i)]
    tstchd['CondM3']=tstchd['CondM3']+tstchd['CondMtemp'+str(i)]

for i in range(1,16):
    tstchd['CondFtemp'+str(i)]=np.where(tstchd['femage'+str(i)]==1,1,0)    
    tstchd['CondMtemp'+str(i)]=np.where(tstchd['malage'+str(i)]==1,1,0)    
    tstchd['CondF4']=tstchd['CondF4']+tstchd['CondFtemp'+str(i)]
    tstchd['CondM4']=tstchd['CondM4']+tstchd['CondMtemp'+str(i)]

tstchd.drop(temp,axis=1,inplace=True)

for i in range(1,5):
    tstchd['Cond'+str(i)]=tstchd['CondF'+str(i)]+tstchd['CondM'+str(i)]

tstchd['pp1']=np.where(tstchd.Cond4>0,1,0)
tstchd['pp2']=np.where(tstchd.Cond3>0,1,0)
tstchd['pp3']=np.where(tstchd.Cond2>0,1,0)
tstchd['pp4']=np.where(tstchd.Cond1>0,1,0)

tstchd['bin']=8*tstchd.pp1+4*tstchd.pp2+2*tstchd.pp3+tstchd.pp4

recchd=[5,4, 7, 3, 8, 6, 9, 2, 16, 14, 15, 10, 12, 11, 13]
recchd1 = pd.DataFrame({'ch16': recchd})
recchd1.index = range(1,len(recchd1)+1)
recchd1['bin'] = recchd1.index
tstchd= pd.merge(tstchd, recchd1, how='left', on=['bin'])
tstchd['ch16']=np.where(tstchd.ch16.isnull(),1,tstchd.ch16)

#***********************************************************************

agesex_temp=tstchd.copy(deep=True)
recage=[1,2,2,2,2,3,3,3,4,4,4,5,5,5,6,6,6,7,7,7,8,8,8,8,9,9,9,9,9,10,10,10,10,10,11,11,11,11,11,12,12,12,12,12,13,13,13,13,13,14,14,14,14,14,15,15,15,15,15,15,15,15,15,15,16]
agesex_temp['wtp2p']=agesex_temp['p2p']*agesex_temp['weight']

for i in range(1,17):
    agesex_temp['fout'+str(i)]=0
    agesex_temp['mout'+str(i)]=0

for i in range(1,16):
    recage1 = pd.DataFrame({'recagef'+str(i): recage})
    recage1.index = range(1,len(recage1)+1)
    recage1['femage'+str(i)]=recage1.index
    agesex_temp= pd.merge(agesex_temp, recage1, how='left', on=['femage'+str(i)])
    agesex_temp['recagef'+str(i)]=np.where(agesex_temp['recagef'+str(i)].isnull(),-1,agesex_temp['recagef'+str(i)])

for i in range(1,16):
    recage1 = pd.DataFrame({'recagem'+str(i): recage})
    recage1.index = range(1,len(recage1)+1)
    recage1['malage'+str(i)]=recage1.index
    agesex_temp= pd.merge(agesex_temp, recage1, how='left', on=['malage'+str(i)])
    agesex_temp['recagem'+str(i)]=np.where(agesex_temp['recagem'+str(i)].isnull(),-1,agesex_temp['recagem'+str(i)])
    
for j in range(1,17):
    for i in range(1,16):
        agesex_temp.loc[agesex_temp['recagef'+str(i)] == j, 'fout'+str(j)] = agesex_temp['fout'+str(j)]+agesex_temp.weight
        agesex_temp.loc[agesex_temp['recagem'+str(i)] == j, 'mout'+str(j)] = agesex_temp['mout'+str(j)]+agesex_temp.weight


del_col=[]
for i in range(1,16):
    del_col.append('femage'+str(i))
    del_col.append('malage'+str(i))
    del_col.append('recagef'+str(i))
    del_col.append('recagem'+str(i))
agesex_temp = agesex_temp.drop(del_col, axis=1)

agesex_temp.columns = [i.lower() for i in agesex_temp.columns]

temp_list = ['CondF1','CondM1','CondF2','CondM2','CondF3',
'CondM3','CondF4','CondM4','Cond1','Cond2','Cond3','Cond4','pp1','pp2','pp3',
'pp4','bin','Index','index','MALES','FEMALES','p2p']

agesex_temp = agesex_temp.drop([i.lower() for i in temp_list],axis=1)

vars()['agesex'+str(period)]=agesex_temp.copy(deep=True)
vars()['agesex'+str(period)].to_pickle(path+'agesex'+str(period)+'.pkl')

#****************************************************************************