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

from future.builtins import str
from future.utils import iteritems

import functools
import inspect

import voluptuous
import voluptuous.humanize
from neptune.internal.common.models.exceptions import NeptuneInvalidArgumentException
from neptune.internal.common.utils.str import to_bytestring, to_unicode


def validate(**kw_validators):
    # Function decorator that validates (and converts to desired type) passed arguments.
    # Validators can be specified as kwargs for named arguments only and are optional.

    def validate_fun(f):
        f_args, _, _, _ = inspect.getargspec(f)  # pylint:disable=deprecated-method

        params_validators = {
            name: voluptuous.Schema(validator) for name, validator in list(kw_validators.items())
        }

        diff = set(kw_validators.keys()).difference(set(f_args))

        assert not diff, "Incorrect specification of validation in function {fun} " \
                         "for non-existent keys: {keys}".format(fun=f.__name__, keys=diff)

        @functools.wraps(f)
        def wrapper(*args, **kwds):
            result_args = inspect.getcallargs(f, *args, **kwds)  # pylint:disable=deprecated-method
            for param_name, param_validator in iteritems(params_validators):
                param_value = result_args[param_name]
                try:
                    validated_param = voluptuous.humanize.validate_with_humanized_errors(
                        data=param_value,
                        schema=param_validator)
                    result_args[param_name] = validated_param
                except voluptuous.error.Error as error:
                    raise NeptuneInvalidArgumentException(
                        u"{cause} Invalid parameter '{param_name}' in function '{fun}'.".format(
                            param_name=param_name,
                            fun=f.__name__,
                            cause=to_unicode(error)))
            return f(**result_args)
        return wrapper
    return validate_fun


def validate_coordinates(f):
    """
    Function decorator that validates that coordinates (named parameters x and y) have
    correct values. Any additional parameters are passed without any modifications
    """

    @functools.wraps(f)
    def wrapper(*args, **kw):
        named_params = set(kw.keys())
        result_args = inspect.getcallargs(f, *args, **kw)  # pylint:disable=deprecated-method
        x, y = result_args.get("x"), result_args.get("y")

        if x is not None:
            if y is not None:
                return f(**result_args)
            else:
                if x is not None and "x" not in named_params:
                    result_args["x"] = None
                    result_args["y"] = x
                    return f(**result_args)
        else:
            if y is not None:
                return f(**result_args)
        raise NeptuneInvalidArgumentException(
            u"Invalid coordinates x='{param_x}', y='{param_y}' in function '{fun}'.".format(
                param_x=x,
                param_y=y,
                fun=f.__name__))
    return wrapper


def singular_conversion(fun, to_type, value):
    try:
        return fun(value)
    except:
        raise voluptuous.Error(
            u"Value '{}' of type '{}' cannot be converted to type '{}'.".format(
                to_unicode(repr(value)), type(value), to_type))


def text_conv(text):
    if text is None:
        return None
    return singular_conversion(to_unicode, 'unicode', text)


def text_conv_coll(text_collection):
    return [singular_conversion(to_unicode, 'unicode', text) for text in text_collection]


def float_conv(num):
    return singular_conversion(float, 'float', num)


def int_conv(num):
    return singular_conversion(int, 'int', num)


def is_function(fun):
    if inspect.isfunction(fun):
        return fun
    else:
        raise voluptuous.Error("{invalid_fun} of type {actual_type} is not a function.".format(
            invalid_fun=str(fun),
            actual_type=type(fun)
        ))


def function_arity(arity):
    def validate_function(fun):
        is_function(fun)
        fun_arg_spec = inspect.getargspec(fun)  # pylint:disable=deprecated-method
        fun_arity = len(fun_arg_spec.args)
        if fun_arity == arity:
            return fun
        else:
            raise voluptuous.Error(
                "Passed function {fun_name} has incorrect number of parameters. "
                "Expected {arity}, got {fun_arity}.".format(
                    fun_name=fun.__name__,
                    arity=arity,
                    fun_arity=fun_arity
                ))
    return validate_function


def of_type_validator(valid_class_or_type):
    def of_type(item):
        try:
            if isinstance(item, valid_class_or_type):
                return item
            else:
                raise Exception()
        except Exception:
            valid_type_module = valid_class_or_type.__module__
            repr_module = valid_type_module + "." if valid_type_module != '__builtin__' else ''
            repr_valid_type = repr_module + valid_class_or_type.__name__
            raise voluptuous.Error(
                to_bytestring(
                    u"Value type '{item_type}' is incorrect. "
                    u"The valid type is '{valid_type}'.".format(
                        item_type=type(item).__name__,
                        valid_type=repr_valid_type)))
    return of_type


ALL_SINGULAR_CONVERTERS = {text_conv, int_conv, float_conv}


def is_conv(valid_value):
    def is_valid(item):
        for converter in ALL_SINGULAR_CONVERTERS:
            try:
                converted_value = converter(item)
                if converted_value == valid_value:
                    return converted_value
            except voluptuous.Error:
                pass
        raise voluptuous.Error(
            u"Item '{item}' cannot be converted to `{valid_value}`.".format(
                item=to_unicode(item),
                valid_value=to_unicode(valid_value)
            )
        )
    return is_valid


def one_of_validator(valid_values):
    def is_one_of(item):
        for valid_value in valid_values:
            try:
                return is_conv(valid_value)(item)
            except voluptuous.Error:
                pass
        raise voluptuous.Error(
            u"Item '{item}' is not one of: {valid_values}.".format(
                item=to_unicode(item),
                valid_values=to_unicode(valid_values)
            )
        )
    return is_one_of


def one_of_type_validator(validators):
    def is_one_of(item):
        for validator in validators:
            try:
                return validator(item)
            except voluptuous.Error:
                pass
        raise voluptuous.Error(
            u"'{item}' has unsupported type.".format(
                item=to_unicode(item)
            )
        )
    return is_one_of
