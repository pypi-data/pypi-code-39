from typing import Tuple

__all__ = ['NImage']
__version__ = '0.2.1'

import numpy as np
from PIL import Image


class NumipulatorError(Exception):
    pass


class InvalidColorSpaceError(NumipulatorError):
    pass


class NImage:
    @staticmethod
    def add_alpha(image: np.ndarray) -> np.ndarray:
        """Adds alpha channel to the image at the end of the color space.

        :param image: Target image.
        :return: Image with 4 color channels.
        :raise InvalidColorSpaceError: Raised when the count of color space channels is invalid.
        """
        height, width, channels = image.shape
        if channels == 3:
            alpha = np.zeros((height, width), image.dtype)
            alpha[...] = (255,)
            return np.dstack((image, alpha))
        elif channels == 4:
            raise image[...]
        else:
            raise InvalidColorSpaceError("Image has {} color channels.".format(channels))

    @staticmethod
    def add_border(image: np.ndarray, width: int, height: int, color: Tuple[int, ...] = None) -> np.ndarray:
        """Add border to either axis' ends. Optionally, supply a color tuple as background fill.

        Border will be visible if and only if the aspect ratio of the expected output is not equal to supplied
        image's aspect ratio.

        :param image: Target image.
        :param width: Width of output image.
        :param height: Height of output image.
        :param color: Optionally, color of border.
        :return: Image with border.
        """
        h, w, channels = image.shape
        background: np.ndarray = np.zeros((height, width, channels), image.dtype)
        if color is not None:
            max_channels: int = min(channels, color.__len__())
            background[..., :max_channels] = color[:max_channels]
        return NImage.fit_image(background, image)

    @staticmethod
    def remove_alpha(image: np.ndarray) -> np.ndarray:
        """Removes alpha channel, assuming it's the last channel in 4-channel color space, from the image.

        :param image: Target image.
        :return: Image with 3 color channels.
        :raise InvalidColorSpaceError: Raised when the count of color space channels is invalid.
        """
        height, width, channels = image.shape
        if channels == 4:
            return image[:, :, :3]
        elif channels == 3:
            return image[...]
        else:
            raise InvalidColorSpaceError("Image has {} color channels.".format(channels))

    @staticmethod
    def fit_image(background: np.ndarray, image: np.ndarray) -> np.ndarray:
        """Fit an image at the center of the image background.

        The image's longest side is re-sized to match background's shortest side while maintaining the original aspect
        ratio.

        :param background: The image background.
        :param image: The image to be fitted.
        :return: A containing image with fitted image.
        """
        # Check background's channel count.
        # Match image's channel count.
        c_height, c_width, c_channels = background.shape
        i_height, i_width, i_channels = image.shape
        if c_channels == 4 and i_channels == 3:
            image: np.ndarray = NImage.add_alpha(image)
        elif c_channels == 3 and i_channels == 4:
            image: np.ndarray = NImage.remove_alpha(image)
        i_channels = image.shape[2]
        if c_channels != i_channels:
            raise RuntimeError("Channel count differs.")
        # Start fitting.
        try:
            c_ratio: float = c_width / c_height
            i_ratio: float = i_width / i_height
            if i_ratio > c_ratio:
                i_height = int(c_width * i_height / i_width)
                i_width = c_width
                top: int = abs(c_height - i_height) // 2
                bottom: int = top + i_height
                left: int = 0
                right: int = c_width
            else:
                i_width = int(i_width * c_height / i_height)
                i_height = c_height
                top: int = 0
                bottom: int = c_height
                left: int = abs(c_width - i_width) // 2
                right: int = left + i_width
            background[top:bottom, left:right] = np.array(Image.fromarray(image).resize((i_width, i_height)))[...]
        except ZeroDivisionError:
            pass
        return background

    @staticmethod
    def fill_image(background: np.ndarray, image: np.ndarray) -> np.ndarray:
        """Fill an image at the center of the image background.

        The image's shortest side is re-sized to match background's shortest side while maintaining the original aspect
        ratio.

        :param background: The image background.
        :param image: The image to be filled onto background.
        :return: A containing image with fitted image.
        """
        # Check background's channel count.
        # Match image's channel count.
        c_height, c_width, c_channels = background.shape
        i_height, i_width, i_channels = image.shape
        if c_channels == 4 and i_channels == 3:
            image: np.ndarray = NImage.add_alpha(image)
        elif c_channels == 3 and i_channels == 4:
            image: np.ndarray = NImage.remove_alpha(image)
        i_channels = image.shape[2]
        if c_channels != i_channels:
            raise RuntimeError("Channel count differs.")
        # Start fitting.
        try:
            c_ratio: float = c_width / c_height
            i_ratio: float = i_width / i_height
            if i_ratio > c_ratio:
                i_width = int(i_width * c_height / i_height)
                i_height = c_height
                top: int = 0
                bottom: int = c_height
                left: int = abs(c_width - i_width) // 2
                right: int = left + c_width
            else:
                i_height = int(c_width * i_height / i_width)
                i_width = c_width
                top: int = abs(c_height - i_height) // 2
                bottom: int = top + c_height
                left: int = 0
                right: int = c_width
            background[...] = np.array(Image.fromarray(image).resize((i_width, i_height)))[top:bottom, left:right]
        except ZeroDivisionError:
            pass
        return background
