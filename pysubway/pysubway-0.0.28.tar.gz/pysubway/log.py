# -*-coding: utf-8-*-

import traceback
from functools import wraps
from typing import Dict, Any, Callable

from flask import g
from flask_restful import current_app


class Log(object):

    @property
    def extra(self) -> Dict[str, Any]:
        return {'trace_id': getattr(g, 'extra', None)}

    @property
    def info(self) -> Callable:
        return current_app.logger.info

    @property
    def info_exception(self) -> Callable:
        return current_app.logger.info

    @property
    def error(self) -> Callable:
        return current_app.logger.error

    @property
    def exception(self) -> Callable:
        return current_app.logger.exception

    @staticmethod
    def content(**kwargs: Dict[str, Any]) -> str:
        result = u''
        for k, v in kwargs.items():
            result += u'{}->{} '.format(k, v)
        return result

    @property
    def traceback(self) -> Callable:
        return traceback.format_exc


logger = Log()


def log_info_input(f: Callable) -> Any:
    @wraps(f)
    def wrap(*args: Any, **kwargs: Any) -> Any:
        try:
            parameter = u'[{}.input] '.format(f.__name__)
            if args:
                for i in args:
                    parameter += u'{} '.format(i)
            if kwargs:
                for i in kwargs:
                    parameter += u'{}={} '.format(i, kwargs[i])
            logger.info(parameter)
        except Exception as e:
            logger.info_exception(e)
        finally:
            return f(*args, **kwargs)

    return wrap


def log_info_output(f: Callable) -> Any:
    @wraps(f)
    def wrap(*args: Any, **kwargs: Any) -> Any:
        result = f(*args, **kwargs)
        try:
            logger.info(u'[{}.output] {}'.format(f.__name__, result), extra=logger.extra)
        except Exception as e:
            logger.info_exception(e, extra=logger.extra)
        finally:
            return result

    return wrap
