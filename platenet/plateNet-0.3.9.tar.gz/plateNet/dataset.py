import os
from pathlib import Path

import cv2
import imutils

import plateNet.color as color
from plateNet.folder import generateFolder
from plateNet.tools import message


class DatasetManager:
    def __init__(self, imgList: list):
        self.imgList = imgList

    def create(self, width: int=448,
               angle: float = .0,
               savefolder:str=None):
        message("preparing dataset...", color.CYELLOW2)

        resultList = []
        for imgPath in self.imgList:
            # print("img : "+imgPath)
            img = cv2.imread(imgPath)
            rotatedImg = imutils.rotate(img, angle)
            resizedImg = imutils.resize(rotatedImg, width)
            resultList.append(resizedImg)
            if savefolder is not None:
                # mainPath = os.path.join(imgPath.split("/")[:-1])

                mainPath = generateFolder(Path(imgPath).parent, savefolder)
                filename = imgPath.split("/")[-1]
                savename = os.path.join(mainPath, filename)
                cv2.imwrite(savename, resizedImg)
        message("dataset ready to use...", color.CYELLOW2)
        return resultList
