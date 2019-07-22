import pandas as pd
import datetime
import numpy as np
import os
import math

def ConcatAll(path_imageIds_train:str, path_imageIds_test:str, path_imageIds_validation:str) -> pd.DataFrame:
    """Concat all the imageid files.

    :param path_imageIds_train: the path of the imageid train file.
    :type path_imageIds_train: str.
    :param path_imageIds_test: the path of the imageid test file.
    :type path_imageIds_test: str.
    :param path_imageIds_validation: the path of the imageid validation file.
    :type path_imageIds_validation: str.
    :return: the concat result.
    :rtype: pd.DataFrame
    """

    boxes_imageIds_train = pd.read_csv(path_imageIds_train, sep=',')
    boxes_imageIds_test = pd.read_csv(path_imageIds_test, sep=',')
    boxes_imageIds_validation = pd.read_csv(path_imageIds_validation, sep=',')
    print('Data shapes:')
    print(boxes_imageIds_train.shape)
    print(boxes_imageIds_test.shape)
    print(boxes_imageIds_validation.shape)
    boxes_imageIds_all = pd.concat([boxes_imageIds_train, boxes_imageIds_test, boxes_imageIds_validation], ignore_index=True)
    return boxes_imageIds_all

def GetWip(path:str, nSet:set, saveName:str):
    """Remove images that do not exist.

    :param path: the path of the file.
    :type path: str.
    :param nSet: the set of imageids that to reserve.
    :type nSet: set.
    :param saveName: the path you want to save.
    :type saveName: str.
    """

    df = pd.read_csv(path, sep=',')
    print('before:', df.shape)
    df = df[df['ImageID'].isin(nSet)]
    print('after:', df.shape)
    df.to_csv(saveName, index=False)

def CheckId(path:str, column:str, length:int) -> int:
    """Check the ImageID's or BoxID's length.

    :param path: the path of the file.
    :type path: str.
    :param column: the column name to be checked.
    :type column: str.
    :param length: the column length.
    :type length: int.
    :return: the count of incorrect ones.
    :rtype: int
    """

    r = 0
    df = pd.read_csv(path, dtype={column: object})
    idList = df[column].tolist()
    for s in idList:
        if len(s)!=length:
            r += 1
    return r 




