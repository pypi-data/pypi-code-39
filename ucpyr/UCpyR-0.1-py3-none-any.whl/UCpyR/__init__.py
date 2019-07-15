##### Implements the UCPR (Uniform Covering by Probabilistic Rejection) -
##### - algorithm as described in Klepper et al, 1994.

import numpy as np
from scipy.stats import f



def UCPR(G,lb,ub,alpha,k,N=200,c=0):

	"""
	Parameters
	==========
	G : function
		The function to be minimized
	lb : array
		The lower bounds of the design variable(s)
	ub : array
		The upper bounds of the design variable(s)
	alpha : scalar
		The desired confidence level
	k : int
		The number of experimental data points being fitted

	Optional
	========
	N : int
		The number of points to generate
	c : scalar
		The safety factor

	Returns
	=======
	Not sure yet

	"""

	assert len(lb)==len(ub), 'Lower- and upper-bounds must be the same length'
	assert hasattr(G, '__call__'), 'Invalid function handle'
	lb = np.array(lb)
	ub = np.array(ub)
	assert np.all(ub>lb), 'All upper-bound values must be greater than lower-bound values'

	vhigh = np.abs(ub - lb)
	vlow = -vhigh



	############### Useful Functions ###############

	def Gc(n,k,alpha,Gmin):
		return (1 +  n * f.ppf(alpha,n,k-n) / (k-n) ) * Gmin#Not sure yet whether this should be pdf or ppf (almost definitely pdf)

	def distance2(x1,x2):		#Vector Distance instead of Euclidean Distance
		distance=[]
		for i in range(len(x1)):
			distance.append( (x1[i] - x2[i]) / x2[i] )
		return distance

	def distance(x1,x2):			#Need to work on this a bit
		return np.sum( (x1-x2/x2 )**2 )


	def setdistance(p,x):
		distances=[]
		for i in range(N):
			distances.append( distance(p,x[i,:]) )

		return min(distances)



	############### Start Algorithm ###############

	if c==0:
		c = -np.log( (alpha)**(1/len(lb)) )

	n = len(lb)	#Number of parameters

	x = np.random.rand(N,n) #First set of points:
	for j in range(N):
		x[j, :] = lb + x[j, :]*(ub - lb)

	Gvalues=[] #Calculate G-values:
	for i in range(N):
		Gvalues.append( G(x[i,:]) )

	count=N
	print(count)

	while max(Gvalues) >= Gc(n,k,alpha,min(Gvalues)):

		print(Gc(n,k,alpha,min(Gvalues)))
		print(max(Gvalues))


		#Calculate R:

		NNdistances=[]
		for i in range(N):
			distances=[]
			for j in range(N):
				distances.append( distance(x[i,:],x[j,:]) )
			NNdistances.append(min(distances))

		'''NNdistances=[]
		for i in range(N):
			for j in range(N):
				NNdistances.append( distance(x[i,:],x[j,:]) )'''

		R=np.mean(NNdistances)*c

		#Generate a new point:

		p = np.random.rand(n)
		p = lb + p*(ub-lb)

		while G(p) > max(Gvalues) or setdistance(p,x) >= R:
			p = np.random.rand(n)
			p = lb + p*(ub-lb)


		#Replace worst point:

		worst = Gvalues.index(max(Gvalues))
		x[worst,:] = p

		Gvalues[worst]=G(p)

		count+=1
		print(count)

		np.savetxt('x_values.csv',x,delimiter=',')

	#Now we have a set of points in Gc

	
	########## Constructing Confidence Area ##########

	#For now, let's just return the points

	return x




########## Constructing Confidence Area ##########

def ConfidenceArea(x):

	upperbound=[]
	lowerbound=[]

	n=x.shape[1]

	for i in range(n):
		upperbound.append(max(x[:,i]))
		lowerbound.append(min(x[:,i]))

	return lowerbound,upperbound




'''		#Calculating R:
	distances=[]
	for i in range(N):
		for j in range(N):
			distances.append( distance(x[i,:],x[j,:]) )

	r_j = max(distances)

	R=[]
	for i in range(len(r_j)):
		R.append(r_j[i]*c)
'''

def g(params):
	x=params[0]
	y=params[1]
	return (2*np.sin(x**2) + np.cos(y**(1/3)) -1)**2

lb=[0,0]
ub=[10,10]

def h(params):
	x=params[0]
	y=params[1]
	return 10 - (np.sin(x) + np.cos(y))**2

lb=[0,-2]
ub=[4,2]




