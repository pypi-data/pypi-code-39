import pandas as pd
import datetime
import numpy as np
import os
import math

#chunkSize = 100000

def MergeImageInfo(rootdir:str, saveName:str, mode:str):
    """Merge the spark image result into a file.

    :param rootdir: the root dir of the data.
    :type rootdir: str.
    :param saveName: path to save result.
    :type saveName: str.
    :param mode: write mode('w' or 'a').
    :type mode: str.
    """

    with open(saveName, mode) as infoFile:
        if(mode=='w'):
            infoFile.write('ImageID,Mode,Width,Height,ImageLuminanceMean,ImageLuminanceStd\n')
        filelist = os.listdir(rootdir)
        for i in range(0,len(filelist)):
            path = os.path.join(rootdir, filelist[i])
            if os.path.isfile(path) and 'part' in path:
                with open(path, 'r') as f:     
                    content = [line.rstrip('\n').strip('()').replace("'","") for line in f]
                    for con in content:
                        temp = con.split(', ')
                        s = temp[0]
                        imageId = s[len(s)-20:len(s)][0:16]
                        newLine = imageId+','+temp[1]+'\n'
                        infoFile.write(newLine)

def ImageT1UpdateWidthAndHeightAndLuminance(path_image_t1:str, path_image_data:str, saveName:str, chunkSize:int):
    """Update image-t1 table's Width, Height, Luminance.

    :param path_image_t1: path of the image-t1 table.
    :type path_image_t1: str.
    :param path_image_data: path of the spark info file.
    :type path_image_data: str.
    :param saveName: path to save result.
    :type saveName: str.
    :param chunkSize: chunk size.
    :type chunkSize: int.
    """

    chunks = pd.read_csv(path_image_t1, sep=',', dtype={'ImageID': object}, chunksize=chunkSize)
    image_data = pd.read_csv(path_image_data, sep=',', dtype={'ImageID': object})
    firstWrite = True
    for c in chunks:
        print("before:", c.shape)       
        #delete Width, Height, Mode, ImageLuminanceMean, ImageLuminanceStd
        c.drop(columns=['Width', 'Height', 'Mode', 'ImageLuminanceMean', 'ImageLuminanceStd'], inplace=True)
        c = pd.merge(c, image_data, on='ImageID', how='inner')   
        print("after:", c.shape)
        if firstWrite:
            c.to_csv(saveName, index=False)
        else:
            c.to_csv(saveName, index=False, header=False, mode='a')
        firstWrite = False

def bbT1UpdateXY(path_bb_t1:str, path_image_t1:str, saveName:str, chunkSize:int):
    """Update bb-t1 table's XMin,YMin,XMax,YMax.

    :param path_bb_t1: path of the image-t1 table.
    :type path_bb_t1: str.
    :param path_image_t1: path of the image-t1 table.
    :type path_image_t1: str.
    :param saveName: path to save result.
    :type saveName: str.
    :param chunkSize: chunk size.
    :type chunkSize: int.
    """

    chunks = pd.read_csv(path_bb_t1, sep=',', dtype={'BoxID': object, 'ImageID': object}, chunksize=chunkSize)
    image_data = pd.read_csv(path_image_t1, sep=',', usecols=['ImageID', 'Width', 'Height'], dtype={'ImageID': object})
    firstWrite = True
    for c in chunks:
        print("before:", c.shape)       
        c = pd.merge(c, image_data, on='ImageID', how='inner')    
        c.eval('XMin = XMin*Width', inplace=True)
        c.eval('YMin = YMin*Height', inplace=True)
        c.eval('XMax = XMax*Width', inplace=True)
        c.eval('YMax = YMax*Height', inplace=True)
        
        c['XMin'] = c['XMin'].map(lambda x: math.floor(x))
        c['YMin'] = c['YMin'].map(lambda x: math.floor(x))
        
        c['XMax'] = c['XMax'].map(lambda x: math.ceil(x))
        c['YMax'] = c['YMax'].map(lambda x: math.ceil(x))
        
        c.eval('Area = (XMax-XMin)*(YMax-YMin)', inplace=True)
        
        #delete Width,Height
        c.drop(columns=['Width', 'Height'], inplace=True)
        print("after:", c.shape)
        if firstWrite:
            c.to_csv(saveName, index=False)
        else:
            c.to_csv(saveName, index=False, header=False, mode='a')
        firstWrite = False

def MergeBoxInfo(rootdir:str, saveName:str, mode:str):
    """Merge the spark box result into a file.

    :param rootdir: the root dir of the data.
    :type rootdir: str.
    :param saveName: path to save result.
    :type saveName: str.
    :param mode: write mode('w' or 'a').
    :type mode: str.
    """

    with open(saveName, mode) as infoFile:
        if(mode=='w'):
            infoFile.write('BoxID,LuminanceMean,LuminanceStd\n')
        filelist = os.listdir(rootdir)
        for i in range(0,len(filelist)):
            path = os.path.join(rootdir, filelist[i])
            if os.path.isfile(path) and 'part' in path:
                with open(path, 'r') as f:     
                    content = [line.rstrip('\n').strip('()').replace("'","") for line in f]
                    for con in content:
                        temp = con.split(', ')
                        s = temp[0]
                        imageId = s[len(s)-20:len(s)][0:16]
                        newLine = imageId+','+temp[1]+'\n'
                        infoFile.write(newLine)

def bbT1UpdateLuminance(path_bb_t1:str, path_image_info:str, saveName:str, chunkSize:int):
    """Update bb-t1 table's Luminance.

    :param path_bb_t1: path of the bb-t1 table.
    :type path_bb_t1: str.
    :param path_image_info: path of the spark info file.
    :type path_image_info: str.
    :param saveName: path to save result.
    :type saveName: str.
    :param chunkSize: chunk size.
    :type chunkSize: int.
    """

    chunks = pd.read_csv(path_bb_t1, sep=',', dtype={'BoxID': object, 'ImageID': object}, chunksize=chunkSize)
    image_data = pd.read_csv(path_image_info, sep=',', dtype={'BoxID': object})
    firstWrite = True
    for c in chunks:
        print("before:", c.shape) 
        #delete LuminanceMean,LuminanceStd
        c.drop(columns=['LuminanceMean', 'LuminanceStd'], inplace=True)
        c = pd.merge(c, image_data, on='BoxID', how='inner')    
        print("after:", c.shape)
        if firstWrite:
            c.to_csv(saveName, index=False)
        else:
            c.to_csv(saveName, index=False, header=False, mode='a')
        firstWrite = False