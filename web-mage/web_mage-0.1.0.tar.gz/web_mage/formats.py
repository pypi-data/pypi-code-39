
from math import floor
import os

class ImageFormat(object):
    """
        Describes a set of requirements that an image must meet after the optimization
        process.
    """
    def __init__(self, max_width=None,
                       max_height=None,
                       max_size_bytes=None,
                       min_quality=60,
                       tag="optimized"):
        self.max_width = max_width
        self.max_height = max_height
        self.max_size_bytes = max_size_bytes
        self.min_quality = min_quality
        self.tag = tag

    def get_tagged_filename(self, filename):
        (base_filename, extension) = os.path.splitext(os.path.basename(filename))
        return base_filename + "_" + self.tag + extension

    def dimensions_for_image(self, image):
        (current_height, current_width) = image.size
        target_ratio = 1

        if self.max_height is not None and self.max_height < current_height:
            target_ratio = min(target_ratio, self.max_height / current_height)
        
        if self.max_width is not None and self.max_width < current_width:
            target_ratio = min(target_ratio, self.max_width / current_width)

        return ((floor(current_height * target_ratio), floor(current_width * target_ratio)), self.min_quality)
            

FULL_WIDTH_27_OR_30_INCH = 2560

# Common image format presets

IMG_FORMAT_DEFAULT = ImageFormat()

IMG_FORMAT_THUMBNAIL_LARGE = ImageFormat(max_width=320, max_height=320, tag="thumbnail_lg")
IMG_FORMAT_THUMBNAIL_LARGE_DOUBLE = ImageFormat(max_width=640, max_height=640, tag="thumbnail_lg_x2")

IMG_FORMAT_AVATAR_LARGE = ImageFormat(max_width=100, max_height=100, tag="avatar_lg")
IMG_FORMAT_AVATAR_MEDIUM = ImageFormat(max_width=80, max_height=80, tag="avatar_md")
IMG_FORMAT_AVATAR_SMALL = ImageFormat(max_width=60, max_height=60, tag="avatar_sm")

IMG_FORMAT_CONTENT_LARGE = ImageFormat(max_width=1280, max_height=960, tag="content_lg")
IMG_FORMAT_CONTENT_MEDIUM = ImageFormat(max_width=960, max_height=720, tag="content_md")
IMG_FORMAT_CONTENT_SMALL = ImageFormat(max_width=720, max_height=540, tag="content_sm")
