""" Utility functions and classes for SRP

Context : SRP
Module  : Polarimetry
Version : 1.0.0
Author  : Stefano Covino
Date    : 10/05/2017
E-mail  : stefano.covino@brera.inaf.it
URL:    : http://www.merate.mi.astro.it/utenti/covino

Usage   : to be imported

Remarks : 
    
History : (10/05/2017) First version.

"""

import numpy as np
from SRP.SRPPolarimetry.MuellerRotationMatrix import MuellerRotationMatrix
from SRP.SRPPolarimetry.MuellerTransmissionMatrix import MuellerTransmissionMatrix


def TNGMuellerTransmissionMatrix (theta=np.radians(0), T1=1.0, T2=0., ebeam=True):
    M = MuellerRotationMatrix(-theta)*MuellerTransmissionMatrix(T1,T2,ebeam)*MuellerRotationMatrix(theta)
    return M


