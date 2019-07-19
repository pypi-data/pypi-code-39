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
from future.utils import python_2_unicode_compatible

import collections
import logging

import neptune.generated.swagger_client.models as api_models
from neptune.internal.common.api.exceptions import NeptuneServerResponseErrorException
from neptune.internal.common.models.parameters_validation import (
    int_conv,
    text_conv,
    text_conv_coll,
    validate
)


@python_2_unicode_compatible
class TagsService(collections.MutableSequence):
    """
    Exposes tags using collections.MutableSequence abstraction.
    A tag is a word that contains only lowercase letters, numbers, underscores and dashes.
    Tags can be assigned to a job or removed from a job anytime throughout job’s lifetime.
    When listing jobs, it is possible to search by tags, so tags are useful to mark jobs.
    Job’s tags can be set from both the configuration file
    and job’s code or by command line parameters.

    Accessing tags::

        my_tag_exists = 'my-tag' in ctx.tags

    Modifying tags::

        ctx.tags.append('new-tag')
        ctx.tags.remove('new-tag')
        ctx.tags += ['tag1', 'tag2', 'tag3']
    """

    def __init__(self, experiment_id, neptune_api_handler):
        """
        Create a new TagsService.

        .. warning:: For internal use only.

           Use :py:attr:`~neptune.netpune.Context.job.tags instead to access and modify tags.

        :param experiment_id: Id of a job these tags are associated with.
        :param neptune_api_handler: Api handler. Tags are managed through Neptune REST API.
        """
        self._logger = logging.getLogger(__name__)
        self._experiment_id = experiment_id
        self._rest_client = neptune_api_handler

    def __len__(self):
        return len(self.__all_tags())

    @validate(item=int_conv)
    def __getitem__(self, item):
        tags = self.__all_tags()
        return tags.__getitem__(item)

    @validate(key=int_conv, value=text_conv)
    def __setitem__(self, key, value):
        tags = self.__all_tags()
        tags.__setitem__(key, value)
        self.__post_changes(tags)

    @validate(key=int_conv)
    def __delitem__(self, key):
        tags = self.__all_tags()
        tags.__delitem__(key)
        self.__post_changes(tags)

    def __str__(self):
        return "[" + u", ".join(self.__all_tags()) + u"]"

    def __iadd__(self, other):
        tags = self.__all_tags()
        tags.__iadd__(other)
        self.__post_changes(tags)
        return self

    def __radd__(self, other):
        return self.__add__(other)

    def __add__(self, other):
        tags = self.__all_tags()
        tags.__add__(other)
        return tags

    @validate(key=int_conv, value=text_conv)
    def insert(self, key, value):
        """
        Adds tag to a job.

        .. warning:: For internal use only.

           Use :py:meth:`~neptune.Context.job.tags.append` and
               :py:meth:`~neptune.Context.job.tags.remove` to access and modify tags.

        :param key: index of a tag in an internal array.
        :param value: tag.
        """
        tags = self.__all_tags()
        if value not in tags:
            tags.insert(key, value)
            self.__post_changes(tags)

    @validate(value=text_conv)
    def remove(self, value):
        """
        Removes tag from a job.

        :param value: value to be removed.
        """
        tags = self.__all_tags()
        if value in tags:
            tags.remove(value)
            self.__post_changes(tags)

    @validate(tags=text_conv_coll)
    def set_tags(self, tags):
        """
        Sets new tags for a job. Previous tags are removed.

        :param tags: new tags
        """
        uniques = set()
        distinct = []
        for tag in tags:
            if tag not in uniques:
                distinct.append(tag)
                uniques.add(tag)
        self.__post_changes(distinct)

    def __post_changes(self, tags):
        edit_experiment_params = api_models.EditExperimentParams()
        edit_experiment_params.tags = tags
        try:
            self._rest_client.update_experiment(self._experiment_id,
                                                edit_experiment_params)
        except NeptuneServerResponseErrorException as exc:
            if exc.status == 400:
                self._logger.warning(exc.response_message)
            else:
                raise

    def __all_tags(self):
        return self._rest_client.get_experiment(self._experiment_id).tags
