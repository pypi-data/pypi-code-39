from operator import itemgetter

import cv2
import imutils
import numpy as np
import sys
from plateNet.save import Saver
import plateNet.color as color
from plateNet.tools import contrast
from plateNet.tools import message
from plateNet.tools import extractPlate


class PlateNetDetector:
    def __init__(self, paths: list):

        message("reading model..", color.CGREEN)
        try:
            self.net = cv2.dnn.readNetFromDarknet(paths[0], paths[1])
            self.layer_names = [self.net.getLayerNames()[index[0] - 1] for index in self.net.getUnconnectedOutLayers()]
        except:
            message("failed to load model", color.CRED)
            sys.exit()

    def fromList(self,
                 imgList: list,
                 angleRange: tuple = (-5, 5),
                 size: int = 448,
                 unitAngle: float = .1,
                 expected_confidence: float = .5):

        self.__from_folder(imgList, angleRange, expected_confidence, size, unitAngle)

    def __from_folder(self, imgList, angleRange, expected_confidence, size, unitAngle):
        startAngle, stopAngle = angleRange
        startAngle = startAngle * 10
        stopAngle = stopAngle * 10
        message("detecting plates...", color.CYELLOW2)
        if len(imgList) > 0:
            message("{} images found".format(len(imgList)), color.CBOLD)
            for currentImg in imgList:
                origImg = contrast(cv2.imread(currentImg))
                combinations_img = []
                for angle in range(startAngle, stopAngle):
                    rotated_img = imutils.rotate(origImg, angle * unitAngle)
                    detected_prob = self.__detect(rotated_img, expected_confidence, size)
                    combinations_img.append(detected_prob)

                plate, confidences, boxes = max(combinations_img, key=itemgetter(1))
                message("[{}/{}] {} : {}".format(imgList.index(currentImg) + 1,
                                                 len(imgList),
                                                 currentImg,
                                                 confidences), color.CBOLD)

                if len(boxes) != 0:
                    saver = Saver(currentImg)
                    saver.savePNG(plate)
                    saver.saveJSON(boxes[0], confidences[0])
                    saver.saveXML(boxes[0], confidences[0])

    def __detect(self, image, expected_confidence, IMG_SIZE):
        boxes = []
        confidences = []
        # H = Height of image
        # W = width of image
        (H, W) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (IMG_SIZE, IMG_SIZE), swapRB=True, crop=False)
        self.net.setInput(blob)
        layer_outputs = self.net.forward(self.layer_names)

        for output in layer_outputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
                # take care when higher ... else skip this
                if confidence > expected_confidence:
                    # print("founded plate confidences : %.2f" % confidence)
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")
                    # x,y positions of detected plate
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))

        idxs = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.5, nms_threshold=0.5)

        # image, plateArea = plot(orig_img,
        #                          image,
        #                          boxes,
        #                          confidences=confidences,
        #                          idxs=idxs,
        #                          expected_confidence=expected_confidence)
        plateArea = extractPlate(image, boxes, idxs)

        return plateArea, confidences, boxes
