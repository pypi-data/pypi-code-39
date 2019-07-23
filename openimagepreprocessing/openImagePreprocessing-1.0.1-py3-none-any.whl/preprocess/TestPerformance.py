import pandas as pd
import timeit
import datetime
import numpy as np
from typing import List, Tuple, Dict

def Testbbox(path_in:str):
    """Test bbox table.

    :param path_in: path of the bbox table.
    :type path_in: str.
    """

    global path
    path = path_in
    print('Load:')
    print(timeit.timeit(stmt="pd.read_csv(path, dtype={'BoxID': object, 'ImageID': object})", number=1, globals=globals()))
    print('Load With Index:')
    print(timeit.timeit(stmt="pd.read_csv(path, index_col=0, dtype={'BoxID': object, 'ImageID': object})", number=1, globals=globals()))

def TestbboxWithDtype(path_in:str):
    """Test bbox table with column types.

    :param path_in: path of the bb-t1 table.
    :type path_in: str.
    """

    global path
    path = path_in
    global type_dict_bbt1
    type_dict_bbt1 = {'BoxID': object, 'ImageID': object, 'XMin': np.int16, 'YMin': np.int16, 'XMax': np.int16, 'YMax': np.int16, 
          'IsOccluded': np.int16, 'IsTruncated': np.int16, 'IsGroupOf': np.int16, 'IsDepiction': np.int16, 
          'IsInside': np.int16, 'LuminanceMean': np.int16, 'LuminanceStd': np.int16}
    print('Load:')
    print(timeit.timeit(stmt="pd.read_csv(path, dtype=type_dict_bbt1)", number=1, globals=globals()))
    print('Load With Index:')
    print(timeit.timeit(stmt="pd.read_csv(path, index_col=0, dtype=type_dict_bbt1)", number=1, globals=globals()))

#these tables are no longer in use
#def TestbbT2ToT6(path_prefix:str, path_suffix:str):
#    """Test bb-t2 to bb-t6.

#    :param path_prefix: path prefix of the bb-t2 to bb-t6 table.
#    :type path_prefix: str.
#    :param path_suffix: path prefix of the bb-t2 to bb-t6 table.
#    :type path_suffix: str.
#    """

#    for i in range(5):
#        global path
#        path = path_prefix + str(i+2) + path_suffix
#        print('Load:')
#        print(timeit.timeit(stmt="pd.read_csv(path)", number=1, globals=globals()))
#        print('Load With Index:')
#        print(timeit.timeit(stmt="pd.read_csv(path, index_col=0)", number=1, globals=globals()))
#        print('Load With Index And List:')
#        print(timeit.timeit(stmt="""pd.read_csv(path, index_col=0, converters={"BoxIDList": lambda x: x.strip("[]").replace("'","").split(", ")})""", number=1, globals=globals()))

def GetListFromString(str1:str) -> List:
    """Parse str into List.

    :param str1: category str.
    :type str1: str.
    :return: the convert result.
    :rtype: List
    """

    result = []
    beginIndex = 0
    endIndex = -1
    while endIndex != len(str1)-1:
        str1 = str1[endIndex+1:]
        beginIndex = str1.index('[')
        endIndex = str1.index(']')
        result.append(str1[beginIndex:endIndex+1])
    
    return result

def GetCategoryList(str1:str) -> List:
    """Parse str into category list.

    :param str1: category list str.
    :type str1: str.
    :return: the convert result.
    :rtype: List
    """

    result = []
    str1 = str1.replace("'","")
    if(len(str1)>2):
        str1 = str1[1:len(str1)-1]
        list1 = GetListFromString(str1)  
        for str2 in list1:
            list2 = str2.strip("[]").split(", ")
            result.append(list2)
    return result

def GetCategoryList2(str1:str) -> List:
    """A faster way to parse str into category list.

    :param str1: category list str.
    :type str1: str.
    :return: the convert result.
    :rtype: List
    """

    result = []
    str1 = str1.replace("'","")
    if(len(str1)>2):
        str1 = str1[1:len(str1)-1]
        list1 = str1.split("], ")
        for str2 in list1:
            list2 = str2.strip("[]").split(", ")
            result.append(list2)
    return result

def TestCateGory(path_in:str):
    """Test category table.

    :param path_in: path of the category table.
    :type path_in: str.
    """

    global path
    path = path_in
    print('Load:')
    print(timeit.timeit(stmt="pd.read_csv(path)", number=1, globals=globals()))
    print('Load With Index:')
    print(timeit.timeit(stmt="pd.read_csv(path, index_col=0)", number=1, globals=globals()))
    print('Load With Index And List:')
    print(timeit.timeit(stmt="""pd.read_csv(path, index_col=0, converters={"BoxIDList": lambda x: x.strip("[]").replace("'","").split(", "), "ImageIDList": lambda x: x.strip("[]").replace("'","").split(", ")})""", number=1, globals=globals()))

def TestImageT1(path_in:str):
    """Test image-t1 table.

    :param path_in: path of the image-t1 table.
    :type path_in: str.
    """

    global path
    path = path_in
    print('Load:')
    print(timeit.timeit(stmt="pd.read_csv(path, dtype={'ImageID': object})", number=1, globals=globals()))
    print('Load With Index:')
    print(timeit.timeit(stmt="pd.read_csv(path, index_col=0, dtype={'ImageID': object})", number=1, globals=globals()))
    print('Load With Index And List:')
    print(timeit.timeit(stmt="""pd.read_csv(path, index_col=0, converters={"BoxIDList": lambda x: x.strip("[]").replace("'","").split(", "), 'CategoryList': lambda x: GetCategoryList2(x)}, dtype={'ImageID': object})""", number=1, globals=globals()))

def TestImageT2(path_in:str):
    """Test image-t2 table.

    :param path_in: path of the image-t2 table.
    :type path_in: str.
    """

    global path
    path = path_in
    print('Load:')
    print(timeit.timeit(stmt="pd.read_csv(path)", number=1, globals=globals()))
    print('Load With Index:')
    print(timeit.timeit(stmt="pd.read_csv(path, index_col=0)", number=1, globals=globals()))
    print('Load With Index And List:')
    print(timeit.timeit(stmt="""pd.read_csv(path, index_col=0, converters={"ImageIDList": lambda x: x.strip("[]").replace("'","").split(", ")})""", number=1, globals=globals()))

def TestImageT3(path_in:str):
    """Test image-t3 table.

    :param path_in: path of the image-t3 table.
    :type path_in: str.
    """

    global path
    path = path_in
    print('Load:')
    print(timeit.timeit(stmt="pd.read_csv(path, dtype={'ImageID': object})", number=1, globals=globals()))
    print('Load With Index:')
    print(timeit.timeit(stmt="pd.read_csv(path, index_col=0, dtype={'ImageID': object})", number=1, globals=globals()))