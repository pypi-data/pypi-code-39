"""
-------------------------------------------------------------------------

Project: SDF: Standard Data Format

Module: sdf_utils.py

A loose collection of utility functions that are not bound to any 
classes.
 
bg 26.05.2010
fs 06.04.2013
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
from . import sdf_object
import xml.etree.ElementTree as ET
import numpy as np

def sdf_Load(filename):
    """
    Load an SDF file and return an sdf_object instance.
    """
    tree = ET.parse(filename)
    root = tree.getroot()
    
    if root.tag not in ('dataset','workspace'):
        print('Error in sdf_Load():', filename, 'does not contain')
        print('      a dataset or workspace.')
        return None

    obj = sdf_object.sdf_object(src=root.tag)
    obj.FromXML(root)

    return obj
        

def IsAnInstance(obj,ID):
    return HasAttr(obj,'ID') and obj.ID == ID


def NormalizeWhiteSpace(text):
    """
    Normalize the input string 'text' by removing all
    line breaks and reducing multiple white space to a
    single white space.
    """
    if not text:
        return None
    else:
        return ' '.join(str(text).split())


def SplitInLines(text, lw=80):
    """
    Split a string into words and combine the words into new lines that
    are shorter than the line width 'lw'.

    Returns an array of strings (which do not contain the '\n' character)
    and can be interpreted as the lines of the string.
    """
    if lw < 30:
        print('Warning: In sdf_utils.SplitInLines():')
        print('         Linewidth is getting too narrow ( < 30 chars).')
        print('         Start to ignore the linewidth parameter.')
        lw = 1000000

    res = []
    words = str(text).split()
    line = ''

    for word in words:
        if (len(line)+len(word)+1) <= lw:
            line = line + ' ' + word
        else:
            res.append(line.strip())
            line = ''
    if res == []: 
        # still empty -> we collected only one line
        res.append(line.strip())
    return res


def xml_encode(text):
    """
    Encoding of text -> xml-text.

    All letters reserved for XML (& < > " ') are replaced by 
    their XML entities (&amp; &gt; &lt; &quot; &apos).
    """
    # '&' MUST be the first:
    ret = text.replace('&','&amp;')  

    # all others can be in arbitrary order:
    for i in range(1,len(sdf_rc.XML_encoding)):
        ret = ret.replace(sdf_rc.XML_encoding[i][0],
                          sdf_rc.XML_encoding[i][1])
    return ret


def xml_decode(XMLtext):
    """
    Encoding of xml-text -> text.

    All special letters in XML represented as (&amp; &gt; &lt; 
    &quot; &apos) are replaced by their original meaning which 
    is one of (& < > " ').
    """
    temp = XMLtext
    for i in range(1,len(sdf_rc.XML_encoding)):
        temp = temp.replace(sdf_rc.XML_encoding[i][1],
                            sdf_rc.XML_encoding[i][0])
    # this must be last:
    temp = temp.replace('&amp;','&')
    return temp


def convert_to_int(x, debug=False, tol=1e-7, max_tries=1000):
    """
    Perform a linear transformation of the data given by x into
    integers with a multiplier and offset. General procedure as
    follows:

    1) Sort x and obtain unique values
    2) Get unique differences in x
    3) Assume that smalles difference found is also smallest
       difference in the dataset. TODO: This might go wrong
       if in fact this difference is itself an integer multiple
       of the real one. In this case, assuming the underlying data
       is of integer type, we might try divide the found difference
       by increasing integers to find the real one. -> Done that.
    4) Divide dataset by said difference, thus yielding integers.
    5) Check if difference's sign should be flipped to reduce the
       number of digits needed
    6) Find offset, substract, convert to hex/int, return

    Parameters of this function:

    x (array-like):
       Data array to be converted. If it is a python list, it will
       be converted to a numpy array within this function. We will
       not however check if x is actually array-like, so beware of
       that case!

    debug (bool):
       Flag that triggers this function to print extensive debug 
       information to the console

    tol (float):
       Tolerance which indicates when to accept a conversion to
       integers as acceptable. If a minimal distance was found, 
       values in x are divided by this distance. Resulting values
       are converted to int by rounding to the nearest integer,
       i.e. 2.5 will be converted to 3 and 2.4 to 2 etc. Conversion
       is accepted, if abs(as_int - x) < tol for all values in x.

    max_tries (int):
       Maximal number of divisions of the first minimal distance 
       found before this function aborts and return failure.

    This function returns 4 objects:

    int_list (array_like of integers):
       List of strings in hex/integer representation or list of
       float strings, if the conversion was not successfull. If
       not, we just return x as a numpy array

    multiplier (float):
       Float multiplier to be applied to hex-data to obtain
       original data.

    offset (float):
       Offset to be applied to hex-data to optain original data.

    success (bool):
       Flag indicating if the conversion was successfull and
       thus actual integer-values have been returned or just the
       original dataset as float-strings

    Original data (within precision of the transformation) can
    be obtained by calculating:
    
       orig_data = int_list * multiplier + offset
    """

    # Check if x is of proper type
    if not isinstance(x, np.ndarray):
        x = np.array(x)

    # If empty array was given, report failure
    # Also, if only one value is given, a conversion
    # is useless and would fail.
    if (len(x) == 0) or (len(x) == 1):
        return x, None, None, False

    # Sort, unique, differences.
    if debug:
        print("#"*70)
        print("o Converting array x to hex...")
        print("\t - Sorting, unique, differences.")
    
    x_s = np.sort(x)
    x_s = np.unique(x_s)
    dx  = np.diff(x_s)
    dx  = np.unique(dx)

    # If there are no unique differences, all the datapoints are
    # exactly the same. The transformation will only incolve an
    # offset
    if (len(dx) == 0):
        offset = x.min()
        return np.zeros_like(x).astype(int), 1, offset, 1

    # If there are no 

    step_initial = dx.min()

    # Transform values and get integers, both positive
    # and negative.
    offset_pos = x.min()
    x_pos_corr = x - offset_pos

    offset_neg = (-x).min()
    x_neg_corr = (-x) - offset_neg

    # Check if we found the smallest difference or if we
    # need to decrease it further.

    if debug:
        print("\t - First guess of atom difference: %e" % step_initial)
        print("\t - Checking if it is itself an integer multiple...")
    
    counter = 1
    while True:

        if counter > max_tries:
            #warnings.warn("\nGiven dataset could not be converted to hex.\n"
            #              "without significant loss of accuracy.\n"
            #              "Is the source really a transformed int?",
            #              RuntimeWarning)

            # We have not been able to transform anything. Return
            # the array itself as a list of strings, report failure
            # and set step to 1 and offset to 0.
            return x, None, None, False

        step = step_initial / counter
    
        as_int_pos = np.round(x_pos_corr / step).astype(int)
        as_int_neg = np.round(x_neg_corr / step).astype(int)
        
        dev_pos  = abs(as_int_pos - x_pos_corr / step)
        dev_neg  = abs(as_int_neg - x_neg_corr / step)
        cond     = np.all( (dev_pos < tol) &
                           (dev_neg < tol))
        
        if cond:
            if debug:
                print("\t\t - Everything seems fine. Continue.")
                print("\t\t - Maximal pos deviation: %e" % dev_pos.max())
                print("\t\t - Maximal pos deviation: %e" % dev_neg.max())
            break
        else:
            counter += 1
            if debug:
                print("\t!!\t - Smallest difference not yet found.")
                print("\t!!\t - Current difference: %e" % step)
                print("\t!!\t - Maximal pos deviation: %e" % dev_pos.max())
                print("\t!!\t - Maximal pos deviation: %e" % dev_neg.max())
                print("\t!!\t - Reducing and retrying. Counter: %d" % counter)
                
    # Check if we need to flip the sign for larger
    # compression.
    n_digits_pos = np.ceil(np.log(as_int_pos + 1) / np.log(16)).sum()
    n_digits_neg = np.ceil(np.log(as_int_neg + 1) / np.log(16)).sum()

    if debug:
        print("\t - Checking if we need to flip the sign.")
        print("\t\t - N of digits pos:", n_digits_pos)
        print("\t\t - N of digits neg:", n_digits_neg)

    if n_digits_pos > n_digits_neg:
        if debug:
            gain = 100 - 100 * (n_digits_neg / n_digits_pos)
            print("\t\t - Flipping is beneficial. Raw gain: %.1f v.H." % gain)
        step   = -step
        as_int = as_int_neg
        offset = -offset_neg
    else:
        if debug:
            gain = 100 - 100 * (n_digits_pos / n_digits_neg)
            print("\t\t - Use as is. Raw gain: %.1f percent" % gain)
        as_int = as_int_pos
        offset = offset_pos

    # Now, convert to hex and concatenate as a string
    # Changed my mind. I'll split this into two functions.
    #if debug:
    #    print("\t - Create hex string")
    #hex_list = [("%x" % i).upper() for i in as_int]
    
    # Recalculate x with new compression and check compression
    if debug:
        print("\t - Recalculate data with new representation.")
        xprime = as_int * step + offset
        
        as_str = " ".join([str(i) for i in x])
        as_hex = " ".join([("%x" % i).upper() for i in as_int])

        compression_ratio = len(as_hex) / len(as_str)

        n_before = len(as_str)
        n_after  = len(as_hex)

        gain     = n_after / n_before * 100.0
        print("==>\t - Length of string before: %d" % n_before)
        print("==>\t - Length of string after: %d" % n_after)
        print("==>\t - Compressed to %.1f percent of previous size." % gain)
        print("==>\t - Total sum of abs diff: %e" % abs(x-xprime).sum())
        print("#"*70)

    # Return proper stuff:
    # What do we need? Basically, a list of strings that can readily
    # be used to be written to a file and a message stating if the
    # conversion was successfull and offsets and multipliers
    # return dx, as_hex, xprime, as_int, offset, step
    return as_int, step, offset, True


def int_to_hex_list(int_list):
    """
    Convert an array-like of ints into a list of hex-strings to write
    to file.
    TODO: We do not check for proper type here.

    Parameters:
       int_list (array-like):
          list of integers. should be of ndtype int

    Returns:
       hex_list (list of string):
          Integers as hex-strings with capital letters without preceding
          0x literal.
    """
    hex_list = ["%x".upper() % i for i in int_list]
    return hex_list


def hex_list_to_int(hex_list):
    """
    Convert an list of strings into an np.array of integers

    TODO: We do not check for proper type here.

    Parameters:
       hex_list (list of strings):
          list of hex strings.

    Returns:
       int_list (ndarray, int type):
          numpy array of integers.
    """

    int_list = [int(i, base=16) for i in hex_list]
    return np.array(int_list)


def numpy_dtype_to_sdf_dtype(npdtype: str) -> str:
    if 'int' in npdtype.name:
        return 'int'
    if 'float' in npdtype.name:
        return 'float'
    raise NotImplementedError('handling of numpy dtype "{}" not implemented yet'.format(npdtype))
