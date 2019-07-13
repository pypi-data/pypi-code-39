#!/usr/bin/env python
import cv2
import math
# import tracking_util.utils.gtutils as gtutils
from . import gtutils


def draw_gtrect(img_list, gtrect_list, normed_gt=False,
        thickness=2, color='blue'):
    assert len(img_list) == len(gtrect_list)

    if normed_gt:
        imgw, imgh, _ = img_list[0].shape
        regular_gtrect_list = gtutils.norm_to_regular(gtrect_list, imgw, imgh)
    else:
        regular_gtrect_list = gtrect_list

    if type(color) is str:
        assert color in ['blue', 'green', 'red'], "Not supported color"
        if color == 'blue':
            color_vec = (255, 0, 0)
        elif color == 'green':
            color_vec = (0, 255, 0)
        elif color == 'red':
            color_vec = (0, 0, 255)
    else:
        assert len(color) == 3
        color_vec = color

    for img, gtrect in zip(img_list, regular_gtrect_list):
        if not math.isnan(gtrect[0]):
            x, y, w, h = gtrect
            pt1 = (int(x), int(y))
            pt2 = (int(x + w), int(y + h))
            cv2.rectangle(img, pt1, pt2, color_vec, thickness)

    # return img_list
