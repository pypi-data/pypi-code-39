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

"""
eoDR file name definition.

"""

from datetime import datetime
from collections import OrderedDict


from geopathfinder.file_naming import SmartFilename


class eoDRFilename(SmartFilename):

    """
    eoDataReaders file name definition using SmartFilename class.
    """

    def __init__(self, fields, ext='.vrt', convert=False):
        """
        Constructor of eoDRFilename class.

        Parameters
        ----------
        fields: dict
            Dictionary specifying the different parts of the filename.
        ext: str, optional
            Extension of the filename (default is '.vrt' for GDAL VRT files)
        convert: bool, optional
            If true, decoding is applied to parts of the filename, where such an operation is available (default is False).
        """
        self.dt_format = "%Y%m%dT%H%M%S"
        self.fields = fields.copy()

        fields_def = OrderedDict([
                     ('id', {'len': 12, 'delim': True}),
                     ('dt_1', {'len': 15, 'delim': True,
                                  'decoder': lambda x: self.decode_datetime(x),
                                  'encoder': lambda x: self.encode_datetime(x)}),
                     ('dt_2', {'len': 15, 'delim': True,
                                  'decoder': lambda x: self.decode_datetime(x),
                                  'encoder': lambda x: self.encode_datetime(x)}),
                     ('band', {'len': None, 'delim': True, 'encoder': lambda x: str(x)})
                    ])

        fields_def_keys = list(fields_def.keys())
        for key in fields.keys():
            if key not in fields_def_keys:
                fields_def[key] = {'len': None, 'delim': True}

        super(eoDRFilename, self).__init__(self.fields, fields_def, pad='-', ext=ext, convert=convert)

    @property
    def stime(self):
        """
        Start time.

        Returns
        -------
        datetime.datetime
            Start time.
        """
        try:
            if "-" not in self['dt_1']:
                return self.decode_datetime(self['dt_1'])
            else:
                return None
        except TypeError:
            return None

    @property
    def etime(self):
        """"
        End time.

        Returns
        -------
        datetime.datetime
            End time.
        """
        try:
            if "-" not in self['dt_2']:
                return self.decode_datetime(self['dt_2'])
            else:
                return None
        except TypeError:
            return None

    def decode_datetime(self, string):
        """
        Decodes a string into a datetime object. The format is given by the class.

        Parameters
        ----------
        string: str, object
            String needed to be decoded to a datetime object.

        Returns
        -------
        datetime.datetime, object
            Original object or datetime object parsed from the given string.
        """
        if isinstance(string, str):
            return datetime.strptime(string, self.dt_format)
        else:
            return string

    def encode_datetime(self, time_obj):
        """
        Encodes a datetime object into a string. The format is given by the class.

        Parameters
        ----------
        time_obj: datetime.datetime, object
            Datetime object needed to be encoded to a string.

        Returns
        -------
        str, object
            Original object or str object parsed from the given datetime object.
        """
        if isinstance(time_obj, datetime):
            return time_obj.strftime(self.dt_format)
        else:
            return time_obj


def create_eodr_filename(filename_string, convert=False):
    """
    Creates a eoDRFilename() object from a given string filename

    Parameters
    ----------
    filename_string : str
        filename following the eoDR filename convention.
        e.g. 'c29cfaab80e2_20170517T171434_---------------_eo_array_contains.vrt'
    convert: bool, optional
            If true, decoding is applied to parts of the filename, where such an operation is available (default is False).

    Returns
    -------
    eoDRFilename
    """
    helper = eoDRFilename({})
    filename_string = filename_string.replace(helper.ext, '')
    parts = filename_string.split(helper.delimiter)

    fields = {'id': parts[0],
              'dt_1': parts[1],
              'dt_2': parts[2],
              'band': parts[3]
             }

    if len(parts) > 4:  # if the filename consists of more than 4 parts, additional "dimensions" are added to the fields dictionary
        for i, part in enumerate(parts[4:]):
            key = 'd' + str(i+1)
            fields[key] = part

    return eoDRFilename(fields, convert=convert)


if __name__ == '__main__':
    pass