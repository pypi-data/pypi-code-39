"""
module for implementing the cortical thickness algorithm by
G.M. Treece, A.H. Gee, P.M. Mayhew, K.E.S. Poole
"""
import sys
sys.path.append( '../fieldwork/field' )

import scipy
from scipy import fftpack as fft
from scipy.special import erf
from scipy import signal
from scipy.ndimage.filters import laplace, gaussian_gradient_magnitude, gaussian_filter1d
import segmentation_tools as ST
import scalarField
from matplotlib import pyplot as plot
from matplotlib.widgets import Slider
import time
import itertools
import pdb

def calcGradient( P, gaussianSigma=None ):
	""" calculates the derivative of all signals in P using averaged
	back and forward difference
	"""
	if gaussianSigma!=None:
		P1 = gaussian_filter1d( P, gaussianSigma )
	else:
		P1 = P
	
	dP = P1[:,1:] - P1[:,:-1]
	dP = scipy.hstack( (dP, dP[:,-1][:,scipy.newaxis]) )
	dP[:,1:-1] = (dP[:,1:-1] + dP[:,:-2]) / 2.0 # average back and forward diff for interior points
	dP = scipy.where( scipy.isfinite(dP), dP, 0.0 )
	return dP
	
def resampleProfile( p, x ):
	""" given discrete signal p, fit spline to it, and resample at x
	positions with even spacing
	"""
	return
	
def modelProfile2( x, y0, y1, y2, x0, x1, sigma, s, a ):
	
	r = s/2.0 * tan(a)
	denom = 2.0*r*sigma*sqrt(pi)
	
def sampleImage( I, G, GD, ND, NLim, spacing ):
	""" samples image along mesh normals at GF material points with
	the current set of field parameters.
	"""
		
	# sample image
	XN = G.evaluate_normal_in_mesh( GD ).T
	XMesh = G.evaluate_geometric_field( GD ).T
	
	# transform for image spacing
	XN = (XN/spacing).T
	XN = XN / scipy.sqrt((XN*XN).sum(1))[:,scipy.newaxis]	# normalise
	XMesh = (XMesh/spacing).T
	NLim = scipy.multiply( NLim, 1.0/scipy.sqrt((spacing*spacing).sum()) )
	
	XSample = ST.genSamplingPoints( XMesh, XN, ND, xLim=NLim )
	NL = NLim[1] - NLim[0]
	P = ST.sampleImage( I, XSample )
	
	return P

def makeObj( modelFunc, data, weights, xMin, xMax ):
	c = itertools.count(0)
	signError = {-1:1000000.0, 0:1000000.0, 1:0.0}	# penalty for negative thickness
	
	def bounds( x0, x1 ):
		return signError[scipy.sign(x0-xMin)] + signError[scipy.sign(xMax-x1)]
	
	def obj( x ):
		modelP = modelFunc( x )[0].real
		err = data - modelP
		#~ pdb.set_trace()
		err = err * err * weights + signError[scipy.sign(x[1]-x[0])] + bounds( x[0], x[1] )
		#~ print 'it:', c.next(), 'rms:', scipy.sqrt((err*err).mean())
		#~ print 'params:', x
		#~ if x[0]>x[1]:
			#~ pdb.set_trace()
			
		return err
		
	return obj

def fitProfile( modelFunc, data, x0, weights, xMin, xMax, **kwargs ):
	
	obj = makeObj( modelFunc, data, weights, xMin, xMax )
	xOpt, cov_x, info_dict, mesg, ier  = ST.leastsq( obj, x0, full_output=1, **kwargs )

	rmsOpt = scipy.sqrt(info_dict['fvec'].mean())

	extraOutputs = {'rms': rmsOpt, 'cov_x':cov_x, 'info_dict':info_dict, 'mesg':mesg, 'ier':ier}
	 
	return xOpt, extraOutputs

def calcCortexSteepestGradient( point, normal, P, dP, x, xtol=1e-5 ):
	# calculate angle between normal and imaging plane
	#~ a = scipy.arctan( normal[2] / scipy.sqrt(normal[0]*normal[0] + normal[1]*normal[1]) )
	
	# x0 is that largest +ve gradient, x1 and is largest -ve gradient
	a0 = dP.argmax()
	a1 = dP.argmin()
	
	x0 = x[ a0 ]
	x1 = x[ a1 ]
	
	# calculate coordinates of cortex boundaries
	#~ t = (x1-x0)*scipy.cos(a)
	t = (x1-x0)
	
	# calculate intensity values y0, y1 and y2 as the mean of the 
	# interior, cortex and exterior regions
	y0 = P[:a0].mean()
	y1 = P[a0:a1].mean()
	y2 = P[a1:].mean()
	
	return x0, x1, y0, y1, y2, t
	
def calcCortexY1Fixed( point, normal, sampledProfile, x, y1, s, p0, weights, xMin, xMax, fftN=None, xtol=1e-5 ):
	
	# calculate angle between normal and imaging plane
	a = scipy.arctan( normal[2] / scipy.sqrt(normal[0]*normal[0] + normal[1]*normal[1]) )
	#~ a = 0.0
	#~ r = s/2.0 * scipy.tan(a)
	xRes = x[1]-x[0]
	aTol = 1e-5
	
	# generate profile model function 2010 paper
	#~ if a < aTol:
		#~ pFunc = makeModelProfileFuncY1Fixed( x, y1, s, a, 'a22' )[0]
	#~ else:
		#~ pFunc = makeModelProfileFuncY1Fixed( x, y1, s, a, 'a3' )[0]
	
	# don't use out of plane blur
	pFunc = makeModelProfileFuncY1Fixed( x, y1, s, a, 'a22' )[0]
	
	# generate profile model function 2011 paper
	#~ pFunc = makeModelProfileFuncY1Fixed( x, y1, s, a, 'a1' )[0]
	
	# fit function
	pOpt, extra = fitProfile( pFunc, sampledProfile, p0, weights, xMin, xMax, xtol=xtol )
	#~ pOpt, rmsOpt = fitProfile( pFunc, sampledProfile, p0, weights, xtol, epsfcn=1e-1 )
	
	# calculate coordinates of cortex boundaries
	x0, x1 = pOpt[0], pOpt[1]
	#~ t = (x1-x0)*scipy.cos(a)
	t = (x1-x0)
	
	return pOpt, extra, pFunc, t
		
def calcCortexY1SigmaFixed( point, normal, sampledProfile, x, y1, s, sigma, p0, weights, xMin, xMax, fftN=None, xtol=1e-5 ):
	"""
	s: slice spacing
	"""
	
	# calculate angle between normal and imaging plane
	a = scipy.arctan( normal[2] / scipy.sqrt(normal[0]*normal[0] + normal[1]*normal[1]) )
	#~ a = 0
	#~ r = s/2.0 * scipy.tan(a)
	xRes = x[1]-x[0]
	aTol = 1e-5
	
	# generate profile model function
	#~ if a < aTol:
		#~ pFunc = makeModelProfileFuncY1SigmaFixed( x, y1, s, a, sigma, 'a22' )[0]
	#~ else:
		#~ pFunc = makeModelProfileFuncY1SigmaFixed( x, y1, s, a, sigma, 'a3' )[0]
	
	# don't use out of plane blur
	pFunc = makeModelProfileFuncY1SigmaFixed( x, y1, s, a, sigma, 'a22' )[0]
		
	# generate profile model function 2011 paper
	#~ pFunc = makeModelProfileFuncY1SigmaFixed( x, y1, s, a, sigma, mode='a1' )[0]
	
	# fit function
	pOpt, extra = fitProfile( pFunc, sampledProfile, p0, weights, xMin, xMax, xtol=xtol )
	#~ pOpt, rmsOpt = fitProfile( pFunc, sampledProfile, p0, weights, xtol, epsfcn=1e-1 )
	
	# calculate coordinates of cortex boundaries
	x0, x1 = pOpt[0], pOpt[1]
	#~ t = (x1-x0)*scipy.cos(a)
	t = (x1-x0)
	
	return pOpt, extra, pFunc, t


def makeModelProfileFuncY1Fixed( x, y1, s, a, mode, **kwargs ):
	
	if mode[0]=='a':
		return makeModelProfileFuncY1FixedAnalytic( x, y1, s, a, mode=mode )
	else:
		return makeModelProfileFuncY1FixedFFT( x, y1, s, a, mode=mode, **kwargs )

def makeModelProfileFuncY1FixedFFT( x, y1, s, a, fftN=None, mode='1NoShift', window='none' ):
	""" produces a function that samples a model profile at positions x
	
	y1 is the fixed cortex CT value, s is slice thickness, a is angle to
	the slice plane, pad is the number of extra x values to pad onto the
	beginning and end of x for calculation. Padding assume x elements 
	are equidistant. The returned vector is of the same length as x.
	
	discretised fourier space evaluation
	"""
	
	if fftN==None:
		fftN=len(x)*2 - 1
		
	n = x.shape[0]
	pad = (fftN - n)/2
	
	convolvers = { '1': doConvolve1,
				   '1NoGo': doConvolve1NoGo,
				   '1NoShift': doConvolve1NoShift,
				   '1NoShiftNoGo': doConvolve1NoShiftNoGo,
				   '2': doConvolve2,
				   'timeDomain': doConvolveTimeDomain,
				   'timeDomainNoGo': doConvolveTimeDomainNoGo
				   }
	
	windows = {'none':1.0,
			   'hamming': scipy.hamming(n+pad*2),
			   'hanning': scipy.hanning(n+pad*2),
			   }
	
	r = s/2.0 * scipy.tan(a)
	
	xRes = x[1]-x[0]
	X = scipy.linspace( x[0]-xRes*pad, x[-1]+xRes*pad, n+pad*2)
	go = scipy.zeros( len(X) )
	go[ scipy.where((X>-r)&(X<r)) ] = 1.0/(2.0*r)
	
	convolver = convolvers[mode]
	wind = windows[window]
		
	def profileFunc( P ):
		""" P = [x0, x1, y0, y2, sigma]
		"""
		x0, x1, y0, y2, sigma = P
		
		yPad = scipy.ones(n+pad*2)*y1
		yPad[scipy.where(X<x0)] = y0
		yPad[scipy.where(X>=x1)] = y2
		
		yPad *= wind
		
		gi = scipy.exp(-(X*X)/(sigma*sigma)) / (sigma*scipy.sqrt(scipy.pi))
		
		yBlur = convolver( yPad, gi/gi.sum(), go/go.sum(), None )
		
		return yBlur[pad:-pad], yPad[pad:-pad], gi[pad:-pad]

	return profileFunc, go[pad:-pad]

def makeModelProfileFuncY1FixedAnalytic( x, y1, sliceSpacing, normalSliceAngle, mode='a1', **kwargs ):
	""" produces a function that samples a model profile at positions x
	
	y1 is the fixed cortex CT value, s is slice thickness, a is angle to
	the slice plane. The returned vector is of the same length as x.
	
	analytic evaluation
	"""
	r = sliceSpacing/2.0 * scipy.tan(normalSliceAngle)
	sqrt2 = scipy.sqrt(2.0)
	
	def profileFunc1( P ):
		""" P = [x0, x1, y0, y2, sigma]
		from 2011 tech report, no Go
		"""
		x0, x1, y0, y2, sigma = P[:5]
		t = x1 - x0
		yBlur = y0 + 0.5*(y1-y0)*( 1 + erf( (x+0.5*t)/(sigma*sqrt2) ) ) + \
					 0.5*(y2-y1)*( 1 + erf( (x-0.5*t)/(sigma*sqrt2) ) )
		return yBlur, None, None
		
	def profileFunc2( P ):
		""" P = [x0, x1, y0, y2, sigma]
		from 2010 paper, no Go
		"""
		x0, x1, y0, y2, sigma = P[:5]
		yBlur = y0 - 0.5*(y1-y0)*erf( (x0-x)/sigma )\
				   - 0.5*(y2-y1)*erf( (x1-x)/sigma )
		return yBlur, None, None
		
	def profileFunc22( P ):
		""" P = [x0, x1, y0, y2, sigma]
		from 2010 paper, no Go, simplified
		"""
		x0, x1, y0, y2, sigma = P[:5]
		A = erf((x0-x)/sigma)
		B = erf((x1-x)/sigma)
		yBlur = y0 - 0.5*( - y0*A + y1*(A-B) + y2*B )
		return yBlur, None, None
		
	def profileFunc3( P ):
		""" P = [x0, x1, y0, y2, sigma]
		from 2010 paper, simplified
		"""
		x0, x1, y0, y2, sigma = P[:5]
		a = (x0-x+r)
		b = (x0-x-r)
		c = (x1-x+r)
		d = (x1-x-r)
		A = a*erf(a/sigma) + s*scipy.exp( -(a*a)/(sigma*sigma) )/scipy.sqrt(scipy.pi)
		B = b*erf(b/sigma) + s*scipy.exp( -(b*b)/(sigma*sigma) )/scipy.sqrt(scipy.pi)
		C = c*erf(c/sigma) + s*scipy.exp( -(c*c)/(sigma*sigma) )/scipy.sqrt(scipy.pi)
		D = d*erf(d/sigma) + s*scipy.exp( -(d*d)/(sigma*sigma) )/scipy.sqrt(scipy.pi)
		
		yBlur = y0 + (1/(4*r))*( y0*(A-B) + y1*( -A+B+C-D ) + y2*( D-C ) )
		return yBlur, None, None
	
	objs = { 'a1': profileFunc1,
			 'a2': profileFunc2,
			 'a22': profileFunc22,
			 'a3': profileFunc3
			 }
			 
	return objs[ mode ], None
	
def makeModelProfileFuncY1SigmaFixed( x, y1, s, a, sigma, mode='a1', **kwargs ):
	""" produces a function that samples a model profile at positions x
	
	y1 is the fixed cortex CT value, s is slice thickness, a is angle to
	the slice plane. The returned vector is of the same length as x.
	
	analytic evaluation
	"""
	r = s/2.0 * scipy.tan(a)
	sqrtPi = scipy.sqrt(scipy.pi)
	sigma2 = sigma*sigma
	sqrt2 = scipy.sqrt(2.0)
	
	def profileFunc1( P ):
		""" P = [x0, x1, y0, y2]
		from 2011 tech report, no Go
		"""
		x0, x1, y0, y2 = P[:4]
		t = x1 - x0
		yBlur = y0 + 0.5*(y1-y0)*( 1 + erf( (x+0.5*t)/(sigma*sqrt2) ) )\
				   + 0.5*(y2-y1)*( 1 + erf( (x-0.5*t)/(sigma*sqrt2) ) )
		return yBlur, None, None
		
	def profileFunc2( P ):
		""" P = [x0, x1, y0, y2]
		from 2010 paper, no Go
		"""
		x0, x1, y0, y2 = P[:4]
		yBlur = y0 - 0.5*(y1-y0)*erf( (x0-x)/sigma )\
				   - 0.5*(y2-y1)*erf( (x1-x)/sigma )
		return yBlur, None, None
		
	def profileFunc22( P ):
		""" P = [x0, x1, y0, y2]
		from 2010 paper, no Go, simplified
		"""
		x0, x1, y0, y2 = P[:4]
		A = erf((x0-x)/sigma)
		B = erf((x1-x)/sigma)
		yBlur = y0 - 0.5*( - y0*A + y1*(A-B) + y2*B )
		return yBlur, None, None
		
	def profileFunc3( P ):
		""" P = [x0, x1, y0, y2]
		from 2010 paper, simplified
		"""
		x0, x1, y0, y2 = P[:4]
		a = (x0-x+r)
		b = (x0-x-r)
		c = (x1-x+r)
		d = (x1-x-r)
		A = a*erf(a/sigma) + s*scipy.exp( -(a*a)/(sigma2) )/sqrtPi
		B = b*erf(b/sigma) + s*scipy.exp( -(b*b)/(sigma2) )/sqrtPi
		C = c*erf(c/sigma) + s*scipy.exp( -(c*c)/(sigma2) )/sqrtPi
		D = d*erf(d/sigma) + s*scipy.exp( -(d*d)/(sigma2) )/sqrtPi
		
		yBlur = y0 + (1/(4*r))*( y0*(A-B) + y1*( -A+B+C-D ) + y2*( D-C ) )
		return yBlur, None, None
	
	objs = { 'a1': profileFunc1,
			 'a2': profileFunc2,
			 'a22': profileFunc22,
			 'a3': profileFunc3
			 }
			 
	return objs[ mode ], None
	

			
def doConvolve1( y, gi, go, N ):
	Y = fft.fft(y, n=N)
	Gi = fft.fft(gi, n=N)
	Go = fft.fft(go, n=N)
	YBlur = Y * Gi * Go
	yBlur = fft.ifft(YBlur, n=N)	# dont need to shift due to doing 2 convolves at once
	return yBlur
			
def doConvolve1NoGo( y, gi, go, N ):
	#~ Y = fft.fftshift(fft.fft(y))
	#~ Gi = fft.fftshift(fft.fft(gi))
	Y = fft.fft(y, n=N)
	Gi = fft.fft(gi, n=N)
	YBlur = Y * Gi
	yBlur = fft.fftshift(fft.ifft(YBlur, n=N))
	#~ yBlur = fft.ifft(YBlur)
	return yBlur

def doConvolve1NoShift( y, gi, go, N ):
	Y = fft.fft(y, n=N)
	Gi = fft.fft(gi, n=N)
	Go = fft.fft(go, n=N)
	
	#~ yBlur1 = fft.ifft( Y*Gi, n=N )
	#~ YBlur1 = fft.fft(yBlur1)
	#~ YBlur2 = YBlur1 * Go
	#~ 
	#~ yBlur2 = fft.ifft(YBlur2, n=N)
	#~ return yBlur2
	
	YBlur = Y * Gi * Go
	yBlur = fft.ifft(YBlur, n=N)
	return yBlur
	
def doConvolve1NoShiftNoGo( y, gi, go, N ):
	Y = fft.fft(y,n=N)
	Gi = fft.fft(gi,n=N)
	YBlur = Y * Gi
	yBlur = fft.ifft(YBlur, n=N)
	return yBlur
	
def doConvolve2( y, gi, go ):
	yBlur = signal.fftconvolve( y, gi, mode='same' )
	yBlur = signal.fftconvolve( yBlur, go, mode='same' )
	return yBlur
	
def doConvolveTimeDomain( y, gi, go ):
	yBlur = scipy.convolve( y, gi, mode='same' )
	yBlur = scipy.convolve( yBlur, go, mode='same' )
	return yBlur
	
def doConvolveTimeDomainNoGo( y, gi, go ):
	yBlur = scipy.convolve( y, gi, mode='same' )
	return yBlur

def makeWeights( x, X0, f ):
	return (x+X0)/(f*(x-X0)**2+(x+X0))

def makeWeightsGradMag( x, sigma ):
	W = gaussian_gradient_magnitude(x,sigma)
	return W/W.max()

def makeWeightPeak( p, x, x0, x1, **kwargs ):
	
	# find peak locations
	peakInd = ST.findPeak( p )
	xx = x1- x[peakInd]	# distance of peaks from x1 in mm
	#~ pdb.set_trace()
	# get closest peak with location < x1
	try:
		cortexPeakInd = peakInd[ positiveMin( xx ) ]
	except ValueError:
		# if no peak found, set it half way between x0 and x1
		cortexPeakInd = len(x)/2
	
	# make shifted gaussian / box
	cortexPeakIndShift = x.shape[0]/2 - cortexPeakInd
	pad = abs( cortexPeakIndShift )+20
	#~ g = signal.gaussian( x.shape[0]+2*pad, kwargs['sigma'] )
	
	#~ xRes = x[1]-x[0]
	#~ X = scipy.linspace( x.min()-xRes*pad, x.max()+xRes*pad, len(x)+2*pad )
	#~ g = makeWeights( X, 1.0, kwargs['f'])
	#~ 
	#~ W1 = g[ pad+cortexPeakIndShift+15: pad+cortexPeakIndShift+15+x.shape[0] ]
	#~ W2 = g[ pad+cortexPeakIndShift-15: pad+cortexPeakIndShift-15+x.shape[0] ]
	#~ W = W1+W2
	#~ W /= W.max()
	#~ W[:cortexPeakInd+20] += 0.05
	
	# 2 peak weighting
	t1 = ( cortexPeakInd-len(x)*kwargs['offset'] )/len(x)		# offset is in fraction of total profile length
	t2 = ( cortexPeakInd+len(x)*kwargs['offset'] )/len(x)
	W1 = makeWeights( scipy.linspace(0.0,1.0,len(x)), t1, kwargs['f'])
	W2 = makeWeights( scipy.linspace(0.0,1.0,len(x)), t2, kwargs['f'])
	W = W1+W2
	
	# 1 peak weighting (outer cortical surface)
	#~ t2 = ( cortexPeakInd+len(x)*kwargs['offset'] )/len(x)
	#~ W = makeWeights( scipy.linspace(0.0,1.0,len(x)), t2, kwargs['f'])
	#~ W += 0.01
	
	#~ W = twoPeaks( x, x[cortexPeakInd]-kwargs['width'] , x[cortexPeakInd]+kwargs['width'], kwargs['f'] )
	#~ pdb.set_trace()
	return W, x[cortexPeakInd]

def twoPeaks( x, x0, x1, f ):
	w1 = makeWeights( x, x0, f )
	w2 = makeWeights( x, x1, f )
	return w1+w2

def twoPeaksGaussian( x, x0, x1, sigma1, sigma2 ):
	centreShift = x.shape[0]/2 - cortexPeakInd
	pad = abs( cortexPeakIndShift )
	g = signal.gaussian( x.shape[0]+2*pad, kwargs['sigma'] )
	W = g[ pad+cortexPeakIndShift: pad+cortexPeakIndShift+x.shape[0] ]
	
def rectangle( L, w ):
	x = scipy.zeros(L)
	mid = L/2
	x[ -w+L/2 : w+L/2 ] = 1.0
	return x

def positiveMin( x ):
	if scipy.all(x<0.0):
		raise ValueError, 'no positives'
	return scipy.ma.masked_array(x, x<0.0).argmin()

def fillByElementMean( GF, GD, maskedX, fill=0.1, limits=None ):
	""" for each value in X with True in mask, replace with the mean X 
	from its element
	"""
	if limits==None:
		limits = [0.0,3.0]
	
	X = maskedX.filled()
	epGroups = GF.getElementPointIPerTrueElement( GD, GF.ensemble_field_function.mesh.elements.keys() )
	
	ep2ElemMap = {}
	for i, e in enumerate(epGroups):
		for ep in e:
			ep2ElemMap[ep] = i
		
	for maskedEpI in scipy.where(maskedX.mask)[0]:
		eI = ep2ElemMap[maskedEpI]
		try:
			# get ep indices of current element
			elemEpInd = epGroups[ep2ElemMap[maskedEpI]]
			# get mean of unmasked data in current element
			xNew = maskedX[elemEpInd].mean()
			
			if scipy.isfinite(xNew) and (limits[0]<xNew<limits[1]):
				X[maskedEpI] = xNew
			else:
				X[maskedEpI] = fill
		except IndexError:
			pdb.set_trace()
			
	return X

def fillByTriSurf( maskedX, getVertexNeighbour, fill=0.1 ):
	""" for each value in X with True in mask, replace with the mean X 
	from its neighbours. Neighbour indices are retrieved from input
	function getVertexNeighbour
	"""
	
	X = maskedX.filled()
	
	for maskedVertexI in scipy.where(maskedX.mask)[0]:
		neighbourVertexI = list( getVertexNeighbour( maskedVertexI )[0] )
		#~ pdb.set_trace()
		xNew = scipy.median( maskedX[ neighbourVertexI ] )
		
		if scipy.isfinite( xNew ):
			X[maskedVertexI] = xNew
			print xNew
		else:
			X[maskedVertexI] = fill
			print 'fill:', fill
		
	return X
	
def calcCovDiag(X):
	
	if X['cov_x']==None:
		C=None
	else:
		C = X['cov_x'].diagonal() * X['info_dict']['fvec'].std()
		#~ pdb.set_trace()
	return C

class cortexAnalyser( object ):
	
	def __init__( self ):
		self.GF = None
		self.I = None
		self.W = None
		self.cov = None
		self.rms = None
		self.T = None
		self.GF = None
		self.I = None
		
	def setGF( self, G ):
		self.GF = G
		
	def setI( self, I, spacing ):
		self.I = I
		self.voxelSpacing = spacing
		
	def setSurfacePoints( self, surfacePoints ):
		self.surfacePoints = surfacePoints
		
	def setSurfaceNormals( self, surfaceNormals ):
		self.surfaceNormals = surfaceNormals
	
	def calcSurfaceFromGF( self, GD, filterBoundaryNormals=1, nNN=5 ):
		
		GFX = self.GF.evaluate_geometric_field( GD ).T
		GFNormal = self.GF.evaluate_normal_in_mesh( GD ).T
		
		if filterBoundaryNormals:
			GFNormal = ST.filterElementBoundaryValues( self.GF, GD, GFNormal, nNN=nNN )
			
		# normalise
		GFNormal = GFNormal / scipy.sqrt((GFNormal**2.0).sum(1))[:,scipy.newaxis]
		
		self.setSurfacePoints( GFX )
		self.setSurfaceNormals( GFNormal )
		self.GD = GD
	
	def getNodeNormals( self ):
		nodeX = self.GF.get_all_point_positions()
		epXTree = ST.cKDTree( self.surfacePoints )
		i = epXTree.query( list(nodeX) )[1]
		#~ pdb.set_trace()
		return self.surfaceNormals[i]
		
	def sampleImage( self, ND, NLim ):
		
		self.XSamples = ST.genSamplingPoints( self.surfacePoints, self.surfaceNormals, ND, xLim=NLim, spacing=self.voxelSpacing )
		self.sampledProfiles = ST.sampleImage( self.I, self.XSamples )
		self.nProfiles = self.sampledProfiles.shape[0]
	
	def makeWeightsGradMag( self, sigma ):
		self.W = scipy.array([ makeWeightsGradMag(p, sigma) for p in self.sampledProfiles ])
		
	def makeWeightPeak( self, x, x0, x1, **kwargs ):
		W = []
		X = []
		for p in self.sampledProfiles:
			w, xPeak = makeWeightPeak( p, x, x0, x1, **kwargs )
			W.append(w)
			X.append(xPeak)
		
		self.W = scipy.array(W)
		self.xPeak = scipy.array(X)
	
	def findCortexSteepestGradient( self, xMin, xMax, xN, originOffset, sigma=None ):
		"""
		find the outer and inner cortical surfaces simply as the points
		of steepest ascent and descent in the intensity profile
		"""
		
		# initialise
		x = scipy.linspace(xMin,xMax,xN)
		xtol = 1e-5 
		self.outerData = []
		self.innerData = []
		self.T = []
		self.rms = []
		self.cov = []
		self.pOpt = []
		
		self.xMin = xMin
		self.xMax = xMax
		self.xN = xN
		
		# calculate the gradient for all profiles
		self.sampledProfileGradient = calcGradient( self.sampledProfiles, gaussianSigma=sigma )

		# for each sample site
		for i in xrange( self.surfacePoints.shape[0] ):
			profile = self.sampledProfiles[i]
			profileGrad = self.sampledProfileGradient[i]
			N = self.surfaceNormals[i]
			origin = self.surfacePoints[i]
			
			#~ print 'sigma:', sigma
			x0, x1, y0, y1, y2, t = calcCortexSteepestGradient( origin, N, profile, profileGrad, x, xtol=1e-5 )
		
			self.pOpt.append( [x0, x1, y0, y2] )
			self.T.append(t)
			self.rms.append( 0.0 )
			self.cov.append( 0.0 )
			print 'point: %(pi)i\tthickness: %(t)6.4f'%{'pi':i, 't':t } 
		
		self.pOpt = scipy.array( self.pOpt )
		x0 = self.pOpt[:,0]
		x1 = self.pOpt[:,1]
		# mesh normals point outwards, cortex algorithm assumes inwards, *-1
		self._calcT( x0, x1 )
		self._calcInnerOuter( x0, x1, originOffset )
		#~ self.T = scipy.array(self.T)
		#~ self.T = self._calcT(x0,x1)
		self.rms = scipy.array(self.rms)
		self.cov = scipy.array(self.cov)
		#~ self.innerData = (self.pOpt[:,0] - originOffset)[:,scipy.newaxis]*self.surfaceNormals + self.surfacePoints	
		#~ self.outerData = (self.pOpt[:,1] - originOffset)[:,scipy.newaxis]*self.surfaceNormals + self.surfacePoints	
		
		return self.pOpt, self.outerData, self.innerData
		
	def findCortexY1Fixed( self, xMin, xMax, xN, y1, s, P0, originOffset, sigma=None, weights=None, xInitOffset=None, autox0x1=False ):
		"""
		if autox0x1: automatically place initial x0 and x1 using steepest gradient estimation
		"""
		
		
		# initialise
		x = scipy.linspace(xMin,xMax,xN)
		xtol = 1e-5 
		self.y1 = y1
		self.pOpt = []
		self.outerData = []
		self.innerData = []
		self.pFuncs = []
		self.T = []
		self.CDiag = []
		self.rms = []
		
		self.xMin = xMin
		self.xMax = xMax
		self.xN = xN
		
		if autox0x1:
			self.sampledProfileGradient = calcGradient( self.sampledProfiles, gaussianSigma=sigma )
		
		if weights==None:
			weightIterator = self.W.__iter__()
			def getWeights():
				return weightIterator.next()
		else:
			self.W = weights
			def getWeights():
				return self.W

		# for each sample site
		for i in xrange( self.surfacePoints.shape[0] ):
			data = self.sampledProfiles[i]
			N = self.surfaceNormals[i]
			origin = self.surfacePoints[i]
			p0 = scipy.array(P0)
			
			if xInitOffset!=None:
				p0[0] = self.xPeak[i]-xInitOffset
				p0[1] = self.xPeak[i]+xInitOffset
			
			if autox0x1:
					profileGrad = self.sampledProfileGradient[i]
					x0SG, x1SG, y0SG, y1SG, y2SG, tSG = calcCortexSteepestGradient( origin, N, data, profileGrad, x, xtol=1e-5 )
					if scipy.isfinite(x0SG):
						p0[0] = x0SG
					if scipy.isfinite(x1SG):
						p0[1] = x1SG
									
			#~ print 'sigma:', sigma
			if sigma!=None:
				pOpt, extras, pFunc, t = calcCortexY1SigmaFixed( origin, N, data, x, y1, s, sigma, p0, getWeights(), xMin, xMax, xtol=1e-5 )
			else:
				pOpt, extras, pFunc, t = calcCortexY1Fixed( origin, N, data, x, y1, s, p0, getWeights(), xMin, xMax, xtol=1e-5 )

					
			self.pOpt.append( pOpt )
			self.pFuncs.append( pFunc )
			self.T.append(t)
			self.CDiag.append( calcCovDiag(extras) )
			self.rms.append( extras['rms'] )
			print 'point: %(pi)i\tthickness: %(t)6.4f\trms: %(rms)6.3f'%{'pi':i, 't':t, 'rms':extras['rms'] } 
		
		self.pOpt = scipy.array( self.pOpt )
		x0 = self.pOpt[:,0]
		x1 = self.pOpt[:,1]
		
		# mesh normals point outwards, cortex algorithm assumes inwards, *-1
		self._calcInnerOuter( x0, x1, originOffset )
		self._calcT( x0 ,x1 )
		self.rms = scipy.array(self.rms)
		return self.pOpt, self.outerData, self.innerData
	
	def _calcT( self, x0, x1 ):
		#~ a = scipy.arctan( self.surfaceNormals[:,2] / scipy.sqrt(self.surfaceNormals[:,0]**2.0 + self.surfaceNormals[:,1]**2.0) )
		#~ self.T = (x1-x0)*scipy.cos(a)
		
		# new method, does not need a. x0 and x1 are in mm, in real coordinates
		self.T = x1 - x0
		
		return self.T
	
	def _calcInnerOuter( self, x0, x1, originOffset ):
		
		# take into account slice spacing
		#~ a = scipy.arctan( self.surfaceNormals[:,2] / scipy.sqrt(self.surfaceNormals[:,0]**2.0 + self.surfaceNormals[:,1]**2.0) )
		#~ X0 = (x0 - originOffset)*scipy.cos(a)[:,scipy.newaxis]
		#~ X1 = (x1 - originOffset)*scipy.cos(a)[:,scipy.newaxis]
		#~ self.innerData = X0*self.surfaceNormals + self.surfacePoints	
		#~ self.outerData = X1*self.surfaceNormals + self.surfacePoints
		
		self.innerData = (x0 - originOffset)[:,scipy.newaxis]*self.surfaceNormals + self.surfacePoints	
		self.outerData = (x1 - originOffset)[:,scipy.newaxis]*self.surfaceNormals + self.surfacePoints
		
		return self.innerData, self.outerData
	
	def maskThickness( self, maskModes, fillMode, customMask=None, fill=None, limits=None, GD=None, getVertexNeighbour=None ):
		
		if isinstance(maskModes, str):
			maskModes = [maskModes,]
			
		mask = scipy.zeros( self.nProfiles, dtype=bool)
		for m in maskModes:
			if m=='rms':
				mask += scipy.bitwise_not(self.rmsFilterMask)
			elif m=='T':
				mask += scipy.bitwise_not(self.thicknessFilterMask)
			elif m=='rmsT':
				mask += scipy.bitwise_not(self.rmsFilterMask & self.thicknessFilterMask)
			elif m=='cov':
				mask += scipy.bitwise_not(self.covFilterMask)
			elif m=='custom':
				mask += customMask
			else:
				raise ValueError, 'unrecognised mask mode '+m
		
		maskedData = scipy.ma.masked_array(self.T, mask)
		
		if fillMode=='none':
			data = maskedData
		elif fillMode=='elementmean':
			if GD==None:
				GD = self.GD
			data = fillByElementMean( self.GF, GD, maskedData, fill=fill, limits=limits )
		elif fillMode=='regionmean':
			maskedData.fill_value = maskedData.mean()
			data = maskedData.filled()
		elif fillMode=='xRes':
			maskedData.fill_value = (self.xMax - self.xMin)/self.xN
			data = maskedData.filled()
		elif fillMode=='tri':
			data = fillByTriSurf( maskedData, getVertexNeighbour, fill=fill )
		else:
			raise ValueError, 'unrecognised fill mode'
		
		if limits!=None:
			data = scipy.where( (data<=limits[0])|(data>=limits[1]), fill, data )
			#~ pdb.set_trace()
			
		self.maskedT = maskedData
		self.fitT = data
		self.mask = mask
		
	def fitThicknessField( self, GD, sobW=None, sobD=None, nW=None, nD=None, xtol=1e-6 ):
		
		self.thicknessField, self.thicknessFieldPOpt, rms = scalarField.fitGeomFieldToMaskedScalar( self.GF, GD, self.fitT, fieldName='ThicknessField', sobW=sobW, sobD=sobD, nW=nW, nD=nD, xtol=xtol )

		self.fittedThickness = self.thicknessField.evaluateField(GD)
		fitErr = abs(self.fittedThickness - self.fitT)
		fitErrRel = abs((self.fittedThickness - self.fitT)/self.fitT)
		self.thicknessFieldFitErrors = { 'abs': fitErr, 'rel':fitErrRel, 'absRMS': rms,  'relRMS': scipy.sqrt((fitErrRel**2.0).mean())}
		
		print 'absRMS:', self.thicknessFieldFitErrors['absRMS']
		print 'relRMS:', self.thicknessFieldFitErrors['relRMS']
		return self.thicknessField, self.thicknessFieldPOpt, self.thicknessFieldFitErrors, self.fittedThickness
		
	def plotProfile( self, i, show=1 ):
		
		imageP = self.sampledProfiles[i]
		modelBlur, modelP, modelGi = self.pFuncs[i](self.pOpt[i])
		x = scipy.linspace(self.xMin, self.xMax, self.xN)
		modelP = scipy.ones(x.shape[0])*self.y1
		modelP[scipy.where(x<self.pOpt[i][0])] = self.pOpt[i][2]
		modelP[scipy.where(x>self.pOpt[i][1])] = self.pOpt[i][3]
		
		f = plot.figure()
		plot.plot(x,imageP)
		plot.plot(x,modelBlur)
		plot.plot(x,modelP)
		if show:
			plot.show()
		
		print 'x0', self.pOpt[i][0]
		print 'x1', self.pOpt[i][1]
		print 'y0', self.pOpt[i][2]
		print 'y2', self.pOpt[i][3]
		try:
			print 's', self.pOpt[i][4]
		except IndexError:
			pass
			
		return f


	def calcProfileError( self, i, weights ):
			
		obj = makeObj( self.pFuncs[i], self.sampledProfiles[i], weights, self.xMin, self.xMax )
		err = obj( self.pOpt[i] )
		rms = scipy.sqrt(err*err.mean())
		
		return err, rms, obj
	
	def	filterByThickness( self, tMin, tMax ):
		""" classify each fitted profile  if the thickness is within
		the provided bounds. Returns a list of booleans
		"""
		self.thicknessFilterMask = (tMin<=self.T)&(self.T<=tMax)
		return self.thicknessFilterMask
		
	def filterByRMS( self, rmsMax ):
		self.rmsFilterMask = self.rms<=rmsMax
		return self.rmsFilterMask
	
	def filterByCov( self, covMax ):
		
		if self.cov==None:
			self.cov = scipy.zeros(self.nProfiles, dtype=float)
			for i,c in enumerate(self.CDiag):
				if c==None:
					self.cov[i]=covMax + 1
				else:
					self.cov[i]=c[:2].max()
	
		self.covFilterMask = self.cov<=covMax		
		return self.covFilterMask
				
	def calcY1( self ):
		""" estimates Y1 (cortical CT value) by examining the maximum
		CT value in each sampled profile, and taking the max
		"""
		return self.sampledProfiles.max(1).max()

class profilePlotter( object ):
	
	lineLabels = ['sample', 'y_blur', 'y', 'weights']
	#~ lineLabels = ['sample', 'y_blur', 'y']
	titlePrefix = 'profile'
	
	def __init__( self, CA ):
		self.CA = CA
		self.nProfiles = self.CA.sampledProfiles.shape[0]
		self.fig = plot.figure()
		self.ax = self.fig.add_subplot(111)
		self.fig.subplots_adjust(bottom=0.2)
		
		axcolor = 'lightgoldenrodyellow'
		slideAxis = plot.axes([0.25, 0.05, 0.65, 0.03], axisbg=axcolor)
		self.profileSlider = Slider( slideAxis, 'profile location', 0, self.nProfiles-1, valinit=0)
		self.profileSlider.on_changed(self._update)
		
		self._drawInitProfile()
		
	def _drawInitProfile( self ):
		iP,mB, mP, w = self._getProfile( 0 )
		x = scipy.linspace( self.CA.xMin, self.CA.xMax, self.CA.xN )
		lines = self.ax.plot( x, iP, 'b', x, mB, 'g', x, mP, 'r', x, w, 'k', linewidth=2.0 )
		#~ lines = self.ax.plot( x, iP, 'b', x, mB, 'g', x, mP, 'r' )
		self.lines = dict( zip( self.lineLabels, lines ) )
		self.title = self.ax.set_title( '%(pre)s %(i)5d | rms: %(rms)5.3f | tpass: %(t)1d | rpass: %(r)1d | cpass: %(c)1d'%{'pre':self.titlePrefix, 'i':0, 'rms':self.CA.rms[0], 't':int(self.CA.thicknessFilterMask[0]), 'r':int(self.CA.rmsFilterMask[0]), 'c':int(self.CA.covFilterMask[0])} )
		self.xlabel = self.ax.set_xlabel('x (mm)')
		self.ylabel = self.ax.set_ylabel('CT Value')
		self.legend = self.ax.legend(  lines, self.lineLabels )
		self.ax.set_ylim(-500.0,2000.0)
		self.ax.set_xlim(self.CA.xMin, self.CA.xMax)
		plot.show()
		
	def drawProfile( self, i ):
		iP,mB, mP, w = self._getProfile( i )
		self.lines['sample'].set_ydata( iP )
		self.lines['y_blur'].set_ydata( mB )
		self.lines['y'].set_ydata( mP )
		self.lines['weights'].set_ydata( w )
		self.title.set_text( '%(pre)s %(i)5d | rms: %(rms)5.3f | tpass: %(t)1d | rpass: %(r)1d | cpass: %(c)1d'%{'pre':self.titlePrefix, 'i':i, 'rms':self.CA.rms[i], 't':int(self.CA.thicknessFilterMask[i]), 'r':int(self.CA.rmsFilterMask[i]), 'c':int(self.CA.covFilterMask[i])} )
		self.fig.canvas.draw_idle()
	
	def _update( self, i ):
		self.drawProfile( int(round(i)) )
		
	def _getProfile( self, i ):
		imageP = self.CA.sampledProfiles[i]
		modelBlur, modelP, modelGi = self.CA.pFuncs[i](self.CA.pOpt[i])
		x = scipy.linspace(self.CA.xMin, self.CA.xMax, self.CA.xN)
		modelP = scipy.ones(x.shape[0])*self.CA.y1
		modelP[scipy.where(x<self.CA.pOpt[i][0])] = self.CA.pOpt[i][2]
		modelP[scipy.where(x>self.CA.pOpt[i][1])] = self.CA.pOpt[i][3]
		
		if self.CA.W.shape.__len__()==1:
			weight = self.CA.W*1000
		else:
			weight = self.CA.W[i]*1000
		
		return imageP, modelBlur, modelP, weight

class profilePlotterSteepestGradient( object ):
	
	lineLabels = ['sample', 'y']
	titlePrefix = 'profile'
	
	def __init__( self, CA ):
		self.CA = CA
		self.nProfiles = self.CA.sampledProfiles.shape[0]
		self.fig = plot.figure()
		self.ax = self.fig.add_subplot(111)
		self.fig.subplots_adjust(bottom=0.2)
		
		axcolor = 'lightgoldenrodyellow'
		slideAxis = plot.axes([0.25, 0.05, 0.65, 0.03], axisbg=axcolor)
		self.profileSlider = Slider( slideAxis, 'profile location', 0, self.nProfiles-1, valinit=0)
		self.profileSlider.on_changed(self._update)
		
		self._drawInitProfile()
		
	def _drawInitProfile( self ):
		iP, mP = self._getProfile( 0 )
		x = scipy.linspace( self.CA.xMin, self.CA.xMax, self.CA.xN )
		lines = self.ax.plot( x, iP, 'b', x, mP, 'r' )
		self.lines = dict( zip( self.lineLabels, lines ) )
		self.title = self.ax.set_title( '%(pre)s %(i)5d | tpass: %(t)1d'%{'pre':self.titlePrefix, 'i':0, 't':int(self.CA.thicknessFilterMask[0])} )
		self.xlabel = self.ax.set_xlabel('x (mm)')
		self.ylabel = self.ax.set_ylabel('CT Value')
		self.legend = self.ax.legend(  lines, self.lineLabels )
		self.ax.set_ylim(-500.0,2000.0)
		self.ax.set_xlim(self.CA.xMin, self.CA.xMax)
		plot.show()
		
	def drawProfile( self, i ):
		iP, mP = self._getProfile( i )
		self.lines['sample'].set_ydata( iP )
		self.lines['y'].set_ydata( mP )
		self.title.set_text( '%(pre)s %(i)5d | tpass: %(t)1d'%{'pre':self.titlePrefix, 'i':i, 't':int(self.CA.thicknessFilterMask[i])} )
		self.fig.canvas.draw_idle()
	
	def _update( self, i ):
		self.drawProfile( int(round(i)) )
		
	def _getProfile( self, i ):
		imageP = self.CA.sampledProfiles[i]
		x = scipy.linspace(self.CA.xMin, self.CA.xMax, self.CA.xN)
		#~ modelP = scipy.ones(x.shape[0])*self.CA.y1
		modelP = scipy.ones(x.shape[0])*1500
		modelP[scipy.where(x<self.CA.pOpt[i][0])] = self.CA.pOpt[i][2]
		modelP[scipy.where(x>self.CA.pOpt[i][1])] = self.CA.pOpt[i][3]
		
		return imageP, modelP


	
def simDataAccuracyTest( x0Targ, x1Targ ):
	x = scipy.linspace(-10,10,200)
	#~ x = scipy.linspace(2*x0Targ,2*x1Targ,200)
	y1Targ = 1750
	s = 1.6
	a = scipy.pi/6.0
	y0Targ = 100
	y2Targ = -100
	sigmaTarg = 1.25
	pTarg = (x0Targ, x1Targ, y0Targ, y2Targ, sigmaTarg)
	pFuncTarg, goTarg = makeModelProfileFuncY1Fixed( x, y1Targ, s, a, mode='a22' )
	yTargBlurred, yTarg, giTarg = pFuncTarg( pTarg )
	
	p0 = (-5, 5, 100, -100, 1.0)
	#~ weights = 1.0
	weights = makeWeights( x, p0[1], 50 ) + 1
	xtol = 1e-12
	y1=1750
	#~ diag = (1.0,1.0,100.0,100.0,1.0)
	pFunc, goOpt = makeModelProfileFuncY1Fixed( x, y1, s, a, mode='a22' )
	#~ pOpt, rmsOpt = fitProfile( pFunc, yTargBlurred.real, p0, weights, xtol=xtol, epsfcn=0.1e-1 )
	pOpt, extra = fitProfile( pFunc, yTargBlurred.real, p0, weights, -10.0, 10.0, xtol=xtol )
	#~ pOpt, rmsOpt = fitProfile( pFunc, yTargBlurred.real, p0, weights, xtol)

	# calculate thickness accuracy
	T = pOpt[1] - pOpt[0]
	dT = T - (pTarg[1] - pTarg[0])
	dParams = pOpt - pTarg
	return dT, T, dParams, pOpt

# fitting accuracy test
def simDataAccuracyTestMain():
	X = scipy.arange(0.1,3.0,0.1)
	dT = []
	T = []
	dParams = []
	for x1 in X:
		dt, t, dp, pOpt = simDataAccuracyTest( -x1, x1 )
		print dt, [-x1, x1], pOpt
		T.append(t)
		dT.append(dt)
		dParams.append(dp)
	
	f=plot.figure()
	plot.scatter( X*2, T )
	plot.plot( X*2, X*2 )
	plot.xlabel('actual width (mm)')
	plot.ylabel('predicted width (mm)')
	plot.title('simulated profile fitting')
	plot.show()
	
if __name__=='__main__':
	simDataAccuracyTestMain()
		
#======================================================================#
#~ x0 = -5
#~ x1 = -2
#~ y0 = -1000
#~ y1 = 1750
#~ y2 = 0
#~ a = scipy.pi/3.0
#~ sigma = 1.0
#~ x = scipy.linspace(-15,15,128)
#~ s = 1.6
#~ n = len(x)
#~ r = s/2.0 * scipy.tan(a)
#~ denom = 2.0*r*sigma*scipy.sqrt(scipy.pi)
#~ sigma2 = sigma*sigma
#~ 
#~ gi = scipy.exp(-(x*x)/(sigma*sigma)) / (sigma*scipy.sqrt(scipy.pi))
#~ 
#~ go = scipy.zeros( n )
#~ go[ scipy.where((x>-r)&(x<r)) ] = 1.0/(2.0*r)
#~ 
#~ y = scipy.ones(x.shape[0])*y1
#~ y[scipy.where(x<x0)] = y0
#~ y[scipy.where(x>=x1)] = y2
#~ 
#~ t0 = time.time()
#~ for i in xrange(1000):
	#~ yBlur = doConvolve1NoShift( y, gi, go )
	#~ 
#~ dt = time.time() - t0
#~ print dt

#======================================================================#
#~ x = scipy.linspace(-10,10,100)
#~ y1 = 1750
#~ s = 1.6
#~ a = scipy.pi/3.0
#~ pFunc, go = makeModelProfileFuncY1Fixed( x, y1, s, a, mode='1NoGo', window='none' )
#~ 
#~ x0 = -3
#~ x1 = 5
#~ y0 = -1000
#~ y2 = 0
#~ sigma = 1.0
#~ 
#~ t0 = time.time()
#~ for i in xrange(1):
	#~ yBlur, y, gi = pFunc( (x0, x1, y0, y2, sigma) )
#~ 
#~ dt = time.time() - t0
#~ print dt
#~ 
#~ plot.figure()
#~ plot.subplot(131)
#~ plot.plot(x,y)
#~ plot.plot(x,yBlur)
#~ plot.subplot(132)
#~ plot.plot(x,gi)
#~ plot.subplot(133)
#~ plot.plot(x,go)
#~ plot.show()

#======================================================================#
#~ # fit testing
#~ 
#~ # create target profiles
#~ x = scipy.linspace(-10,10,100)
#~ y1 = 1750
#~ s = 1.6
#~ a = scipy.pi/3.0
#~ x0Targ = -1
#~ x1Targ = 0.0
#~ y0Targ = -1200
#~ y2Targ = 0
#~ sigmaTarg = 1.0
#~ pTarg = (x0Targ, x1Targ, y0Targ, y2Targ, sigmaTarg)
#~ pFuncTarg, goTarg = makeModelProfileFuncY1Fixed( x, y1, s, a, mode='1', window='none' )
#~ yTargBlurred, yTarg, giTarg = pFuncTarg( pTarg )
#~ 
#~ # fit to blurred target profile
#~ 
#~ # fit function
#~ p0 = (-1.0, 1.0, -800, 200, 1.0)
#~ weights = 1.0
#~ xtol = 1e-9
#~ pFunc, goOpt = makeModelProfileFuncY1Fixed( x, y1, s, a, mode='1', window='none' )
#~ pOpt = fitProfile( pFunc, yTargBlurred.real, p0, weights, xtol, epsfcn=1e-1 )
#~ yOptBlurred, yOpt, giOpt = pFunc( pOpt )
#~ print 'pTarg:', pTarg
#~ print 'pOpt:', pOpt
#~ # calculate coordinates of cortex boundaries
#~ x0, x1 = pOpt[0], pOpt[1]
#~ 
#~ plot.figure()
#~ plot.subplot(131)
#~ plot.plot(x,yTarg)
#~ plot.plot(x,yTargBlurred)
#~ plot.plot( x, yOpt )
#~ plot.plot( x, yOptBlurred )
#~ plot.scatter( [x0,x1], [pOpt[2], pOpt[3]] )
#~ plot.subplot(132)
#~ plot.plot(x,giTarg)
#~ plot.plot(x,giOpt)
#~ plot.subplot(133)
#~ plot.plot(x,goTarg)
#~ plot.plot(x,goOpt)
#~ plot.show()

#======================================================================#

