from ..file_io.sdf_load import sdf_load
from ..sdf_object       import sdf_object
from ..sdf_data_sc      import sdf_data_sc
from ..sdf_par          import sdf_par

import os
import numpy as np

#=====================================================================
class sdf_force(object):
    """
    A class giving easy access to data of force curves.
    """

    def __init__(self, sdf_obj, debug=False):
        """
        Initialize this thing. 
        """

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Set attributes
        self._debug = debug

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # If the sdf_object is a path, load it. Otherwise, use as is.
        if isinstance(sdf_obj, str):
            self._path       = sdf_obj
            self._sdf_object = sdf_load(self._path)
        else:
            self._path       = None
            self._sdf_object = sdf_obj

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Get the global parameters and set them
        # First the instrument, then its parameters
        self._instr      = self._sdf_object.GetInstrument(0)
        self._instr_pars = self._instr.Get()[1]
        for par in self._instr_pars:
            
            name, unit, value = par.Get()

            # Check types:
            if value == "None":
                value = None
            elif name in ["spring_constant", "sensitivity"]:
                value = float(value)
            
            setattr(self, name, value)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Set up segment list.
        self.segment = []
        for _seg in self._sdf_object.Get():
            _sdf_force_segment = sdf_force_segment(_seg,
                                                   debug=self._debug,
                                                   parent=self)
            self.segment.append(_sdf_force_segment)

        self._num_segments = len(self.segment)

        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Get various parameters and numbers from this class
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def GetSegmentNumber(self):
        """
        Return the number of segments in a force curve.

        :returns: Number of segments, i.e. the length of the list *segment*
        :rtype: int
        """
        return self._num_segments


    def GetSegmentNames(self):
        """
        Return a list of names of the segments. Usually those names are *segment 0*, *segment 1*, etc.

        :returns: List of names of the segments as strings
        :rtype: list of str
        """

        names = [i.name.value for i in self._sdf_object.Get()]
        return names
            
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Save the SDF-file after some changes were made.
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def SaveAs(self, sname=None):
        """
        Save the SDF-object to a file, where the filename resp. path is given by *sname*. This function will ask for confirmation, if the path points to an already existing file.

        :param sname: Path to location where file should be saved.

        :type sname: str or None

        :returns: Nothing

        :rtype: None

        :raises TypeError: if type of *sname* is not str or None

        :raises ValueError: if no *sname* path was given, and the path in this class is set to ``None``. That usually happens if this instance was created using an ``sdf_object`` instead of a path to a file. Then, you must provide *sname*.
        """

        if (sname is None) and (self._path is None):

            msg = "Error in save_as: No path given and no path in " +\
                  "class. You must provide a save path."
            raise ValueError(msg)

        elif (sname is None):

            sname = self._path

        elif not isinstance(sname, str):

            msg = "Error in save_as: sname must be string."
            raise TypeError(msg)


        # Check if path exists
        if os.path.exists(sname):

            while True:
                
                print("Warning: Path already exists. Overwrite? [y,N] ")

                choice = input().lower()

                if choice in "Y y yes Yes".split() :

                    break

                elif ((choice in "N n no No".split()) or
                      (not choice)):

                    print("Aborting.")
                    return None

                else:

                    print("#!# Input not know. Answer with Y, y, yes, Yes"
                          " N, n, no or No.")
                    print()

        # Open file pointer, write stuff.
        fp = open(sname, "w")
        fp.write(self._sdf_object.AsXML())
        fp.flush()
        fp.close()

            
    def Save(self):
        """
        Save SDF file without changing its name. This function is a shortcut of :meth:`SaveAs` with argument ``None``. This function will ask if you really want to overwrite a file that already exists, so that nothing is overwritten by accident.

        :returns: Nothing
        :rtype: None
        """
        self.SaveAs(None)
    

#=====================================================================
class sdf_force_segment(object):
    """
    Class representing a segment within a force curve.
    """

    def __init__(self, sdf_segment, debug=False, parent=None):
        """
        Initialize this class with a sdf_force_segment, which is
        inherently a workspace. Provide a proper interface to 
        its standardized content.
        """

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Set parameters
        # @TODO: Check if sdf_segment is of proper type
        self._segment = sdf_segment
        self._debug   = debug
        self._parent  = parent

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # A dictionary mapping a name to the data_sc object
        self._data_sc_dict = {}
        for ds in self._segment.Get():
            name = self._SanitizeName(ds.name.value)
            self._data_sc_dict[name] = ds.Get()

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Construct a dictionary combining data line names
        # with corresponding getter functions
        self._getter_dict = {}
        for ds in self._segment.Get():
            name = self._SanitizeName(ds.name.value)
            self._getter_dict[name] = ds.Get().Get

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Construct an analogous dictionary mapping line names
        # to setters, if this is needed later.
        self._setter_dict = {}
        for ds in self._segment.Get():
            name = self._SanitizeName(ds.name.value)
            self._setter_dict[name] = ds.Get().Set

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # And the list of data lengths, for good measure.
        self._numvals_dict = {}
        for ds in self._segment.Get():
            numvals = ds.Get().numvals
            name = self._SanitizeName(ds.name.value)
            self._numvals_dict[name] = numvals

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Other parameters of a segment
        # First the instrument, then its parameters
        self._instr      = self._segment.GetInstrument(0)
        self._instr_pars = self._instr.Get()[1]
        self._par_dict   = {}
        
        for par in self._instr_pars:
            
            name, unit, value = par.Get()

            # Check for types:
            if value == "None":
                value = None
            elif name in ["duration", "x", "y"]:
                value = float(value)
            elif name in ["position_index"]:
                value = int(value)

            # Put into par dict
            self._par_dict[name] = value

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Calculate the velocity, if needed.
        if "velocity" not in self._par_dict:
            if self._debug:
                print("Velocity not found in this segment. "
                      "Calculating...")
            self._CalculateVelocity()

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Calculate tip sample separation, if not found yet
        if (("tipSample" not in self._par_dict) or
            ("measuredTipSample" not in self._par_dict)):

            if self._debug:
                print("tipSample separation not found here. "
                      "Calculating...")
            self._CalculateTipSampleSeparation()


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def _SanitizeName(self, name):
        """
        Make sure that there are not illegal characters in segment
        data line names, here mainly replacing hyphens with under-
        scores.
        """
        if "-" in name:
            name = name.replace("-", "_")

        return name


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def _CalculateVelocity(self):
        """
        Calculate the velocity of this segment using the duration
        parameter that should have been read and the difference
        between the first and last measured height value which should 
        be available through the height-dataline.

        @TODO: Check this conversion here carefully with someone
               who knows things.
        """

        delta_height = self.measuredHeight[0] - self.measuredHeight[-1]
        velocity     = delta_height / self.duration

        # Add to dict and parameter
        setattr(self, "velocity", velocity)


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def _CalculateTipSampleSeparation(self):
        """
        Calculate the tip sample separation from the measuredHeight
        and the vDeflection, expressed in meters, i.e. the distance.

        @TODO: Check this conversion here carefully with someone
               who knows things.
        """
        distance = self.vDeflection / self._parent.spring_constant
        
        measuredTipSample = self.measuredHeight + distance
        tipSample         = self.height + distance
        
        # create the new data line.
        setattr(self, "measuredTipSample", measuredTipSample)
        setattr(self, "tipSample", tipSample) 
        

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def ListData(self):
        """
        Return a list of all available data, i.e. the data lines and their names that are available, and also the names and vailability of parameters. If the value of a certain data line or parameter is ``None``, this function will report the parameter or data line as missing. Data line names listed here can be used to query scaling in :meth:`GetScaling`.

        :returns: Nothing, just a printout of information
        :rtype: None
        """
        print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("| DATA LINES:")
        print("|")
        for line in self._getter_dict:
            if self._getter_dict[line] is None:
                print("|%20s: Missing." % line)
            else:
                print("|%20s: Available. NumPoints: %d" %
                      (line, self._numvals_dict[line]))

        print("|")
        print("| PARAMETERS")
        print("|")
        for line in self._par_dict:
            if self._par_dict[line] is None:
                print("|%20s: Missing." % line)
            else:
                print("|%20s: Available." % line)
        print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def GetScaling(self, name):
        """
        Get the scaling and offset of some data line in this segment. Data is usually saved in a linearly scaled way, i.e. the data has to be multiplied by the *multiplier* and the *offset* added to obtain the actual data. This is done to save space on disk, e.g. when data is saved as integers and then converted to floating point numbers using the multiplier and offset. 

        Data, especially when saved in hex format, is sometimes given as an array of integers, that are converted to actual data by first multiplying with the multiplier and then adding the offset. If this function returns ``None`` for the *multiplier*, 1.0 is implicitly used. If it returns ``None`` for the *offset*, 0.0 is implicitly used.

        :param str name: Name of the data line. Can be one of the entries shown by :meth:`ListData`. 

        :returns: Tuple of two floats, namely *multiplier* and *offset*
        :rtype: tuple of floats
        """

        if name not in self._data_sc_dict:
            msg = "Error in SDF_force_segment: Trying to access " +\
                  "nonexisting data line '%s'" % name
            raise ValueError(msg)
        
        else:
            return self._data_sc_dict[name].GetScaling()
        

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __getattr__(self, name):
        """
        Overriding the getattr method of this class. Whenever an
        attribute of this class is requested, this method is called.
        We check if the requested attribute exists, i.e. is provided
        by the .force.sdf file, and call its getter if it is.

        Otherwise, throw an error or display a warning, I'm not yet
        sure what's better.
        """

        if self._debug:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Attempting to get parameter %s" % name)

        if name in self._getter_dict:
            if self._debug:
                print("Found it. Returning values...")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            return self._getter_dict[name]()[0]

        elif name in self._par_dict:
            if self._debug:
                print("Found it in pars. Returning values...")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            return self._par_dict[name]
        
        else:
            msg = "Attribute not found in segment."
            raise NameError(msg)

        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __setattr__(self, name, value):
        """
        Is called whenever someone tries to set an attribute of this
        class, like s.test = 30, where s is an instance of this class.
        
        Where appropriate, calls to the proper setters are made.
        This function also checks, if the data is valid in terms of
        length. New data, which is of different shape than data
        already saved in there are rejected.
        """

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # CASE 1
        #
        # The parameter starts with an underscore, thus being an
        # internal parameter, set it as usual.
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if name.startswith("_"):
            super().__setattr__(name, value)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # CASE 2
        #
        # It's in the setter dict, i.e. its one of the data lines.
        # The user tries to overwrite the data already present in the
        # data lines. Redirect to appropriate setters
        #
        # It must be of equal length as the data line before, other-
        # wise setting will be rejected.
        #
        # @TODO: We will not check the length of the new data here,
        #        which should be done at some point! For example
        #        in the setter itself.
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        elif name in self._setter_dict:

            if len(value) != self._numvals_dict[name]:
                msg = "Error in SDF_force_segment.__setattr__: " +\
                      "New data length %d does not match " % len(value) +\
                      "previous data length of %d" % self._numvals_dict[name]
                raise ValueError(msg)

            else:
                self._setter_dict[name](value)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # CASE 3
        #
        # Its in the parameter dict for this class. I.e. we have to
        # assume that the user wants to change a parameter. Let's
        # make this happen...
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        elif name in self._par_dict:

            # Set to new value in _par_dict:
            self._par_dict[name] = value

            # Set within sdf-class-structure
            # @TODO: We are not dealing with maybe existing units
            # here!
            for par in self._instr_pars:

                n, u, v =  par.Get()
                if name == n:
                    par.value = value
                
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # CASE 4
        #
        # It's not a name already known as a data line, but its also
        # not a string or a single value. Thus, we assume that we are
        # dealing with a new data line the user wants to add.
        #
        # We convert it to a sdf_data_sc object and add to the parent
        # sdf file.
        #
        # We will warn the user about what is going to happen, just
        # to be sure they know what they did. They may then check if
        # it was their intention to do this.
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        elif isinstance(value, np.ndarray) or isinstance(value, list):

            # TODO: Maybe add a confirmation dialog?
            # TODO: It might me important, that all data
            #       in a segment are of equal length. But
            #       I don't know right now if this always
            #       holds -> Ask Ingo
            
            # Create empty DS object and populate
            new_obj  = sdf_object("ds")
            new_obj.SetName(name)
                
            new_data = sdf_data_sc(value,
                                   dtype='hex',
                                   multiplier=None,
                                   offset=None)

            new_obj.SetData(new_data)

            # Add to segment in SDF
            self._segment.AppendObject(new_obj)
            
            # Add to internals of this class
            self._setter_dict[name]  = new_data.Set
            self._getter_dict[name]  = new_data.Get
            self._numvals_dict[name] = new_data.numvals
            self._data_sc_dict[name] = new_data

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # CASE 5:
        #
        # Something else, thus a string or a single value. Maybe some-
        # thing else (@TODO: Catch weird values like dicts?)
        #
        # We will assume the user wants to set a single parameter in
        # this class. Add it as an sdf_par and append to parent sdf.
        #
        # Also, then add it to the self._par_dict
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        else:
            
            par = sdf_par(name=name,
                          val=value,
                          unit=None,
                          parent_par=None)

            self._instr.AppendPar(par)
            self._par_dict[name] = value
