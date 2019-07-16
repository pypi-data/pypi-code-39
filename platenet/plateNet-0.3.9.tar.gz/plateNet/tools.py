import sys
from datetime import datetime

import cv2
import numpy as np

import plateNet.color as color


def merge(first, second):
    """
    merge two images horizontally
    :param first:image(numpy array) will on the left
    :param second:image(numpy array) will on the right
    :return:
    """
    ha, wa = first.shape[:2]
    hb, wb = second.shape[:2]
    max_height = np.max([ha, hb])
    total_width = wa + wb
    new_img = np.zeros(shape=(max_height, total_width, 3))
    new_img[:ha, :wa] = first
    new_img[:hb, wa:wa + wb] = second

    return new_img


def contrast(image, clipLimit=4.0, tileGridSize=(8, 8)):
    """
    Apply more contrast to image
    :param image: image(numpy array)
    :param clipLimit: Threshold for contrast limiting.
    :param tileGridSize: Size of grid for histogram equalization. Input image will be divided into
                         equally sized rectangular tiles. tileGridSize defines the number of tiles in row and column
    :return:
    """
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=tileGridSize)
    cl = clahe.apply(l)

    limg = cv2.merge((cl, a, b))
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    return final


def getPlate(origImg, currentImg, coord):
    # coord[0] = x
    # coord[1] = y
    # coord[2] = w
    # coord[3] = h
    x_rate = origImg.shape[0] / currentImg.shape[0]
    y_rate = origImg.shape[1] / currentImg.shape[1]

    new_x = int(coord[0] * x_rate)
    new_y = int(coord[1] * y_rate)
    new_w = int(coord[2] * x_rate)
    new_h = int(coord[3] * y_rate)

    return origImg[new_y - 1:new_y + new_h + 1, new_x - 1:new_x + new_w + 1]


def extractPlate(img, boxes, idxs):
    if len(idxs) > 0:
        for i in idxs.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            return img[y:y + h, x:x + w]


def plot(orig_img, rotated_img, mboxes, confidences, idxs, plate_ratio=1, expected_confidence=.5, thickness=1):
    (H, W) = rotated_img.shape[:2]

    plate_area = None

    if len(idxs) > 0:
        for i in idxs.flatten():
            # tespit edilen plaka özellikleri
            (x, y) = (mboxes[i][0], mboxes[i][1])
            (w, h) = (mboxes[i][2], mboxes[i][3])

            # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # apply_lab(image)
            # image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

            if confidences[i] > expected_confidence:
                # sol üst
                cv2.line(rotated_img,
                         pt1=(x, y),
                         pt2=(0, H - plate_ratio * h),
                         color=color.orange,
                         thickness=thickness)
                # sağ üst
                cv2.line(rotated_img,
                         pt1=(x + w, y),
                         pt2=(plate_ratio * w, H - plate_ratio * h),
                         color=color.orange,
                         thickness=thickness)
                # sağ alt
                cv2.line(rotated_img,
                         pt1=(x + w, y + h),
                         pt2=(plate_ratio * w, H),
                         color=color.orange,
                         thickness=thickness)
                # sol alt
                cv2.line(rotated_img,
                         pt1=(x, y + h),
                         pt2=(0, H),
                         color=color.orange,
                         thickness=thickness)
                # original halinden bulunan plaka alanını al
                plate_area = orig_img[
                             y:y + h,
                             x:x + w]
                # # find_contours(plate_area)
                # plate_area = getPlate(rotated_img, [H, W], [x, y, w, h])
                # plakayı plate_ratio oranında büyülterek sol altta göster
                rotated_img[H - plate_ratio * h:H, 0:plate_ratio * w] = cv2.resize(plate_area, (plate_ratio * w,
                                                                                                plate_ratio * h))
                # Büyük formdaki plakaya çerçeve yap
                cv2.rectangle(rotated_img,
                              pt1=(0, H - plate_ratio * h),
                              pt2=(plate_ratio * w, H),
                              color=color.orange,
                              thickness=thickness)
                # confidence değeri arkaplanı
                cv2.rectangle(rotated_img, (x, y - h), (x + w, y), color.black, cv2.FILLED)
                # confidence değeri
                text = "%{:.2f}".format(confidences[i] * 100)
                cv2.putText(rotated_img, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 150, 250), 1)

                # plaka çerçevesi
                cv2.rectangle(rotated_img, (x, y), (x + w, y + h), color.orange, thickness)

    else:
        cv2.line(rotated_img, (0, 0), (rotated_img.shape[1], rotated_img.shape[0]), color.red, 5)
        cv2.line(rotated_img, (rotated_img.shape[1], 0), (0, rotated_img.shape[0]), color.red, 5)

    return rotated_img, plate_area


def getTime():
    """
    get current time formatted type
    :return:
    """
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return now


def message(message: str, color=color.CBOLD):
    """
    print colored text message
    :param message: message to be written
    :param color:message text color from
    :return:
    """
    sys.stderr.write("\n%s" % color + "[%s] " % getTime() + message.strip() + '\x1b[0m\n')
