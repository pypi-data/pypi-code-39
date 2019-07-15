from trippy import psf
from astropy.io import fits
import numpy as np
import time

with fits.open('/Volumes/WtFFastDataAlpha/ColOSSOS/REDUCED/2014B/Optical/O13BL3RG/mrgN20140829S0126.fits') as han:
    data = han[1].data

p = psf.modelPSF(restore='/Volumes/WtFFastDataAlpha/ColOSSOS/REDUCED/2014B/Optical/O13BL3RG/mrgN20140829S0126.psf.fits')
p.fitMoffat(data,3393.50, 2940.66, boxSize = 40, bgRadius=35, verbose=False, quickFit = True)
p.fitMoffat(data,3393.50, 2940.66, boxSize = 40, bgRadius=35, verbose=False)
t1 = time.time()
p.fitMoffat(data,3393.50, 2940.66, boxSize = 40, bgRadius=35, verbose=False, quickFit = True)
t2 = time.time()
print(p.alpha,p.beta)
p.fitMoffat(data,3393.50, 2940.66, boxSize = 40, bgRadius=35, verbose=False)
print(p.alpha,p.beta)
t3 = time.time()
print(t3-t2,t2-t1)
