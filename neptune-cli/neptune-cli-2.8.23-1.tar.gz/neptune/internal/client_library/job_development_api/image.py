# -*- coding: utf-8 -*-
#
# Copyright (c) 2016, deepsense.io
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
#
from future import standard_library

standard_library.install_aliases()

# pylint: disable=wrong-import-position

from future.builtins import object

import base64
import io

import PIL.Image

from neptune.generated.swagger_client import InputImage
from neptune.internal.common.models.parameters_validation import (
    of_type_validator,
    text_conv,
    validate
)


class Image(object):
    """
    Represents information about images sent to image channels.
    """

    @validate(name=text_conv, description=text_conv, data=of_type_validator(PIL.Image.Image))
    def __init__(self, name, description, data):
        """
        Creates a new Image.

        :param name: Name of the image, displayed in the Channels tab on job's dashboard.
        :param description: Description of the image displayed in the Channels tab
                            on job's dashboard.
        :param data: Image data.
        :type name: unicode
        :type description: unicode
        :type data: PIL.Image
        """
        self._name = name
        self._description = description
        self._data = data

    def to_input_image(self):
        """
        Creates InputImage that can be sent to Neptune.

        :return: input image in format appropriate to be sent to Neptune.
        :rtype: InputImage
        """
        image_buffer = io.BytesIO()
        self.data.save(image_buffer, format='PNG')
        contents = image_buffer.getvalue()
        image_buffer.close()

        input_image = InputImage()
        input_image.name = self.name
        input_image.description = self.description
        input_image.data = base64.b64encode(contents).decode('utf-8')

        return input_image

    @property
    def name(self):
        """
        Gets name of this Image.

        :return: The name of this Image.
        :rtype: str
        """
        return self._name

    @property
    def description(self):
        """
        Gets description of this Image.

        :return: The description of this Image.
        :rtype: str
        """
        return self._description

    @property
    def data(self):
        """
        Gets data of this Image.

        :return: The data of this Image.
        :rtype: PIL.Image
        """
        return self._data
