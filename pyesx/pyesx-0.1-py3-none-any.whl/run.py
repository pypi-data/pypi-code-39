"""
Package to import and treat ESX model outputs

Compatibility: Python 3.7

A. Enguehard - 07/2019

ToDO:
* rolling average

"""

import numpy as np
import matplotlib.pyplot as plt
import os
from pyesx import utils as esxutils
from pyesx import lib as esxlib
from pyesx import plots as esxplots
from pyesx.path import esxrunpath
from copy import deepcopy
import pandas as pd
import pickle


# -----------------------------------------------------------------------------

class esxrun:
    """Results from an ESX experiment to be studied:

    The class 'esxrun' allows to treat easily the results from a simulation
    made using the ESX model. The class includes attributes storing data
    and the simulation framework, local functions to analyse it and treat
    it, and associated plotting methods.

    Attributes
    ----------

    """

    def __init__(self, project, output_name, dateformat='%d/%m/%Y %H:%M:%S'):

        self.project = project
        self.prefixe = output_name
        self.dateformat = dateformat
        self.filter = []

        # Create the structure of the dictinnary where data will be stored
        self.data = {}

        self.path = esxrunpath(project, output_name)
        return

    def _get_frame(self, basefile='__Meteo__T__Value__degC.csv'):
        """Get the general time and space frame associated with simulations

        It uses the basefile to import the dataset, and this one should be
        changed in case names change, etc..

        Returns:
        -------
        datetime : array with date time ordered
        cumtime : array with integers giving cumulative time in seconds
        solar : solar incidence in (W.m-2)
        z : mid-box height for each ESX level
        """
        #

        self.basefile = self.path.outputpath + '/' + self.prefixe + basefile
        # open the file
        file = np.genfromtxt(self.basefile, delimiter=',',
                             dtype='<U10')
        # Import the framework
        self.cumtime = file[1:, 0].astype(float).astype(int)
        self.datetime = pd.Series(esxutils.get_datetime(file[1:, 1],
                                                        file[1:, 2]))
        self.solar = file[1:, 3].astype(float)
        self.z = file[0, 4:].astype(float)
        self.nt = np.size(self.datetime)
        self.nz = np.size(self.z)

        # Convert to Series with index=datetime and values=datetime
        self.datetime = pd.Series(self.datetime.values, index=self.datetime)

        # Calculations for z frame precision
        def get_zframe():
            """Get the dz and z_boundary positions
            """
            dz = [self.z[0]*2]  # Layer's thickness
            zb = [self.z[0]*2]  # Top boundary of each layer height
            dzb = []  # Thickness between two layers' mid_points
            for i in range(len(self.z)-1):
                dz.append(2 * (self.z[i+1] - zb[i]))
                zb.append(zb[i] + dz[i+1])
                dzb.append(0.5*dz[i] + 0.5*dz[i+1])
            return np.array(dz), np.array(zb), np.array(dzb)

        def get_tmid():
            """Get mid time steps points

            WARNING: It is thus 1 time step shorter than the other scale
            """
            t = self.datetime
            tmid = [t[i] + (t[i+1]-t[i])/2 for i in range(len(t)-1)]
            return tmid

        self.datetime_mid = get_tmid()
        self.dz, self.zb, self.dzb = get_zframe()

        self.baseframe = self._getfromfile(self.basefile)
        print("=> (time, space) frame of %s updated" %self.prefixe)
        return

    def _checkupdate_dict(self, spcs, var):
        """Check is the dictionnary entry exists already or has to be created
        Creates the entry if needed

        ex:
        TestRun._checkupdate_dict('O3', 'CANDEP_NL')
        "The variable O3 CANDEP_NL already exists in the TestRun dictionnary"
        or
        "New entry TestRun.data[O3][CANDEP_NL] created"
        """
        spcs_exists = esxutils.is_in(spcs, list(self.data.keys()))[0]
        if spcs_exists is False:
            # var_exists = esxutils.is_in(spcs, list(self.data[spcs].keys()))[0]
            print("==>      TestRun.data[%s]"
                  %spcs)
            self.data[spcs] = {}  # Initialize the dictionnary entry
        return

    def _import_spcs(self, spcs):
        """Import all the files related to a given spcs (ex: 'O3', 'Mair')

        return : Import dictionnary
        """
        print("****************************************************")
        print("** Start to create the %s dictionnary of %s run **"
              %(spcs, self.prefixe))
        os.chdir(self.path.outputpath)

        # Create the dictionnary with the entries
        tmp_dict = {}
        tmp_dict[spcs] = []

        # Listing files related to the given species
        listfiles = [f for f in os.listdir(self.path.outputpath) if
                     os.path.isfile(os.path.join(self.path.outputpath, f))
                     and f[-3:] == 'csv'
                     and esxutils.filename_strip(f)[2] == spcs]
        # Create the list of variables to import
        for f in listfiles:
            spcs, var = esxutils.filename_strip(f)[2], \
                        esxutils.filename_strip(f)[3]
            tmp_dict[spcs].append(var)

        # Import all the files related to the species
        self._import_dict(tmp_dict)
        return

    def _makedict(self):
        """Create a complete dictionnary of possibilities for a simulation

        format :
        --------
        {'O3':['CANDEP_NL', 'ppb','GS'], 'NO':['ppb'], 'NO2':['ppb']}
        """
        print("****************************************************")
        print("** Start to create the full dictionnary of %s run **"
              %self.prefixe)
        tmp_dict = {}
        # List the output files associate with the simulation
        listfiles = [f for f in os.listdir(self.path.outputpath) if
                     os.path.isfile(os.path.join(self.path.outputpath, f))
                     and f[-3:] == 'csv']
        # For each file name do:
        for f in listfiles:
            # Get the spcs and var from the name of the file
            pref, type, spcs, var,  unit = esxutils.filename_strip(f)

            # Create the dictionnary with the entries
            if not esxutils.is_in(spcs, list(tmp_dict.keys()))[0]:
                tmp_dict[spcs] = []
                print("=> %s" %spcs)
            tmp_dict[spcs].append((type, var, unit))
            print("    - %s (in %s)" %(var, spcs))

        self.dict_tot = tmp_dict
        print("****************************************************")
        return

    def _getfromfile(self, filename):
        """Import the numerical array of a given file which has ESX format
        """
        # ESX csv file imported as a str arrays
        # Converts to float and keeps the array only with the data
        # 2D array :
        try:
            file = np.genfromtxt(filename, delimiter=',', dtype='<U10')
            # Eliminated impossible values
            file[1:, 4:][file[1:, 4:] == '-1.798+308'] = '-1.798E+308'
            array = file[1:, 4:].astype(float)
            columns = list(self.z)
            index = list(self.datetime)
        # 1D array
        except ValueError:
            file = np.genfromtxt(filename, delimiter=',', dtype='<U10',
                                 usecols=(0, 1, 2, 3, 4))
            array = file[1:, 4].astype(float)
            columns = ['Arbitrary']
            index = list(self.datetime)
        return pd.DataFrame(array, columns=columns, index=index)

    def _import_file(self, type, var, spcs, unit):
        """Import a datafile for ESX according to the entries

        Parameters:
        ----------
        spcs : str
            The chemical of meteorological variable you are interested to
        var_unit : str
            The last needed parameter to compute the name of the wanted file
            which can be the units for concentration (ppb, moleccm3, mXs)
            or the type of flux or resistance (ADV, GRNDEP, GS)

        ex:
        >>> TestRun._import_file('O3', 'CANDEP_NL')
        "Simulation Run32 has been updated with TestRun_O3_CANDEP_NL.csv"
        """
        os.chdir(self.path.outputpath)
        filename = self.prefixe + '__' + type + '__' + spcs + '__' \
            + var + '__' + unit + '.csv'

        # Check if the dictionnary entries exist:
        self._checkupdate_dict(spcs, var)

        # Add to the dictionnary
        if type == 'Conc':
            var = 'Conc'
        self.data[spcs][var] = self._getfromfile(filename)
        print('    *    %s : %s added to %s' %(spcs, var, self.prefixe))

    def _import_dict(self, dict):
        """Import all the files associated with a given dictionnary

        example of dictionnary:
        {'O3':['ppb', 'CANDEP_S', 'CANDEP_NL'], 'P':['Pa']}
        """
        os.chdir(self.path.outputpath)
        print("************ Start import dictionnary **************")
        # Iterate over all the variables
        for spcs in list(dict.keys()):
            # Iterate for each variable associated with the species / met_var
            for type, var, unit in dict[spcs]:
                self._import_file(type, var, spcs, unit)  # Import thedataset
        print("************* End import dictionnary ***************")
        return

    def _import_all(self):
        """Import the entire dataset given for a simulation
        """
        # Check if the frame is already imported
        if not hasattr(self, 'nt'):
            self._get_frame()

        os.chdir(self.path.outputpath)
        # Create the complet dictionnary of the available files if not existing
        if not hasattr(self, 'impdict'):
            self._makedict()
        # Import the whole dataset
        self._import_dict(self.dict_tot)
        return

    def _chem_treat(self, spcs):
        """Call routines to derive the chemistry modeled by ESX for a species

        * Changes names in the self.data dictionnary
        * Creates new entries :
            - [spcs]['CChem'] : Total chemical flux in each layer (nmol.m-2.s-1)
            - [spcs]['CChem_prod'] : Total chemical production flux
            - [spcs]['CChem_loss'] : Total chemical loss flux
        * Creates / updates new attributes :
            - self.chembudget_spcs
            - self.chembudget_reactions
        """
        # In this text xi refers to a given tracer
        # Update list of reactions associated with the species
        list_reactions = []
        list_sink = []
        list_prod = []
        # Create arrays to store the values
        shape = np.shape(self.data[spcs]['Concs'])
        self.data[spcs]['CChem'] = pd.DataFrame(0.0, columns=list(self.z),
                                              index=list(self.datetime))
        self.data[spcs]['CChem_loss'] = pd.DataFrame(0.0, columns=list(self.z),
                                                   index=list(self.datetime))
        self.data[spcs]['CChem_prod'] = pd.DataFrame(0.0, columns=list(self.z),
                                                   index=list(self.datetime))

        print('***** Computation of the chemical fluxes *****')
        print(' =>  %s Chemistry' %(spcs))
        for reac in list(self.data.keys()):
            if esxutils.is_in('TRACER', reac)[0] and esxutils.is_in(spcs, reac)[0]:
                # We assume that all the tracers are set for a single spcs
                list_reactions.append(reac[7:])  # Do not import 'TRACER'
                if esxutils.is_in('TRACER_'+ spcs, reac)[0]:  # Comsumption
                    list_sink.append(reac[7:])
                else:
                    list_prod.append(reac[7:])

        # Treat derive a chemical flux (nmol.m-2.s-1) for each (t,zi, xi)
        for reac in list_reactions:
            # basically the chemical flux is given by the storage flux
            # of a passive, non-advected tracer
            print('- ' + reac)
            self.data[spcs][reac] = self._storage_flux('TRACER_' + reac)
            if esxutils.is_in(reac, list_sink)[0]:
                # A sink of ozone is counted as positive
                self.data[spcs]['CChem'] += self.data[spcs][reac]
                self.data[spcs]['CChem_loss'] += self.data[spcs][reac]
            else:
                self.data[spcs]['CChem_prod'] += self.data[spcs][reac]
                # Thus a source of ozone is negative
                self.data[spcs]['CChem'] -= self.data[spcs][reac]
        # Store the lists of reactions to deal with easily
        if not hasattr(self, 'listreac'):
            self.listreac = {}
        if not esxutils.is_in(spcs, self.listreac.keys())[0]:
            self.listreac[spcs] = {}
        self.listreac[spcs]['All'] = list_reactions
        self.listreac[spcs]['Prod'] = list_prod
        self.listreac[spcs]['Sink'] = list_sink

        return

    def _filter_time(self, date0, date1):
        """Filters the dataset to erase the unwanted values in time

        Parameters:
        ----------
        """

        print("******************* Start Filtration ************************")

        frame = deepcopy(self)

        # Check if datetime already imported for the simulation
        if not hasattr(self, 'datetime'):
            self._get_frame()

        # Erase datetimes within the intervals for each variable
        for spcs in list(self.data.keys()):
            for var in list(self.data[spcs].keys()):
                frame.data[spcs][var] = esxutils.filterframe(frame.data[spcs][var],
                                                            date0, date1)

        # Save the filter parameters for post check
        frame.filter.append([date0, date1])

        # Update attributes
        frame.datetime = esxutils.filterseries(self.datetime, date0, date1)
        frame.nt = np.size(frame.datetime)
        print("********************* End Filtration ********************")
        return frame

    def _interpolate_timeseries(self, timeseries):
        """
        Get an interpolated dataframe based on a given time serie

        Parameters:
        ----------
        * timeseries : (pd.Series)
            Time serie on which to interpolate values of the data we have
            ex: index              value
                '2012-08-12 10:00' '2012-08-12 10:00'
        """
        object = deepcopy(self)
        t = pd.Series(index=timeseries)

        for spcs in list(self.data.keys()):
            for var in list(self.data[spcs].keys()):
                object.data[spcs][var] = \
                    esxutils.interpolate_t_frame(object.data[spcs][var], t)

        # Update attributes
        object.datetime = timeseries
        return object

    def _storage_flux(self, spcs):
        """Calculates the storage fluxes along an ESX simulation

        formula :
        --------

        fstor(z,t+1) = (C(z,t+1) - C(z,t)) / dt  *
                       (AirDensity(z,t+1) - AirDensity(z,t))e6 / 2 * dz(z)

        C : concentration (ppb)
        AirDensity : Air molecular concentration (cm-3)
        dz : layer thickness (m)
        """
        # Check if the frame is already imported
        if not hasattr(self, 'nt'):
            self._get_frame()

        # check if the air density is imported already
        if not esxutils.is_in('Mair', list(self.data.keys()))[0]:
            try:
                self._import_spcs('Mair')
            except:
                # Default air density (molec.cm-3)
                Mair = pd.DataFrame(2.4e19, index=list(self.datetime),
                                    columns=list(self.nz))
                print("WARNING : Use default Airdensity = %f" %Mair)
        else:
            var = list(self.data['Mair'].keys())[0]
            Mair = self.data['Mair'][var]

        # Create an empty array to store the values
        Fstor = np.zeros([self.nt, self.nz])

        # Compute the storage flux (nmol/m2/s)
        for i in range(self.nt-1):
            dt = self.cumtime[i+1] - self.cumtime[i]    # in s
            dc = (self.data[spcs]['Concs'].iloc[i+1] - \
                  self.data[spcs]['Concs'].iloc[i]) \
                  * 1e-9    # ppb * 1e-9 => fraction
            Mair_m = (Mair.iloc[i+1] + Mair.iloc[i]) / 2  # cm-3
            # in N.cm-3 converted to nmol.m-3 and then multiplied by m
            Fstor[i+1] = np.multiply(np.multiply(
                                     np.divide(dc, dt),
                                     Mair_m * esxlib.Ncm3_2_nmolm3), self.dz)
            #print(np.sum(np.array(Fstor[i]))) : Gives the advection budget
        res = pd.DataFrame(Fstor, index=list(self.datetime),
                                columns=list(self.z))
        self.data[spcs]['Stor'] = res

        return res

    def _storage_flux_integrated(self, spcs):
        """Get in each grib the integrated storage flux from the ground to zb
        """
        # get the storage flux array
        Fstor_int = self._storage_flux(spcs)
        # Recursive integration of the flux
        for i in range(1, self.nz):
            Fstor_int.iloc[:, i] = Fstor_int.iloc[:, i] + Fstor_int.iloc[:, i-1]
        return Fstor_int

    def _checkattributes(self, listing, var=True):
        """Check if esxrun object (esxrun.data) has all the wanted attributes

        Returns True if has all the attributes, False otherwise
        """
        value = True
        if var:
            for att in listing:
                if not esxutils.is_in(att, list(self.data.keys()))[0]:
                    print("%s.data has no entry %s" %(self.prefixe, att))
                    value = False
        else:
            for att in listing:
                if not hasattr(self, att):
                    print("%s has no attribute %s" %(self.prefixe, att))
                    value = False
        return value

    def _turb_flux(self, spcs):
        """Computes an approximation of the turbulent fluxes derived from K-th

        Theory:
        ------
        * Fturb(zbi,t) = - Kz(zbi,t) * ( C(zi+1,t) - C(zi,t) ) / dzbi

        From esx_Outputs we get :
        * Kz : Legendre_Gauss integral at top boundary of each layer
        * C : ppb concentrations at t, iz (converted to 1e9*cm-3 using Mair)
        """
        # Check the content of self before computing
        if not self._checkattributes([spcs, 'Mair', 'Kz']):
            return

        # Create an empty array to store the values
        Fturb = pd.DataFrame(0.0, index=list(self.datetime),
                             columns=list(self.zb[:-1]))

        # Compute for each grid_point at each time step Fturb
        Mair_array = self.data['Mair']['Value']  # Easier reading
        # cf. J-P calculation (esx_ZDiffSolver.f90)
        # Mair_mid = np.array([Mair_array[:, i] * self.dz[i+1]
        #                     + Mair_array[:, i+1] * self.dz[i]
        #                     / (2*self.dzb[i]) for i in range(self.nz-1)])
        # Kz = self.data['Kz']['m2Xs']
        # Ua = Kz *
        for it in range(self.nt):
            for iz in range(self.nz-1):
                dc = self.data[spcs]['Concs'].iat[it, iz+1] * \
                     Mair_array.iat[it, iz+1] \
                     - self.data[spcs]['Concs'].iat[it, iz] * \
                     Mair_array.iat[it, iz]
                dzb = float(self.dzb[iz])
                Kz = self.data['Kz']['Value'].iat[it, iz]  # Hard_coding again

                # Compute the turbulent flux
                Fturb.iat[it, iz] = -Kz * dc * 1e-9 / dzb * esxlib.Ncm3_2_nmolm3

        return Fturb

    def _tot_flux(self, spcs, h):
        # Calculate all the fluxes:
        CanDep_s = self._integrate_z(spcs, 'CanDep_s', h)
        CanDep_s_loss, CanDep_s_prod = esxutils.plusminus_series(CanDep_s)
        CanDep_ns = self._integrate_z(spcs, 'CanDep_ns', h)
        CanDep_ns_loss, CanDep_ns_prod = esxutils.plusminus_series(CanDep_ns)
        CanDep_nl = self._integrate_z(spcs, 'CanDep_nl', h)
        CanDep_nl_loss, CanDep_nl_prod = esxutils.plusminus_series(CanDep_nl)
        GrndDep = self.data[spcs]['GrndDep'].sum(axis=1)
        GrndDep_loss, GrndDep_prod = esxutils.plusminus_series(GrndDep)
        Stor = self._integrate_z(spcs, 'Stor', h)
        Stor_prod, Stor_loss = esxutils.plusminus_series(Stor)
        Chem = self._integrate_z(spcs, 'Chem', h)
        Chem_prod, Chem_loss = esxutils.plusminus_series(Chem)

        # Sum of the processes (Production and Loss)
        Sinks = CanDep_s_loss + CanDep_ns_loss + CanDep_nl_loss + GrndDep_loss \
                + Stor_loss + Chem_loss
        Sources = CanDep_s_prod + CanDep_ns_prod + CanDep_nl_prod + \
                  GrndDep_prod + Chem_prod + Stor_prod
        Tot = Sinks + Sources
        return Tot

    def _integrate_z(self, spcs, flux, z, zscale='mid', divz=False):
        """ Returns the z integrated value of the fluxes (WARNING UNITS)
        """
        a = self._interpolate_z(spcs, flux, z, zscale)
        # Z-integration
        b = self.data[spcs][flux].iloc[:,
            :esxutils.is_higher(z, self.z)-1].sum(axis=1) + a
        return b

    def _interpolate_z(self, spcs, var, z, zscale='mid', divz=False):
        """Linear interpolation of a given variable to get its value at z

        Parameters:
        ----------
        * zscale : (str) - 'Mid' / 'Bound'
            Define the grid_points to which the variable correspounds (mid grid
            point or boundaries of the layers)
        * divz : (Bool)
            Divide by z thickness of the layers - usually to get nmol/m3/s
            rather than nmol/m2/s for the fluxes
        """
        # Get the right z-scale
        dzserie = [1] * len(self.z)
        if zscale == 'mid':
            zserie = self.z
            if divz is True:
                dzserie = self.dz
        else:
            zserie = self.zb
            if divz is True:
                dzserie = self.dzb

        # Get the z factor for linear interpolation
        iz_sup = esxutils.is_higher(z, zserie)
        factor = (z - zserie[iz_sup-1]) / (zserie[iz_sup] - zserie[iz_sup-1])

        dz1 = dzserie[iz_sup]
        dz0 = dzserie[iz_sup - 1]
        # Get the numerical value at interpolated height
        diff = self.data[spcs][var].iloc[:, iz_sup] / dz1 \
            - self.data[spcs][var].iloc[:, iz_sup - 1] / dz0
        value_at_z = self.data[spcs][var].iloc[:, iz_sup - 1] / dz0 + \
            (factor * diff)

        return value_at_z

    def _hourlymean(self, spcs, var, divz=False):
        """Compute the hour based average of the data in a 24H frame

        Parameters:
        ----------
        * spcs (str)
            The species you are interested into (O3, Mair...)
        * var (str)
            The variable associated to compute the hourly average
            (ex: Turb, Value, Concs, CanDep_s)

        Outputs:
        --------
        * mean (array)
            (1, 24) shape array with averaged values
        * std (array)
            (1, 24) shape array with the associated standart deviation
        """
        if divz is True:
            frame = self.data[spcs][var].divide(self.dz)  # convert to /m3/s
        else:
            frame = self.data[spcs][var]

        # Compute the average on a 24H frame
        groups = frame.groupby(frame.index.hour)
        mean = groups.mean()
        std = groups.std()

        return mean, std

    def _plot_timeseries_var(self, spcs, var, z, timescale='on', zscale='mid', integrated=False):
        """Datetime plot for a given variable

        Parameters:
        -----------
        spcs: str
            species you are interested into (ex: 'O3', 'Kz')
        var : str
            variable associated (ex: 'Concs', 'm2Xs')
        z : float
            outpupt height (WARNING: Linear interpolation)
        timescale : 'on', 'midpoints'
            if the variable corresponds to mid-time steps or on-time timesteps
            ex: Kz/CANDEP_S : on-time steps
            ex: storage     : mid-time_steps
        zscale : 'mid', 'bound'
            if the variable is at mid-layer grid-points of boundary points
        """
        # Get the right time scale according to the esxrun library
        if timescale == 'on':
            time = self.datetime
        else:
            time = self.datetime_mid

        # Get the value at z
        if integrated:
            z_value = self._integrate_z(spcs, var, z, zscale)
        else:
            z_value = self._interpolate_z(spcs, var, z, zscale)

        # Date_time plots
        return plt.plot(z_value, 'o', label='%s : %s' %(spcs, var))

    def _plot_profile_t(self, spcs, var, datetime, ax, zscale='mid', divz=False, linestyle='-', marker='o'):
        """Plot the profile of a variable at t (datetime)
        """
        # z-scale
        z, dz = esxutils.set_zscale(self, zscale=zscale)

        serie = self.data[spcs][var].loc[datetime]
        lab = self.prefixe + ' on ' + datetime.strftime(datetime, self.dateformat)
        ax.plot(z, serie.values, marker=marker, linestyle=linestyle, label=lab)
        return

    def _plot_profile_mean_t(self, spcs, var, t, ax, zscale='mid', fill=True, divz=False, linestyle='-', marker='o'):
        """Plot mean profile of a variable at a given hour of the day
        """
        # z-scale
        z, dz = esxutils.set_zscale(self, zscale=zscale)

        # get the data
        frame = self.data[spcs][var]
        if divz is True:
            frame = frame.divide(dz)
        groups = frame.groupby(frame.index.hour)
        mean = groups.mean().iloc[t, :]
        std = groups.std().iloc[t, :]

        # --- Plot ---
        lab = self.prefixe + ' Time (H): ' + str(t)
        if fill is True:
            ax.plot(z, mean, marker=marker, linestyle=linestyle, label=lab)
            ax.fill_between(z, mean-std, mean+std, alpha=0.3)
        else:
            ax.plot(z, mean, marker=marker, linestyle=linestyle, label=lab)
        return

    def _plot_hourlymean(self, spcs, var, list_heights, zscale='mid', divz=False, integrate=False, measures=False, meas_var_name=None, meas_data=None, metadata=True):
        """Plot the diurnal cycle of a given variable at different heights.
        This can be compared with measurmements.

        Parameters:
        ----------
        * spcs : (str)
            Name of the studied species (ex: 'O3', 'Kz')
        * var : (var)
            Name of the variable associated to plot (ex: 'Value', 'Concs')
        * list_heights : (list)
            List of heights (in m) to plot (ex: [0, 3, 10])
        * measures : (bool)
            Tell if you want to display measurements too
        * meas_data : (esxPreProcess object)
            Use the imported measurements / data
        * meas_var_name : (str)
            Precise name in the measurements in case it is different from spcs
        * zscale : (str)
            'mid' = use mid-points as heights / 'bound' = use boundary heights
        * divz : (bool)
            Divide values by each layer thickness (useful for chemical flux)
        * metadata : (bool)
            Display metadata (title, legend, etc...)
        """
        # ------ Definitions -----
        # AE: As Turb is always at boundaries we can systematize it (hard code)
        if var == 'Turb':
            zscale = 'bound'
        if meas_var_name is None:  # Assume identical names for mod. and meas.
            meas_var_name = spcs

        c = ['orange', 'purple', 'cyan']

        # ----- Loop over heights ----
        i = -1
        for h in list_heights:
            i = i + 1
            if integrate is True:
                val = self._integrate_z(spcs, var, h, zscale=zscale, divz=divz)
            else:
                val = self._interpolate_z(spcs, var, h, zscale=zscale, divz=divz)
            # ---- Plot the modeled values -----
            esxplots.p24H(val, h, label='Simulation ' + self.prefixe + ' ', color=c[i])
            # ----- Measurements -----
            if measures is True:
                try:  # Get measurements and plot it
                    key = meas_var_name + ':' + str(h) + 'm'
                    m = meas_data.data[key]
                    esxplots.p24H(m, h=str(h) , fill=False, dbg=True, color=c[i], linestyle='dashed')
                except KeyError:
                    print('Not found: ' + key)

        # Display outlines:
        if metadata:
            plt.title('Diurnal cycle for ' + spcs + ' - ' + var)
            plt.ylabel('Value: ' + spcs + ' - ' + var)
            plt.xlabel('Time (H)')
            plt.legend()

        return

    def _plot_series(self, spcs, h, measures=False, meas_data_file=None, ylim=[-5, 30], averaged=False, width=0.24, curves=True, bar=True):
        """Plot the time serie for all the variables
        """

        if measures is True:
            os.chdir(self.path.datapath)
            meas = pickle.load(open(meas_data_file, 'rb'))
            if averaged is True:
                grp = meas.groupby(meas.index.hour)
                meas, meas_std = grp.mean(), grp.std()

        if averaged is True:
            time = tuple([i for i in range(24)])
            width = 0.98
        else:
            time = tuple(self.datetime)

        # Calculate all the fluxes:
        CanDep_s = self._integrate_z(spcs, 'CanDep_s', h)
        CanDep_s_loss, CanDep_s_prod = esxutils.plusminus_series(CanDep_s)
        CanDep_ns = self._integrate_z(spcs, 'CanDep_ns', h)
        CanDep_ns_loss, CanDep_ns_prod = esxutils.plusminus_series(CanDep_ns)
        CanDep_nl = self._integrate_z(spcs, 'CanDep_nl', h)
        CanDep_nl_loss, CanDep_nl_prod = esxutils.plusminus_series(CanDep_nl)
        # GrndDep = self.data[spcs]['GrndDep'].sum(axis=1)
        # GrndDep_prod, GrndDep_loss = esxutils.plusminus_series(GrndDep)
        Stor = self._integrate_z(spcs, 'Store', h)
        Stor_prod, Stor_loss = esxutils.plusminus_series(Stor)
        Chem = self._integrate_z(spcs, 'Chem', h)
        Chem_prod, Chem_loss = esxutils.plusminus_series(Chem)
        Turb = self._interpolate_z(spcs, 'Turb', h, zscale='bound')
        Adv = self._integrate_z(spcs, 'Adv', h)
        Adv_prod, Adv_loss = esxutils.plusminus_series(Adv)

        # Sum of the processes (Production and Loss)
        # + GrndDep_loss
        Sinks = CanDep_s_loss + CanDep_ns_loss + CanDep_nl_loss + \
                Stor_loss + Chem_loss + Adv_loss
         # + GrndDep_prod
        Sources = CanDep_s_prod + CanDep_ns_prod + CanDep_nl_prod \
                  + Chem_prod + Stor_prod + Adv_loss
        Tot = Sinks + Sources

        ll = [CanDep_nl_loss, CanDep_ns_loss, CanDep_s_loss,
              Stor_loss, Chem_loss, Adv_loss]
        ls = [CanDep_nl_prod, CanDep_ns_prod, CanDep_s_prod,
              Stor_prod, Chem_prod, Adv_prod]

        # 24H mean:
        if averaged is True:
            tot_grp = Tot.groupby(Sinks.index.hour)
            Tot, st = tot_grp.mean(), tot_grp.std()
            i = -1
            for loss in ll:  # 24H average for each loss term
                i = i + 1
                ll[i] = loss.groupby(loss.index.hour).mean()
            i = -1
            for source in ls:  # 24H average for each source term
                i = i + 1
                ls[i] = source.groupby(source.index.hour).mean()
            grpt = Turb.groupby(Turb.index.hour)
            Turb, tstd = grpt.mean(), grpt.std()

        # Plot the stacked
        col = ['brown', 'purple', 'blue', 'g', 'yellow', 'pink']
        lab = ['Ground Deposition', 'Non-Leaf Deposition',
               'Non-Stomatal Deposition', 'Stomatal Deposition',
               'Storage Flux', 'Chemical Flux']
        if bar is True:
            for i in range(len(ll)):
                bottom = [0]*len(ll[0])
                if i > 0:
                    bottom = sum(ll[:i])
                plt.bar(time, tuple(ll[i]), width=width, bottom=tuple(bottom),
                        color=col[i], yerr=None, label=lab[i], alpha=0.8)
            for i in range(len(ls)):
                bottom = [0]*len(ll[0])
                if i > 0:
                    bottom = sum(ls[:i])
                plt.bar(time, tuple(ls[i]), width=width, color=col[i],
                        yerr=None, bottom=tuple(bottom), alpha=0.8)
        # pGrndDep = plt.bar(time, tuple(GrndDep_loss), width=width, color='brown',
        #                     yerr=None, label='Ground Deposition')
        # pCanDep_nl = plt.bar(time, tuple(CanDep_nl_loss), width=width,
        #                      color='purple', bottom=tuple(GrndDep_loss), yerr=None,
        #                      label='Non_Leaf Deposition')
        # pCanDep_ns = plt.bar(time, tuple(CanDep_ns_loss), width=width, color='blue',
        #                      bottom=tuple(GrndDep_loss + CanDep_nl_loss), yerr=None,
        #                      label='Non_Stomatal Deposition')
        # pCanDep_s = plt.bar(time, tuple(CanDep_s_loss), width=width, color='g',
        #                     bottom=tuple(GrndDep_loss + CanDep_nl_loss + CanDep_ns_loss),
        #                     yerr=None, label='Stomatal Deposition')
        # pStorage = plt.bar(time, tuple(Stor_loss), width=width, color='yellow',
        #                   bottom=tuple(GrndDep_loss + CanDep_nl_loss + \
        #                                CanDep_ns_loss + CanDep_s_loss),
        #                   yerr=None, label='Storage Flux')
        # pChem = plt.bar(time, tuple(Chem_loss), width=width, color='pink',
        #                 bottom=tuple(GrndDep_loss + CanDep_nl_loss + CanDep_ns_loss + CanDep_s_loss +
        #                 Stor_loss), yerr=None, label='Chemical Flux')

        # Negative Values
        # lGrndDep = plt.bar(time, tuple(GrndDep_prod), width=width, color='brown',
        #                     yerr=None)
        # lCanDep_nl = plt.bar(time, tuple(CanDep_nl_prod), width=width,
        #                      color='purple', bottom=tuple(GrndDep_prod), yerr=None,)
        # lCanDep_ns = plt.bar(time, tuple(CanDep_ns_prod), width=width, color='blue',
        #                      bottom=tuple(GrndDep_prod + CanDep_nl_prod), yerr=None,)
        # lCanDep_s = plt.bar(time, tuple(CanDep_s_prod), width=width, color='g',
        #                     bottom=tuple(GrndDep_prod + CanDep_nl_prod + CanDep_ns_prod),
        #                     yerr=None)
        # lStorage = plt.bar(time, tuple(Stor_prod), width=width, color='yellow',
        #                   bottom=tuple(GrndDep_prod + CanDep_nl_prod + \
        #                                CanDep_ns_prod + CanDep_s_prod),
        #                   yerr=None)
        # lChem = plt.bar(time, tuple(Chem_prod), width=width, color='pink',
        #                 bottom=tuple(GrndDep_prod + CanDep_nl_prod + CanDep_ns_prod + CanDep_s_prod +
        #                 Stor_prod), yerr=None)

        # lStorage = plt.bar(time, tuple(Stor_prod), width=width, color='yellow',
        #                    yerr=None)
        # lChem = plt.bar(time, tuple(Chem_prod), width=width, color='pink',
        #                bottom=tuple(Stor_prod), yerr=None)

        # Turbulent flux
        pTurb = plt.plot(time, Turb, 'o-', label='ESX Turbulent flux',
                         markersize=2, color='b')
        # Explicit calculation of all the processes
        #AETMP: pTot = plt.plot(time, Tot, 'o-', label='Sum of all processes',
        #                markersize=2, color='orange')
        if averaged is True and curves is True:
            plt.fill_between(time, Turb - tstd, Turb + tstd, alpha=0.5, color='b')
        # Measurements
        if measures is True:
            pInpt = plt.plot(tuple(meas.index), -meas, 'o-',
                             label='Measurements', markersize=2, color='orange')
            if averaged is True and curves is True:
                plt.fill_between(time, -meas + meas_std,
                                 -meas - meas_std, alpha=0.5, color='orange')

        plt.ylabel('Downward Flux (nmol/m2/s)')
        plt.xlabel('Day Time (Hour)')
        plt.title('%s - Ozone sinks partition in the canopy (below %s)'
                  %(self.prefixe, str(h)))
        plt.legend()
        plt.ylim(ylim)

        plt.show()
        return

    def _plot_chemical_balance(self, spcs, h, integrated=True):
        """Plot the chemical balance (Importance of different reactions) of a
        given spcs within a 24H time-frame.

        Parameters:
        ----------
        * spcs : (str)
            Chemical species to study (Warning: Should be treated by ESX first)
        * h : (float)
            Height
        * integrated : (Bool)
            True (default) => Chemical balance from ground level up to h
                              (nmol/m2/s)
            False => At a given height (nmol/m3/s)

        Output:
        ------
        * 24H Histogram plot (matplotlib)
        """

        # In self._chem_treat already treated tracers to get lists of reactions
        # and their importance using the stroage fluxe formulas.

        # Difference between integration up to h and local values
        if integrated is True:
            f = self._integrate_z
            unit = 'nmol/m2/s'
            trs = ' up to '
            divz = False
        else:
            f = self._interpolate_z
            unit = 'nmol/m3/s'
            trs = ' at '
            divz = True

        # Parameters for the graph
        width = 1
        time = [i for i in range(24)]
        base = pd.Series([0.]*24, time)
        jet = plt.get_cmap('gist_ncar')
        colors = iter(jet(np.linspace(0, 1, 20)))

        # Reaction of production (Negative on the graph)
        for reaction in self.listreac['O3']['Prod']:
            val = f(spcs, reaction, h, divz=divz)
            grps = val.groupby(val.index.hour)
            mean = - grps.mean()   # (-) to get negative plot
            plt.bar(time, tuple(mean), width=width,
                    color=next(colors), bottom=tuple(base), yerr=None,
                    label=reaction)
            base = base + mean

        # Reactions of destruction (Positive on the graph)
        base = pd.Series([0.]*24, time)
        for reaction in self.listreac['O3']['Sink']:
            val = f(spcs, reaction, h, divz=divz)
            grps = val.groupby(val.index.hour)
            mean = grps.mean()
            plt.bar(time, tuple(mean), width=width,
                    color=next(colors), bottom=tuple(base), yerr=None,
                    label=reaction)
            base = base + mean

        # Plot the general trend:
        self._plot_hourlymean(spcs, 'CChem', [h], divz=divz,
                              integrate=integrated, metadata=False)

        plt.legend(loc='upper  left')
        plt.xlabel('Day-time (24H)')
        plt.ylabel('Consumption flux in ' + unit)
        plt.title('Chemical balance of ' + spcs + ' in ' + self.prefixe
                  + trs + str(h))

        return

    def _plot_map_reaction(self, spcs, reaction, valmax=None, valmin=None, norm=None, levels=10, divz=True, cmap='viridis'):
        """Display a z-time 24H map of a given reaction

        Parameters:
        -----------
        spcs : (str)
            Species with which is associated the reaction in the structure
        reaction : (str)
            ex: 'O3XNO_NO2' : Reaction of O3 with NO giving NO2
        norm : (str)
            Normalization of the data

        Output:
        ------
            Map of the chemical flux in each layer (nmol/m2/s)
        """

        # Compute the 24H hour statistics
        mean, std = self._hourlymean(spcs, reaction, divz=divz)
        if valmax is not None:
            mean[mean > valmax] = valmax
        if valmin is not None:
            mean[mean < valmin] = valmin

        yaxis = mean.columns
        plt.contourf(mean.transpose(), origin='lower', levels=levels, cmap=cmap)
        plt.colorbar()
        plt.yticks(range(len(yaxis)), yaxis, size='small')

        return

    def _sum(self, spcs_inpt, var_inpt, list_spcs, list_var):
        """ Compute the sum of elements and output it

        Parameters:
        ----------
        * spcs_inpt: (str)
            Name of the new entry in the self.data Dictionnary
        * var_inpt: (str)
            Name of the entry in the self.data[spcs_inpt] Dictionnary
        * list_spcs: (list o str)
            List of the species on which to compute the sum
        * list_var: (list of str / str)
            Use list if different var to sum
            If only one type applied for each species, use str

        Outputs:
        -------
        * Update self.data[spcs_inpt][var_inpt] with the sum
        * Output a pandas.DataFrame of the sum
        """
        # Number of iterations for the sum
        ll = len(list_spcs)
        if ll < 2:
            return 'No sum to compute...'
        if type(list_var) == str:
            list_var = [list_var]
        if len(list_var) == 1:
            # Means compiute the sum always with the same variable
            list_var = list_var * ll

        # Create the entry
        if not esxutils.is_in(spcs_inpt, list(self.data.keys()))[0]:
            print('Create new entry : ' + spcs_inpt)
            self.data[spcs_inpt] = {}

        # Compute the sum
        summ = self.data[list_spcs[0]][list_var[0]]
        for i in range(len(list_spcs)):
            summ = summ + self.data[list_spcs[i]][list_var[i]]
        # Add to the structure the sum
        self.data[spcs_inpt][var_inpt] = summ
        return summ

    def _AE_treat(self):
        """TMP Arthur Enguehard Classic chain
        """
        self._import_all()
        self._chem_treat('O3')
        self._storage_flux('O3')
        # self._sum('MNT', 'Concs', ['APINENE', 'BPINENE'], 'Concs')
        os.chdir(self.path.outputpath + '/../')
        try:
            os.remove(self.prefixe + '.pckl')
        except FileNotFoundError:
            pass
        pickle.dump(self, open(self.prefixe + '.pckl', 'wb'))
        return

    def _D_value(self):
        """Return the value D giving information about the photo-equilibirum
        state of a given Ox-NOx system under Temperature T and Solar incoming
        radiation Q.

        - O3 (float) : Ozone concentration (ppb)
        - NO (float) : Nitrogen Oxide concentration (ppb)
        - NO2 (float) : Nitrogen Oxide 2 concentration (ppb)
        - T (float) : Temperature (Kelvin)
        - Q (float) : Total incoming radiation (W.m-2)

        * Outputs:
          -------
        - D (float)
            PhotoEq stat

        * Theorie:
          -------
          (https://www.cerc.co.uk/environmental-software/assets/data/doc_techspec/P18_02.pdf)
          ADMS-5 Model (from CERC) NOx chemistry used.

          D = (K1/K2) * [O3]*[NO]/[NO2]
          """

        # Concentrations in ppb
        O3 = self.data['O3']['Concs']
        NO = self.data['NO']['Concs']
        NO2 = self.data['NO2']['Concs']
        # convert degC to Kevin
        T = self.data['T']['Value'] + 273.1
        # Convert umol/m2/s to W/m2
        Q = self.data['PARz']['Value'] / (esxlib.PARfrac * esxlib.Wm2_uE)

        # Define the constantes:
        k11 = 4.405e-2
        k12 = -1370

        k21 = 8e-4
        k22 = -10
        k23 = 7.4e-6

        # Compute the values:
        K1 = k11 * np.exp(k12/T)
        K2 = k21 * np.exp(k22/Q) + k23 * Q

        D = (K1 / K2) * O3 * NO / NO2
        return D.replace(np.inf, np.NaN)


# ================ PLOT TOOL FUNCTIONS =================


def compare_series(serie1, serie2):
    """Return a dataframe with the matching points of the two series
    """
    return pd.merge(pd.DataFrame(serie1), pd.DataFrame(serie2), how='inner',
                    right_index=True, left_index=True)

def tauL(z, ustar, hc, d=None):
    """Compute the Lagrangian Time scale from Leuning 2000
    """
    if d is None:     # Zero displacement plane
        d = 2/3 * hc  # Typical forest scaling

    def zruf(d, hc, k=0.4):
        """ Calculate the roughness layer height / thickness"""
        return d + (0.4 * hc * (1.25**2) / k)

    def nr_hyperbola(x, a, b, d, theta):
        """ Non-rectangular hyperbola """
        return [(a*x + b) + d*((a*x + b)**2 - 4*theta*a*b*x)**0.5]/(2*theta)

    # Conditions on height (bottom or top canopy parameterization)
    bottom = z < 0.25 * hc
    top = not bottom and z < zruf(d, hc)/hc
    # parameters from Leuning 2000
    theta = 0.98
    if top:
        a = 0.256
        b = 0.40
        d = 1
        x = z / hc - 0.8
        y = nr_hyperbola(x, a, b, d, theta)
    elif bottom:
        a = 0.850
        b = 0.41
        d = -1
        x = 4 * z / hc
        y = nr_hyperbola(x, a, b, d, theta)
    else:
        y = 0.4
    return y * hc / ustar


def Kz_eq(flux, dc, dz):
    """ Compute Kz matching with flux equilibrium
    """
    return flux * dz / dc


def sigmaW_inv_ustar(Kz, taul, ustar):
    """ Compute the sigma_W value associated with given Kz and TauL
    """
    return (taul * Kz)**0.5 / ustar


def CRFactor(runNOemis, runNoNOemis, z_ctrl, meas=True, meas_file=None, meas_var_name='FNO', fact=1):
    """Calculate a Canopy Reduction factor using two simulations

    Parameters:
    ----------
    * runNOemis: (esxrun object)
        A simulation with NO emissions from the ground and including NO / NO2
        turbulent fluxes
    * runNoNOemis: (esxrun object)
        A simulation without NO emissions from the ground still with NO / NO2
        turbulent fluxes
    * z_ctrl: (float)
        height at which you want to compare the ground flux to
    * meas_file: (esxPreProcess object)
        Give the measurements of NO ground emissions
    * fact: (float)
        In case there is a need to change units, etc...
    """
    # Get the fluxes at z_ctrl
    FNO_ne_z = runNoNOemis._interpolate_z('NO', 'Turb', z_ctrl)
    FNO2_ne_z = runNoNOemis._interpolate_z('NO2', 'Turb', z_ctrl)
    FNO_z = runNOemis._interpolate_z('NO', 'Turb', z_ctrl)
    FNO2_z = runNOemis._interpolate_z('NO2', 'Turb', z_ctrl)
    # Calculate the NOx fluxes
    FNOx_ne = FNO_ne_z + FNO2_ne_z
    FNOx = FNO_z + FNO2_z
    # Difference: Impact on flux of adding NO emissions on NOx transfer
    diff_FNOx = FNOx - FNOx_ne

    # I did not code any use of simulated emissions

    # Get the NO emissions from ground level from measurements:
    date0 = runNoNOemis.datetime[0]
    date1 = runNoNOemis.datetime[-1]
    os.chdir(runNoNOemis.path.datapath)
    # Import
    measf = pickle.load(open(meas_file, 'rb'))
    if meas is True:
        FNOmeas, tmp = measf._get_spcs(meas_var_name, date0, date1) * fact

    # CRF = diff_FNOx.divide(FNOmeas.transpose())
    return FNOmeas, diff_FNOx

def difference(run1, run2):
    """Compute the difference between two runs for all the variables.
                     * frame1 - frame2

    If needed for only one variable, please use Pandas functions

    Parameters:
    ----------

    Output:
    ------
    * run_diff (esxrun)
        Gives an esxrun object storing the difference between two runs
    """
    print(' ******* Differenciation two runs %s and %s ******'
             %(run1.prefixe, run2.prefixe))
    attributes = [k for k in dir(run1) if k[0] != '_' and k != 'var']

    run_diff = deepcopy(run1)
    species1 = pd.Series(sorted(list(run1.data.keys())))
    species2 = pd.Series(sorted(list(run2.data.keys())))
    #same = species1.equals(species2)

    # Check on which variable the runs can be compared
    common_species = species1[species1 == species2]
    noncommon_species = species1[species1 != species2]
    print('Non-common species : ', end='')
    print(list(noncommon_species))

    for spcs in common_species:
        vars = list(run1.data[spcs].keys())
        for var in vars:
            run_diff.data[spcs][var] = run1.data[spcs][var] - run2.data[spcs][var]
    for spcs in noncommon_species:
        vars = list(run1.data[spcs].keys())
        for var in vars:
            run_diff.data[spcs][var].iloc[:] = np.NaN
    return run_diff


def diurnal_difference(run1, run2, spcs, var):
    """Diurnal mean difference
    """
    diff = difference(run1, run2)
    mean_diff, std_diff = diff._hourlymean(spcs, var)
    return mean_diff, std_diff


def AE_general_import(project, list_experiments, spcs_chem='O3', add2dict=None):
    print("**** Initialization ****")
    # Intialization
    if add2dict is not None:
        run = add2dict
    else:
        run = {}
    for exp in list_experiments:
        run[exp] = esxrun(project, exp)
        run[exp]._get_frame()
        run[exp]._import_all()
        run[exp]._chem_treat(spcs_chem)

    # Save the variables
    os.chdir(run[list_experiments[0]].path.outputpath + '/../')
    for exp in list_experiments:
        pickle.dump(run[exp], open(exp + '.pckl', 'wb'))
    return


def import_pickle(project, list_experiments, add2dict=None):
    """ Import a list of experiments
    """
    if add2dict is not None:
        run = add2dict
    else:
        run = {}
    path = esxrun(project, list_experiments[0])
    print("**** Importation ****")
    os.chdir(path.path.outputpath + '/../')
    for exp in list_experiments:
        print(" => %s" %(exp))
        run[exp] = pickle.load(open(exp + '.pckl', 'rb'))
    return run
