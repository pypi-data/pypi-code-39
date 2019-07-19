import os
os.environ["OMP_NUM_THREADS"] = "1"
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

import numpy as np
import pandas as pd
import numpy.core.multiarray
import fastcluster
from multiprocessing import Pool,cpu_count
from functools import partial
from contextlib import closing
from joblib import Parallel, delayed
import itertools
import scipy.stats as st

def flatten(container):
    for i in container:
        if isinstance(i, (list,tuple)):
            for j in flatten(i):
                yield j
        else:
            yield i
def flatx(x):
    return tuple(sorted(flatten(x)))

def dist(R,method):
	N = R.shape[0]
	d = R[np.triu_indices(N,1)]


	if method=='average':
		out = fastcluster.average(d)
	if method=='complete':
		out = fastcluster.complete(d)
	if method=='single':
		out = fastcluster.single(d)

	outI = out.astype(int)

	dend = {i:(i,) for i in xrange(N)}

	for i in xrange(len(outI)):
		dend[i+N] = (dend[outI[i][0]],dend[outI[i][1]])


	for i in xrange(N):
		dend.pop(i,None)

	dend = [(flatx(a),flatx(b)) for a,b in dend.values()]

	dend ={flatx((a,b)):(np.array(a),np.array(b)) for a,b in dend}
	return dend
   
def singPV(Rb,method):
    
    if method=='average':
        rxy = dict(map(lambda (k,(a,b)): (k,Rb[a][:,b].mean()),LV.items()))
    if method=='complete':
        rxy = dict(map(lambda (k,(a,b)): (k,Rb[a][:,b].max()),LV.items()))
    if method=='single':
        rxy = dict(map(lambda (k,(a,b)): (k,Rb[a][:,b].min()),LV.items()))

    PV = map(lambda (k,q):int(rxy[q]<rxy[k]), gen.items())
    
    return PV

#X,LV,nan,method,gen
def SingleBoot(nan,method,metric,sel):
    
    Xb = Xg[:,sel]
    if nan==False:
		if metric=='pearson':
			Rb = 1.-np.corrcoef(Xb)
		elif metric=='spearman':
			Rb = 1.-st.spearmanr(Xb.T)[0]
    else:
        Rb = 1.-np.array(pd.DataFrame(Xb.T).corr())
        
    return singPV(Rb,method)

    
def BootDist(method,Nt=1000,nan=False,ncpu=1,metric='pearson'):
	
	global gen
	gen = {tuple(s):k for k in LV for s in LV[k] if len(s)>1}

	sels = np.random.choice(range(Xg.shape[1]),replace=True,size=(Nt,Xg.shape[1]))
	
	f = partial(SingleBoot,nan,method,metric)

	PV = Parallel(n_jobs=ncpu, backend="threading")(delayed(f)(sel) for sel in sels)

	return sorted(zip(np.array(PV).mean(axis=0),gen.keys()))
    
def FDR(PV,alpha,N):
	p = np.array(zip(*PV)[0])
	thr = np.arange(1,len(PV)+1)*alpha/len(PV)

	sel = np.where(p<thr)[0]
	if len(sel)==0: 
		thr=-1.
	else:
		thr = thr[sel][-1]

	L = [range(N)]+[PV[i][1] for i in np.where(p<=thr)[0]]
	L = map(tuple,sorted(L,key=len,reverse=True))
	
	PV = {c:p for p,c in PV}
	PV[tuple(range(N))] = np.nan
	return L,PV

def Analytic_PV(r,n):

	R = 1-r
	gen = {tuple(s):k for k in LV for s in LV[k] if len(s)>1}

	sd = np.vectorize(lambda x: (1./n)*(1-x**2)**2)
	COV = lambda (j,k),(h,m): (0.5/n)*(((R[j,h]-R[j,k]*R[h,k])*(R[k,m]-R[k,h]*R[h,m]))+((R[j,m]-R[j,h]*R[h,m])*(R[k,h]-R[k,j]*R[j,h]))+((R[j,h]-R[j,m]*R[m,h])*(R[k,m]-R[k,j]*R[j,m]))+((R[j,m]-R[j,k]*R[k,m])*(R[k,h]-R[k,m]*R[m,h])))

	PV = []
	for h,(son,fat) in enumerate(gen.items()):
		
		
		a_s,b_s = LV[son]
		a_f,b_f = LV[fat]

		m = R[a_s][:,b_s].mean()-R[a_f][:,b_f].mean()

		ss = sd(R[a_s][:,b_s])
		sf = sd(R[a_f][:,b_f])

		elm_f = list(itertools.product(a_f, b_f))
		elm_s = list(itertools.product(a_s, b_s))

		ns = 1./np.size(ss)
		nf = 1./np.size(sf)

		cf = (nf**2)*2*sum(COV(elm_f[i],elm_f[j]) for i in xrange(len(elm_f)) for j in xrange(i))
		cs = (ns**2)*2*sum(COV(elm_s[i],elm_s[j]) for i in xrange(len(elm_s)) for j in xrange(i))
		cmix = -2*(ns*nf)*sum(COV(elm_f[i],elm_s[j]) for i in xrange(len(elm_f)) for j in xrange(len(elm_s)))
		
		x = (ns**2)*ss.sum()+(nf**2)*sf.sum()+cf+cs+cmix
		
		s = np.sqrt(x)

		PV.append((st.norm.cdf(0,m,s),son))

	return PV
	
def Find_ValidatedCluster(X,Nt=1000,alpha=0.05,nan=False,ncpu=cpu_count(),dendrogram=None,method='average',metric='pearson'):
	if nan==False:
		if metric=='pearson':
			R = 1 - np.corrcoef(X)
		elif metric=='spearman':
			R = 1-st.spearmanr(X.T)[0]
	else:
		R = 1. -np.array(pd.DataFrame(X.T).corr()) 
		
	global Xg
	Xg = X
	
	global LV
	if dendrogram==None:
		LV = dist(R,method)
	else:
		LV = dendrogram
	
	
	if Nt==0:
		PV = Analytic_PV(R,X.shape[1])
	else:	
		PV = BootDist(method,Nt,nan,ncpu,metric)
	
	
	L,PV = FDR(PV,alpha,X.shape[0])

	return L,PV,LV
	
	

