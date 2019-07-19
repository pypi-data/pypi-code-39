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

from neptune.generated.swagger_client.models import ParameterTypeEnum as PTE

from neptune.internal.cli import MLFramework
from neptune.internal.common.values import Tag


UNKNOWN_ML_FRAMEWORK = u"Invalid ml framework '{}'. Must be one of {}."
_PARAM_TYPE_MISMATCH = ("Invalid value '{value}' for parameter '{name}'. "
                        "Type declared in config is '{type}'.")
_INVALID_TYPE = "Invalid type '{type}' declared for parameter '{name}'."


def validate_parameters(value, rule_obj, path):  # pylint:disable=unused-argument

    parameters = value

    if not isinstance(parameters, dict):
        raise AssertionError(u"Invalid structure of the parameters' section in the config file.")

    return True


def validate_tags(value, rule_obj, path):  # pylint:disable=unused-argument

    tags = value

    for tag in tags:

        try:
            Tag.create_from(tag)
        except ValueError as error:
            raise AssertionError(str(error))

    return True


def validate_ml_framework(value, rule_obj, path):   # pylint:disable=unused-argument

    legal_frameworks = MLFramework.__members__.values()  # pylint:disable=no-member

    framework = value

    if framework not in legal_frameworks:
        raise AssertionError(
            UNKNOWN_ML_FRAMEWORK.format(framework, ', '.join(legal_frameworks)))

    return True


def guess_swagger_type(value):
    if isinstance(value, int):
        return PTE.double
    elif isinstance(value, float):
        return PTE.double
    elif isinstance(value, dict):
        return PTE.double
    elif isinstance(value, list):
        return _guess_list_swagger_type(value)
    else:
        return PTE.string


def _guess_list_swagger_type(value):
    value_types = set()

    for v in value:
        value_types.add(guess_swagger_type(v))

    return _calculate_type(value_types)


def _calculate_type(value_types):
    if value_types == {PTE.double}:
        return PTE.double

    return PTE.string


def _guess_dict_swagger_type(value):
    if 'ranges' in value:
        return PTE.double


def _is_valid(param_type, rule_obj):
    # pylint:disable=protected-access
    return param_type in rule_obj._schema_str['map']['type']['enum']
