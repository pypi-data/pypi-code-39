#!/usr/bin/env python


def norm_to_regular(norm_gts, img_w, img_h):

    regular_gts = []
    for c in norm_gts:
        x, y, w, h = c
        xr, yr, wr, hr = x * img_w, y * img_h, w * img_w, h * img_h
        regular_gts.append([xr, yr, wr, hr])

    return regular_gts


def regular_to_norm(regular_gts, img_w, img_h):

    normed_gts = []
    for c in regular_gts:
        x, y, w, h = c
        xr, yr, wr, hr = x / img_w, y / img_h, w / img_w, h / img_h
        normed_gts.append([xr, yr, wr, hr])

    return normed_gts

def type_convert(gt_list, src_type, tar_type='xywh'):
    if src_type == 'xyxy' and tar_type == 'xywh':
        return xyxy_to_xywh(gt_list)
    elif src_type == 'xywh' and tar_type == 'xyxy':
        return xywh_to_xyxy(gt_list)
    elif src_type == 'xyxy' and tar_type == 'yxyx':
        return xyxy_to_yxyx(gt_list)
    else:
        print("Not implemented conversion")
        exit(1)

def xywh_to_xyxy(xywh_boxes):
    xyxy_boxes = []
    for b in xywh_boxes:
        x, y, w, h = b
        x1 = x + w
        y1 = y + h
        xyxy_boxes.append([x, y, x1, y1])
    return xyxy_boxes


def xyxy_to_xywh(xyxy_boxes):
    xywh_boxes = []
    for b in xyxy_boxes:
        x, y, x1, y1 = b
        w = x1 - x
        h = y1 - y
        xywh_boxes.append([x, y, w, h])
    return xywh_boxes


def xyxy_to_yxyx(xyxy_boxes):
    yxyx_boxes = []
    for b in xyxy_boxes:
        x, y, x1, y1 = b
        yxyx_boxes.append([y, x, y1, x1])
    return yxyx_boxes
