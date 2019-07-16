"""
-------------------------------------------------------------------------
Project: SDF: Standard Data Format

Module: sdf_object.py

Class sdf_object: This is the highest class in the SDF project. It 
                  contains either a dataset or a workspace.
 
bg 11.09.2015 : Completely remodeled class hierarchy

-------------------------------------------------------------------------
    Copyright (C) 2010-2019 Burkhard Geil, Ilyas Kuhlemann, Filip Savic

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from . import sdf_rc
from .sdf_gen_val import sdf_gen_val
from .sdf_name import sdf_name
from .sdf_date import sdf_date
from .sdf_owner import sdf_owner
from .sdf_comment import sdf_comment
from .sdf_sample import sdf_sample
from .sdf_instrument import sdf_instrument
from .sdf_par import sdf_par
from .sdf_data import sdf_data
from .sdf_data_sc import sdf_data_sc
from .sdf_data_img import sdf_data_img
from .sdf_data_mc import sdf_data_mc


class sdf_object(sdf_gen_val):
    """
    This class contains either an SDF workspace or a single SDF
    dataset.

    This decision is made by the type of the sdf_object.value:

    o if value is an instance of sdf_data then the sdf_object 
      is a dataset.
    o if value is a Python list(*) then the sdf_object is a workspace
      and the list can contain multiple sdf_datasets or a mixture
      of datasets and workspaces (the latter as instances of sdf_objects).

    (*) It is NOT allowed that the object contains an instance of an
        sdf_object. Embedded workspaces MUST be enclosed in a Python list! 
        
    """
    def __init__(self, src='ws'):
        """ 
        Create an empty sdf_object. 
        """
        if src == 'workspace' or src == 'ws':
            val = []
        elif src == 'dataset' or src == 'ds':
            val = sdf_data()
        else:
            val = None

        super(sdf_object, self).__init__(val)

        self.ID = 'sdf-object'
        self.name = sdf_name()
        self.date = sdf_date()
        self.owner = sdf_owner()
        self.comment = sdf_comment()

        self.par = []           # becomes a list of sdf_par
        self.instrument = []    # becomes a list of sdf_instrument
        self.sample = []        # becomes a list of sdf_sample
        self.parent = None        
        self.debug = False

    def __str__(self):
        """
        Printable contents of the object. Used by: 'print ds'
        (For debugging purpose mainly).
        """
        res = '=' * 80 + '\n' 
        if self.IsWorkspace():
            res = res + 'WORKSPACE '
            res = res + str(self.name) 
        elif self.IsDataset():
            res = res + 'DATASET '
            res = res + str(self.name) 
            res = res + '        TYPE = ' + str(self.value.datatype) + '\n' 
        else:
            raise RuntimeError("Object is neither DATASET nor WORKSPACE")
        # now parse recursively into its contents:
        if not self.owner.IsEmpty():
            res = res + str(self.owner)
        if not self.date.IsEmpty():
            res = res + str(self.date)
        if not self.comment.IsEmpty():
            res = res + str(self.comment)
        for sample in self.sample:
            res = res + str(sample)
        for instrument in self.instrument:
            res = res + str(instrument)
        for par in self.par:
            res = res + 'PARAMETER ' + str(par) + '\n'

        res = res + str(self.value) 
        res = res + '=' * 80
        return res

    def Set(self, val):
        """
        Set values of an sdf_object. 
        """
        # pass
        raise NotImplementedError("sdf_object.Set not implemented yet.")

    def SetName(self, name, encoding=None):
        if encoding:
            self.name.Set(name, encoding)
        else:
            self.name.Set(name)

    def SetDate(self, datestr, dateformat=None):
        if dateformat:
            self.date.Set(datestr, dateformat)
        else:
            self.date.Set(datestr)
            
    def SetOwner(self, owner, encoding=None):
        if encoding:
            self.owner.Set(owner, encoding)
        else:
            self.owner.Set(owner)

    def SetComment(self, comment, encoding=None):
        if encoding:
            self.comment.Set(comment, encoding)
        else:
            self.comment.Set(comment)

    def SetData(self, data):

        if not isinstance(data, sdf_data):
            msg = "data must be an instance of the sdf_data class"
            raise RuntimeError(msg)
        self.value = data

    def AppendComment(self, comment):
        """
        Append text to a comment creating a new paragraph.
        """
        self.comment.Append(comment)

    def AppendSample(self, sname=None, scomment=None):
        """
        Append a sample to the sample-section of the dataset
        or workspace.
        """
        self.sample.append(sdf_sample(sname, scomment))

    def AppendInstrument(self, instrument):
        """
        Append an instrument to the list of instruments.
        """
        if not isinstance(instrument, sdf_instrument):
            msg = 'Error in sdf_object.AppendInstrument():'
            msg += '   Argument is not an sdf_instrument instance.'
            raise KeyError(msg)
        self.instrument.append(instrument)

    def AppendPar(self, par):
        """
        Append a parameter to the list of the datasets or workspaces
        parameters.
        """
        # NOTE: If you change something here, it propably also has to
        #       be changed inf the sdf_instrument.AppendPar() function.  

        if isinstance(par, sdf_par):
            self.par.append(par)
        elif isinstance(par, list):
            self.par = self.par + par  # this is Pythons list concatenation
        elif isinstance(par, str):
            self.par.append(sdf_par(name=par))  # create a new, empty 
                                                # subparameter list 

    def AppendObject(self, obj):
        """
        Append another sdf_object to this workspace's self.value.
        This is a valid function only for workspaces. To set the value
        of a dataset, use the function sdf_object.SetData .
        @param obj Instance of sdf_object (workspace or dataset).
        """
        if not self.IsWorkspace():
            msg = "ERROR: can't call function sdf_object.AppendObject"
            msg += " for datasets, only for workspaces."
            raise RuntimeError(msg)

        if isinstance(obj, sdf_object):
            self.value.append(obj)
            obj.parent = self            

    def AsXML(self, indent=0, lw=1000000):
        """
        Create the XML representation of an SDF object.
        """
        if self.debug:
            if indent:
                print("=" * indent)
            print("Enter function sdf_object.AsXML")
        if indent == 0:  # if beginning of file, define document type xml
            res = ' ' * indent + '<?xml version="1.0"?>\n'
        else:  # else, create empty string res
            res = ''
        if self.IsWorkspace():
            if self.debug:
                print("sdf_object identified as workspace")
            if indent == 0:
                res = res + ' ' * indent + '<!DOCTYPE workspace>\n'
            res = res + ' ' * indent + '<workspace>\n'
        elif self.IsDataset():
            if self.debug:
                print("sdf_object identified as dataset")
            if indent == 0:
                res = res + ' ' * indent + '<!DOCTYPE dataset>\n'
            res = res + ' ' * indent + "<dataset type='"
            res = res + self.value.datatype + "' >\n"
        else:
            raise RuntimeError("Object is neither DATASET nor WORKSPACE")
        
        if not self.name.IsEmpty():
            res = res + self.name.AsXML(indent + sdf_rc._tabsize) + '\n'

        if not self.owner.IsEmpty():
            res = res + self.owner.AsXML(indent + sdf_rc._tabsize) + '\n'        

        if not self.date.IsEmpty():
            res = res + self.date.AsXML(indent + sdf_rc._tabsize) + '\n'

        if not self.comment.IsEmpty():
            res = res + self.comment.AsXML(indent + sdf_rc._tabsize) + '\n'
        for sample in self.sample:
            res = res + sample.AsXML(indent + sdf_rc._tabsize) + '\n'

        for par in self.par:
            res = res + (par.AsXML(indent=indent + sdf_rc._tabsize)) + '\n'

        for instrument in self.instrument:
            res = res + instrument.AsXML(indent + sdf_rc._tabsize) + '\n'

        # handle single datasets:
        if self.IsDataset():
            res = res + self.value.AsXML(indent + sdf_rc._tabsize) + '\n'

        else:
            if self.debug:
                print("will now go through objects in this workspace ...")
            for obj in self.value:
                if self.debug:
                    print("... arrived at object " + obj.name.__str__())
                    obj.debug = True
                res = res + obj.AsXML(indent + sdf_rc._tabsize) + '\n'
        if self.IsWorkspace():
            res = res + ' ' * indent + '</workspace>\n'
        elif self.IsDataset():
            res = res + ' ' * indent + '</dataset>\n'

        if self.debug:
            print("done converting to XML")
            if indent:
                print("=" * indent)
        return res

    def Save(self, filename):
        """
        Save the sdf_object as an SDF-file.
        """
        ofp = open(filename, 'wt', encoding='utf-8')
        ofp.write(self.AsXML())
        ofp.close()

    def FromXML(self, etree_node):
        """
        Create an SDF_object from an XML ElementTree node.
        """
        if etree_node.tag == 'dataset':
            self.value.datatype = etree_node.attrib['type']
        
        for child in etree_node:
            if child.tag == 'name':
                self.name.FromXML(child)
            if child.tag == 'date':
                self.date.FromXML(child)
            if child.tag == 'owner':
                self.owner.FromXML(child)
            if child.tag == 'comment':
                self.comment.FromXML(child)
            if child.tag == 'par':
                self.par.append(sdf_par())
                self.par[-1].FromXML(child)
            if child.tag == 'instrument':
                self.instrument.append(sdf_instrument())
                self.instrument[-1].FromXML(child)
            if child.tag == 'sample':
                self.sample.append(sdf_sample())
                self.sample[-1].FromXML(child)

            if child.tag == 'workspace':
                ws = sdf_object('ws')
                ws.FromXML(child)
                self.AppendObject(ws)

            if child.tag == 'dataset':
                if etree_node.tag != 'workspace':
                    print('Error in SDF file structure: ', end='')
                    print('only workspaces can contain datasets.')
                    return
                ds = sdf_object('ds')
                self.AppendObject(ds)

                if child.attrib['type'] == 'img':
                    ds.value = sdf_data_img()
                elif child.attrib['type'] == 'sc':
                    ds.value = sdf_data_sc()
                elif child.attrib['type'] == 'mc':
                    ds.value = sdf_data_mc()
                else:
                    msg = "ERROR: unknown data type in attrib " + str(child.attrib) + '\n'
                    raise RuntimeError(msg)

                ds.FromXML(child)

            if child.tag == 'data':
                if etree_node.tag != 'dataset':
                    print('Error in SDF file structure: ', end='')
                    print('only datasets can contain data blocks.')
                    return
                self.value.FromXML(child)

    def GetChild(self, i):
        """
        Think I (ilyas) introduced this for the QtTreeViewModel.
        """
        if self.IsWorkspace():
            return self.value[i]
        else:
            return None

    def Get(self, key=None):
        
        if key is None:
            return self.value
        if isinstance(key, int):
            return self.value[key]
        if isinstance(key, str):
            for v in self.value:
                if v.name.value == key:
                    return v
            msg = "No child with name \"{}\" found.".format(key)
            raise KeyError(msg)
        msg = "key needs to be of type int or str"
        raise TypeError(msg)

    def __getitem__(self, item):
        return self.Get(item)

    def __contains__(self, item: str):
        if not isinstance(item, str):
            raise TypeError('item needs to be of type str')
        for v in self.value:
            if v.name.value == item:
                return True
        return False


    def GetPar(self, key):
        """
        More comfortable way to get a parameter in sdf_object.par either by
        index or name.
        """
        if isinstance(key, int):
            return self.par[key]
        if isinstance(key, str):
            for p in self.par:
                if p.name.value == key:
                    return p
            msg = "No parmeter by name \"{}\" found.".format(key)
            raise KeyError(msg)
        msg = "key needs to be of type int or str"
        raise TypeError(msg)

    def GetInstrument(self, key):
        """
        More comfortable way to get a parameter in sdf_object.par either by
        index or name.
        """
        if isinstance(key, int):
            return self.instrument[key]
        if isinstance(key, str):
            for inst in self.instrument:
                if inst.name.value == key:
                    return inst
            msg = "No instrument by name \"{}\" found.".format(key)
            raise KeyError(msg)
        msg = "key needs to be of type int or str"
        raise TypeError(msg)                        


    def IsValid(self):
        """
        Check validity of an sdf_object. 
        """
        pass
    
    def IsWorkspace(self):
        """
        Check whether the object is a workspace.
        """
        return isinstance(self.value, list)

    def IsDataset(self):
        """
        Check whether the object is a dataset.
        """
        return isinstance(self.value, sdf_data)
