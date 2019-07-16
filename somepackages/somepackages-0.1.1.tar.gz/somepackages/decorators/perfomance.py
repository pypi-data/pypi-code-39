from time import time
import logging


def timeit(func_name="anon", limit=4):
    '''
    timeit is decorator to profile by time executed method or function
    :param func_name: is function name
    :param limit: how many second should work by seconds
    :return: func
    '''
    def decorator(f):
        def wrapper(*args, **kwargs):
            start = time()
            result = f(*args, **kwargs)
            end = time()
            t = end - start
            if t * 1000 >= limit * 1000:
                logging.warning("is too slow")
            else:
                print('%s - %2.2f ms' % (func_name, (end - start) * 1000))
            return result

        return wrapper

    return decorator