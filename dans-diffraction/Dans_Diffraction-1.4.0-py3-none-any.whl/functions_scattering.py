# -*- coding: utf-8 -*-
"""
Module: functions_scattering.py

By Dan Porter, PhD
Diamond
2018

Usage:
    - Run this file in an interactive console
    OR
    - from Dans_Diffraction import functions_crystallography as fc

Version 0.1
Last updated: 11/11/18

Version History:
11/11/18 0.1    Version History started.

@author: DGPorter
"""

import sys, os, re
import numpy as np

from . import functions_general as fg
from . import functions_crystallography as fc

__version__ = '0.1'


def phase_factor(hkl, uvw):
    """
    Return the complex phase factor:
        phase_factor = exp(i.2.pi.HKL.UVW')
    :param HKL: array [n,3] integer reflections
    :param UVW: array [m,3] atomic positions in atomic basis units
    :return: complex array [n,m]
    """

    hkl = np.asarray(np.rint(hkl), dtype=np.float).reshape([-1, 3])
    uvw = np.asarray(uvw, dtype=np.float).reshape([-1, 3])

    dotprod = np.dot(hkl, uvw.T)
    return np.exp(1j * 2 * np.pi * dotprod)


def structure_factor(scattering_factor, occupancy, debyewaller, phase):
    """
    Return the complex structure factor:
        structure_factor = sum_i( sf.occ.dw.phase )
    :param scattering_factor: array [n,m] or [n]: radiation dependent scattering factor/ form factor,/ scattering length
    :param occupancy: array [m]: occupancy of each atom
    :param debyewaller: array [n,m]: thermal vibration factor of each atom and reflection
    :param phase: array [n,m]: complex phase factor
    :return: complex array [n]
    """
    nrefs, natoms = phase.shape
    scattering_factor = np.asarray(scattering_factor, dtype=np.float).reshape([nrefs, -1])
    occupancy = np.asarray(occupancy, dtype=float).reshape([-1, natoms])
    return np.sum(scattering_factor * occupancy * debyewaller * phase, axis=1)


def intensity(structurefactor):
    """
    Returns the squared structure factor
    :param structurefactor: complex array [n] structure factor
    :return: array [n]
    """
    return np.real( structurefactor * np.conj(structurefactor) )


def sf_xray(hkl, uvw, occ, formfactor, debyewaller=1.0):
    """
    Calculate the squared structure factor for the given HKL, using x-ray scattering factors
    :param hkl: [n,3] array of hkl reflections
    :param uvw: [m,3] array of atomic positions in r.l.u.
    :param occ: [m,1] array of atomic occupancies
    :param formfactor: [n,m] array of atomic  x-ray form factors
    :param debyewaller: [n,m] array of thermal factors
    :return sf: [n,1] complex array of structure factors
    Example:

      Scattering.sf_x_ray([1,0,0])
      Scattering.sf_x_ray([[1,0,0],[2,0,0],[3,0,0])
    Returns an array with the same length as HKL, giving the real intensity at each reflection.
    """

    hkl = np.asarray(hkl, dtype=np.float).reshape((-1, 3))
    uvw = np.asarray(uvw, dtype=np.float).reshape((-1, 3))
    occ = np.asarray(occ, dtype=np.float).reshape((len(uvw), 1))

    # Calculate structure factor
    # Broadcasting used on 2D ff
    dot = np.dot(hkl, uvw.T)
    sf = np.sum(formfactor * debyewaller * occ * np.exp(1j * 2 * np.pi * dot), axis=1)
    # SF = np.zeros(Nref,dtype=np.complex)
    # for ref in range(Nref):
    #    for at in range(Nat):
    #        SF[ref] += ff[ref,at]*dw[ref,at]*occ[at]*np.exp(1j*2*np.pi*dot_KR[ref,at])
    return sf


def x_ray_fast(xtl, HKL):
    """
    Calculate the squared structure factor for the given HKL, using atomic number as scattering length
      Scattering.x_ray_fast([1,0,0])
      Scattering.x_ray_fast([[1,0,0],[2,0,0],[3,0,0])
    Returns an array with the same length as HKL, giving the real intensity at each reflection.
    """

    HKL = np.asarray(np.rint(HKL), dtype=np.float).reshape([-1, 3])
    Nref = len(HKL)

    uvw, type, label, occ, uiso, mxmymz = xtl.Structure.get()
    Nat = len(uvw)

    # Get atomic form factors
    ff = fc.atom_properties(type, 'Z')

    # Get Debye-Waller factor
    if self._use_isotropic_thermal_factor:
        Qmag = xtl.Cell.Qmag(HKL)
        dw = fc.debyewaller(uiso, Qmag)
    elif self._use_anisotropic_thermal_factor:
        raise Exception('anisotropic thermal factor calculation not implemented yet')
    else:
        dw = 1

    # Calculate dot product
    dot_KR = np.dot(HKL, uvw.T)

    # Calculate structure factor
    SF = np.sum(ff * dw * occ * np.exp(1j * 2 * np.pi * dot_KR), axis=1)

    SF = SF / xtl.scale

    if self._return_structure_factor: return SF

    # Calculate intensity
    I = SF * np.conj(SF)
    return np.real(I)


def neutron(xtl, HKL):
    """
    Calculate the squared structure factor for the given HKL, using neutron scattering length
      Scattering.neutron([1,0,0])
      Scattering.neutron([[1,0,0],[2,0,0],[3,0,0])
    Returns an array with the same length as HKL, giving the real intensity at each reflection.
    """

    HKL = np.asarray(np.rint(HKL), dtype=np.float).reshape([-1, 3])
    Nref = len(HKL)

    uvw, type, label, occ, uiso, mxmymz = xtl.Structure.get()
    Nat = len(uvw)

    # Get atomic form factors
    ff = fc.atom_properties(type, 'Coh_b')

    # Get Debye-Waller factor
    if self._use_isotropic_thermal_factor:
        Qmag = xtl.Cell.Qmag(HKL)
        dw = fc.debyewaller(uiso, Qmag)
    elif self._use_anisotropic_thermal_factor:
        raise Exception('anisotropic thermal factor calculation not implemented yet')
    else:
        dw = 1

    # Calculate dot product
    dot_KR = np.dot(HKL, uvw.T)

    # Calculate structure factor
    SF = np.sum(ff * dw * occ * np.exp(1j * 2 * np.pi * dot_KR), axis=1)

    SF = SF / xtl.scale

    if self._return_structure_factor: return SF

    # Calculate intensity
    I = SF * np.conj(SF)
    return np.real(I)


def magnetic_neutron(xtl, HKL):
    """
    Calculate the magnetic component of the structure factor for the given HKL, using neutron rules and form factor
      Scattering.magnetic_neutron([1,0,0])
      Scattering.magnetic_neutron([[1,0,0],[2,0,0],[3,0,0])
    Returns an array with the same length as HKL, giving the real intensity at each reflection.
    """

    HKL = np.asarray(np.rint(HKL), dtype=np.float).reshape([-1, 3])
    Nref = len(HKL)

    uvw, type, label, occ, uiso, mxmymz = xtl.Structure.get()
    Nat = len(uvw)

    Q = xtl.Cell.calculateQ(HKL)
    Qhat = fg.norm(Q).reshape([-1, 3])
    Qmag = xtl.Cell.Qmag(HKL)

    # Get magnetic form factors
    if self._use_magnetic_form_factor:
        ff = fc.magnetic_form_factor(type, Qmag)
    else:
        ff = np.ones([len(HKL), Nat])

    # Calculate moment
    momentmag = fg.mag(mxmymz).reshape([-1, 1])
    momentxyz = xtl.Cell.calculateR(mxmymz)
    moment = momentmag * fg.norm(momentxyz)  # broadcast n*1 x n*3 = n*3
    moment[np.isnan(moment)] = 0.

    # Calculate dot product
    dot_KR = np.dot(HKL, uvw.T)

    # Calculate structure factor
    SF = np.zeros(Nref, dtype=np.complex)
    for n, Qh in enumerate(Qhat):
        SFm = [0., 0., 0.]
        for m, mom in enumerate(moment):
            # Calculate Magnetic part
            QM = mom - np.dot(Qh, mom) * Qh

            # Calculate structure factor
            SFm = SFm + ff[n, m] * np.exp(1j * 2 * np.pi * dot_KR[n, m]) * QM

        # Calculate polarisation with incident neutron
        if self._polarised:
            SF[n] = np.dot(SFm, self._polarisation_vector_incident)
        else:
            # SF[n] = np.dot(SFm,SFm) # maximum possible
            SF[n] = (np.dot(SFm, [1, 0, 0]) + np.dot(SFm, [0, 1, 0]) + np.dot(SFm,
                                                                              [0, 0, 1])) / 3  # average polarisation

    SF = SF / xtl.scale

    if self._return_structure_factor: return SF

    # Calculate intensity
    I = SF * np.conj(SF)
    return np.real(I)


def xray_magnetic(xtl, HKL):
    """
    Calculate the non-resonant magnetic component of the structure factor
    for the given HKL, using x-ray rules and form factor
      Scattering.xray_magnetic([1,0,0])
      Scattering.xray_magnetic([[1,0,0],[2,0,0],[3,0,0])
    Returns an array with the same length as HKL, giving the real intensity at each reflection.

    From Hill+McMorrow Acta Cryst. 1996 A52, 236-244 Equ. (2)
    Book: "X-ray Scattering and Absorption by Magnetic Materials" by Loevesy and Collins. Ch 2. Eqn.2.21+1
    No orbital component assumed
    magnetic moments assumed to be in the same reference frame as the polarisation
    """

    HKL = np.asarray(np.rint(HKL), dtype=np.float).reshape([-1, 3])
    Nref = len(HKL)

    uvw, type, label, occ, uiso, mxmymz = xtl.Structure.get()
    Nat = len(uvw)

    Qmag = xtl.Cell.Qmag(HKL)

    # Get magnetic form factors
    if self._use_magnetic_form_factor:
        ff = fc.magnetic_form_factor(type, Qmag)
    else:
        ff = np.ones([len(HKL), Nat])

    # Calculate moment
    momentmag = fg.mag(mxmymz).reshape([-1, 1])
    momentxyz = xtl.Cell.calculateR(mxmymz)  # moment direction in cartesian reference frame
    moment = momentmag * fg.norm(momentxyz)  # broadcast n*1 x n*3 = n*3
    moment[np.isnan(moment)] = 0.

    # Calculate dot product
    dot_KR = np.dot(HKL, uvw.T)

    # Calculate structure factor
    SF = np.zeros(Nref, dtype=np.complex)
    for n in range(Nref):
        # Calculate vector structure factor
        SFm = [0., 0., 0.]
        for m, mom in enumerate(moment):
            SFm = SFm + ff[n, m] * np.exp(1j * 2 * np.pi * dot_KR[n, m]) * mom

        # Calculate polarisation with incident x-ray
        # The reference frame of the x-ray and the crystal are assumed to be the same
        # i.e. pol=[1,0,0] || mom=[1,0,0] || (1,0,0)
        if self._polarised:
            SF[n] = np.dot(SFm, self._polarisation_vector_incident)
        else:
            # SF[n] = np.dot(SFm,SFm) # maximum possible
            SF[n] = (np.dot(SFm, [1, 0, 0]) + np.dot(SFm, [0, 1, 0]) + np.dot(SFm,
                                                                              [0, 0, 1])) / 3  # average polarisation

    SF = SF / xtl.scale

    if self._return_structure_factor: return SF

    # Calculate intensity
    I = SF * np.conj(SF)
    return np.real(I)


def xray_resonant(xtl, HKL, energy_kev=None, polarisation='sp', F0=1, F1=1, F2=1, azim_zero=[1, 0, 0], PSI=[0],
                  disp=False):
    """
    Calculate structure factors using resonant scattering factors in the dipolar approximation
      I = Scattering.xray_resonant(HKL,energy_kev,polarisation,F0,F1,F2)
    Returns an array with the same length as HKL, giving the real intensity at each reflection.
        energy_kev = x-ray energy in keV
        polarisation = x-ray polarisation: 'ss',{'sp'},'ps','pp'
        F0/1/2 = Resonance factor Flm
        azim_zero = [h,k,l] vector parallel to the origin of the azimuth
        psi = azimuthal angle defining the scattering plane

    Uses the E1E1 resonant x-ray scattering amplitude:
        fxr_n = (ef.ei)*F0 -i(ef X ei).z_n*F1 + (ef.z_n)(ei.z_n)F2

    Where ei and ef are the initial and final polarisation states, respectively,
    and z_n is a unit vector in the direction of the magnetic moment of the nth ion.
    The polarisation states are determined to be one of the natural synchrotron
    states, where sigma (s) is perpendicular to the scattering plane and pi (p) is
    parallel to it.
            ( s-s  s-p )
            ( p-s  p-p )

    From Hill+McMorrow Acta Cryst. 1996 A52, 236-244 Equ. (15)
    """

    if energy_kev is None:
        energy_kev = self._energy_kev

    HKL = np.asarray(np.rint(HKL), dtype=np.float).reshape([-1, 3])
    Nref = len(HKL)

    PSI = np.asarray(PSI, dtype=np.float).reshape([-1])
    Npsi = len(PSI)

    uvw, type, label, occ, uiso, mxmymz = xtl.Structure.get()
    Nat = len(uvw)

    Qmag = xtl.Cell.Qmag(HKL)

    # Get Debye-Waller factor
    if self._use_isotropic_thermal_factor:
        dw = fc.debyewaller(uiso, Qmag)
    elif self._use_anisotropic_thermal_factor:
        raise Exception('anisotropic thermal factor calculation not implemented yet')
    else:
        dw = 1

    # Calculate dot product
    dot_KR = np.dot(HKL, uvw.T)

    SF = np.zeros([Nref, Npsi], dtype=np.complex)
    for psival in range(Npsi):
        # Get resonant form factor
        fxres = self.xray_resonant_scattering_factor(HKL, energy_kev, polarisation, F0, F1, F2, azim_zero, PSI[psival],
                                                     disp=disp)

        # Calculate structure factor
        # Broadcasting used on 2D fxres
        SF[:, psival] = np.sum(fxres * dw * occ * np.exp(1j * 2 * np.pi * dot_KR), axis=1)

    SF = SF / xtl.scale

    if self._return_structure_factor: return SF

    # Calculate intensity
    I = SF * np.conj(SF)
    return np.real(I)


def xray_resonant_scattering_factor(xtl, HKL, energy_kev=None, polarisation='sp', F0=1, F1=1, F2=1,
                                    azim_zero=[1, 0, 0], psi=0, disp=False):
    """
    Calcualte fxres, the resonant x-ray scattering factor
      fxres = Scattering.xray_resonant_scattering_factor(HKL,energy_kev,polarisation,F0,F1,F2,azim_zero,psi)
    energy_kev = x-ray energy in keV
        polarisation = x-ray polarisation: 'ss',{'sp'},'ps','pp'
        F0/1/2 = Resonance factor Flm
        azim_zero = [h,k,l] vector parallel to the origin of the azimuth {[1,0,0]}
        psi = azimuthal angle defining the scattering plane {0}

    Uses the E1E1 resonant x-ray scattering amplitude:
        fxr_n = (ef.ei)*F0 -i(ef X ei).z_n*F1 + (ef.z_n)(ei.z_n)F2

    Where ei and ef are the initial and final polarisation states, respectively,
    and z_n is a unit vector in the direction of the magnetic moment of the nth ion.
    The polarisation states are determined to be one of the natural synchrotron
    states, where sigma (s) is perpendicular to the scattering plane and pi (p) is
    parallel to it.
            ( s-s  s-p )
            ( p-s  p-p )

    From Hill+McMorrow Acta Cryst. 1996 A52, 236-244 Equ. (15)
    """

    if energy_kev is None:
        energy_kev = self._energy_kev

    HKL = np.asarray(np.rint(HKL), dtype=np.float).reshape([-1, 3])
    Nref = len(HKL)
    Qmag = xtl.Cell.Qmag(HKL)
    tth = fc.cal2theta(Qmag, energy_kev)

    mxmymz = xtl.Structure.mxmymz()
    Nat = len(mxmymz)

    fxres = np.zeros([Nref, Nat], dtype=np.complex)
    for ref in range(Nref):
        # Resonant scattering factor
        # Electric Dipole transition at 3d L edge
        # F0,F1,F2 = 1,1,1 # Flm (form factor?)
        z1, z2, z3 = self.scatteringcomponents(mxmymz, HKL[ref], azim_zero, psi).T
        tthr = np.deg2rad(tth[ref])

        polarisation = polarisation.replace('-', '').replace(' ', '')
        if polarisation in ['sigmasigma', 'sigsig', 'ss']:  # Sigma-Sigma
            f0 = 1 * np.ones(Nat)
            f1 = 0 * np.ones(Nat)
            f2 = z2 ** 2
        elif polarisation in ['sigmapi', 'sigpi', 'sp']:  # Sigma-Pi
            f0 = 0 * np.ones(Nat)
            f1 = z1 * np.cos(tthr) + z3 * np.sin(tthr)
            f2 = -z2 * (z1 * np.sin(tthr) - z3 * np.cos(tthr))
        elif polarisation in ['pisigma', 'pisig', 'ps']:  # Pi-Sigma
            f0 = 0 * np.ones(Nat)
            f1 = z3 * np.sin(tthr) - z1 * np.cos(tthr)
            f2 = z2 * (z1 * np.sin(tthr) + z3 * np.cos(tthr))
        elif polarisation in ['pipi', 'pp']:  # Pi-Pi
            f0 = np.cos(2 * tthr) * np.ones(Nat)
            f1 = -z2 * np.sin(2 * tthr)
            f2 = -(np.cos(tthr) ** 2) * (z1 ** 2 * np.tan(tthr) ** 2 + z3 ** 2)
        else:
            raise ValueError('Incorrect polarisation. pol should be e.g. ''ss'' or ''sp''')
        fxres[ref, :] = F0 * f0 - 1j * F1 * f1 + F2 * f2
        if disp:
            print('( h, k, l)   TTH  (    mx,    my,    mz)  (    z1,    z2,    z3)')
            fmt = '(%2.0f,%2.0f,%2.0f) %6.2f  (%6.3f,%6.3f,%6.3f)  (%6.3f,%6.3f,%6.3f)  f0=%8.4f  f1=%8.4f  f2=%8.4f fxres= (%8.4f + %8.4fi)'
            for at in range(Nat):
                vals = (HKL[ref, 0], HKL[ref, 1], HKL[ref, 2], tth[ref],
                        mxmymz[at, 0], mxmymz[at, 1], mxmymz[at, 2],
                        z1[at], z2[at], z3[at],
                        f0[at], f1[at], f2[at],
                        fxres[ref, at].real, fxres[ref, at].imag)
                print(fmt % vals)
    return fxres


def scatteringcomponents(xtl, mxmymz, hkl, azim_zero=[1, 0, 0], psi=0):
    """
    Transform magnetic vector into components within the scattering plane
        ***warning - may not be correct for non-cubic systems***
    """

    # Define coordinate system I,J,Q (U1,U2,U3)
    Qhat = fg.norm(xtl.xtl.Cell.calculateQ(hkl))  # || Q
    AxQ = fg.norm(np.cross(azim_zero, Qhat))
    Ihat = fg.norm(np.cross(Qhat, AxQ))  # || to azim_zero
    Jhat = fg.norm(np.cross(Qhat, Ihat))  # -| to I and Q

    # Rotate coordinate system by azimuth
    Ihat_psi = fg.norm(np.cos(np.deg2rad(psi)) * Ihat + np.sin(np.deg2rad(psi)) * Jhat)
    Jhat_psi = fg.norm(np.cross(Qhat, Ihat_psi))

    # Determine components of the magnetic vector
    U = np.vstack([Ihat_psi, Jhat_psi, Qhat])
    z1z2z3 = np.dot(mxmymz, U.T)  # [mxmymz.I, mxmymz.J, mxmymz.Q]
    return fg.norm(z1z2z3)


def scatteringvectors(xtl, hkl, energy_kev=None, azim_zero=[1, 0, 0], psi=0, polarisation='s-p'):
    """
    Determine the scattering and polarisation vectors of a reflection based on energy, azimuth and polarisation.
    :param xtl: Crystal Class
    :param hkl: [n,3] array of reflections
    :param energy_kev: x-ray scattering energy in keV
    :param azim_zero: [1,3] direction along which the azimuthal zero angle is determind
    :param psi: float angle in degrees about the azimuth
    :param polarisation: polarisation with respect to the scattering plane, options:
                'ss' : sigma-sigma polarisation
                'sp' : sigma-pi polarisation
                'ps' : pi-sigma polarisation
                'pp' : pi-pi polarisation
    :return: kin, kout, ein, eout
    Returned values are [n,3] arrays
        kin : [n,3] array of incident wavevectors
        kout: [n,3] array of scattered wavevectors
        ein : [n,3] array of incident polarisation
        eout: [n,3] array of scattered polarisation

    The basis is chosen such that Q defines the scattering plane, sigma and pi directions are normal to this plane.
    """

    if energy_kev is None:
        energy_kev = self._energy_kev

    # Define coordinate system I,J,Q (U1,U2,U3)
    # See FDMNES User's Guide p20 'II-11) Anomalous or resonant diffraction'
    Qhat = fg.norm(xtl.Cell.calculateQ(hkl))  # || Q
    AxQ = fg.norm(np.cross(azim_zero, Qhat))
    Ihat = fg.norm(np.cross(Qhat, AxQ))  # || to azim_zero
    Jhat = fg.norm(np.cross(Qhat, Ihat))  # -| to I and Q

    # Determine wavevectors
    bragg = xtl.Cell.tth(hkl, energy_kev)
    rb = np.deg2rad(bragg)
    rp = np.deg2rad(psi)
    kin = np.cos(rb) * np.cos(rp) * Ihat - np.cos(rb) * np.sin(rp) * Jhat - np.sin(rb) * Qhat
    kout= np.cos(rb) * np.cos(rp) * Ihat - np.cos(rb) * np.sin(rp) * Jhat + np.sin(rb) * Qhat
    esig = np.sin(rp)*Ihat + np.cos(rb)*Jhat # sigma polarisation (in or out)
    piin = np.cross(kin, esig) # pi polarisation in
    piout= np.cross(kout, esig) # pi polarisation out

    # Polarisations
    polarisation = polarisation.replace('-', '').replace(' ', '')
    if polarisation in ['sigmasigma', 'sigsig', 'ss']:
        ein = 1.0*esig
        eout = 1.0*esig
    elif polarisation in ['sigmapi', 'sigpi', 'sp']:
        ein = 1.0*esig
        eout= 1.0*piout
    elif polarisation in ['pisigma', 'pisig', 'ps']:
        ein = 1.0*piin
        eout= 1.0*esig
    elif polarisation in ['pipi', 'pp']:
        ein = 1.0*piin
        eout= 1.0*piout
    else:
        raise ValueError('Incorrect polarisation. pol should be e.g. ''ss'' or ''sp''')
    return kin, kout, ein, eout


def xray_nonresonant_magnetic(xtl, HKL, energy_kev=None, azim_zero=[1, 0, 0], psi=0, polarisation='s-p'):
    """
    Calculate the non-resonant magnetic component of the structure factor
    for the given HKL, using x-ray rules and form factor
      Scattering.xray_magnetic([1,0,0])
      Scattering.xray_magnetic([[1,0,0],[2,0,0],[3,0,0])
    Returns an array with the same length as HKL, giving the real intensity at each reflection.

    From Hill+McMorrow Acta Cryst. 1996 A52, 236-244 Equ. (2)
    Book: "X-ray Scattering and Absorption by Magnetic Materials" by Loevesy and Collins. Ch 2. Eqn.2.21+1
    No orbital component assumed
    magnetic moments assumed to be in the same reference frame as the polarisation
    """

    HKL = np.asarray(np.rint(HKL), dtype=np.float).reshape([-1, 3])
    Nref = len(HKL)

    uvw, type, label, occ, uiso, mxmymz = xtl.Structure.get()
    Nat = len(uvw)

    kin, kout, ein, eout = scatteringvectors(xtl, HKL, energy_kev, azim_zero, psi, polarisation)

    Qmag = xtl.Cell.Qmag(HKL)

    # Get magnetic form factors
    if self._use_magnetic_form_factor:
        ff = fc.magnetic_form_factor(type, Qmag)
    else:
        ff = np.ones([len(HKL), Nat])

    # Calculate moment
    momentmag = fg.mag(mxmymz).reshape([-1, 1])
    momentxyz = xtl.Cell.calculateR(mxmymz)  # moment direction in cartesian reference frame
    moment = momentmag * fg.norm(momentxyz)  # broadcast n*1 x n*3 = n*3
    moment[np.isnan(moment)] = 0.

    # Magnetic form factor
    # f_non-res_mag = i.r0.(hw/mc^2).fD.[.5.L.A + S.B] #equ 2 Hill+McMorrow 1996
    # ignore orbital moment L
    B = np.cross(eout, ein) + \
        np.cross(kout, eout)*np.dot(kout, ein) - \
        np.cross(kin, ein)*np.dot(kin, eout) - \
        np.cross(np.cross(kout, eout), np.cross(kin, ein))
    fspin = 1j * ff * np.dot(moment, B)

    # Calculate dot product
    dot_KR = np.dot(HKL, uvw.T)

    # Calculate structure factor
    sf = np.sum(fspin * occ * np.exp(1j * 2 * np.pi * dot_KR), axis=1)

    SF = SF / xtl.scale

    if self._return_structure_factor: return SF

    # Calculate intensity
    I = SF * np.conj(SF)
    return np.real(I)