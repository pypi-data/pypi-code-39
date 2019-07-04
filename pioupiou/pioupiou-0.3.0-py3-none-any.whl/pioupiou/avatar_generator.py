import glob
import logging
import random
import typing

from PIL import Image

from pioupiou.exceptions import ImageGivenShouldHaveAlphaLayer
from pioupiou.exceptions import UnsupportedImageMode

LAYER_FILE_IMAGE_PATTERN = "{folder_path}/{layer_name}_[0-9]*.png"
PILLOW_ALPHA_MODES = ["RGBA", "LA", "RGBa"]
LOGGER_NAME = "pioupiou"


class Layer(object):
    def __init__(self, level: int, variation_images_paths: typing.List[str], name: str):
        """
         An layer is a part of an avatar theme, a layer
        :param variation_images_paths: paths of different images possible for this layer, a
        layer as differents image variations
        :param level: level of layer, higher mean image will apply be over others.
        :param images: path of image
        """
        self.level = level
        self.variations_images_paths = variation_images_paths
        self.name = name

    def get_random_image(self, allow_no_alpha_layer: bool = False) -> Image:
        """Get random image from layer based on current seed"""
        assert self.variations_images_paths
        chosen_path = random.choice(self.variations_images_paths)
        logging.getLogger(LOGGER_NAME).debug(
            'open "{}" for layer "{}" of level "{}"'.format(chosen_path, self.name, self.level)
        )
        image = Image.open(chosen_path)
        # INFO - GM - 03/07/2019 - We do not support image without alpha layer unless
        if image.mode not in PILLOW_ALPHA_MODES:
            if not allow_no_alpha_layer:
                raise ImageGivenShouldHaveAlphaLayer(
                    "This image  doesn't contain alpha layer but this layer is required"
                    "to process correctly this layer"
                )
            else:
                if image.mode == "RGB":
                    image = image.convert("RGBA")
                elif image.mode == "LA":
                    image = image.convert("L")
                else:
                    raise UnsupportedImageMode(
                        "the mode {} of this image is unsupported".format(image.mode)
                    )
        return image


class AvatarTheme(object):
    def __init__(self, layers: typing.List[Layer]):
        self.layers = layers

    def generate_avatar(self, token: str) -> Image:
        """
        Generate avatar Image by obtaining layer and applying them
        :param token: token used as seed to decide layer variation to use.
        """
        random.seed(token)
        sorted_layers = sorted(self.layers, key=lambda x: x.level)
        current_image = sorted_layers[0].get_random_image(allow_no_alpha_layer=True)
        for layer in sorted_layers[1:]:
            current_image = Image.alpha_composite(current_image, layer.get_random_image())
        return current_image

    def save_on_disk(self, avatar: Image, path: str) -> str:
        """
        Save avatar on disk
        :param avatar: image of avatar to save
        :param path: path where image should be saved
        :return: path of image saved, same as path given in entry
        """
        avatar.save(path)
        return path


class FolderAvatarTheme(AvatarTheme):
    """
    Theme based on folder allowing easy setup of theme.
    """

    def __init__(self, folder_path: str, layers_name: typing.List[str]):
        """

        :param folder_path: path of folder where different layers are available
        :param layers_name: name of layers, order is important to decide which layer is over which. last layers are
        put over previous one.
        """
        self.folder_path = folder_path
        self.layers_name = layers_name
        layers = []
        for layer_number, layer_name in enumerate(layers_name):
            file_list = glob.glob(
                LAYER_FILE_IMAGE_PATTERN.format(
                    folder_path=self.folder_path, layer_name=glob.escape(layer_name)
                )
            )
            assert file_list
            layers.append(
                Layer(level=layer_number, variation_images_paths=file_list, name=layer_name)
            )
        assert layers
        super().__init__(layers)
