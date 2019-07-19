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

from neptune.internal.cli.exceptions.params_exceptions import ReadOnlyException
from neptune.internal.common.models.parameter_value_converter import ParameterValueConverter


class ContextParams(object):
    """
    Parameters are a set of user-defined variables that will be passed to the job’s program.

    Job’s parameters are defined in the configuration file.
    Parameters’ values can be passed to a job using command line parameters
    when enqueuing or executing the job.
    Each parameter has:

    - name,
    - description,
    - type(string, integer, float, bool),
    - optional default value,
    - ‘required’ flag - defines whether a parameter is necessary for job execution.

    Parameter values can be retrieved using two different notations:
    the object notation and the dictionary notation.

    Access with object notation::

        print ctx.params.x

    Access with dict-like notation::

        print ctx.params['y']
    """

    def __init__(self):
        """
        Create a new instance of neptune.params.ContextParams

        .. warning:: For internal use only.

           Use :py:attr:`neptune.Context.params` instead to access and modify params.
        """
        pass

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value, immutable=True):
        if immutable:
            raise ReadOnlyException()
        return setattr(self, item, value, False)

    def __setattr__(self, key, value, immutable=True):
        if immutable:
            raise ReadOnlyException()
        super(ContextParams, self).__setattr__(key, value)

    def __delitem__(self, key):
        raise ReadOnlyException()

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    @classmethod
    def create_from(cls, job_api_model):

        job_parameters = cls()

        for param in job_api_model.parameters:
            job_parameters.__setattr__(param.name,
                                       ParameterValueConverter(param).convert_value(param.value, param.parameter_type),
                                       immutable=False)

        return job_parameters
