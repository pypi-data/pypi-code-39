"""
Objects necessary to build ESX simulations and lauch them with python3

A. Enguehard - 07/2019
"""

import os
import subprocess
import numpy as np
from pyesx import utils as esxutils
from pyesx.path import esxpath, esxprojectpath, esxexppath


class esxveg():
    """Definition of a vegetation object used in ESX simulations
    """

    def __init__(self, project=None, filename=None):
        """
        """
        self.filename = filename
        self.project = project

        self.path = esxpath()
        if project is not None:
            self.path = esxprojectpath(project)
        if filename is not None and project is not None:
            try:
                os.chdir(self.path.datapath)
                self._readfile(filename)
            except FileNotFoundError:
                print('No file found in %s' %(self.path.datapath))
        return

    def _add_attribute(self, name, value):
        setattr(self, name, value)
        return

    def _change_attribute(self, name, value):
        setattr(self, name, value)
        return

    def _readfile(self, filename):
        """ Create a vegetation object from information given in a file

        Parameters:
        ----------
        * filename : (str)
            Name of the file to use to get the vegetation parameters

        Format:
        ------
        attribute, value
        """
        file = np.genfromtxt(filename, delimiter=',', dtype='<U20',
                             comments='!', skip_header=3)
        names = file[:, 0]
        values = file[:, 1]
        print('   - Start import from ' + filename)
        for i in range(len(names)):
            name = names[i]
            try:
                value = int(values[i])
            except ValueError:
                try:
                    value = float(values[i])
                except ValueError:
                    value = values[i].strip()
            self._add_attribute(name, value)
        return

    def _write_VegUsed(self, file):
        """Write the line for 'VegUsed' in a file (standardized)

        Parameters:
        ----------
        * file : (file)
            Opened file in which to add the line
        """
        ll = ['code', 'lai_method', 'profile', 'gsto_method',
              'fphen_method']
        # Check if all the attributes do exist already and continues if True
        if esxutils.checkattributes(self, ll):
            line = esxutils.compute_line(self, ll)
            file.write(line)
        return

    def _write_VegTypes(self, file):
        """Write the line for 'VegTypes' in a file (standardized)

        Parameters:
        ----------
        * file : (file)
            Opened file in which to add the line
        """
        ll = ['code', 'name', 'type', 'LPJtype', 'is_forest', 'is_veg',
              'is_crops', 'is_water', 'is_ice', 'comments']
        # Check if all the attributes do exist already and continues if True
        if esxutils.checkattributes(self, ll):
            line = esxutils.compute_line(self, ll)
            file.write(line)
        return

    def _write_VegDefTab(self, file):
        """Write the line for 'VegTypes' in a file (standardized)

        Parameters:
        ----------
        * file : (file)
            Opened file in which to add the line
        """
        ll = ['code', 'hveg', 'alb', 'd/h', 'z0/h', 'z0Gr', 'LAI', 'SAI',
              'nsides', 'Lw', 'SGS', 'EGS', 'Ga_s', 'Ga_v', 'BioD', 'SLW',
              'Eiso', 'Emtl', 'Emtp', 'Eno']
        # Check if all the attributes do exist already and continues if True
        if esxutils.checkattributes(self, ll):
            line = esxutils.compute_line(self, ll)
            file.write(line)
        return

    def _write_VegDefPhenol(self, file):
        """Write the line for 'VegTypes' in a file (standardized)

        Parameters:
        ----------
        * file : (file)
            Opened file in which to add the line
        """
        ll = ['code', 'SGS50', 'DSGS', 'EGS50', 'DEGS', 'LAImin', 'LAImax',
              'SLAIlen', 'ELAIlen']
        # Check if all the attributes do exist already and continues if True
        if esxutils.checkattributes(self, ll):
            line = esxutils.compute_line(self, ll)
            file.write(line)
        return

    def _write_emepdo3seDefs(self, file):
        """Write the line for 'emepdo3seDefs' in a file (standardized)

        Parameters:
        ----------
        * file : (file)
            Opened file in which to add the line
        """
        ll = ['code', 'gmax', 'fmin', 'f_phen_a', 'f_phen_b',
              'f_phen_c', 'f_phen_d', 'f_phen_e', 'f_phen_f', 'Astart', 'Aend',
              'f_light', 'f_temp_min', 'f_temp_opt', 'f_temp_max', 'RgsS',
              'RgsO', 'f_VDP_max', 'f_VDP_min', 'VPD', 'f_SWP_max', 'f_SWP_PWP',
              'rootd', 'do3seLw']
        # Check if all the attributes do exist already and continues if True
        if esxutils.checkattributes(self, ll):
            line = esxutils.compute_line(self, ll)
            file.write(line)
        return


class esxesx():
    """
    """

    def __init__(self, project=None):
        self.project = project

        self.path = esxpath()
        if project is not None:
            self.path = esxprojectpath(project)
        return

    def _readfile(self, filename, type='esx', in_data=False):
        """Read in the datafile
        """
        if in_data:
            os.chdir(self.path.datapath)
        print('   - Start import from ' + filename + '  - type is:' + type)
        file = np.genfromtxt(filename, delimiter=':', dtype='<U200',
                             comments='!', skip_header=3)
        # Get the future attributes and values to write
        names = list(file[:, 0])
        lists_of_values = file[:, 1]  # str
        i = -1  # Line counter
        for list_of_values in lists_of_values:
            i = i + 1
            # Turn the lists of values to a proper list
            list_of_values = list_of_values.split(',')
            # Get the right format in the list
            for j in range(len(list_of_values)):
                list_of_values[j] = list_of_values[j].strip()
                # Determine if there are number and int or float
                try:
                    list_of_values[j] = int(list_of_values[j])
                except ValueError:
                    try:
                        list_of_values[j] = float(list_of_values[j])
                    except ValueError:
                        pass
            names[i] = names[i].strip()
            self._add_attribute_esx(names[i], list_of_values)
        if type == 'esx':
            self.driverlist = list(dict.fromkeys(names))  # Removing duplicates
        if type == 'debug':
            self.debuglist = list(dict.fromkeys(names))
        if type == 'chem':
            self.chemlist = list(dict.fromkeys(names))
        return

    def _add_attribute_esx(self, name, list_values):
        """Add an attribute compatible with the format

        Parameters:
        ----------
        * name : (str)
            Name of the attribute to esx to add
        * list_values : (1D numpy array or list)
            The values to append to the attribute list as an element
        """
        val = np.array([list_values])  # 2D np.array
        if not hasattr(self, name):
            setattr(self, name, val)
        else:
            ancient_val = getattr(self, name)  # 2D np.array
            val = np.concatenate((ancient_val, val), axis=0)
            setattr(self, name, val)
        return

    def _change_attribute(self, name, array2D):
        """Replace the attributes by the given 2Darray
        """
        setattr(self, name, array2D)
        return

    def _write_esxfile(self, filename):
        """

        ex: 'testfile_esx.nml'
        """
        file = open(filename, 'a')
        # --- Driving parameters ---
        file.write('&esxDriver_config\n')
        for name in self.driverlist:
            file.write('esx%' + name + ' = ')
            array2D = getattr(self, name)
            for element in array2D:
                # Compute the line
                line = esxutils.compute_line_list(element, name=name)
                # hard coded exception:
                # Write it
                file.write(line)
        file.write('\n')  # Skip a line to let it readable
        # --- debug parameters ---
        for name in self.debuglist:
            file.write('debug%' + name + ' = ')
            array2D = getattr(self, name)
            for element in array2D:
                # Compute the line
                line = esxutils.compute_line_list(element)
                # Write it
                file.write(line)
        file.write('\n/\n')  # Skip a line to let it readable
        # --- Chemical boundary conditions ---
        file.write('&chem_config\n')
        for name in self.chemlist:
            file.write(name + ' = ')
            array2D = getattr(self, name)
            for element in array2D:
                # Compute the line
                line = esxutils.compute_line_list(element)
                # Write it
                file.write(line)
            file.write('\n')  # Skip a line to let it readable
        file.write('\n/\n')
        file.close()
        return


class esxlocal():
    """
    """

    def __init__(self, project=None, filename=None):
        self.filename = filename
        self.project = project

        self.path = esxpath()
        if project is not None:
            self.path = esxprojectpath(project)
        if filename is not None and project is not None:
            try:
                os.chdir(self.path.datapath)
                self._readfile(filename)
            except FileNotFoundError:
                print('No file found in %s' %(self.path.datapath))
        return

    def _add_attribute(self, name, value):
        setattr(self, name, value)
        return

    def _readfile(self, filename,  in_data=False):
        """
        """
        if in_data:
            os.chdir(self.path.datapath)
        print('   - Start import from ' + filename)
        file = np.genfromtxt(filename, delimiter=':', dtype='<U20',
                             comments='!', skip_header=3)
        # Get the future attributes and values to write
        names = file[:, 0]
        values = file[:, 1]  # str
        for i in range(len(names)):
            name = names[i]
            try:
                value = int(values[i])
            except ValueError:
                try:
                    value = float(values[i])
                except ValueError:
                    value = values[i].strip()
            self._add_attribute(name, value)
        self.namelist = names
        return

    def _write_locfile(self, filename):
        """
        """
        file = open(filename, 'a')
        file.write('&esxLocal_config\n')
        for name in self.namelist:
            val = getattr(self, name)
            file.write('Loc%' + name + ' = ' + str(val) + '\n')
        file.write('\n/\n')
        file.close()
        return


class esxsimu():
    """
    """

    def __init__(self, esx, veg_list, local, name, project, experiment, datafile=None):
        self.esx = esx
        self.veg_list = veg_list
        self.local = local
        self.name = name
        self.project = project
        self.experiment = experiment

        if datafile is not None:
            self.datafile = datafile
        else:
            self.datafile = None

        self.path = esxexppath(project, experiment)
        print('*** Initialization of simulation ' + self.name + ' ***')
        return

    def _write_runfile(self):
        """Create the run file needed to launch based on the ex in scripts
        """
        print(' * Write RUN.sh')
        # Open the example file in scripts directory
        os.chdir(self.path.scriptpath)
        with open('RUN_ex.sh', 'r') as file:
            runf = file.read()
        # Replace the lines by the matching ones
        runf = runf.replace('ESXFILE', self.esxfile)
        runf = runf.replace('VEGFILE', self.vegfile)
        runf = runf.replace('LOCFILE', self.locfile)
        runf = runf.replace('RUNNAME', self.name)
        if self.datafile is not None:
            runf = runf.replace('DATAFILE', self.datafile)
        # Check the files / directories
        self._setup_dirs()
        # Write the RUN file in the right directory
        os.chdir(self.path.experimentpath)
        with open('RUN.sh', 'w') as file:
            file.write(runf)
        return

    def _setup_dirs(self):
        """
        """
        if not os.path.exists(self.path.projectpath):
            os.makedirs(self.path.projectpath)
            os.makedirs(self.path.projectpath + '/experiments')
            os.makedirs(self.path.projectpath + '/data')
            os.makedirs(self.path.projectpath + '/output')
        if not os.path.exists(self.path.experimentpath):
            os.makedirs(self.path.experimentpath)
        return

    def _setup_simu(self, name=None, remove=True):
        """Create a simulation from scratch
        """
        # Create the directories if do not exist
        self._setup_dirs()
        # Write the files in the directory
        # Write .nml
        os.chdir(self.path.experimentpath)
        self._write_all(name=name, remove=remove)
        # Write the run file launching this simulation only
        self._write_runfile()
        return

    def _write_all(self, name=None, remove=False):
        """
        """
        if name is None:
            name = self.name
        if remove:
            try:
                os.remove(name + '_Veg.nml')
                os.remove(name + '_esx.nml')
                os.remove(name + '_Local.nml')
            except FileNotFoundError:
                print('No file to remove...')
        self._write_VegFile(name + '_Veg.nml')
        print(' * Write ' + name + '_Veg.nml')
        self._write_EsxFile(name + '_esx.nml')
        print(' * Write ' + name + '_esx.nml')
        self._write_LocFile(name + '_Local.nml')
        print(' * Write ' + name + '_Local.nml')
        return

    def _write_VegFile(self, filename):
        """Write a file describing a canopy used for an ESX simulation

        Parameters:
        ----------
        * filename : (str)
            Name of the file to write (ex: Test_Veg.nml)
            Should end by '.nml'
        """
        file = open(filename, 'a')
        # Write all the statements needed
        file.write('&esxVeg_config\n')
        file.write('VegUsed = \n')
        for veg in self.veg_list:
            veg._write_VegUsed(file)
        file.write('VegDefTypes = \n')
        for veg in self.veg_list:
            veg._write_VegTypes(file)
        file.write('VegDefTab = \n')
        for veg in self.veg_list:
            veg._write_VegDefTab(file)
        file.write('VegDefPhenol = \n')
        for veg in self.veg_list:
            veg._write_VegDefPhenol(file)
        file.write('emepdo3seDefs = \n')
        for veg in self.veg_list:
            veg._write_emepdo3seDefs(file)
        file.write('\n/\n')
        file.close()
        self.vegfile = filename
        return

    def _write_EsxFile(self, filename):
        """
        """
        self.esx._write_esxfile(filename)
        self.esxfile = filename
        return

    def _write_LocFile(self, filename):
        """
        """
        self.local._write_locfile(filename)
        self.locfile = filename
        return

    def _run_esx(self, make=False):
        """Launch an esx simulation according to the RUN.sh file in experiment
        """
        if make is True:
            make = 'T'
        else:
            make = 'F'
        # go to the run directory
        os.chdir(self.runpath)
        subprocess.call(['./RUNNER.sh', self.project, self.experiment,
                         make])
        return
