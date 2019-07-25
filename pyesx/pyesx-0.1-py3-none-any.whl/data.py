"""
Package to import and format data extern from ESX

It creates a esxdata object storing all the information and that can be
manipulated
"""

import pandas as pd
import os
from pyesx import utils as esxutils
from pyesx.path import esxprojectpath
import numpy as np
import collections
from copy import deepcopy
import pickle

# -----------------------------------------------------------------------------


class esxdata():
    """esxdata object storing informations from external data

    Parameters:
    ----------
    * project : (str)
        name of the project you work onto (for path setup)

    How to:
    -------
    * Format my dataset - Please refer to the document ....
    """

    def __init__(self, project, id='data', datename='date'):
        """Initialize the esxdata object

        Attributes:
        -----------
        * datename : (str) : name for the date (index) column
        * project : (str) : name of the project to find data in files
        * id : (str) : identification for comparisons
        * scriptpath : (str) : path to scripts directory
        * datapath : (str) : path to data in the project directory
        * imported : (list of str) : list pf files used as dataset
        * data : (Pandas DataFrame) : data stored
        """
        self.datename = datename  # String to identify the date column (index)
        self.project = project    # project in which to get the data
        self.id = id              # identification name of the dataset
        self.path = esxprojectpath(project)
        self.imported = []  # List of th imported files in the structure

        # Creates an empty frame to fill
        self.data = pd.DataFrame({self.datename: []}).set_index(self.datename)
        self.datetime = pd.Series([])
        return

    #             Add data to the structure
    # ===================================================

    def _addfile_csv(self, filename, skipline=0, datename=None, format='%d/%m/%Y %H:%M'):
        """Add a csv file into the structure according to the DateTime column

        Parameters:
        ----------
        filename: (str)
            name of the file
        skipline: (int)
            default = 0
            lines to skip before reaching the header (ex: =1 if comments above)
        datename: (str)
            Suggest another name for the date column than the general one
        format : (str)
            Format of the date column to convert to datetime object
        """
        first = len(list(self.data.index)) == 0  # first import

        # Get from the right directory
        os.chdir(self.path.datapath)

        print('    => Try to import %s' %filename)
        # Open and read the csv file
        tmp = pd.read_csv(filename, skiprows=skipline)
        print(tmp.dtypes)
        # Rename the column with the name of the date to a common one(self one)
        # This is needed to merge with the rest of the dataframe
        if datename is not None:
            tmp = tmp.rename(columns={datename: self.datename})
        datename = self.datename
        print('Date name : ' + datename)
        print(tmp[datename][0])

        # Convert string dates into dates
        tmp[datename] = pd.to_datetime(tmp[datename], format=format)
        # Indexing according to the date column
        tmp = tmp.set_index(datename)
        print('Index set up')

        if not first:
            # Merging with the already existing DataFrame
            self.data = pd.merge(self.data, tmp, how='outer',
                                 left_index=True, right_index=True, sort=True,
                                 suffixes=('', '_' + filename))
        else:
            self.data = tmp

        # Add to the list pf imported files
        self.imported.append(filename)
        self._check_index()
        return

    def _addfile_csv_list(self, list):
        """ Updates according to a list of files the variable

        Parameters:
        ----------
        * list : (list of str)
            ex: ['File1.csv', 'File2.csv']
        """
        for file in list:
            self._addfile_csv(file)
        return

    def _addfile_csv_prefix(self, prefix):
        """Import all the files with a given prefix

        Parameters:
        ----------
        * prefix : (str)
            Identification string of files to import and merge
        """

        def _make_list(self, prefix):
            """Lists the files with a given prefix
            """
            print('** List the files associated with %s' %prefix)
            index = len(prefix)
            # Lists the csv files with a given prefix availables
            listfiles = [f for f in os.listdir(self.path.datapath) if
                         os.path.isfile(os.path.join(self.path.datapath, f))
                         and f[-3:] == 'csv' and f[:index] == prefix]
            for f in listfiles:
                print('    - ' + f)
            return listfiles

        print('** Start to import **')
        list = self._make_list(prefix)
        self._addfile_csv_list(list)
        self.data = self.data.set_index(self.datename)
        print('** End to import **')
        # AETMP: Debug needed to avoid duplication during merging
        self.data = self._remove_duplicates()
        return

    def _addesxdata(self, data, id=None):
        """Merge the data with another esxdata variable
        """
        # Get the same index name befor merging
        data.data.index.name = self.data.index.name

        # Merging the dataframes
        self.data = pd.merge(self.data, data.data, how='outer',
                             left_index=True, right_index=True,
                             sort=True, suffixes=('', '_' + data.id))
        # Update metadata
        if id is not None:
            self.id = id
        self.imported = self.imported + data.imported
        self._check_index()
        return

    #       Sort the structure and add information
    # ===================================================

    def _filter_time(self, date0, date1):
        """
        """
        data = deepcopy(self)
        data.data = esxutils.filterframe(self.data, date0, date1)
        data.datetime = esxutils.filterseries(self.datetime, date0, date1)
        #AE: Need more work ! To complet
        return data

    def _check_index(self, first=False):
        """ Updatethe datetime index of the data
        """

        def set_datetime(self):
            self.datetime = pd.Series(self.data.index, index=self.data.index)
            return

        if not len(self.datetime) == len(self.data.index):
            set_datetime(self)
        return

    def _sort_header(self):
        """Sort the header according to the architecture:
        date/num_var/str_var
        aphabetic order
        height order

        Add information to the structure

        """

        # Separate the different types of data
        int_float = self.data.select_dtypes(['float64', 'int64'])
        datecol = self.data.select_dtypes('datetime64[ns]')
        string = self.data.select_dtypes('object')

        def list_names(header):
            """List the variables from a header
            """
            list_keys = []
            # iterate over the whole header to get the names
            for i in range(len(header)):
                name, height = esxutils.get_name_height(header[i])
                list_keys.append(name)
            list_keys = collections.Counter(list_keys).keys()
            return list(list_keys)

        def reindexing(frame):
            """Apply the two filters to re-index the frames
            """
            print('** Re-indexing**')
            # frame.set_index(list(frame.columns)[0], inplace = True)
            new_frame = frame.reindex(columns=sorted(frame.columns))
            # Organize each variable in height order from the bottom to top
            new_frame = new_frame.reindex(columns=pd.Index(
                           esxutils.quick_sort(list(new_frame.columns))))
            return new_frame

        def dict_heights(header, list_keys):
            """Use the header to list the heights associated with each variable
            """
            dict_heights = {}
            # Dictionnary initialization
            for key in list_keys:
                dict_heights[key] = []
            # Get name and height of each element
            for elmt in header:
                key, height = esxutils.get_name_height(elmt)
                dict_heights[key].append(height)
            return dict_heights

        # Counting the numbers
        self.Ncol = len(list(self.data.columns))
        list_tot = list_names(self.data.columns)
        self.list_keys = list_tot
        self.Nvar = len(self.list_keys)
        list_num = list_names(int_float.columns)
        self.Ncolnum = len(list(int_float.columns))
        self.Nvarnum = len(list_num)
        list_str = list_names(string.columns)
        self.Ncolstr = len(list(string.columns))
        self.Nvarstr = len(list_str)

        # Sort in alphabetic order each frame
        int_float = reindexing(int_float)
        string = reindexing(string)
        print('** After REINDEXING **')

        # Merge the tables
        self.data = datecol.join(int_float.join(string, how='inner'),
                                 how='inner')
        # AETMP: Debug needed to avoid duplication during merging
        self.data = self._remove_duplicates()
        print(list(self.data.columns))

        self.dict_heights = dict_heights(self.data.columns, self.list_keys)
        return

    def _remove_height(self):
        """Remove the height set in the header
        """
        i = -1
        head = list(self.data.columns)
        for item in head:
            i = i + 1
            head[i] = item[:esxutils.is_in(':', item)[1]]
        self.data.columns = head
        return

    def _set_height(self, height, overwrite=False):
        """Add a height to the header readable by ESX (in m)

        By default it does not overwrite if a height is already written
        """

        def already_height(item):  # Test if there is already a height set
            return esxutils.is_in(':', item)[0] and item[-1] == 'm'

        i = -1
        head = list(self.data.columns)
        for item in head:  # Iterate over the header
            i = i + 1
            if not already_height(item):
                head[i] = item + ':' + str(height) + 'm'
            elif overwrite:
                head[i] = item + ':' + str(height) + 'm'
        self.data.columns = head
        return

    def _set_suffixe(self, suffix):
        """Add a suffix to each element of the header
        """
        i = -1
        head = list(self.data.columns)
        for item in head:  # Iterate over the header
            i = i + 1
            head[i] = item + '_' + suffix
        self.data.columns = head
        return

    def _write_file(self, filename):
        """Write a csv file according to the dataframe we have
        """
        os.chdir(self.path.datapath)
        # Open the File
        if filename[-3:] != 'csv':
            filename.append('.csv')
        f = open(filename, 'a')  # Open in Appending mode
        # Write the first line with the ESX needed numbers (+1 as date is index)
        line = str(self.Ncol + 1) + ', ' \
            + str(self.Nvar + 1) + ', ' + str(self.Ncolnum) + '\n'
        f.write(line)
        # Add the dataFrame
        self.data.to_csv(f)
        f.close
        return

    #                   Utilities
    # ===================================================

    def _remove_duplicates(self):
        """ remove the duplicated dates from previous computations
        AE: Should be debugged then
        """
        dates = list(self.data.index)
        rm_dates = []
        for i in range(1, len(dates)):
            if dates[i] == dates[i-1]:
                rm_dates.append(dates[i])
        return self.data.drop(rm_dates, axis=0)

    def _interpolate_z(self, spcs, h):
        """Give the value at z from a linear interpolation between two
        values measured of a variable.
        If h > z(highest measurement):
            value = value_at_z(highest measurement)
            (IDEM for lowest measurement)

        Parameters:
        ----------
        * spcs (str)
        * h (float)

        Outputs:
        -------
        values (1D pandas dataframe, index = time)
        """
        # Get heights for interpolation
        try:
            ih_sup = esxutils.is_higher(h, self.dict_heights[spcs])
            h_sup = self.dict_heights[spcs][ih_sup]
            h_inf = self.dict_heights[spcs][ih_sup-1]

            factor = (h - h_inf) / (h_sup - h_inf)
            list_sup = self.data[spcs + ':' + str(int(h_sup)) + 'm']
            list_inf = self.data[spcs + ':' + str(int(h_inf)) + 'm']

            value_z = list_inf + factor * (list_sup - list_inf)

        except:  # h > z(highest level)
            if h >= self.dict_heights[spcs][-1]:
                h_sup = self.dict_heights[spcs][-1]
                value_z = self.data[spcs + ':' + str(int(h_sup)) + 'm']
            elif h <= self.dict_heights[spcs][0]:
                h_inf = self.dict_heights[spcs][0]
                value_z = self.data[spcs + ':' + str(int(h_inf)) + 'm']

        return value_z

    def _get_spcs(self, spcs, mindate=None, maxdate=None):
        """Import as a DataFrame all the variables associated with spcs
        Usually profiles of chemicals or meteorological variables for example

        Parameters:
        ----------
        * spcs : (str)
            N ame of the variable to get from the bigger dataframe
        * mindate : (datetime object)
            Lower boundary for the dataframe
        * maxdate : (datetime object)
            Upper boundary for the imported datframe
        """
        list_import = []
        # Import the DataSet
        for h in self.dict_heights[spcs]:
            list_import.append(self.data[spcs + ':' + str(int(h)) + 'm'])

        # Create a DataFrame
        frame = pd.DataFrame(list_import).transpose()
        frame.columns = [int(h) for h in self.dict_heights[spcs]]

        # Filter the dataframe:*
        frame = esxutils.filterframe(frame, mindate, maxdate)
        # if mindate is not None:
        #     idatemin = esxutils.is_in(mindate, frame.index)[1]
        #     if idatemin == -1:
        #         idatemin = 0
        # else:
        #     idatemin = 0
        # if maxdate is not None:
        #     idatemax = esxutils.is_in(maxdate, frame.index)[1]
        #     if idatemax == -1:
        #         idatemax = len(frame.index) - 1
        # else:
        #     idatemax = len(frame.index) - 1
        # frame = frame.iloc[idatemin:idatemax, :]

        # Metadata print out
        print(' ===== Get species : ' + spcs + ' from the data file =====')
        print('Date start measurements imported : '
              + frame.index[0].strftime('%d-%m-%Y %H:%M:%S'))
        print('Date end measurements imported : '
              + frame.index[-1].strftime('%d-%m-%Y %H:%M:%S'))
        print('Heights: ' + ' '.join(map(str, frame.columns)))

        return frame

    #                   Others
    # ===================================================

    def _plot_meanprofile_box_at_t(self, spcs, t, ax, date0=None, date1=None):
        """ Plot with boxes the measurements  associated with a given hour

        Parameters:
        ----------
        * spcs : (str)
            variable to plot using all the availble heights
        * t : (int)
            Hour of the day (ex: 12 for noon)
        * ax : (plt.Axes)
            Axe to which linking the plot (for comparisons)

        Outputs:
        -------
        Add on ax the box plot of the measurements
        """
        m = self._get_spcs(spcs, date0, date1)
        grp = esxutils.hourlygroup(m, t)
        pos = [float(m.columns[i]) for i in range(len(m.columns))]
        return grp.plot(kind='box', positions=pos, label='Measurements',
                        showmeans=True, ax=ax)

    def _AE_perso_treat(self, name):
        """Additional treatment only for me (AE:03/2019)
        """
        self.data = self.data.replace(-999, np.NaN)
        self.data = self.data.dropna(how='all')  # Limits duplicates and compu
        copied = self.data
        pickle.dump(self.data, open(name + '_withoutInterp.pckl', 'wb'))
        self.data = self.data.interpolate('linear')  # Fill the missing values
        self.data = self.data.dropna(how='any')  # remove the first rows
        # No NO ground flux negative : replace negative vlaues by zeros
        self.data['FNO:0m'][self.data['FNO:0m'] < 0] = 0
        return copied


# -----------------------------------------------------------------------------

def add_height_infile(filename, height, skipline=0, datename='date'):
    """Add an ESX friendly height format to all the variables of the header
    from a csv file

    Rows can be skipped by using 'skipline = 1, 2, ...'
    """
    # open the file
    tmp = pd.read_csv(filename, skiprows=skipline)
    header = list(tmp.columns)
    string = ':' + str(height) + 'm'
    # replace / Add the height behind the name of the variable
    new_header = [esxutils.get_name_height(s)[0] + string for s in header]
    # Change the names in the header but not the date which is the first co
    for i in range(1, len(header)):
        tmp = tmp.rename(columns={header[i]: new_header[i]})
    tmp = tmp.set_index(datename)
    # Remove the old file
    os.remove(filename)
    # Write the new file
    tmp.to_csv(filename)
    return

# Additional commands to use
# --------------------------
# test.data = test.data.dropna(how='all')
# test.data = test.data.replace(-999, np.NaN)

# Classic Arthur's code lines
# from ESX_PreProcess import *
# run = esxdata('Bosco', datename='date')
# run._addfile_csv_prefix('Imp')
# run._sort_header()
# run._AE_perso_treat()
