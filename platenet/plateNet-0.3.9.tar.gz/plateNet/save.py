import json

import cv2

from plateNet.folder import generateOutputFolder
import xml.etree.cElementTree as ET
from plateNet.tools import getTime


class Saver:

    def __init__(self, imagePath, savefolder="plates"):
        self.imagePath = imagePath
        self.savefolder = savefolder
        self.mainPath, self.filename =generateOutputFolder(imagePath, savefolder)

    def saveJSON(self, boxes,confidence):
        json_fileName = "{}/{}.json".format(self.mainPath, self.filename)
        boxes = {
            'Date': getTime() ,
            'File': "{}".format(self.imagePath),
            'Confidence': confidence,
            'X': boxes[0],
            'Y': boxes[1],
            'W': boxes[2],
            'H': boxes[3]
        }
        with open(json_fileName, 'w') as json_file:
            json.dump(boxes, json_file, ensure_ascii=False, indent=4)


    def saveXML(self,boxes,confidence):
        xml_fileName = "{}/{}.xml".format(self.mainPath, self.filename)

        root = ET.Element("PlateNet")
        features = ET.SubElement(root, "features")

        ET.SubElement(features, "date", name="detect time").text = getTime()
        ET.SubElement(features, "file", name="input image").text = self.imagePath
        ET.SubElement(features, "conf", name="confidence").text = str(confidence)

        position = ET.SubElement(features,"position")
        ET.SubElement(position, "x", name="x coord").text = str(boxes[0])
        ET.SubElement(position, "y", name="y coord").text = str(boxes[1])
        ET.SubElement(position, "w", name="width").text = str(boxes[2])
        ET.SubElement(position, "h", name=" height").text = str(boxes[3])

        tree = ET.ElementTree(root)
        tree.write(xml_fileName)
    def savePNG(self, img):
        # original resim + plaka işaretli resim
        # result_img = Combine(imutils.resize(origImg, width=size), plotted)

        # result_name = "{}/{}_combine.png".format(mainPath, input_file_name)
        # cv2.imwrite(result_name, result_img)

        if img is not None:
            imgName = "{}/{}.png".format(self.mainPath, self.filename)
            cv2.imwrite(imgName, img)

    # def saver(currentImg,plate,boxes):

    # savePNG(main_path,currentImg,plate)
    # saveJSON(main_path,currentImg,boxes[0])
