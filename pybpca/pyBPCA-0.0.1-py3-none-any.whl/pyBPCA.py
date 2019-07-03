############################################################################
#         Here we attempt to solve the boundary-constrained PCA.
# The chosen formalism is based on the paper "Principal component analysis with boundary constraints"
# P. Giordani and Henk Kiers, J. Chemometrics, 2007, 21: 547-556
#
# Being applied towards RENCI geo-physics work (B.BLanton, J.Tilson)
#                             genetics work (J. Tilson, K. Wilhelmsen)
#
# J.L.Tilson, B. Blanton and discussions with K. Wilhelmsen
#############################################################################

import sys
import time as tm
import pandas as pd
import numpy as np
import seaborn as sns
from scipy.sparse.linalg import svds
from scipy import stats,array, linalg, dot
from scipy.optimize import nnls
from numpy import arange, dot
from numpy.linalg import norm
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

########################################################################
# Solve the NNLS for the implicitely bound problem
# First initial guess is always an SVD
#
# INPUT:
# X: the optionally transformed nxm data matrix to process
# bmin,bmax the SCALER lower ands upper bounds e.g., 0,1. These will be expanded and transformed as required
# inp: Number of components to retain (p)
# maxiter (default=100) maxmimum number of convergence iterations
# numRandom (default=None) Number of random starts for A and B (incompatible with startdSVD, takes precedence)
# scalingMethod = 0,1,2. 0=None, 1=Standardized, 2=MinMaq
#
# OUTPUT:
# If input data were scaled, then on output the solution is DESCALED
#
# Return Aopt (nxp), Bopt (mxp) as numpy ndarrays for the optimum solution
# Return X_reconstructed as X = AoptBopt^t for the selected p

def solveNNLS(GG,hh):
    nr,nc = GG.shape
    E = np.concatenate((GG.T,hh.T.reshape(1,-1)),axis=0)
    f = np.zeros(nc+1)
    f[nc]=1
    nnlsval,rnorm = nnls(E,f) 
    rnorms = np.dot(E,nnlsval)-f
    z = -rnorms[0:nc]/rnorms[nc]
    return (z)

def solveBoundedMatrix(M,xi,blow,bup):
    """For input data if dimension (n,m) for n observations and m features
    M of dimension (m,p) or (n,p) respectively
    xi the partial projection vector (B^txi or A^txi) (p,)
    bmin is a vector of minimum values (length m or n)
    bmax is a vector of maximum values (length m or n)
    """
    n,p = M.shape
    MM = np.dot(M.T,M)
    Mxi = np.dot(M.T,xi)
    h = np.concatenate((blow,-bup),axis=0)
    G = np.concatenate((M,-M),axis=0)
    # Generate inverse part of solution
    R = linalg.cholesky(MM,lower=False)
    RR = linalg.inv(R)
    EEinv = np.dot(RR,RR.T) # is equiv to linalg.inv(np.dot(M.T,M))
    # other matrix-vector products 
    GG = np.dot(G,RR)
    hh = h - np.dot(G,np.dot(EEinv,Mxi))
    # Solve the NNLS
    nnlsSolve = solveNNLS(GG,hh)
    solution  = np.dot(RR,nnlsSolve)+np.dot(EEinv,Mxi)
    return (solution)

############################################################################
# Sum squares of error
def sumSquaresDiff(In,Out):
    ssq = np.sum((In-Out)**2)
    return (ssq)

# Frobenius norm diffs
def frobNorm(In,Out):
    frac_k = np.linalg.norm(In-Out)
    return (frac_k)

##############################################################################
# Scaling the feature (column) data. Need to retain parameters for Descaling later
# Add bounds conversion

def MinMaxScaling(X):
    Xmax = X.max(axis=0)
    Xmin = X.min(axis=0)
    scaler = MinMaxScaler(feature_range=(0.0,1.0)) # Might also want 0.1,0.9 instead
    Xscaled = scaler.fit_transform(X)
    return (Xscaled,Xmin,Xmax)

def MinMaxDeScaling(Xscaled,Xmin,Xmax):
    m = Xscaled.shape[1]
    n = Xscaled.shape[0]
    Xdescaled = np.zeros((n,m))
    for i in range(0,m):
        max = Xmax[i]
        min = Xmin[i]
        Xdescaled[:,i] = [(max-min)*j+min for j in X[:,i]]
    return (Xdescaled)

def MinMaxScaleBounds(Xmin,Xmax,bamin,bamax):
    """Take on input bamin,bamax VECTORS (m,) of probably =0,1 respectively
    and scale 
    """
    m = bamin.shape[0]
    bamin_scaled = np.zeros(m)
    bamax_scaled = np.zeros(m)
    for i in range(0,m):
        max = Xmax[i]
        min = Xmin[i]
        bamin_scaled[i] = (bamin[i]-min)/(max-min)
        bamax_scaled[i] = (bamax[i]-min)/(max-min)
    return (bamin_scaled,bamax_scaled)

def StandardScaling(X):
    """Perform center mean and variance one standardization
    Scale the data as scale = (X-means)/SQRT(vars)
    """
    scaler = StandardScaler()  
    Xscaled = scaler.fit_transform(X)
    means = scaler.mean_
    variances = scaler.var_
    return (Xscaled, means, variances)

def StandardDeScaling(Xscaled,means,variances):
    """Descale the input matrix X as Xde = X*SQT(vars)+means
    """
    Xdescaled = (Xscaled * np.sqrt(variances)) + means
    return (Xdescaled)

def StandardScaleBounds(means,variances,bamin,bamax):
    """Perform the centering and std scaling of the bounds
    Take on input bamin,bamax VECTORS (m,) of probably =0,1 respectively
    and scale
    """
    invSD = 1.0/np.sqrt(variances)
    bamin_scaled = (bamin-means)*invSD
    bamax_scaled = (bamax-means)*invSD
    return (bamin_scaled,bamax_scaled)

##############################################################################
# Misc
def expandToMatrix(n,m,bamin,bamax):
    """Take a VECTOR (m,) of BAMIN and BAMAX and expand to 
    a matrix of size (n,m) where we replicate data across rows
    """
    bamax_mat = np.full((n,m),0.0)
    bamin_mat = np.full((n,m),0.0)
    for i in range(0,n):
        bamax_mat[i,:]=bamax
        bamin_mat[i,:]=bamin
    return (bamin_mat,bamax_mat)

##############################################################################

class pyBPCA(object):
    """An implementation of the Boundary PCA method. This is a prototype to ascertain 
    performance issues and final architecture
    """

    def reportParameters(self):
        print('pyBPCA current parameters')
        print('filename is '+self.filename)
        print('num Components (p) '+str(self.p))
        print('maxiterations '+str(self.maxiter))
        print('epsilon '+str(self.epsilon))
        if (self.scalingMethod==1):
            print('Scaling: Center mean and variance')
        elif (self.scalingMethod==1):
            print('Scaling: MinMax')
        else:
            print('No scaling')
        print('bmax and bmin '+str(self.bmax)+' '+str(self.bmin))

    def __init__(self, filename=None, p=0, maxiter=100, epsilon=1e-6, numRandom=1, scalingMethod=0, showTimes=False):
        self.filename = filename
        self.p = p
        self.maxiter = maxiter
        self.epsilon = epsilon
        self.numRandom = numRandom
        self.scalingMethod=0
        if (scalingMethod==1):
            self.scalingMethod=1
        if (scalingMethod==2):
            self.scalingMethod=2
        self.showTimes = showTimes
        self.bmax = 1.0
        self.bmin = 0.0
        self.reportParameters()

    def runProcess(self):
        """The test_pyBPCA case doesn;t have the proper format
        """
        #infilename = 'test_pyBPCA.tsv'
        #df_X = pd.read_csv(infilename,header=0,index_col = 0, delim_whitespace=True)
        infilename = self.filename
        df_X = pd.read_csv(infilename,header=None,delim_whitespace=True,skiprows=[0,1])
        # 
        X = df_X.values
        n = df_X.shape[0]
        m = df_X.shape[1]
        p = self.p
        # 
        # Initial (untransformed bounds) as scalers
        bmax = self.bmax # Assumes an untransformed dataset.
        bmin = self.bmin # Assumes an untransformed dataset.
        # 
        #Initial guess type is always SVD. Set numRandom =1 for a single cycle
        # using SVDF guess. Else if > 1 remaining cycles are random restarts for
        # A,B. The best A,B, [air is reported after maxiter cycles
        numRandom=self.numRandom
        #
        # Scale the data ? (0,1,2) 1=Center/scale,2=MinMax, else no
        scalingMethod=self.scalingMethod
        # Show individual times per iteration
        showTimes=self.showTimes
        #
        # Convergence criteria macro/microiterations
        fracOpt = 1e6 # Set convergence initial check large
        maxiter = self.maxiter 
        epsilon = self.epsilon 
        # 
        numBPCAcomponents = p # Check if larger than min(nrows,ncols)
        # 
        if (p > np.minimum(n,m)):
           print('p too big')
           raise SystemExit
        #
        # Build a bamin/bamax VECTOR based on bmin and bmax scalers (will be expanded to a matrix later)
        bamax_vec = np.full((X.shape[1]),bmax)
        bamin_vec = np.full((X.shape[1]),bmin)
        # 
        # If scalingMethod is not 1 or 2 then do no scaling
        # Now expand bounds
        bamin,bamax = expandToMatrix(n,m,bamin_vec,bamax_vec)
        Xrun = X
        #
        # If MinMax transform do so here including the bounds
        if (scalingMethod==2):
            print('MinMax scale the data and bounds')
            Xscaled,Xmin,Xmax = MinMaxScaling(X)
            bamin_scaled,bamax_scaled = MinMaxScaleBounds(Xmin,Xmax,bamin_vec,bamax_vec)
            # Now expand scaled bounds
            bamin,bamax = expandToMatrix(n,m,bamin_scaled,bamax_scaled)
            Xrun = Xscaled
        # 
        # If Center/variance scaling
        if (scalingMethod==1):
            print('Standard scale the data and bounds')
            Xscaled,means,variances = StandardScaling(X)
            bamin_scaled,bamax_scaled = StandardScaleBounds(Xmin,Xmax,bamin_vec,bamax_vec)
            bamin,bamax = expandToMatrix(n,m,bamin_scaled,bamax_scaled)
            Xrun = Xscaled
        # 
        frac_old = 1e12
        frac = 0.0
        # 
        tmin = tm.time()
        for istart in range(0,numRandom):
            if (istart == 0):
                print('SVD initial guess')
                U, s, VT = svds(X.astype('d'),k=p,which='LM')
                high2low = np.argsort(s)[::-1][:p]
                s = s[high2low]
                U = U[:,high2low]
                VT = VT[high2low,:]
                d = np.identity(p)
                np.fill_diagonal(d, s)
                Aa = np.dot(U,d)
                Bb = VT.T
            else:
                print('Randomized BPCA restart '+str(istart))
                Aa = np.random.rand(n,p)
                Bb = np.random.rand(m,p)
            frac = sumSquaresDiff(Xrun,np.dot(Aa,Bb.T))
            iter = 0
        ######################################## Start macroiterations
            while np.abs(frac-frac_old) > epsilon:
                tmin = tm.time()
                frac_old = frac
                for i in range(0,n):
                    xi = Xrun[i,:]
                    bupper = bamax[i,:]
                    blower = bamin[i,:]
                    ai_k = solveBoundedMatrix(Bb,xi,blower,bupper)
                    Aa[i,:] = ai_k.reshape(1,-1)
                for j in range(0,m):
                    aupper = bamax[:,j]
                    alower = bamin[:,j]
                    xj = Xrun[:,j]
                    bj_k = solveBoundedMatrix(Aa,xj,alower,aupper)
                    Bb[j,:] = bj_k
                # Compute error measurement
                frac = sumSquaresDiff(Xrun,np.dot(Aa,Bb.T)) # Alt is # frac_k = frobNorm(X,np.dot(A,B.T))
                if (np.mod(iter,40)==0):
                    print(frac_old-frac)
                iter += 1
                if (iter >= maxiter):
                    print('Microiteration Convergence cancelled because of maxiter ceiling '+str(iter))
                    break
                timeit = tm.time()-tmin
                if (showTimes):
                    print('Time for iteration is '+str(timeit))
            if (frac < fracOpt): # This is for outer random-restart loop
                print('Update current solution')
                fracOpt = frac
                Aopt = Aa
                Bopt = Bb
        
        ttotal = tm.time()-tmin
        print('Total BPCA runtime is '+str(ttotal))
        # Report FitP metric from Giordani et al.
        FitP=(1-(np.sum((Xrun-np.dot(Aopt,Bopt.T))**2)/np.sum(Xrun**2)))*100
        print('FitP '+str(FitP))
        #
        # Construct final signal and report overall max / min: Are we feasible? 
        X_reconstructed = np.dot(Aopt,Bopt.T)
        print(str(X_reconstructed.max().max()))
        print(str(X_reconstructed.min().min()))
        #
        # No scaling was performed
        Xopt = X_reconstructed
        # MinMax Descale if neccessary ( No need to descale bounds )
        if (scalingMethod==2):
            print('Descaling MinMax transforfmed data')
            Xopt = MinMaxDeScaling(X_reconstructed,Xmin,Xmax)
        if (scalingMethod==1):
            print('Descaling Standard transforfmed data')
            Xopt = StandardDeScaling(X_reconstructed,means,variances)
        print('BPCA is complete')
        return (Aopt,Bopt,Xopt)

# Move to a better parser such as argparse. In the meantime all val;ues are mandatory
# Examples
# infilename = '/projects/sequence_analysis/vol1/prediction_work/ClimateML/SEA-ICE-rawdata/goddard_nt_seaice_conc_monthly_withll_23Apr2019.dat'
# p=60

#def main();
#    """Expose some of the obvious parameters to adjust: Need to move to a better method though
#    or build this as a bonifide class
#    """
#    print('Execute the pyBPCA method')
#    infilename = argv[1]
#    p = int(argv[2])
#    numRandom=int(argv[3])
#    scalingMethod=int(argv[4])
#    maxiter = int(argv[5])
#    epsilon = float(argv[6])
#
#if __name__== 'main:'
#    main()

