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
from future.builtins import object

from neptune.generated.swagger_client.models.channel_type import ChannelType as SwaggerChannelType
from neptune.internal.client_library.job_development_api.image import Image


class ChannelType(object):
    """
    Represents the kind of information that can be sent via Neptune Channel.
    Currently supported values are: :py:attr:`~neptune.ChannelType.NUMERIC`,
    :py:attr:`~neptune.ChannelType.TEXT` and
    :py:attr:`~neptune.ChannelType.IMAGE`.
    """

    def __init__(self):
        """Initializes ChannelType"""
        pass

    #: Numeric channel, accepts float values.
    NUMERIC = SwaggerChannelType.numeric

    #: Text channels, accepts str values.
    TEXT = SwaggerChannelType.text

    #: Image channel, accepts neptune.Image values.
    IMAGE = SwaggerChannelType.image

    @staticmethod
    def get_channel_type(obj):
        """
        Determines the type of channel based on the given object

        :param obj The object used to determine type of channel:
        :return The type of channel to use:
        """
        if obj is None:
            raise ValueError(u"Value must not be null")
        if isinstance(obj, Image):
            return ChannelType.IMAGE
        try:
            float(obj)
            return ChannelType.NUMERIC
        except TypeError:
            pass
        except ValueError:
            pass
        return ChannelType.TEXT
