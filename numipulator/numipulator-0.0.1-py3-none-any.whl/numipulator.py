__all__ = ['NImage']
__version__ = '0.0.1'

import numpy as np
import scipy.misc


class NImage(object):
    def __init__(self) -> None:
        super().__init__()
        raise NotImplementedError("Don't call the constructor!")

    @staticmethod
    def fit_image(container: np.ndarray, image: np.ndarray) -> np.ndarray:
        """Fit an image at the center of the image container.

        The image's longest side is re-sized to match container's shortest side while maintaining the original aspect
        ratio.

        :param container: The image container.
        :param image: The image to be fitted.
        :return: A containing image with fitted image.
        """
        # Check container's channel count.
        # Match image's channel count.
        container: np.ndarray = container.copy()
        c_height, c_width, c_channels = container.shape
        i_height, i_width, i_channels = image.shape
        if c_channels == 4 and i_channels == 3:
            image: np.ndarray = np.dstack(image, np.zeros((c_height, c_width)))
        elif c_channels == 3 and i_channels == 4:
            image: np.ndarray = image[:, :, :3]
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
            container[top:bottom, left:right] = scipy.misc.imresize(image, (i_height, i_width))[...]
        except ZeroDivisionError:
            pass
        return container

    @staticmethod
    def fill_image(container: np.ndarray, image: np.ndarray) -> np.ndarray:
        """Fill an image at the center of the image container.

        The image's shortest side is re-sized to match container's shortest side while maintaining the original aspect
        ratio.

        :param container: The image container.
        :param image: The image to be filled onto container.
        :return: A containing image with fitted image.
        """
        # Check container's channel count.
        # Match image's channel count.
        container: np.ndarray = container.copy()
        c_height, c_width, c_channels = container.shape
        i_height, i_width, i_channels = image.shape
        if c_channels == 4 and i_channels == 3:
            image: np.ndarray = np.dstack(image, np.zeros((c_height, c_width)))
        elif c_channels == 3 and i_channels == 4:
            image: np.ndarray = image[:, :, :3]
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
            container[...] = scipy.misc.imresize(image, (i_height, i_width))[top:bottom, left:right]
        except ZeroDivisionError:
            pass
        return container
