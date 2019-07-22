import pandas as pd
import json
import operator
import math
from typing import List, Tuple, Dict

#chunkSize = 100000 

def GetHexString(x:int) -> str:
    """Get the hex string of a digit.

    :param x: a digit.
    :type x: int.
    :return: the convert result.
    :rtype: str
    """

    s1= hex(x)[2:]
    n = 8 - len(s1)
    return '0'*n + s1

def GetBasicData(path_boxes_classes:str, path_all_classes:str, path_parents:str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, Dict]:
    """Get the basic data.

    :param path_boxes_classes: path of the file(box classes).
    :type path_boxes_classes: str.
    :param path_all_classes: path of the file(all classes).
    :type path_all_classes: str.
    :param path_parents: path of the class hierarchy json file.
    :type path_parents: str.
    :return: the basic data.
    :rtype: Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, Dict]
    """

    #600 classes
    boxes_classes = pd.read_csv(path_boxes_classes, sep=',', header=None, index_col=0)
    #all classes(19985)
    all_classes = pd.read_csv(path_all_classes, sep=',', header=None, index_col=0)

    #600 classes
    boxes_classes2 = pd.read_csv(path_boxes_classes, sep=',', header=None, index_col=1)
    #all classes(19985)
    all_classes2 = pd.read_csv(path_all_classes, sep=',', header=None, index_col=1)

    #parents
    with open(path_parents,'r') as load_f:
        parents_dict = json.load(load_f)

    return boxes_classes, all_classes, boxes_classes2, all_classes2, parents_dict

def GetLabelDes(labelName:str, boxes_classes:pd.DataFrame, all_classes:pd.DataFrame) -> str:
    """Get the corresponding description of the class.

    :param labelName: the label name.
    :type labelName: str.
    :param boxes_classes: box classes data.
    :type boxes_classes: pd.DataFrame.
    :param all_classes: all classes data.
    :type all_classes: pd.DataFrame.
    :return: the corresponding description of the class.
    :rtype: str
    """

    labelDes = "not in"
    try:
        labelDes = boxes_classes.loc[labelName][1]
    except KeyError:
        try:
            labelDes = all_classes.loc[labelName][1]
        except KeyError:
            return labelDes 
        else:
            return labelDes
    else:         
        return labelDes

def GetLabelName(labelDes:str, boxes_classes2:pd.DataFrame, all_classes2:pd.DataFrame) -> str:
    """Get the corresponding class of the description.

    :param labelDes: the label description.
    :type labelDes: str.
    :param boxes_classes2: box classes2 data.
    :type boxes_classes2: pd.DataFrame.
    :param all_classes2: all classes2 data.
    :type all_classes2: pd.DataFrame.
    :return: the corresponding class of the description.
    :rtype: str
    """

    labelName = "not in"
    try:
        labelName = boxes_classes2.loc[labelDes][0]
    except KeyError:
        try:
            labelName = all_classes2.loc[labelDes][0]
        except KeyError:
            return labelName 
        else:
            return labelName
    else:         
        return labelName

def GetParents(labelName:str, parents_dict:Dict) -> List:
    """Get the parents of the class.

    :param labelName: the label name.
    :type labelName: str.
    :param parents_dict: parent_dict data.
    :type parents_dict: Dict.
    :return: the parents of the class.
    :rtype: List
    """

    return parents_dict[labelName]

def GetCategoryList(labelName:str, boxes_classes:pd.DataFrame, all_classes:pd.DataFrame, parents_dict:Dict) -> List:
    """Get the categorylist of the class.

    :param labelName: the label name.
    :type labelName: str.
    :param boxes_classes: box classes data.
    :type boxes_classes: pd.DataFrame.
    :param all_classes: all classes data.
    :type all_classes: pd.DataFrame.
    :param parents_dict: parents dictionary.
    :type parents_dict: Dict.
    :return: the categorylist of the class.
    :rtype: List
    """

    parents = getParents(labelName, parents_dict)
    labelDes = getLabelDes(labelName, boxes_classes, all_classes)
    return [[labelDes] + parent  for parent in parents]

def Createbbox(path:str, saveName:str, boxes_classes:pd.DataFrame, all_classes:pd.DataFrame, parents_dict:Dict, firstWrite:bool, chunkSize:int):
    """Create bbox table.

    :param path: path of the bbox annotation file.
    :type path: str.
    :param saveName: the save path of the result.
    :type saveName: str.
    :param boxes_classes: box classes data.
    :type boxes_classes: pd.DataFrame.
    :param all_classes: all classes data.
    :type all_classes: pd.DataFrame.
    :param parents_dict: parents dictionary.
    :type parents_dict: Dict.
    :param firstWrite: if first write the result.
    :type firstWrite: bool.
    :param chunkSize: size of the chunk.
    :type chunkSize: int.
    """

    chunks = pd.read_csv(path, sep=',', chunksize=chunkSize, dtype={'ImageID': object})
    for boxes_data in chunks:
        print("before:", boxes_data.shape)
        boxes_data['LabelName'] = boxes_data['LabelName'].map(lambda x: getLabelDes(x, boxes_classes, all_classes))

        #modify the LabelName column name to Category
        boxes_data.rename(columns={'LabelName':'Category'}, inplace = True)
        
        #drop Source,Confidence
        boxes_data.drop(columns=['Source', 'Confidence'], inplace=True)

        boxes_data['LuminanceMean'] = 0
        boxes_data['LuminanceStd'] = 0        
        boxes_data['Area'] = 0

        print("after:", boxes_data.shape)
        #print(boxes_data.head())
        if firstWrite == True:
            boxes_data.to_csv(saveName, index=False)
        else:
            boxes_data.to_csv(saveName, index=False, header=False, mode='a')
        firstWrite = False

def bboxAddBoxID(path:str, saveName:str, chunkSize:int):
    """Add BoxID to the bbox table.

    :param path: path of the bb-t1.csv.
    :type path: str.
    :param saveName: the save path of the result.
    :type saveName: str.
    :param chunkSize: size of the chunk.
    :type chunkSize: int.
    """

    chunks = pd.read_csv(path, sep=',', chunksize=chunkSize, dtype={'ImageID': object})
    firstWrite = True
    for boxes_data in chunks:
        print("before:", boxes_data.shape)      
        
        boxes_data['BoxID'] = boxes_data.index.map(lambda x: getHexString(x)) 
        
        #modify the order of the columns
        order = ['BoxID', 'ImageID', 'XMin', 'XMax', 'YMin', 'YMax', 'Area', 'IsOccluded', 'IsTruncated', 'IsGroupOf', 
                 'IsDepiction', 'IsInside', 'LuminanceMean', 'LuminanceStd', 'Category']
        boxes_data = boxes_data[order]
        
        print("after:", boxes_data.shape)
        if firstWrite == True:
            boxes_data.to_csv(saveName, index=False)
        else:
            boxes_data.to_csv(saveName, index=False, header=False, mode='a')
        firstWrite = False

#these tables are no longer in use
#def CreatebbT2toT5(col:str, path:str, saveName:str):  
#    """Create bb-t2 to bb-t6.

#    :param col: group by col name.
#    :type col: str.
#    :param path: path of the bb-t1.csv.
#    :type path: str.
#    :param saveName: save path of the result.
#    :type saveName: str.
#    """

#    boxes_data = pd.read_csv(path, sep=',', usecols=['BoxID', col], dtype={'BoxID': object})
#    print("before:", boxes_data.shape)
#    #groupby
#    gb = boxes_data.groupby(col)

#    result = pd.DataFrame(data=None, columns=[col, 'BoxIDList'])

#    for name, group in gb:
#        boxIDList = group['BoxID'].tolist()
#        newLine = pd.DataFrame({col: name, 'BoxIDList': [boxIDList]})
#        result = result.append(newLine)

#    print("after:", result.shape)
#    print(result.head())
#    result.to_csv(saveName, index=False)

def CreateCategory(path:str, saveName:str):
    """Create category table.

    :param path: path of the bb-t1.csv.
    :type path: str.
    :param saveName: save path of the result.
    :type saveName: str.
    """

    boxes_data = pd.read_csv(path, sep=',', usecols=['BoxID', 'ImageID', 'Category'], dtype={'BoxID': object, 'ImageID': object})
    print("before:", boxes_data.shape)
    #groupby
    gb = boxes_data.groupby('Category')
    
    result = pd.DataFrame(data=None, columns=['Category', 'BoxIDList', 'ImageIDList'])
    
    for name, group in gb:
        boxIDList = group['BoxID'].tolist()
        imageIDList = group['ImageID'].unique().tolist()
        newLine = pd.DataFrame({'Category': name, 'BoxIDList': [boxIDList], 'ImageIDList': [imageIDList]})
        result = result.append(newLine)
        
    print("after:", result.shape)
    print(result.head())
    result.to_csv(saveName, index=False)

def GetCategorys(imageID:str, gb, boxes_classes:pd.DataFrame, all_classes:pd.DataFrame, boxes_classes2:pd.DataFrame, all_classes2:pd.DataFrame, parents_dict:Dict) -> List:
    """Get categorys of an image.

    :param imageID: the image id.
    :type imageID: str.
    :param gb: the result of bb-t1 dataframe group by ImageID.
    :type gb: pandas.core.groupby.generic.DataFrameGroupBy.
    :param boxes_classes: box classes data.
    :type boxes_classes: pd.DataFrame.
    :param all_classes: all classes data.
    :type all_classes: pd.DataFrame.
    :param boxes_classes2: box classes2 data.
    :type boxes_classes2: pd.DataFrame.
    :param all_classes2: all classes2 data.
    :type all_classes2: pd.DataFrame.
    :param parents_dict: parents dictionary.
    :type parents_dict: Dict.
    :return: the categorys of the image.
    :rtype: List
    """

    result = []
    list_all = []
    try:
        group = gb.get_group(imageID)
    except KeyError:
        list_all = []
    else:    
        list_all = group['Category'].tolist()
               
    for labelDes in list_all:  
        labelName = getLabelName(labelDes, boxes_classes2, all_classes2)
        clists = getCategoryList(labelName, boxes_classes, all_classes, parents_dict)
     
        for cl in clists:
            ifAdd = True
            for r in result:
                if operator.eq(cl,r):
                    ifAdd = False
                    break
            if ifAdd:        
                result.append(cl)
    
    return result

def GetBoxIdList(imageID:str, gb) -> List:
    """Get box id list of an image.

    :param imageID: the image id.
    :type imageID: str.
    :param gb: the result of bb-t1 dataframe group by ImageID.
    :type gb: pandas.core.groupby.generic.DataFrameGroupBy.
    :return: the box id list of the image.
    :rtype: List
    """

    result = []
    try:
        group = gb.get_group(imageID)
    except KeyError:
        result = []
    else:
        result = group['BoxID'].tolist()
    return result   

def CreateImageT1(gb, path:str, saveName:str, firstWrite:bool, chunkSize:int, boxes_classes:pd.DataFrame, all_classes:pd.DataFrame, boxes_classes2:pd.DataFrame, all_classes2:pd.DataFrame, parents_dict:Dict):
    """Create image-t1 table.

    :param gb: the result of bb-t1 dataframe group by ImageID.
    :type gb: pandas.core.groupby.generic.DataFrameGroupBy.
    :param path: path of the image id file.
    :type path: str.
    :param saveName: save path of the result.
    :type saveName: str.
    :param firstWrite: if first wirte the file.
    :type firstWrite: bool.
    :param chunkSize: size of the chunk.
    :type chunkSize: int.
    :param boxes_classes: box classes data.
    :type boxes_classes: pd.DataFrame.
    :param all_classes: all classes data.
    :type all_classes: pd.DataFrame.
    :param boxes_classes2: box classes2 data.
    :type boxes_classes2: pd.DataFrame.
    :param all_classes2: all classes2 data.
    :type all_classes2: pd.DataFrame.
    :param parents_dict: parents dictionary.
    :type parents_dict: Dict.
    """

    chunks = pd.read_csv(path, sep=',', usecols=['ImageID'], dtype={'ImageID': object}, chunksize=chunkSize)
    for boxes_data in chunks:
        print("before:", boxes_data.shape)            
        boxes_data['BoxIDList'] = boxes_data['ImageID'].map(lambda x: getBoxIdList(x, gb))
        
        #set the column with a value of 0 and update it later
        boxes_data['ImageLuminanceMean'] = 0
        boxes_data['ImageLuminanceStd'] = 0
        boxes_data['ImageQualityMean'] = 0
        boxes_data['ImageQualityStd'] = 0
        
        boxes_data['CategoryList'] = boxes_data['ImageID'].map(lambda x: getCategorys(x, gb, boxes_classes, all_classes, boxes_classes2, all_classes2, parents_dict))
        
        print("after:", boxes_data.shape)
        #print(boxes_data.head())
        if firstWrite == True:
            boxes_data.to_csv(saveName, index=False)
        else:
            boxes_data.to_csv(saveName, index=False, header=False, mode='a')
        firstWrite = False

def CreateImageT2p1(path:str, saveName:str):
    """Create image-t2 table(step1).

    :param path: path of the bb-t1.csv.
    :type path: str.
    :param saveName: save path of the result.
    :type saveName: str.
    """

    boxes_data = pd.read_csv(path, sep=',', usecols=['BoxID', 'ImageID'], dtype={'BoxID': object, 'ImageID': object})
    print("before:", boxes_data.shape)
    
    gb = boxes_data['BoxID'].groupby(boxes_data['ImageID']) 
    result = gb.count()
    print("after:", result.shape)
    result.to_csv(saveName, header=['NumofBoundingBox'])

def CreateImageT2p2(path:str, saveName:str):
    """Create image-t2 table(step2).

    :param path: path of the step1 result.
    :type path: str.
    :param saveName: save path of the result.
    :type saveName: str.
    """

    boxes_data = pd.read_csv(path, sep=',', dtype={'ImageID': object})
    print("before:", boxes_data.shape)
    #groupby
    gb = boxes_data.groupby('NumofBoundingBox')

    result = pd.DataFrame(data=None, columns=['NumofBoundingBox', 'ImageIDList'])

    for name, group in gb:
        imageIDList = group['ImageID'].tolist()
        newLine = pd.DataFrame({'NumofBoundingBox': name, 'ImageIDList': [imageIDList]})
        result = result.append(newLine)

    print("after:", result.shape)
    print(result.head())
    result.to_csv(saveName, index=False)

def CreateImageT3(path_image_t1:str, path_image_url:str, saveName:str, chunkSize:int):
    """Create image-t3 table.

    :param path_image_t1: path of the image-t1.csv.
    :type path_image_t1: str.
    :param path_image_url: path of the file contains ImageID and Url.
    :type path_image_url: str.
    :param saveName: save path of the result.
    :type saveName: str.
    :param chunkSize: size of the chunk.
    :type chunkSize: int.
    """

    chunks = pd.read_csv(path_image_t1, sep=',', usecols=['ImageID'], dtype={'ImageID': object}, chunksize=chunkSize)
    url_data = pd.read_csv(path_image_url, sep=',', usecols=['ImageID' ,'Url'], dtype={'ImageID': object, 'Url': object})
    print('url_data:', url_data.shape)
    firstWrite = True
    for boxes_data in chunks:
        print("before:", boxes_data.shape)                       
        boxes_data = pd.merge(boxes_data, url_data, on='ImageID', how='inner')     
        print("after:", boxes_data.shape)
        if firstWrite:
            boxes_data.to_csv(saveName, index=False)
        else:
            boxes_data.to_csv(saveName, index=False, header=False, mode='a')
        firstWrite = False