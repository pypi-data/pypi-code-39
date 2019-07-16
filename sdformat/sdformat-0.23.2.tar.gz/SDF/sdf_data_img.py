"""
-------------------------------------------------------------------------
Project: SDF: Standard Data Format

Module: sdf_data_img.py

Class sdf_data_img: A class to respresent an image data-block in 
                    SDF-files.

@Note Works only with uu encoded image files so far!
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

import numpy as np
import uu
import base64
from PIL import Image
import os
from .sdf_data import sdf_data
from . import sdf_rc



class sdf_data_img(sdf_data):
    """
    A class for image datasets in the SDF project.
    """    
    def __init__(self, data='', dtype='',
                 encoding='base64code', cdata=True):
        """
        Create an empty sdf_data_img object.
        """
        if encoding not in sdf_rc.KNOWN_VALUE_TYPES:
            msg = "unknown data type: " + str(encoding)
            raise RuntimeError(msg)        
        super(sdf_data_img, self).__init__('img')
        self.ID = 'sdf-data-img'
        self.data = data
        self.cdata = cdata
        self.dtype = dtype
        self.encoding = encoding

    def Set(self, data='', dtype='', encoding='base64code', cdata=True):
        """
        Set values of the sdf_data_img instance.
        @param data Image data, encoded as string.
        """
        self.data = data
        self.cdata = cdata
        self.dtype = dtype
        self.encoding = encoding        

    def __str__(self):
        """
        Printable representation of its contents. 
        """
        res = "DATA TYPE = %s, (%s, encoding: %s)" % (self.datatype, self.dtype, self.encoding)
        """
        res = res + " NUM-VALUES = %d\n" % self.numvals
        if self.numvals > 1 :
            res = res + '     [%s ... %s]\n' % (str(self.data[0]), 
                                                str(self.data[-1]))
        elif self.numvals == 1:
            res = res + '     [%s]\n' % str(self.data[0])
        else:
            res = res + '     [-]\n'
        """
        return res

    def AsXML(self, indent=0, lw=1000000):
        """
        Return this dataset's contents as XML formatted string.
        @param indent [Integer] Specifies indent of XML block, 
                      usually provided by parental SDF object.
        @param lw NOT USED AT THE MOMENT.
        """
        if not self.cdata:
            return 
        ret = ' ' * indent + "<data dtype='%s' encoding='%s' >" % (self.dtype, self.encoding) + '\n'
        ret = ret + ' ' * (indent + sdf_rc._tabsize) + "<![CDATA[" + self.data + "]]>\n"            
        ret = ret + ' ' * indent + "</data>\n"
        return ret            

    def FromXML(self, etree_node):
        """
        Create an sdf_data_img block from an XML ElementTree node.
        """
        if etree_node.attrib['encoding'] == 'uucode' or etree_node.attrib['encoding'] == 'base64code':
            self.Set(data=etree_node.text.lstrip().rstrip() + '\n', dtype = etree_node.attrib['dtype'], encoding = etree_node.attrib['encoding'])
        else:
            msg = "unknown encoding in attrib: " + str(etree_node.attrib)
            raise RuntimeError(msg)
        
    def Get(self):
        """
        Return a tuple with the contents
        """
        pass
        
    def GetType(self):
        """
        Return the type of the data-block
        """
        pass

    def GetImgAsArray(self):
        """
        Return the image data as a numpy array.
        """
        if self.cdata:
            ## 1. Create temporary uu encoded text file.
            with open('.tmp_img.txt', 'wt') as f:
                if self.encoding == 'uucode':
                    ## 1.a. Replace substitute strings with CDATA escape sequence.
                    enc_str = self.data.replace(sdf_rc._CDATA_REPLACE, ']]>')
                else:
                    enc_str = self.data
                ## 1.b. Write to file.
                f.write(enc_str)
                f.close()
            ## 2. Convert encoded text to temporary PNG.
            if self.encoding == 'uucode':
                uu.decode(open('.tmp_img.txt', 'rb'), open('.tmp_img.png', 'wb'))
            elif self.encoding == 'base64code':                
                base64.decode(open('.tmp_img.txt', 'rb'), open('.tmp_img.png', 'wb'))
            else:
                msg = "Unknown encoding " + str(self.encoding) + " !"
                raise RuntimeError(msg)            
            ## 3. Read image to buffer as image object.
            img = np.array(Image.open('.tmp_img.png'))
            ## 4. Remove temporary files.
            os.remove('.tmp_img.txt')
            os.remove('.tmp_img.png')
            return img        
        else:
            msg = "GetImgAsArray currently only implemented for encoding=='uucode' or 'base64code'."
            raise RuntimeError(msg)
            
    def IsValid(self):
        """
        Check if the contents of this class are valid.
        """
        pass
        
    def IsEmpty(self):
        """
        Check if this class instance is empty
        """
        pass
