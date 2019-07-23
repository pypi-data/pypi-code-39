# Copyright (c) 2018, Vienna University of Technology (TU Wien), Department
# of Geodesy and Geoinformation (GEO).
# All rights reserved.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL VIENNA UNIVERSITY OF TECHNOLOGY,
# DEPARTMENT OF GEODESY AND GEOINFORMATION BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


class FilenameObj(object):
    """
    Empty class which is used to hold different attributes of the filename.
    """

    def __init__(self):
        pass


class SmartFilename(object):

    """
    SmartFilename class handles file names with pre-defined field names
    and field length.
    """

    def __init__(self, fields, fields_def, ext=None, pad='-', delimiter='_', convert=False):
        """
        Define name of fields, length, pad and delimiter symbol.

        Parameters
        ----------
        fields : dict
            Name of fields (keys) and (values).
        field_def : OrderedDict
            Name of fields (keys) in right order and length (values).
        ext : str, optional
            File name extension (default: None).
        pad : str, optional
            Padding symbol (default: '-').
        delimiter : str, optional
            Delimiter (default: '_')
        convert: bool, optional
            If true, decoding is applied to parts of the filename, where such an operation is available (default is False).
        """
        self.fields = fields
        self.fields_def = fields_def
        self.ext = ext
        self.delimiter = delimiter
        self.pad = pad
        self.convert = convert
        self._check_def()
        self.obj = self.__init_filename_obj()
        self.full_string = self._build_fn()

    def __init_filename_obj(self):
        """
        Initialises the class 'FilenameObj' to set all filename attributes as class variables.
        This enables an easier access to filename properties.

        Returns
        -------
        FilenameObj

        """
        filename_obj = FilenameObj()
        for key, value in self.fields.items():
            if self.convert:
                setattr(filename_obj, key, self.__decode(key, value))
            else:
                setattr(filename_obj, key, self.__encode(key, value))

        return filename_obj

    def _check_def(self):
        """
        Check if fields names and length comply with definition.

        """
        for key, value in self.fields.items():
            if key in self.fields_def:
                if not self.fields_def[key]:
                    continue
                value = self.__encode(key, value)
                if self.fields_def[key]['len'] and len(value) > self.fields_def[key]['len']:
                    raise ValueError("Length does not comply with "
                                     "definition: {:} > {:}".format(
                                         len(value), self.fields_def[key]['len']))
                if 'delim' not in self.fields_def[key].keys():
                    self.fields_def[key]['delim'] = True
            else:
                raise KeyError("Field name undefined: {:}".format(key))

    def _build_fn(self):
        """
        Build file name based on fields, padding and length.

        Returns
        -------
        filename : str
            Filled file name.

        """
        filename = ''
        for name, keys in self.fields_def.items():

            if not keys:
                continue

            length = keys['len'] if keys['len'] else 1
            delimiter = self.delimiter if keys['delim'] else ''

            if name in self.fields:
                value = self.__encode(name, self.fields[name])
                if filename == '':
                    filename = value.ljust(length, self.pad)
                else:
                    filename += delimiter + value.ljust(length, self.pad)
            else:
                if filename == '':
                    filename = self.pad * length
                else:
                    filename += delimiter + self.pad * length

        if self.ext is not None:
            filename += self.ext

        return filename

    def get_field(self, key):
        """
        Returns the value of the field with a given key.

        Parameters
        ----------
        key : str
            Name of the field.

        Returns
        -------
        str, object
            Part of the filename associated with given key. Depending on the chosen flag 'convert', it is either a str
            (convert=False) or an object.
        """

        field = self.__encode(key, self.fields[key])

        # check and reset the attribute of the object variable
        field_obj = self.__encode(key, getattr(self.obj, key))
        if field_obj and (field_obj != field):
            if self.fields_def[key]['len'] and (len(field_obj) <= self.fields_def[key]['len']):
                field = field_obj
                self[key] = field

        field = field.replace(self.pad, '')

        if self.convert:
            return self.__decode(key, field)
        else:
            return field

    def __getitem__(self, key):
        """
        Returns the value of the field with a given key.

        Parameters
        ----------
        key : str
            Name of the field.

        Returns
        -------
        str, object
            Part of the filename associated with given key. Depending on the chosen flag 'convert', it is either a str
            (convert=False) or an object. If the key can't be found in the fields definition, the method tries to return
            a property of an inherited class.
        """
        if key in self.fields_def:
            return self.get_field(key)
        elif hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError('"{}" is neither a class variable nor a file attribute.'.format(key))

    def __setitem__(self, key, value):
        """
        Sets the value of a filename field corresponding to the given key.

        Parameters
        ----------
        key : str
            Name of the field.
        value: object
            Value of the field.

        """
        if key in self.fields_def and self.fields_def[key]:
            value = self.__encode(key, value)
            if self.fields_def[key]['len'] and (len(value) > self.fields_def[key]['len']):
                raise ValueError("Length does not comply with "
                                 "definition: {:} > {:}".format(
                                     len(value), self.fields_def[key]['len']))
            else:
                self.fields[key] = value
                value = value.replace(self.pad, '')
                if self.convert:
                    setattr(self.obj, key, self.__decode(key, value))
                else:
                    setattr(self.obj, key, value)
        else:
            raise KeyError("Field name undefined: {:}".format(key))

    def __repr__(self):
        """
        Returns the string representation of the class.

        Returns
        -------
        str
            String representation of the class.
        """
        return self._build_fn()

    def __decode(self, key, value):
        """
        Decodes a certain value (str -> object) specified by the given key if an entry 'decoder' is available.

        Parameters
        ----------
        key : str
            Name of the field.
        value: object
            Value of the field.

        Returns
        -------
        str
            Decoded or original value.
        """
        if self.fields_def[key] and 'decoder' in self.fields_def[key].keys():
            decoder = self.fields_def[key]['decoder']
            try:
                dec_value = decoder(value)
                return dec_value
            except:
                return value
        else:
            return value

    def __encode(self, key, value):
        """
        Encodes a certain value (object -> str) specified by the given key if an entry 'encoder' is available.

        Parameters
        ----------
        key : str
            Name of the field.
        value: object
            Value of the field.

        Returns
        -------
        str
            Encoded or original value.
        """
        if (not isinstance(value, str)) and self.fields_def[key] and ('encoder' in self.fields_def[key].keys()):
            encoder = self.fields_def[key]['encoder']
            try:
                enc_value = encoder(value)
                return enc_value
            except:
                return value
        else:
            return value
