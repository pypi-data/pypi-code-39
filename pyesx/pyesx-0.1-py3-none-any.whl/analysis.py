"""
Package to run analysis of the data modeled vs measured / observed

A. Enguehard - 07/

ToDo:
* May have to change "mod" to a list of modelled (?)
"""

from pyesx import data
from pyesx import utils
import numpy as np


class esxanalysis():
    """
    """

    def __init__(self, obs, mod):
        """
        Creates the object esxanalysis made to compare models and external data

        Attributes:
        ----------
        * date0_mod / obs : (Timestamp)
            First date of the time intersection between observations and models
        * date1_mod / obs : (Timestamp)
            Last date of the time intersection between observations and models
        * obs : (esxdata object)
            The data frame of the observations over the intersection
            Time intervalle of the measurmeents is included in the time
            intervalle of the modelled values
        * mod : (esxrun object)
            Simulation to compare with
        * match : (bool)
            If the time steps of the measurements all match with model ones
        * mod_int : (esxrun object)
            Linear interpolation of the model data to match measurements
        """
        # Get the first common date and last one in obs
        self.date0_obs, self.date0_mod, self.idate0_obs, self.idate0_mod = \
            utils.firstdate(obs.datetime, mod.datetime)
        self.date1_obs, self.date1_mod, self.idate1_obs, self.idate1_mod = \
            utils.lastdate(obs.datetime, mod.datetime)
        # Get the time intersection of the data
        self.obs = obs._filter_time(self.date0_obs, self.date1_obs)
        self.mod = mod._filter_time(self.date0_mod, self.date1_mod)
        # Gives if the time steps all match or not
        self.match = self.obs.data.index.isin(self.mod.datetime) is True
        # Calculate the time interpolated model frames
        self.mod_int = mod._interpolate_timeseries(self.obs.datetime)
        return

    # def _error_z(self, obs_name, mod_spcs, mod_var, z, type='quadratic', zscale='mid', divz=False, integrate=False, other_series=None):
    #     """ Computes a distance between measured and modeled series
    #
    #     Parameters:
    #     ----------
    #     * obs_name : (str)
    #         Name of the variable in the observations to use
    #     * mod_spcs : (str)
    #         Species to use from the model
    #     * var_mod : (str)
    #         Variable in the model
    #     * z : (float)
    #         Height at which to get the modeled values
    #     * type : (str)
    #         Type of distance to compute
    #     * zscale : (str) - 'mid' / 'bound'
    #         Zscale of the modeled values to get a good interpolation
    #     * divz : (bool)
    #         In case you want to divide the values of the serie by the height
    #     * integrate : (bool)
    #         To verticaly integrate the data
    #     * other_serie : (pd.Series)
    #         If you want to compare with another serie you have
    #     """
    #
    #     # Get the data
    #     serie_obs = self.obs._interpolate_z(obs_name, z)
    #     if integrate is False and other_serie is None:
    #         serie_mod = self.mod_int._interpolate_z(mod_spcs, mod_var, z,
    #                                                 zscale=zscale, divz=divz)
    #     elif other_serie is None:
    #         serie_mod = self.mod_int._integrate_z(mod_spcs, mod_var, z,
    #                                               zscale=zscale, divz=divz)
    #     else:
    #         serie_mod = other_series
    #
    #     if type == 'quadratic':
    #         a = 2
    #     return
