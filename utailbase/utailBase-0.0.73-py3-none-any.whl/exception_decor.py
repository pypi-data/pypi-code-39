# -*- coding: utf-8 -*-
import functools
import inspect
from timeit import default_timer as timer

def exception(logger):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as inst:
                # log the exception
                err = "There was an exception in {}. msg:{}".format(func.__name__, inst.args)
                logger.error(err)
                raise
        return wrapper
    return decorator


def exceptionDB(logger, loggers_idx = 0):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as inst:
                # log the exception
                err = "There was an exception in {}. msg:{}".format(func.__name__, inst.args)
                logger.error(err)
                return None
            finally:
                if args[loggers_idx] is not None:
                    args[loggers_idx].close()
        return wrapper
    return decorator


# def task_timeChecker(logger):
#     def decorator(func):
#         def task_timeCheckerWrapper(*args, **kwargs):
#             # startTime = timer()
#             # try:
#             #     func(*args, **kwargs)

#             #     endTime = timer()
#             #     return (True, endTime - startTime)
#             # except Exception as inst:
#             #     logger.error(inst.args)
#             #     return (False, 0)

#             startTime = timer()
#             func(*args, **kwargs)
#             endTime = timer()
#             return (True, endTime - startTime)
            
#         return task_timeCheckerWrapper
#     return decorator