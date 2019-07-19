import urllib3
import urllib
import sys
import pandas as pd
import numpy as np
import numpy.lib.recfunctions as rfn
import inspect
import csv
from enum import Enum

# Global vars

httppool = urllib3.PoolManager()
norgate_web_api_base_url = 'http://localhost:38889/api/v1/'

#######################################################################################################
# Internal helper functions
#######################################################################################################

def build_api_url(dataitem,item,parameters = None):
    url = norgate_web_api_base_url + dataitem
    if (item is not None):
        item = str(item)
        url += '/' + urllib.parse.quote(item)
    #parameters["pyfile"] = __file__ # for diagnosis
    #parameters["pymain"] = '__main__'  # for diagnosis
    #parameters["pyargv0"] = sys.argv[0] # for diagnosis
    if (parameters is not None):
        url += '?' + urllib.parse.urlencode(parameters);
    return url

def get_api_data(dataitem,item,parameters = None):
    url = build_api_url(dataitem,item,parameters)
    try:
        apiresponse = httppool.request('GET', url)
    except Exception:
        raise ValueError("Unable to obtain Norgate Data - perhaps NDU is not running?")
    return apiresponse

def validate_existing_array(pandas_dataframe,numpy_ndarray,numpy_recarray,format):
    if pandas_dataframe is not None:
        start_date,end_date,limit = validate_dataframe(pandas_dataframe,format)
    if numpy_ndarray is not None:
        start_date,end_date,limit = validate_ndarray(numpy_ndarray,format)
    if numpy_recarray is not None:
        start_date,end_date,limit = validate_recarray(numpy_recarray,format)
    return start_date,end_date,limit

def validate_dataframe(pandas_dataframe,format):
    if (format != 'pandas-dataframe'):
        raise ValueError("Format specified is " + format + " but the parameter pandas_dataframe was provided.  You need to pass in an array of the same type as the format you require.  Perhaps you didn't explicitly specify the format?")
    if (not(isinstance(pandas_dataframe,pd.core.frame.DataFrame))):
        raise ValueError(inspect.currentframe().f_back.f_code.co_name + ": pandas_dataframe passed was not a Pandas DataFrame - it is actually " + str(type(pandas_dataframe)))
    if (pandas_dataframe.index.name != 'Date'):
        raise ValueError(inspect.currentframe().f_back.f_code.co_name + ": Expected dataframe to have index of Date but found " + pandas_dataframe.index.name)
    start_date = pandas_dataframe.first_valid_index()
    end_date = pandas_dataframe.last_valid_index()
    limit = -1
    return start_date,end_date,limit

def validate_recarray(numpy_recarray,format):
    if (format != 'numpy-recarray'):
        raise ValueError("Format specified is " + format + " but the parameter numpy_recarray was specified. You need to pass in an array of the same type as the format you require.  Perhaps you didn't explicitly specify the format?")
    if (not(isinstance(numpy_recarray,np.recarray))):
        raise ValueError(inspect.currentframe().f_back.f_code.co_name + ": numpy_recarray was not a Numpy recarray - it is actually " + str(type(numpy_recarray)))
    if (numpy_recarray.dtype.names[0] != 'Date'):
        raise ValueError(inspect.currentframe().f_back.f_code.co_name + ": Expected recarray to have first field of Date but found " + numpy_recarray.dtype.names[0])
    start_date = numpy_recarray[0][0]
    end_date = numpy_recarray[-1][0]
    limit = -1
    return start_date,end_date,limit

def validate_ndarray(numpy_ndarray,format):
    if (format != 'numpy-ndarray'):
        raise ValueError("Format specified is " + format + " but the parameter numpy_ndarray was specified.  You need to pass in an array of the same type as the format you require.  Perhaps you didn't explicitly specify the format?")
    if (not(isinstance(numpy_ndarray,np.ndarray))):
        raise ValueError(inspect.currentframe().f_back.f_code.co_name + ": numpy_ndarray was not a Numpy ndarray array - it is actually " + str(type(numpy_ndarray)))
    if (numpy_ndarray.dtype.names[0] != 'Date'):
        raise ValueError(inspect.currentframe().f_back.f_code.co_name + ": Expected recarray to have first field of Date but found " + numpy_ndarray.dtype.names[0])
    start_date = numpy_ndarray[0][0]
    end_date = numpy_ndarray[-1][0]
    limit = -1
    return start_date,end_date,limit


def validate_api_response(r,symbol):
    if (r.status == 404):
        raise ValueError(inspect.currentframe().f_back.f_code.co_name + ': ' + str(symbol) + " was not found");
    if (not (r.status == 200 or r.status == 204)) :
        raise ValueError(inspect.currentframe().f_back.f_code.co_name + ": Error in receiving Norgate Data - check paramters are correctly formatted.  Status code is: " + str(r.status));

def create_pandas_dataframe(r,pandas_dataframe = None,lowercase_columns = False):
    recordcount = int(r.headers['X-Norgate-Data-Record-Count'])
    if (lowercase_columns):
        fields = r.headers['X-Norgate-Data-Field-Names'].lower().split(',')
    else:
        fields = r.headers['X-Norgate-Data-Field-Names'].split(',')
    formats = r.headers['X-Norgate-Data-Field-Formats'].split(',')
    fieldcount = int(r.headers['X-Norgate-Data-Field-Count'])
    npdates = np.frombuffer(r.data,formats[0],recordcount)  # 'datetime64[D]'
    npdates = npdates.copy()
    indicatorType = []
    for i in range(1,fieldcount):
        indicatorType.append((fields[i],formats[i]))
    npdata = np.frombuffer(r.data,indicatorType,-1,recordcount * 8)
    npdata = npdata.copy()
    pdf = pd.DataFrame(data=npdata,index=npdates)
    pdf.index.name=fields[0]
    if pandas_dataframe is None:
        return pdf
    pandas_dataframe=pd.merge(pandas_dataframe,pdf, how='left', left_index=True, right_index=True)
    return pandas_dataframe

def create_numpy_ndarray(r,np_ndarray = None):
    recordcount = int(r.headers['X-Norgate-Data-Record-Count'])
    fields = r.headers['X-Norgate-Data-Field-Names'].split(',')
    formats = r.headers['X-Norgate-Data-Field-Formats'].split(',')
    fieldcount = int(r.headers['X-Norgate-Data-Field-Count'])
    indicatorType = []
    for i in range(0,fieldcount):
        indicatorType.append((fields[i],formats[i]))
    npdata = np.frombuffer(r.data,indicatorType,recordcount)
    if np_ndarray is not None:
        np_ndarray = rfn.join_by("Date",np_ndarray,npdata)
        return np_ndarray
    return npdata


def create_numpy_recarray(r,np_recarray = None):
    npdata = create_numpy_ndarray(r)
    npdata2 = npdata.view(np.recarray)
    if np_recarray is not None:
        np_recarray = rfn.join_by("Date",np_recarray,npdata2)
        return np_recarray
    return npdata2

