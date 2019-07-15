# Copyright 2017 The KaiJIN Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""We using iaa as backend to process a variety of metas info.
  There, two method has implemented.
  `MetaAugment` for collectively augments (image, bbox, mask, segmentation, kps)
  `Compose` for just augments image by:
  Compse([
    ...,
  ])
"""
import math
import numpy as np
import imgaug as ia
from imgaug import augmenters as iaa


class MetaAugment():
  def __init__(self, transform):
    self.aug = transform

  def _aug_bbox(self, bboxes, img_h, img_w, det=None):
    """det is a self.aug.to_deterministic()"""
    if det is None:
      det = self.aug.to_deterministic()

    # construct ia bounding box class
    ia_bbs = [ia.BoundingBox(*bbox, label=i) for i, bbox in enumerate(bboxes)]

    # sticky on image
    ia_bbs_img = ia.BoundingBoxesOnImage(ia_bbs, (img_h, img_w))

    # augment
    aug_bbs = det.augment_bounding_boxes(ia_bbs_img)

    # remove out exterior
    refine_bbs = aug_bbs.remove_out_of_image(
        fully=True, partly=False).clip_out_of_image()

    # new idx
    bbs_idx = [bbox.label for bbox in refine_bbs.bounding_boxes]
    bbs_list = refine_bbs.to_xyxy_array().tolist()

    # bbs_idx e.g. [0, 1, 3, 5, 6]
    return bbs_list, bbs_idx

  def _aug_polygon(self, polygons, img_h, img_w, det=None):
    if det is None:
      det = self.aug.to_deterministic()

    # construct ia polygons
    ia_pgs = []
    for p in polygons:
      ia_pgs.append(ia.Polygon([i for i in zip(p[0][::2], p[0][1::2])]))

    # stick on image
    ia_pgs_img = ia.PolygonsOnImage(ia_pgs, shape=(img_h, img_w))
    aug_pgs = det.augment_polygons(ia_pgs_img).polygons

    # return
    pgs_list = [[p.exterior.reshape([-1]).tolist()] for p in aug_pgs]
    return pgs_list

  def __call__(self, image, label=None, bbox=None,
               polygon=None, heatmap=None, kps=None):
    """
    Args:
      image: [H, W, C].
      label: [N] for bbox, it may be changed by filtering bbox.
      bbox: [N, 4] xyxy.
      polygon:

    Returns:
      augmentors (dict{'images':, 'bboxes':, 'polygons':})
    """
    # check
    assert isinstance(image, np.ndarray)
    assert len(image.shape) == 3
    ret = {}

    # determinstic for images
    det = self.aug.to_deterministic()

    # augment and assign to ret
    h, w, c = image.shape
    _image = det.augment_image(image)
    ret['image'] = _image

    # augment bbox
    if bbox:
      bbox_list, bbox_idx = self._aug_bbox(bbox, h, w, det)
      ret['bbox'] = bbox_list
      ret['bbox_idx'] = bbox_idx
      # filtering labels
      assert label is not None
      _label = [label[i] for i in bbox_idx]
      ret['label'] = _label

    # augment masks
    if polygon:
      _polygon = self._aug_polygon(polygon, h, w, det)
      if 'bbox_idx' in ret:
        _polygon = [_polygon[i] for i in ret['bbox_idx']]

    if heatmap:
      raise NotImplementedError

    if kps:
      raise NotImplementedError

    return ret


class Compose():
  def __init__(self, transforms):
    self.transforms = transforms

  def __call__(self, img):
    """img should have shape [n, h, w, c] / [h, w, c] / [h, w]
    Rets:
      image with shape: [n, c, h, w]
    """
    assert 4 >= len(img.shape) >= 2
    if len(img.shape) == 2:
      img = np.reshape(img, [1] + list(img.shape) + [1])
    elif len(img.shape) == 3:
      img = np.reshape(img, [1] + list(img.shape))
    if img.shape[3] == 1:
      img = GreyToRGB()(img)
    if img.shape[3] == 4:
      img = img[:, :, :, 0:3]
    assert img.shape[3] == 3
    # transform
    for t in self.transforms:
      img = t(img)
    return img

  def __repr__(self):
    format_string = self.__class__.__name__ + '('
    for t in self.transforms:
      format_string += '\n'
      format_string += '    {0}'.format(t)
    format_string += '\n)'
    return format_string


class RandomFlipLR():
  def __init__(self, prob=0.5):
    self.fn = iaa.Fliplr(prob)

  def __call__(self, images):
    assert len(images.shape) == 4
    return self.fn(images=images)


class RandomFlipUD():
  def __init__(self, prob=0.5):
    self.fn = iaa.Flipud(prob)

  def __call__(self, images):
    assert len(images.shape) == 4
    return self.fn(images=images)


class Crop():
  def __init__(self, left, right, top, bottom):
    self.fn = iaa.Crop(px=(top, right, bottom, left))

  def __call__(self, images):
    assert len(images.shape) == 4
    return self.fn(images=images)


class Pad():
  def __init__(self, left, right, top, bottom):
    self.fn = iaa.Pad(px=(left, right, top, bottom), keep_size=False)

  def __call__(self, images):
    assert len(images.shape) == 4
    return self.fn(images=images)


class GreyToRGB():
  def __call__(self, images):
    assert len(images.shape) == 4
    if images.shape[3] == 1:
      return np.stack((images,) * 3, axis=3).squeeze(axis=4)
    return images


class RandomCropAndPadToFixedSize():
  def __init__(self, h, w):
    self.fn = iaa.Sequential([
        iaa.PadToFixedSize(width=w, height=h),
        iaa.CropToFixedSize(width=w, height=h)
    ])

  def __call__(self, images):
    assert len(images.shape) == 4
    return np.array(self.fn(images=images))


class RandomSizeCrop():
  def __init__(self, edge):
    """random crop [0, edge] for each border"""
    self.fn = iaa.Crop(px=(0, edge))

  def __call__(self, images):
    assert len(images.shape) == 4
    return self.fn(images=images)


class Scale():
  def __init__(self, scale=255.):
    self.scale = float(scale)

  def __call__(self, images):
    assert len(images.shape) == 4
    return np.divide(images, self.scale)


class Normalize():
  def __init__(self, mean, std):
    self.mean = mean
    self.std = std

  def __call__(self, images):
    assert len(images.shape) == 4
    n_img = []
    for image in images:
      n_img.append((image - self.mean) / self.std)
    return np.array(n_img)


class Standardize():
  def __call__(self, images):
    assert len(images.shape) == 4
    n, h, w, c = images.shape
    images = images.astype('float32')
    for idx in range(n):
      min_std = 1.0 / math.sqrt(float(h * w * c))
      adjust_std = max(np.std(images[idx]), min_std)
      images[idx] = (images[idx] - np.mean(images[idx])) / adjust_std
    return images


class Resize():
  def __init__(self, h, w, interploate='nearest'):
    # ``nearest``, ``linear``, ``area`` or ``cubic``
    self.fn = iaa.Resize(size={'height': h, 'width': w},
                         interpolation=interploate)

  def __call__(self, images):
    return self.fn(images=images)


class GrayScale():
  def __init__(self):
    self.fn = iaa.Grayscale(alpha=1.0)

  def __call__(self, images):
    return self.fn(images=images)


class RandomGrayScale():
  def __init__(self, low, high):
    self.fn = iaa.Grayscale(alpha=(low, high))

  def __call__(self, images):
    return self.fn(images=images)


class RandomHueAndSaturation():
  def __init__(self, low, high):
    self.fn = iaa.AddToHueAndSaturation((low, high))

  def __call__(self, images):
    return self.fn(images=images)


if __name__ == "__main__":
  def test1():
    aug = MetaAugment(iaa.SomeOf((6, 6), [
        iaa.GaussianBlur((0.0, 5.0)),
        iaa.Multiply((0.5, 1.5)),
        iaa.Grayscale(alpha=(0.0, 1.0)),
        iaa.Fliplr(0.5),
        iaa.Flipud(0.5),
        iaa.OneOf([iaa.Affine(rotate=90),
                   iaa.Affine(rotate=180),
                   iaa.Affine(rotate=270)]),
    ]))

    import cv2
    from matplotlib import pyplot as plt

    img = cv2.imread('asserts/crowd.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    plt.subplot(121)
    plt.axis('off')
    plt.imshow(img)

    plt.subplot(122)
    plt.axis('off')
    img = aug(img)['image']
    plt.imshow(img)

    plt.show()

  def test2():
    import cv2
    from matplotlib import pyplot as plt

    img = cv2.imread('asserts/crowd.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    transform = Compose([
        Scale(255),
        Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    img1 = transform(img)[0]

    plt.subplot(121)
    plt.axis('off')
    plt.imshow(img)

    plt.subplot(122)
    plt.axis('off')
    plt.imshow(img1)

    plt.show()

  test2()
