# Copyright (C) 2018-2019  The Plenpy Authors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Module defining the :class:`SpectralImage` class.

"""

import re
from pathlib import Path
from typing import Optional, Union, Any

import imageio
import matplotlib.pyplot as plt
import numpy as np
import scipy.io

import plenpy.logg
from plenpy.utilities import colors
from plenpy.utilities import core
from plenpy.utilities.core import BandInfo
from plenpy.utilities.misc import get_avail_extensions

logger = plenpy.logg.get_logger()

_all_ = ['SpectralImage', BandInfo]

# Here, prefer the FreeImage plugin over PIL to be able to read 16bit data
imageio.formats.sort('-FI', '-PIL')


class SpectralImage(core.SpectralArray):
    """SpectralImage class representing a multi-color-channel image.

    This class is derived from the core
    :class:`core.SpectralArray` class.

    This class is mostly equivalent to the
    :class:`core.SpectralArray` class but restricts the
    number of dimensions to 3 exactly, i.e. it will always be of shape
    (x, y, num_channels). It then extends its parent class by some
    useful methods for multi- or hyperspectral images as well as multiple
    methods to create/read/show a spectral image.

    See Also:
        See the parent class :class:`core.SpectralArray`
        for the basic Attributes.
    """

    def __new__(cls, *args, **kwargs) -> 'SpectralImage':
        # Set ndim_exp=3, everything else is done in SpectralArray class.
        return super().__new__(cls,*args, **kwargs, ndim_exp=3)

    @classmethod
    def from_file(cls,
                  path: Any,
                  format: Optional[str] = None,
                  **kwargs) -> 'SpectralImage':
        """Initialize a SpectralImage from a single image file path.

        The image is loaded using ``imageio`` which, for most multispectral
        formats, requires the GDAL plugin. For RGB images, no extra plugin
        is required.

        Args:
            path: Image file system path.

            format: Image format to read. When None, imageio tries to guess
                    one based on the extension. When loadeing ENVI files, use
                    'GDAL' explicitly.

            **kwargs : See :class:`core.SpectralArray`
        """
        # Parse path
        path = Path(path)
        logger.info(f"Reading SpectralImage from file {path.absolute()} ...")

        # Load local image
        img = imageio.imread(path.absolute(), format)

        # Transpose axis as imageio uses (ch, x, y) shape for spectral images
        if format is not None and format.lower() == 'gdal':
            img = np.transpose(img,  (1, 2, 0))

        # Return HSI object initialized from data.
        logger.info("... done.")
        return cls(array=img, **kwargs)

    @classmethod
    def from_file_collection(cls,
                             path: Any,
                             format: str = None,
                             **kwargs) -> 'SpectralImage':
        """Initialize a SpectralImage from multiple image files.
        Each image corresponds to one color channel.

        Args:
            path: System path to folder containing the subaperture view images.
                The folder must not contain any other image data.

            format: Image format.
                By default, imageio selects an appropriate one based
                on the filename and its contents.
                Use :func:`plenpy.utilities.misc.get_avail_extensions()`
                to get a list of available formats.

            **kwargs : See :class:`core.SpectralArray`
        """
        path = Path(path)

        if not path.is_dir():
            raise ValueError("Path '{path}' is not a folder.")

        logger.info(f"Reading hyperspectral image from folder {path} ...")

        image_paths = []
        for file in path.iterdir():
            # Check that the file is a readable image file
            # no npz file allowed
            # exclude files with "rgb" in filename
            if file.suffix in get_avail_extensions() and \
                    not file.suffix.endswith('.npz') and \
                    str(file).lower().find("rgb") == -1:
                image_paths.append(file)

        # Sort list alphanumerically
        image_paths.sort()

        # Read the images and check that they are of same shape
        image_list = []
        for file in image_paths:
            image_list.append(np.squeeze(
                np.asarray(imageio.imread(file.absolute(), format))))

        shape = image_list[0].shape
        for image in image_list:
            if not image.shape == shape:
                raise ValueError(f"The images are not all of the same shape.")

        if not len(shape) == 2:
            raise ValueError(f"The given images are not greyscale images.")

        # Ready to put images together to HSI data
        data = np.stack(image_list, axis=-1)

        logger.info("... done.")

        return cls(data, **kwargs)

    @classmethod
    def from_mat_file(cls,
                      path: Any,
                      key: Optional[str] = None,
                      order: str = '012',
                      **kwargs) -> 'SpectralImage':
        """Read HSI from matlab file.

        Args:
            path: System path to ``.mat`` file.

            key: Key name of the data in ``.mat`` file. If only one variable
                 is contained, option is ignored and key is found automatically.
                 If more than one key is contained, the ``key`` option must be
                 specified.

            order: Order of the axes of the data in the matlab file.
                   Possible values are: ``'012'``, corresponding to a shape
                   (x, y, lambda) and ``'201'``, corresponding to a shape
                   (lambda, x, y).

            **kwargs : See :class:`core.SpectralArray`
        """
        path = Path(path)
        logger.info(f"Reading SpectralImage from Matlab file {path}...")

        if not (order == '012' or order == '201'):
            raise ValueError("Option 'order' must be '012' or '201'")

        mat_data = scipy.io.loadmat(path.absolute())

        # Find data, ignore headers
        keys = []
        for tmp_key, value in mat_data.items():
            if not re.findall('__.*__', tmp_key) == [tmp_key]:
                keys.append(tmp_key)

        if len(keys) == 0:
            raise ValueError("Did not find a data key in Matlab file.")

        if not len(keys) == 1:
            if key is None:
                raise ValueError(f"Found more than one key in Matlab file. "
                                 f"Keys found: {keys}. Please specify a single"
                                 f" key using the 'key' option.")
            else:
                if key in keys:
                    keys = [key]
                else:
                    raise KeyError(f"No key '{key}' in keys '{keys}'.")

        logger.info(f"Found key '{keys[0]}' in Matlab file with data of shape "
                    f"{mat_data[keys[0]].shape}.")
        # Get data from variable
        data = mat_data[keys[0]]
        del mat_data

        # Transpose if in incorrect order to match standard order of HSI class
        if order == '201':
            logger.info("Transposing data...")
            data = np.transpose(data, (1, 2, 0))
            logger.info(f"Transposed data to shape '{data.shape}'.")

        logger.info("... done.")

        return cls(data, **kwargs)

    def save(self, path: Any,
             create_dir: bool = False,
             dtype: Union[np.uint8, np.uint16] = np.uint8):
        """Save the spectral image channel wise.
        To save as a numpy array, use Numpy's :func:`numpy.save()` function
        instead. To save a RGB image, use :func:`save_rgb()`.

        Args:
            path: System path to save the image. For each channel, an index
                  will be appended. Needs to include an extension.

            create_dir: If ``True``, parent folder will be created if not existent.

            ext: Extension of target image.

            dtype: Target dtype. Either uint8 or uint16.
        """
        path = Path(path)

        if path.suffix == '':
            raise ValueError("Path needs to include an extension.")

        if create_dir:
            path.parent.mkdir(parents=True, exist_ok=True)

        if not path.parent.is_dir():
            raise FileNotFoundError(f"Path '{path.parent}' does not exist.")

        logger.info(f"Saving SpectralImage channel wise to {path.absolute()}...")
        x, y, num_ch = self.shape

        logger.info(f"Dtype conversion from {self.dtype} to {dtype} "
                    f"might be lossy.")

        mult = 2**8 - 1 if dtype == np.uint8 else 2**16 -1

        for ch in range(num_ch):

            # Append channel number to path
            if num_ch > 99:
                tmp_path = path.parent / Path(path.stem + f"_{ch:03}" + path.suffix)

            else:
                tmp_path = path.parent / Path(path.stem + f"_{ch:02}" + path.suffix)

            # Save channel image
            imageio.imsave(uri=tmp_path.absolute(),
                           im=(mult*self[..., ch]).astype(dtype))

        logger.info("...done")
        return

    def save_rgb(self, path: Any):
        """Saves the SpectralImage as RGB image.

        Args:
            path: Path where to save image including extension.

        See Also:
            :func:`core.SpectralArray.get_rgb()`
        """
        path = Path(path)

        if path.suffix == '':
            raise ValueError("Path needs to include an extension.")

        logger.info("Saving SpectralImage in RGB representation")

        # Convert to RGB
        if self._numChannels > 3:
            imageio.imsave(uri=path.absolute(), im=self.get_rgb())
        else:
            imageio.imsave(uri=path.absolute(), im=self)

    def get_spectral_filter(self, spec_filter_type: str):
        """

        Args:
            spec_filter_type: Type of the filter array.
                If ``random`` is specified, use random arrangement of the spectral filter,
                if ``uniform`` is specified, use uniform arrangement of the spectral filter.

        Returns:
            Spectral filter array.

        """
        x, y, ch = self.shape

        m = int(np.sqrt(self._numChannels))
        col = np.zeros((m, m))
        spec_filter = col
        if spec_filter_type == "uniform":
            block = np.arange(ch).reshape((m, m))
            spec_filter = np.tile(block, (x // m + 1, y // m +1))

        elif spec_filter_type == "random":
            for i in range(x // m + 1):
                for j in range(y // m + 1):
                    block = np.arange(ch)
                    np.random.shuffle(block)
                    block = block.reshape((m, m))
                    if j == 0:
                        col = block
                    else:
                        col = np.vstack((col, block))
                if i == 0:
                    spec_filter = col
                else:
                    spec_filter = np.hstack((spec_filter, col))
        else:
            raise ValueError(f"Unknown mask type {spec_filter_type}.")

        spec_filter = spec_filter.reshape(m * (x // m + 1), m * (y // m + 1))
        spec_filter = spec_filter[:x, :y]

        return spec_filter

    def get_sensor_image(self, spec_filter_type: str):
        """

        Args:
           spec_filter_type: Type of the filter array.
                If ``random`` is specified, use random arrangement of the spectral filter,
                if ``uniform`` is specified, use uniform arrangement of the spectral filter.

        Returns:
            Sensor image.

        """
        x, y, ch = self.shape

        spec_filter = self.get_spectral_filter(spec_filter_type)
        sen_im = np.zeros((x, y))
        for i in range(x):
            for j in range(y):
                for k in range(self._numChannels):
                    if spec_filter[i, j] == k:
                        sen_im[i, j] = self[i, j, k]
        return sen_im

    def show(self):
        """Visualize the SpectralImage.

         Plotting the SpectralImage either in RGB view or channel-wise.

         Use scrolling to scroll through the color channels.
         Enable per-color-channel view by clicking the scroll wheel once.
         Reset to the regular view by double clicking the scroll wheel.

         Double click in the image area opens a new figure showing the
         spectrum of the corresponding pixel.
        """
        x, y, num_ch = self.shape

        # Flag whether scrolling is possible
        is_scrollable = True if num_ch > 1 else False

        # Flag whether to reverse color channels, e.g. for RGB images
        rev_color_ch = True if num_ch == 3 else False

        # Flag whether scrolling was enabled
        scroll_enabled = False
        show_color = False

        # Wavelengths for color images to scroll through
        lambda_start = 430
        lambda_end = 650
        wavelength_list = np.linspace(lambda_start, lambda_end, num_ch)

        if rev_color_ch:
            wavelength_list = np.flipud(wavelength_list)

        # Index of the current wavelength, start at lambda_start
        curr_wave_index = 0

        press = None

        # Convert data if necessary
        im = self
        # Get color converter instance, calculate RGB values of wavelengths
        converter = colors.WavelengthConverter()
        wavelength_rgb = converter.to_rgb(wavelength_list)

        if num_ch > 3:
            logger.info("Converting spectra to RGB image...")
            sp_converter = colors.SpectrumConverter(wavelength_list)

            # Create rgb lf data from hs data
            rgb_data = np.zeros((x, y, 3))

            # Reshape to get one spectrum per column
            spectra = np.reshape(self, (x*y, num_ch))

            rgb = sp_converter.to_rgb(spectra)

            rgb_data = np.reshape(rgb, rgb_data.shape)
            logger.info("...done.")
            im = rgb_data

        # Show image, if one channel, use grayscale
        fig = plt.figure()
        img = plt.imshow(np.squeeze(im), cmap='gray')
        plt.title(f"Image")
        plt.xlabel("x")
        plt.ylabel("y")

        plt.pause(.025)
        plt.draw()

        def draw_canvas(color_index=None):
            nonlocal im, img, is_scrollable, press

            if num_ch == 1 or num_ch == 3:
                im = self

            if num_ch > 3:
                im = rgb_data

            if color_index is not None and scroll_enabled:
                rgb = wavelength_rgb[color_index]

                # Select sub view, mono channel
                im = self[..., color_index]

                # Calculate mono color representation
                if show_color:
                    im = np.reshape(np.outer(im, rgb), im.shape + (3,))

            # Set new image
            plt.title(f"Image of channel {color_index}")
            img.set_data(np.squeeze(im))
            fig.canvas.draw()

            return

        def draw_spectrum(x: int, y: int):
            if x is None or y is None:
                logger.info("You have clicked outside of the image...")
                return

            x, y = int(x), int(y)
            logger.info(f"Plotting spectrum of (x, y) = "
                        f"{x, y}.")

            x_data = np.arange(0, num_ch)
            y_data = self[x, y, :]
            plt.figure("Spectrum")
            plt.title(f"Spectrum")
            plt.plot(x_data, y_data, 'o-', label=f"{x, y}")
            plt.xlabel("Color channel")
            plt.ylabel("Reflectance")
            plt.legend()
            #plt.ylim(0, 1)

            # Set the color channel labels to integer
            ch_int = range(0, num_ch)
            if len(ch_int) > 10:
                ch_int = ch_int[::2]

            plt.xticks(ch_int)
            plt.show()

            return

        def on_press(event):
            nonlocal im, img, scroll_enabled, press

            # On Double click on button 1: show spectrum
            if event.dblclick and event.button == 1:
                x, y = event.ydata, event.xdata

                draw_spectrum(x=x, y=y)

                return

            # On double click of scroll wheel: Set scroll modus
            if event.button == 2:
                if not is_scrollable:
                    logger.info("Scrolling is not possible for b&w images.")
                elif scroll_enabled:
                    # Reset on double scroll wheel click
                    logger.info("Resetting to normal modus.")
                    scroll_enabled = False
                    draw_canvas()
                    return

                elif is_scrollable and not scroll_enabled:
                    logger.info("Setting scroll modus.")
                    logger.info(f"Showing color channel {curr_wave_index}.")

                    scroll_enabled = True
                    draw_canvas(curr_wave_index)

                    return

            # On button press get coordinates
            press = event.xdata, event.ydata

        def on_scroll(event):
            # When scrolling, show color channels seperately
            nonlocal scroll_enabled, curr_wave_index, press

            if event.button == 'up' and scroll_enabled:
                # Scroll up increases color channel
                curr_wave_index += 1
                curr_wave_index = min(num_ch - 1, curr_wave_index)

                logger.info(f"Showing color channel {curr_wave_index}.")

                draw_canvas(curr_wave_index)
                return

            if event.button == 'down' and scroll_enabled:
                # Scroll down decreases color channel
                curr_wave_index -= 1
                curr_wave_index = max(0, curr_wave_index)

                logger.info(f"Showing color channel {curr_wave_index}.")

                draw_canvas(curr_wave_index)
                return

        def on_release(event):
            nonlocal press
            # On release we reset the press data
            press = None
            fig.canvas.draw()

        # Connect to matplotlib event API
        fig.canvas.mpl_connect('button_press_event', on_press)
        fig.canvas.mpl_connect('button_release_event', on_release)
        fig.canvas.mpl_connect('scroll_event', on_scroll)
        plt.show()
        return
