""" Retrievals of backscatter and extinction based on Raman measurements

.. warning::
   These functions have not been tested!
"""


import numpy as np
from scipy.signal import savgol_filter

from molecular import rayleigh_scattering, utilities


def raman_extinction(signal, dz, emission_wavelength, raman_wavelength, angstrom_aerosol, temperature, pressure,
                     window_size, order, C=385., rh=0.):
    r"""
    Calculates the aerosol extinction coefficient based on pre-processed Raman signals and molecular profiles.

    The derivative is calculated using a Savitzky-Golay filter.

    Parameters
    ----------
    signal : (M,) array
       The range_corrected molecular signal. Should be 1D array of size M.
    dz : float
       Altitude step, used in the derivative [m]
    emission_wavelength, raman_wavelength : float
       The emission and detection wavelengths [nm]
    angstrom_aerosol : float
       The aerosol Angstrom exponent.
    temperature : (M,) array
       Atmospheric temperature profile, same shape as the lidar signal [Kelvin]
    pressure : (M,) array
       Atmospheric pressure profile, same shape as the lidar signal [hPa]
    window_size : int
       the length of the smoothing window. Must be an odd integer number.
    order : int
       The order of the polynomial used in the filtering.
       Must be less then `window_size` - 1.
    C : float
       CO2 concentration [ppmv].
    rh : float
       Relative humidity from 0 to 100 [%]

    Returns
    -------
    alpha_aer : arrays
       The aerosol extinction coefficient [m-1]
       
    Notes
    -----
    The aerosol extinction coefficient is given by the formula:
    
    .. math::
       \alpha_{aer}(R,\lambda_0) = \frac{\frac{d}{dR}ln[\frac{N_{Ra}(R)}
       {S(R,\lambda_{Ra})}] - \alpha_{mol}(R,\lambda_0) - \alpha_{mol}(R,\lambda_{Ra})}
       {[1 + (\frac{\lambda_0}{\lambda_{Ra}})^{\alpha(R)}]}

    References
    ----------
    Ansmann, A. et al. Independent measurement of extinction and backscatter profiles
    in cirrus clouds by using a combined Raman elastic-backscatter lidar.
    Applied Optics Vol. 31, Issue 33, pp. 7113-7131 (1992)    
    """
    # Calculate profiles of molecular extinction
    alpha_molecular_emission = rayleigh_scattering.alpha_rayleigh(emission_wavelength, pressure, temperature, C, rh)
    alpha_molecular_raman = rayleigh_scattering.alpha_rayleigh(raman_wavelength, pressure, temperature, C, rh)

    # Calculate number density of the target molecule
    number_density = utilities.number_density_at_pt(pressure, temperature, rh)

    alpha_aer = retrieve_raman_extinction(signal, dz, emission_wavelength, raman_wavelength, alpha_molecular_emission,
                              alpha_molecular_raman, angstrom_aerosol, number_density, window_size, order)

    return alpha_aer


def retrieve_raman_extinction(signal, dz, emission_wavelength, raman_wavelength, alpha_molecular_emission,
                              alpha_molecular_raman, angstrom_aerosol, number_density, window_size, order):
    """ Calculates the aerosol extinction coefficient based on pre-processed Raman signals and molecular profiles.

    The derivative is calculated using a Savitzky-Golay filter.

    Parameters
    ----------
    signal : (M,) array
       The range-corrected molecular signal. Should be 1D array of size M.
    dz : float
       Altitude step, used in the derivative [m]
    emission_wavelength, raman_wavelength : float
       The emission and detection wavelength [nm]
    alpha_molecular_emission, alpha_molecular_raman : (M,) array
       The molecular extinction coefficient at each point of the signal profile for emission and raman wavelength.
    number_density : (M,) array
       The number density of the scattering molecule. E.g. the number density of N2 particles for typical Raman systems.
    angstrom_aerosol: float
       The aerosol Angstrom exponent.
    window_size : int
       the length of the smoothing window. Must be an odd integer number.
    order : int
       The order of the polynomial used in the filtering.
       Must be less then `window_size` - 1.

    Returns
    -------
    alpha_aer: arrays
       The aerosol extinction coefficient [m-1]
    """

    # Ratio to apply derivative
    ratio = np.ma.log(number_density / signal)

    derivative = savgol_filter(ratio, window_size, order, deriv=1, delta=dz,
                               mode='nearest')  # Calculate 1st derivative

    alpha_aer = (derivative - alpha_molecular_emission - alpha_molecular_raman) / (
                 1 + (emission_wavelength / float(raman_wavelength)) ** angstrom_aerosol)

    return alpha_aer


def raman_backscatter():
    r"""
    Calculates the aerosol backscatter coefficient based on:
    * Preprocessed elastic & raman signals.
    * The retrieved aerosol extinction coefficient.
    
    Parameters
    ----------
    
    Returns
    -------
    
    Notes
    -----
    The aerosol backscatter coefficient is given by the formula:
    
    .. math::
       \beta_{aer}(R,\lambda_0) = [\beta_{aer}(R_0,\lambda_0) + \beta_{mol}(R_0,\lambda_0)]
       \cdot \frac{P(R_0,\lambda_{Ra}) \cdot P(R,\lambda_0)}{P(R_0,\lambda_0) \cdot P(R,\lambda_{Ra})}
       \cdot \frac{e^{-\int_{R_0}^{R} [\alpha_{aer}(r,\lambda_{Ra}) + \alpha_{mol}(r,\lambda_{Ra})]dr}}
       {e^{-\int_{R_0}^{R} [\alpha_{aer}(r,\lambda_0) + \alpha_{mol}(r,\lambda_0)]dr}} - \beta_{mol}(R,\lambda_0)
    
    References
    ----------
    Ansmann, A. et al. Independent measurement of extinction and backscatter profiles
    in cirrus clouds by using a combined Raman elastic-backscatter lidar.
    Applied Optics Vol. 31, Issue 33, pp. 7113-7131 (1992)
    """
