import os

import numpy as np
from scipy.special import sph_harm 
from scipy.special import genlaguerre 
from scipy.special import factorial as fact
from scipy.optimize import minimize as scipimin

#from masstable import Table
#import periodictable as pt

quantum_numbers_map = {
    '1s':(1,0,0,None),
    '2s':(2,0,0,None),
    '3s':(3,0,0,None),
    '4s':(4,0,0,None),
    '5s':(5,0,0,None),
    '6s':(6,0,0,None),
    '7s':(7,0,0,None),
    '2pz':(2,1,0,None),
    '2px':(2,1,1,'+'),
    '2py':(2,1,1,'-'),
    '3pz':(3,1,0,None),
    '3px':(3,1,1,'+'),
    '3py':(3,1,1,'-'),
    '4pz':(4,1,0,None),
    '4px':(4,1,1,'+'),
    '4py':(4,1,1,'-'),
    '5pz':(5,1,0,None),
    '5px':(5,1,1,'+'),
    '5py':(5,1,1,'-'),
    '3dz2':(3,2,0,None),
    '3dxz':(3,2,1,'+'),
    '3dyz':(3,2,1,'-'),
    '3dxy':(3,2,2,'+'),
    '3dx2-y2':(3,2,2,'-'),
    '4dz2':(4,2,0,None),
    '4dxz':(4,2,1,'+'),
    '4dyz':(4,2,1,'-'),
    '4dxy':(4,2,2,'+'),
    '4dx2-y2':(4,2,2,'-'),
    '4fz3':(4,3,0,None),
    '4fxz2':(4,3,1,'+'),
    '4fyz2':(4,3,1,'-'),
    '4fxyz':(4,3,2,'+'),
    '4fz(x2-y2)':(4,3,2,'-'),
    '4fx(x2-3y2)':(4,3,3,'+'),
    '4fy(3x2-y2)':(4,3,3,'-'),
    }

bohr_rad_A = 0.529177       #Angstrom
elec_mass_amu = 5.485799090 #amu

def spherical_harmonic(l,m,theta,phi):
    """Compute values of a spherical harmonic function.

    This is a direct wrapper around scipy.special.sph_harm,
    and you may as well just use that.

    Parameters
    ----------
    l : int
        Angular momentum quantum number
    m : int
        Magnetic quantum number
    theta : array
        Theta values (azimuthal spherical coordinates)
        at which the spherical harmonic will be computed
    phi : array
        Phi values (polar spherical coordinates)
        at which the spherical harmonic will be computed

    Returns
    -------
    Ylm : array
        Array of complex-valued spherical harmonics 
    """
    return sph_harm(m,l,theta,phi)

def radial_wf(n,l,r_A,Z=1,N_neut=0):
    """Get wavefunction values wrt radial distance from the nucleus.

    Parameters
    ----------
    n : int
        principal quantum number
    l : int
        angular momentum quantum number
    r_A : array of float
        array of radial points (in Angstroms)
        at which the wavefunction will be computed
    Z : int
        number of protons in the nucleus
    N_neut : int
        number of neutrons in the nucleus

    Returns
    ------- 
    Rnl : array
        array of complex wavefunction values
        at all of the input points `r_A`
    """
    
    # TODO: 
    # use nucmt to determine nuclear mass from Z+N
    # nucmt gives mass excess in energy units
    # M_nuc = Z + N + (mass_excess)/c^2
    #atmass = Get atomic mass of either most common or weighted-average isotope
    #nucmt = Table('AME2003')
    #mu = (reduced mass of nucleus-electron system, approx equal to m_e) 
    #a_mu = elec_mass_amu / mu * bohr_rad_A  
    a_mu = bohr_rad_A       # a_mu in units of Angstrom

    r_a_mu = r_A/a_mu       # radius in units of a_mu
    Zr_a_mu = Z*r_a_mu      # Z*r in units of a_mu

    # get generalized laguerre for n,l
    lagpoly = genlaguerre(n-l-1,2*l+1)
    lag_of_r = lagpoly(2*Zr_a_mu/n)

    # a_mu has units of Angstrom --> Rnl has units of Angstrom^(-3/2)
    Rnl = np.array(
        np.sqrt( (2*Z/float(n*a_mu))**3 * fact(n-l-1) / (2*n*fact(n+l)) )
        * np.exp(-1*Zr_a_mu/n)
        * (2*Zr_a_mu/n)**l 
        * lag_of_r
        / (2*np.sqrt(np.pi))
        )
    
    return Rnl

def enc_chg_diffsqr(n,l,enc_chg,Z,N_neut,r):
    integ = radial_wf_integral(n,l,np.linspace(0.,r,500).ravel(),Z,N_neut)
    diffsqr = (integ-enc_chg)**2
    return diffsqr

def enclosed_density_radius(n,l,enc_chg,Z=1,N_neut=0):
    enc_chg_diffsqr = lambda r : (radial_wf_integral(n,l,np.linspace(0,r,1000),Z,N_neut)-enc_chg)**2

    r0 = 0.
    ec_r0 = 0.
    while ec_r0<enc_chg:
        r0 += 0.1
        ec_r0 = radial_wf_integral(n,l,np.linspace(0,r0,1000),Z,N_neut)

    opt = scipimin(enc_chg_diffsqr,r0)

    ### DBG
    #Rnl,Rnlsqr,isolev = radial_probability(n,l,opt.x[0],Z,N_neut)
    #from hwaves import hwf_plot
    #from matplotlib import pyplot as plt
    #fig = hwf_plot.plot_radial_wf(n,l,np.linspace(0,10,1000),showplot=False)
    #plt.plot([opt.x[0]],[isolev],'g*')
    #plt.show()
    #######

    return opt.x[0]

def radial_density(n,l,r_A,Z=1,N_neut=0):
    Rnl = radial_wf(n,l,r_A,Z,N_neut)
    # Rnl has units of Angstrom^(-3/2)
    # Rnlsqr has units Angstrom^(-3): density per volume 
    return Rnl, Rnl * Rnl

def radial_probability(n,l,r_A,Z=1,N_neut=0):   
    Rnl, Rnlsqr = radial_density(n,l,r_A,Z,N_neut)
    # Rnlsqr has units Angstrom^(-3): density per volume 
    # Pnl has units Angstrom^(-1): spherical-shell integrated density per radius
    # TODO: figure out whether or not the 4*pi term belongs here
    # ... if so, then the Rnlsqr scaling factor has to change accordingly 
    Pnl = Rnlsqr * 4 * np.pi * r_A**2  
    #Pnl = Rnlsqr * r_A**2  
    return Rnl, Rnlsqr, Pnl

def radial_wf_integral(n,l,r_A,Z=1,N_neut=0):
    Rnl, Rnlsqr, Pnl = radial_probability(n,l,r_A,Z,N_neut)
    # we assume that max(r)/(len(r)-1) = dr
    integ = np.sum(Pnl) * np.max(r_A) / (r_A.shape[0]-1)
    #print(integ) 
    return integ

def psi_xyz(n,l,m,x_grid,y_grid,z_grid,Z=1,N_neut=0):
    lag = genlaguerre(n-l-1,2*l+1)
    r_grid = np.sqrt(x_grid**2+y_grid**2+z_grid**2)
    Zr_a0 = Z*r_grid/bohr_rad_A
    #lag_of_r = lag(2*Zr_a0/n)
    Rnl = radial_wf(n,l,r_grid,Z,N_neut)
    th_grid = np.arctan(y_grid/x_grid)
    ph_grid = np.arctan(np.sqrt(x_grid**2+y_grid**2)/z_grid)
    #th_grid, ph_grid = np.meshgrid(th,ph)
    Ylm = sph_harm(m,l,th_grid,ph_grid) 
    return Rnl * Ylm

def real_wf_xyz(designation,x_grid,y_grid,z_grid,Z=1,N_neut=0):
    n,l,absm,pm = quantum_numbers_map[designation]
    return real_wf_nlm_xyz(n,l,absm,pm,x_grid,y_grid,z_grid,Z,N_neut)

def real_wf_nlm_xyz(n,l,absm,plusminus,x_grid,y_grid,z_grid,Z=1,N_neut=0):
    wf_func = lambda nn,ll,mm: psi_xyz(nn,ll,mm,x_grid,y_grid,z_grid,Z,N_neut)
    if absm<0:
        raise ValueError('The absm argument was {}- must be greater than or equal to zero'.format(absm))
    if absm==0:
        return wf_func(n,l,absm)
    else:
        psi_mpos = wf_func(n,l,absm)
        psi_mneg = wf_func(n,l,-1*absm)
        if plusminus == '+':
            return 1./np.sqrt(2) * (psi_mpos + psi_mneg)
        elif plusminus == '-':
            return 1./(1j*np.sqrt(2)) * (psi_mpos - psi_mneg)
        else:
            raise ValueError('The plusminus argument was {}- must be either "+" or "-".'.format(plusminus))

