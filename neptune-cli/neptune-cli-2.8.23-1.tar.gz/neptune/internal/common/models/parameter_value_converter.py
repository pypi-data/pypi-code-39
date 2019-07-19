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

from neptune.internal.common.models.exceptions import NeptuneParameterConversionException
from neptune.internal.common.parsers.type_mapper import TypeMapper
from neptune.internal.common.utils.str import to_unicode


class ParameterValueConverter(object):
    PARAMETER_TYPE_INT = u'int'
    PARAMETER_TYPE_DOUBLE = u'double'
    PARAMETER_TYPE_BOOLEAN = u'boolean'
    PARAMETER_TYPE_STRING = u'string'

    _PYTHON_TYPES = {
        PARAMETER_TYPE_INT: int,
        PARAMETER_TYPE_DOUBLE: float,
        PARAMETER_TYPE_BOOLEAN: bool,
        PARAMETER_TYPE_STRING: str
    }

    _CONVERSION_FUNCTIONS = {
        PARAMETER_TYPE_INT: TypeMapper.to_int,
        PARAMETER_TYPE_DOUBLE: TypeMapper.to_float,
        PARAMETER_TYPE_BOOLEAN: TypeMapper.to_bool,
        PARAMETER_TYPE_STRING: to_unicode
    }

    def __init__(self, parameter_api_model):
        super(ParameterValueConverter, self).__init__()
        self.parameter_api_model = parameter_api_model

    def convert_value(self, parameter_value, parameter_type):
        param_type = self._is_int_float_or_bool(parameter_value, parameter_type)
        if parameter_value is None:
            return None

        conversion_function = self.type2conversion(param_type)
        destination_type = self.type2python(param_type)

        try:
            converted_value = conversion_function(parameter_value)
            return converted_value
        except ValueError as ex:
            raise NeptuneParameterConversionException(
                self.parameter_api_model,
                parameter_value,
                destination_type,
                ex)

    @classmethod
    def type2python(cls, type_name):
        if type_name in cls._PYTHON_TYPES:
            return cls._PYTHON_TYPES[type_name]
        else:
            raise ValueError(u'Unsupported parameter type: "{}"'.format(type_name))

    def _is_int_float_or_bool(self, s, defined_type):
        if s == "True" or s == "False":
            return self.PARAMETER_TYPE_BOOLEAN
        if defined_type == self.PARAMETER_TYPE_STRING:
            return self.PARAMETER_TYPE_STRING
        try:
            floating = float(s)
            try:
                integer = int(s)
                if floating == integer:
                    return self.PARAMETER_TYPE_INT
                else:
                    return self.PARAMETER_TYPE_DOUBLE
            except ValueError:
                return self.PARAMETER_TYPE_DOUBLE
        except ValueError:
            return self.PARAMETER_TYPE_STRING

    @classmethod
    def type2conversion(cls, type_name):
        if type_name in cls._CONVERSION_FUNCTIONS:
            return cls._CONVERSION_FUNCTIONS[type_name]
        else:
            raise ValueError(u'Unsupported parameter type: "{}"'.format(type_name))
